from flask_pymongo import PyMongo
from flask import Blueprint, render_template, request, flash, redirect, url_for, Flask, session
import os
from .database import db
from .helpers import get_skill_names_from_gear, get_slot_info_from_gearlist
from bson import ObjectId

gearsets = Blueprint('gearsets', __name__)

@gearsets.route('/view_gearsets/<email>', methods=['GET'])
def view_gearsets(email):
    if 'email' in session:
        if email == session['email']:
            user_info = db.users.find_one({'email': session['email']})
            gearsets = db.gearsets.find({'user_id': user_info['_id']})
            return render_template('view_gearsets.html', gearsets=gearsets, email=session['email'])
        else:
            flash('You are not authorized to view this page.')
            return redirect(url_for('view_gear.overview'))
    flash('You must be logged in to view your gearsets.')
    return render_template('login.html')

@gearsets.route('/public_gearsets_overview/', methods=['GET'])
def public_gearset_overview():
    if 'email' in session:
        return render_template('public_gearsets.html', email=session['email'])
    return render_template('public_gearsets.html')

@gearsets.route('/view_public_gearsets/<weapon_type>', methods=['GET'])
def view_public_gearsets(weapon_type):
    gearset_list_query = db.gearsets.find({'weapon_type': weapon_type, 'public': True})
    print(gearset_list_query)

    gearset_list = {}

    for gearset in gearset_list_query:
        if gearset['helmet'] == "" or gearset['armor'] == "" or gearset['gloves'] == "" or gearset['belt'] == "" or gearset['legs'] == "":
            continue
        gearset_list[gearset['_id']] = gearset
    print(gearset_list)

    if 'email' in session:
        return render_template('view_public_gearsets.html', gearset_list=gearset_list, email=session['email'])
    return render_template('view_public_gearsets.html', gearset_list=gearset_list)

@gearsets.route('/view_gearset/<gearset_id>', methods=['GET'])
def view_gearset(gearset_id):
    obj_instance = ObjectId(gearset_id)
    gearset = db.gearsets.find_one({'_id': obj_instance})
    weapon_info = db.weapons.find_one({'name': gearset['weapon']})
    helmet_info = db.helmets.find_one({'name': gearset['helmet']})
    armor_info = db.armor.find_one({'name': gearset['armor']})
    gloves_info = db.gloves.find_one({'name': gearset['gloves']})
    belt_info = db.belts.find_one({'name': gearset['belt']})
    legs_info = db.legs.find_one({'name': gearset['legs']})
    
    slot_info = get_slot_info_from_gearlist(gearset)

    # pull skill names from slot_info
    # name is skills_list[0], max is skills_list[1], count is skills_list[2]
    skills_list = []
    for slot in slot_info:
        if slot_info[slot][2] != "" and (slot_info[slot][2] not in skills_list):
            skills_list.append([slot_info[slot][2], int(slot_info[slot][3]), 1])
        else:
            # add one to the count of the skill
            for skill in skills_list:
                if skill[0] == slot_info[slot][2]:
                    skill[2] += 1
                    break

    # get skill names from gearset
    skills_list.append(get_skill_names_from_gear(helmet_info))
    skills_list.append(get_skill_names_from_gear(armor_info))
    skills_list.append(get_skill_names_from_gear(gloves_info))
    skills_list.append(get_skill_names_from_gear(belt_info))
    skills_list.append(get_skill_names_from_gear(legs_info))
    
    # remove blank entries
    skills_list = [skill for skill in skills_list if skill != []]
    
    # un-nest skills_list
    new_skills_list = [skill[0] for skill in skills_list]
    for item in skills_list:
        if len(item) > 1:
            new_skills_list.append(item[1])

    skills_list = new_skills_list
    print(skills_list)
    
    # check skills_list for duplicates
    # if duplicate, add the count of the two together and combine the two skills
    for i in range(len(skills_list)):
        for j in range(i+1, len(skills_list)):
            if skills_list[i][0] == skills_list[j][0]:
                skills_list[i][2] += skills_list[j][2]
                skills_list.pop(j)
                break
    print(skills_list)

    for skill in skills_list:
        if skill[2] > skill[1]:
            skill[2] = skill[1]
    print(skills_list)

    # sort skill_list by highest count
    skills_list.sort(key=lambda x: x[2], reverse=True)

    creator = db.users.find_one({'_id': gearset['user_id']})
    creator_email = creator['email']

    if 'email' in session:
        return render_template('view_gearset.html', gearset=gearset, creator_email=creator_email, email=session['email'], weapon_info=weapon_info,
                                helmet_info=helmet_info, armor_info=armor_info, gloves_info=gloves_info, belt_info=belt_info,
                                legs_info=legs_info, skills_list=skills_list)
    return render_template('view_gearset.html', gearset=gearset, creator_email=creator_email, weapon_info=weapon_info, helmet_info=helmet_info,
                            armor_info=armor_info, gloves_info=gloves_info, belt_info=belt_info, legs_info=legs_info, skills_list=skills_list)

@gearsets.route('/add_gearset/', methods=['GET', 'POST'])
def add_gearset():
    if 'email' in session:
        if request.method == 'POST':
            public = True
            if request.form.get('public') == 'public':
                public = True
            elif request.form.get('public') == 'private':
                public = False

            user_info = db.users.find_one({'email': session['email']})
            gearset = {
                'name': request.form['name'],
                'user_id': user_info['_id'],
                'creator_username': user_info['username'],
                'description': request.form['description'],
                "weapon": "",
                "weapon_type": "",
                'helmet': "",
                'armor': "",
                'gloves': "",
                'belt': "",
                'legs': "",
                'public': public
            }
            db.gearsets.insert_one(gearset)
            return redirect(url_for('gearsets.view_gearsets', email=session['email']))
        return render_template('add_gearset.html', email=session['email'])

    flash('You must be logged in to add a gearset.')
    return render_template('login.html')

@gearsets.route('/add_to_gearset/<gearset_id>/<gear_type>/<gear_id>', methods=['GET'])
def add_to_gearset(gearset_id, gear_type, gear_id):
    if 'email' in session:
        obj_instance = ObjectId(gearset_id)
        gearset = db.gearsets.find_one({'_id': obj_instance})

        if gearset['user_id'] != db.users.find_one({'email': session['email']})['_id']:
            flash('You do not have permission to edit this gearset.')
            return render_template('overview.html', gearset=gearset, email=session['email'])

        if gear_type.lower() == "weapons":
            weapon = db.weapons.find_one({'_id': ObjectId(gear_id)})
            slot1grade = weapon['gem1']
            slot2grade = weapon['gem2']
            slot3grade = weapon['gem3']
            rampagegrade = weapon['rampage_gem']
            db.gearsets.update_one({'_id': obj_instance}, {'$set': {'weapon': weapon['name'], 'weapon_type': weapon['weapon_type'], 'weaponslot1': [slot1grade, ""],
                                                                    'weaponslot2': [slot2grade, ""], 'weaponslot3': [slot3grade, ""], 'rampageslot': [rampagegrade, ""]}})
        elif gear_type.lower() == "helmets":
            helmet = db.helmets.find_one({'_id': ObjectId(gear_id)})
            slot1grade =  helmet['gem1']
            slot2grade = helmet['gem2']
            slot3grade = helmet['gem3']
            db.gearsets.update_one({'_id': obj_instance}, {'$set': {'helmet': helmet['name'], 'helmetslot1': [slot1grade, ""], 'helmetslot2': [slot2grade, ""],
                                                                    'helmetslot3': [slot3grade, ""]}})
        elif gear_type.lower() == "armor" or gear_type.lower() == "chest":
            armor = db.armor.find_one({'_id': ObjectId(gear_id)})
            slot1grade = armor['gem1']
            slot2grade = armor['gem2']
            slot3grade = armor['gem3']
            db.gearsets.update_one({'_id': obj_instance}, {'$set': {'armor': armor['name'], 'armorslot1': [slot1grade, ""], 'armorslot2': [slot2grade, ""],
                                                                    'armorslot3': [slot3grade, ""]}})
        elif gear_type.lower() == "gloves":
            gloves = db.gloves.find_one({'_id': ObjectId(gear_id)})
            slot1grade = gloves['gem1']
            slot2grade = gloves['gem2']
            slot3grade = gloves['gem3']
            db.gearsets.update_one({'_id': obj_instance}, {'$set': {'gloves': gloves['name'], 'glovesslot1': [slot1grade, ""], 'glovesslot2': [slot2grade, ""],
                                                                    'glovesslot3': [slot3grade, ""]}})
        elif gear_type.lower() == "belts":
            belt = db.belts.find_one({'_id': ObjectId(gear_id)})
            slot1grade = belt['gem1']
            slot2grade = belt['gem2']
            slot3grade = belt['gem3']
            db.gearsets.update_one({'_id': obj_instance}, {'$set': {'belt': belt['name'], 'beltslot1': [slot1grade, ""], 'beltslot2': [slot2grade, ""], 'beltslot3': [slot3grade, ""]}})
        elif gear_type.lower() == "legs":
            legs = db.legs.find_one({'_id': ObjectId(gear_id)})
            slot1grade = legs['gem1']
            slot2grade = legs['gem2']
            slot3grade = legs['gem3']
            db.gearsets.update_one({'_id': obj_instance}, {'$set': {'legs': legs['name'], 'legsslot1': [slot1grade, ""], 'legsslot2': [slot2grade, ""], 'legsslot3': [slot3grade, ""]}})

        flash('Gear added to gearset')
        return redirect(url_for('gearsets.view_gearsets', email=session['email']))
    flash('You must be logged in to add to a gearset.')
    return render_template('login.html')

@gearsets.route('/remove_from_gearset/<gearset_id>/<gear_type>', methods=['GET'])
def remove_from_gearset(gearset_id, gear_type):
    if 'email' in session:
        obj_instance = ObjectId(gearset_id)
        gearset = db.gearsets.find_one({'_id': obj_instance})

        if gearset['user_id'] != db.users.find_one({'email': session['email']})['_id']:
            flash('You do not have permission to edit this gearset.')
            return render_template('overview.html', gearset=gearset, email=session['email'])

        #remove gear from the gearset
        db.gearsets.update_one({'_id': obj_instance}, {'$set': {gear_type: "", gear_type + 'slot1': ["", ""], gear_type + 'slot2': ["",""], gear_type + 'slot3': ["",""]}})

        if gear_type == 'weapon':
            db.gearsets.update_one({'_id': obj_instance}, {'$set': {'weapon_type': ""}})

        flash('Gear removed from gearset')
        return redirect(url_for('gearsets.view_gearset', gearset_id=gearset_id, email=session['email']))
    flash('You must be logged in to remove a gearset.')
    return render_template('login.html')

@gearsets.route('/add_deco_to_gear/<gearset_id>/<deco_id>', methods=['GET'])
def add_deco_to_gear(gearset_id, deco_id):
    if 'email' in session:
        gearset_instance = ObjectId(gearset_id)
        gearset = db.gearsets.find_one({'_id': gearset_instance})
        
        decoration_instance = ObjectId(deco_id)
        decoration = db.decorations.find_one({'_id': decoration_instance})

        if gearset['user_id'] != db.users.find_one({'email': session['email']})['_id']:
            flash('You do not have permission to edit this gearset.')
            return render_template('overview.html', gearset=gearset, email=session['email'])
        
        # check all gem grades and names in gearset
        slot_info = get_slot_info_from_gearlist(gearset)

        # sort slot_info by first item in each value, smallest to largest
        slot_info = sorted(slot_info.items(), key=lambda x: x[1][0])

        filtered_slot_info = {}
        for key, value in slot_info:
            if value[1] == "" and value[0] != "0" and value[0] != "":
                filtered_slot_info[key] = value

        # look for first slot with empty name
        slot_key = ""
        for key, value in filtered_slot_info.items():
            if value[1] == "" and value[0] >= decoration['grade']:
                slot_key = key
                break

        if slot_key == "":
            flash('You cannot add this decoration to this gearset.')
            return redirect(url_for('view_gear.decorations', email=session['email']))
        
        # add decoration to gearset
        db.gearsets.update_one({'_id': gearset_instance}, {'$set': {slot_key: [gearset[slot_key][0], decoration['name']]}})

        flash('Decoration added to gearset')
        return redirect(url_for('view_gear.decorations', email=session['email']))
    else:
        flash('You must be logged in to remove a gearset.')
        return render_template('login.html')

@gearsets.route('/add_rampage_deco_to_gear/<gearset_id>/<deco_id>', methods=['GET'])
def add_rampage_deco_to_gear(gearset_id, deco_id):
    if 'email' in session:
        gearset_instance = ObjectId(gearset_id)
        gearset = db.gearsets.find_one({'_id': gearset_instance})
        
        r_decoration_instance = ObjectId(deco_id)
        r_decoration = db.rampage_decorations.find_one({'_id': r_decoration_instance})

        if gearset['user_id'] != db.users.find_one({'email': session['email']})['_id']:
            flash('You do not have permission to edit this gearset.')
            return render_template('overview.html', gearset=gearset, email=session['email'])
        
        # check all gem grades and names in gearset
        slot_info = gearset['rampageslot']
        if slot_info[1] == "":
            if slot_info[0] >= r_decoration['grade']:
                db.gearsets.update_one({'_id': gearset_instance}, {'$set': {'rampageslot': [slot_info[0], r_decoration['name']]}})
                flash('Decoration added to gearset')
                return redirect(url_for('view_gear.rampage_decorations', email=session['email']))
            else:
                flash('You cannot add this decoration to this gearset.')
                return redirect(url_for('view_gear.rampage_decorations', email=session['email']))
        else:
            flash('There is already a decoration in this slot.')
            return redirect(url_for('view_gear.rampage_decorations', email=session['email']))
    else:
        flash('You must be logged in to make changes to a gearset.')
        return render_template('login.html')

@gearsets.route('/remove_decoration/<gearset_id>/<gear_type>/<decoration_info>', methods=['GET'])
def remove_decoration(gearset_id, gear_type, decoration_info):
    if 'email' in session:
        # get gearset instance
        gearset_instance = db.gearsets.find_one({'_id': ObjectId(gearset_id)})

        # get decoration info
        decoration_info = decoration_info.split('-')
        decoration_grade = decoration_info[1]
        decoration_name = decoration_info[0]

        # remove decoration from gearset
        if gear_type == 'weapon':
            if gearset_instance['weaponslot1'][0] == decoration_grade and gearset_instance['weaponslot1'][1] == decoration_name:
                db.gearsets.update_one({'_id': gearset_instance['_id']}, {'$set': {'weaponslot1': [decoration_grade, '']}})
            elif gearset_instance['weaponslot2'][0] == decoration_grade and gearset_instance['weaponslot2'][1] == decoration_name:
                db.gearsets.update_one({'_id': gearset_instance['_id']}, {'$set': {'weaponslot2': [decoration_grade, '']}})
            elif gearset_instance['weaponslot3'][0] == decoration_grade and gearset_instance['weaponslot3'][1] == decoration_name:
                db.gearsets.update_one({'_id': gearset_instance['_id']}, {'$set': {'weaponslot3': [decoration_grade, '']}})
        elif gear_type == 'helmet':
            if gearset_instance['helmetslot1'][0] == decoration_grade and gearset_instance['helmetslot1'][1] == decoration_name:
                db.gearsets.update_one({'_id': gearset_instance['_id']}, {'$set': {'helmetslot1': [decoration_grade, '']}})
            elif gearset_instance['helmetslot2'][0] == decoration_grade and gearset_instance['helmetslot2'][1] == decoration_name:
                db.gearsets.update_one({'_id': gearset_instance['_id']}, {'$set': {'helmetslot2': [decoration_grade, '']}})
            elif gearset_instance['helmetslot3'][0] == decoration_grade and gearset_instance['helmetslot3'][1] == decoration_name:
                db.gearsets.update_one({'_id': gearset_instance['_id']}, {'$set': {'helmetslot3': [decoration_grade, '']}})
        elif gear_type == 'armor':
            if gearset_instance['armorslot1'][0] == decoration_grade and gearset_instance['armorslot1'][1] == decoration_name:
                db.gearsets.update_one({'_id': gearset_instance['_id']}, {'$set': {'armorslot1': [decoration_grade, '']}})
            elif gearset_instance['armorslot2'][0] == decoration_grade and gearset_instance['armorslot2'][1] == decoration_name:
                db.gearsets.update_one({'_id': gearset_instance['_id']}, {'$set': {'armorslot2': [decoration_grade, '']}})
            elif gearset_instance['armorslot3'][0] == decoration_grade and gearset_instance['armorslot3'][1] == decoration_name:
                db.gearsets.update_one({'_id': gearset_instance['_id']}, {'$set': {'armorslot3': [decoration_grade, '']}})
        elif gear_type == 'gloves':
            if gearset_instance['glovesslot1'][0] == decoration_grade and gearset_instance['glovesslot1'][1] == decoration_name:
                db.gearsets.update_one({'_id': gearset_instance['_id']}, {'$set': {'glovesslot1': [decoration_grade, '']}})
            elif gearset_instance['glovesslot2'][0] == decoration_grade and gearset_instance['glovesslot2'][1] == decoration_name:
                db.gearsets.update_one({'_id': gearset_instance['_id']}, {'$set': {'glovesslot2': [decoration_grade, '']}})
            elif gearset_instance['glovesslot3'][0] == decoration_grade and gearset_instance['glovesslot3'][1] == decoration_name:
                db.gearsets.update_one({'_id': gearset_instance['_id']}, {'$set': {'glovesslot3': [decoration_grade, '']}})
        elif gear_type == 'belt':
            if gearset_instance['beltslot1'][0] == decoration_grade and gearset_instance['beltslot1'][1] == decoration_name:
                db.gearsets.update_one({'_id': gearset_instance['_id']}, {'$set': {'beltslot1': [decoration_grade, '']}})
            elif gearset_instance['beltslot2'][0] == decoration_grade and gearset_instance['beltslot2'][1] == decoration_name:
                db.gearsets.update_one({'_id': gearset_instance['_id']}, {'$set': {'beltslot2': [decoration_grade, '']}})
            elif gearset_instance['beltslot3'][0] == decoration_grade and gearset_instance['beltslot3'][1] == decoration_name:
                db.gearsets.update_one({'_id': gearset_instance['_id']}, {'$set': {'beltslot3': [decoration_grade, '']}})
        elif gear_type == 'legs':
            if gearset_instance['legsslot1'][0] == decoration_grade and gearset_instance['legsslot1'][1] == decoration_name:
                db.gearsets.update_one({'_id': gearset_instance['_id']}, {'$set': {'legsslot1': [decoration_grade, '']}})
            elif gearset_instance['legsslot2'][0] == decoration_grade and gearset_instance['legsslot2'][1] == decoration_name:
                db.gearsets.update_one({'_id': gearset_instance['_id']}, {'$set': {'legsslot2': [decoration_grade, '']}})
            elif gearset_instance['legsslot3'][0] == decoration_grade and gearset_instance['legsslot3'][1] == decoration_name:
                db.gearsets.update_one({'_id': gearset_instance['_id']}, {'$set': {'legsslot3': [decoration_grade, '']}})
        else:
            flash('Error')
            return redirect(url_for('gearsets.view_gearset', gearset_id=gearset_id))
        flash('Decoration removed.')
        return redirect(url_for('gearsets.view_gearset', gearset_id=gearset_id))
    else:
        flash('You must be logged in to do that.')
        return redirect(url_for('login'))

@gearsets.route('/remove_rampage_decoration/<gearset_id>/<decoration_info>/', methods=['GET'])
def remove_rampage_decoration(gearset_id, decoration_info):
    if 'email' in session:
        # get gearset instance
        gearset_instance = db.gearsets.find_one({'_id': ObjectId(gearset_id)})

        # get decoration info
        decoration_info = decoration_info.split('-')
        decoration_grade = decoration_info[1]
        decoration_name = decoration_info[0]
        
        # remove from weapon
        if gearset_instance['rampageslot'][0] == decoration_grade and gearset_instance['rampageslot'][1] == decoration_name:
            db.gearsets.update_one({'_id': gearset_instance['_id']}, {'$set': {'rampageslot': [decoration_grade, '']}})
            flash('Decoration removed.')
            return redirect(url_for('gearsets.view_gearset', gearset_id=gearset_id))
        else:
            flash('Error')
            return redirect(url_for('gearsets.view_gearset', gearset_id=gearset_id))
    else:
        flash('You must be logged in to do that.')
        return redirect(url_for('login'))

@gearsets.route('/delete_gearset/<gearset_id>', methods=['GET'])
def delete_gearset(gearset_id):
    if 'email' in session:
        obj_instance = ObjectId(gearset_id)
        gearset = db.gearsets.find_one({'_id': obj_instance})

        if gearset['user_id'] != db.users.find_one({'email': session['email']})['_id']:
            flash('You do not have permission to edit this gearset.')
            return render_template('overview.html', gearset=gearset, email=session['email'])

        db.gearsets.delete_one({'_id': obj_instance})
        flash('Gearset deleted')
        return redirect(url_for('gearsets.view_gearsets', email=session['email']))
    flash('You must be logged in to delete a gearset.')
    return render_template('login.html')