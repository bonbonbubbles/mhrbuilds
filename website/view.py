from flask_pymongo import PyMongo
from flask import Blueprint, render_template, request, flash, redirect, url_for, Flask, session
import os
from .database import db

view = Blueprint('view', __name__)

@view.route('/about', methods=['GET'])
def about():
    if 'email' in session:
        return render_template('about.html', email=session['email'])
    return render_template('about.html')

@view.route('/view_skills', methods=['GET'])
def view_skills():
    skills = db.skills.find().sort("name")
    if 'email' in session:
        return render_template('view_skills.html', skills=skills, email=session['email'])
    return render_template('view_skills.html', skills=skills)

@view.route('/edit_skill/<skill_name>', methods=['GET', 'POST'])
def edit_skill(skill_name):
    if request.method == 'POST':
        description = request.form['description']
        rank1 = request.form['rank1']
        rank2 = request.form['rank2']
        rank3 = request.form['rank3']
        rank4 = request.form['rank4']
        rank5 = request.form['rank5']
        rank6 = request.form['rank6']
        rank7 = request.form['rank7']

        db.skills.update_one({'name': skill_name}, {'$set': {'description': description, 'rank1': rank1, 'rank2': rank2, 'rank3': rank3, 'rank4': rank4, 'rank5': rank5,
                                                            'rank6': rank6, 'rank7': rank7}})
        return redirect(url_for('view.view_skills'))
    else:
        skill = db.skills.find_one({'name': skill_name})
        if 'email' in session:
            return render_template('edit_skill.html', skill=skill, email=session['email'])
        return render_template('edit_skill.html', skill=skill)

@view.route('/view_gear_skill/<skill_name>', methods=['GET'])
def view_gear_skill(skill_name):
    helmets_query = db.helmets.find()
    gloves_query = db.gloves.find()
    belts_query = db.belts.find()
    legs_query = db.legs.find()
    armor_query = db.armor.find()

    helmets = []
    gloves = []
    belts = []
    legs = []
    armor = []

    for helmet in helmets_query:
        for skill in helmet['skills']:
            if skill[0] == skill_name:
                helmets.append(helmet)
    for glove in gloves_query:
        for skill in glove['skills']:
            if skill[0] == skill_name:
                gloves.append(glove)
    for belt in belts_query:
        for skill in belt['skills']:
            if skill[0] == skill_name:
                belts.append(belt)
    for leg in legs_query:
        for skill in leg['skills']:
            if skill[0] == skill_name:
                legs.append(leg)
    for item in armor_query:
        for skill in item['skills']:
            if skill[0] == skill_name:
                armor.append(item)

    decorations = db.decorations.find({'skill': skill_name})

    if 'email' in session:
        user_info = db.users.find_one({'email': session['email']})
        gearsets = db.gearsets.find({'user_id': user_info['_id']})
        return render_template('view_gear_by_skill.html', helmets=helmets, decorations=decorations, gearsets=gearsets, chests=armor, gloves=gloves, belts=belts, legs=legs, skill_name=skill_name, email=session['email'])
    return render_template('view_gear_by_skill.html', helmets=helmets, decorations=decorations, chests=armor, gloves=gloves, belts=belts, legs=legs, skill_name=skill_name)

@view.route('/convert_weapon_skills_to_list', methods=['GET'])
def convert_weapon_skills_to_list():
    weapons = db.weapons.find()
    for weapon in weapons:
        if 'skill1' in weapon:
            skill1 = weapon['skill1']
            skill2 = weapon['skill2']
            skill3 = weapon['skill3']
            skill4 = weapon['skill4']
            try:
                skill5 = weapon['skill5']
            except:
                skill5 = None
            try:
                skill6 = weapon['skill6']
            except:
                skill6 = None
            try:
                skill7 = weapon['skill7']
            except:
                skill7 = None
            try:
                skill8 = weapon['skill8']
            except:
                skill8 = None
            try:
                skill9 = weapon['skill9']
            except:
                skill9 = None
            try:
                skill10 = weapon['skill10']
            except:
                skill10 = None
            try:
                skill11 = weapon['skill11']
            except:
                skill11 = None
            try:
                skill12 = weapon['skill12']
            except:
                skill12 = None
            try:
                skill13 = weapon['skill13']
            except:
                skill13 = None
            try:
                skill14 = weapon['skill14']
            except:
                skill14 = None
            try:
                skill15 = weapon['skill15']
            except:
                skill15 = None
            try:
                skill16 = weapon['skill16']
            except:
                skill16 = None
            try:
                skill17 = weapon['skill17']
            except:
                skill17 = None
            try:
                skill18 = weapon['skill18']
            except:
                skill18 = None
            try:
                skill19 = weapon['skill19']
            except:
                skill19 = None
            try:
                skill20 = weapon['skill20']
            except:
                skill20 = None
            try:
                skill21 = weapon['skill21']
            except:
                skill21 = None
            db.weapons.update_one({'_id': weapon['_id']}, {'$set': {'skills': [skill1, skill2, skill3, skill4, skill5, skill6, skill7, skill8, skill9, skill10, skill11, skill12,
                                                                                skill13, skill14, skill15, skill16, skill17, skill18, skill19, skill20, skill21]}})
    return redirect(url_for('view_gear.view_weapons'))

@view.route('/remove_weapon_skills', methods=['GET'])
def remove_weapon_skills():
    weapons = db.weapons.find()
    for weapon in weapons:
        if 'skill1' in weapon:
            db.weapons.update_one({'_id': weapon['_id']}, {'$unset': {'skill1': ''}})
            db.weapons.update_one({'_id': weapon['_id']}, {'$unset': {'skill2': ''}})
            db.weapons.update_one({'_id': weapon['_id']}, {'$unset': {'skill3': ''}})
            db.weapons.update_one({'_id': weapon['_id']}, {'$unset': {'skill4': ''}})
            db.weapons.update_one({'_id': weapon['_id']}, {'$unset': {'skill5': ''}})
            db.weapons.update_one({'_id': weapon['_id']}, {'$unset': {'skill6': ''}})
            db.weapons.update_one({'_id': weapon['_id']}, {'$unset': {'skill7': ''}})
            db.weapons.update_one({'_id': weapon['_id']}, {'$unset': {'skill8': ''}})
            db.weapons.update_one({'_id': weapon['_id']}, {'$unset': {'skill9': ''}})
            db.weapons.update_one({'_id': weapon['_id']}, {'$unset': {'skill10': ''}})
            db.weapons.update_one({'_id': weapon['_id']}, {'$unset': {'skill11': ''}})
            db.weapons.update_one({'_id': weapon['_id']}, {'$unset': {'skill12': ''}})
            db.weapons.update_one({'_id': weapon['_id']}, {'$unset': {'skill13': ''}})
            db.weapons.update_one({'_id': weapon['_id']}, {'$unset': {'skill14': ''}})
            db.weapons.update_one({'_id': weapon['_id']}, {'$unset': {'skill15': ''}})
            db.weapons.update_one({'_id': weapon['_id']}, {'$unset': {'skill16': ''}})
            db.weapons.update_one({'_id': weapon['_id']}, {'$unset': {'skill17': ''}})
            db.weapons.update_one({'_id': weapon['_id']}, {'$unset': {'skill18': ''}})
            db.weapons.update_one({'_id': weapon['_id']}, {'$unset': {'skill19': ''}})
            db.weapons.update_one({'_id': weapon['_id']}, {'$unset': {'skill20': ''}})
            db.weapons.update_one({'_id': weapon['_id']}, {'$unset': {'skill21': ''}})
    return redirect(url_for('view_gear.view_weapons'))

@view.route('/convert_rarity_strings_to_int', methods=['GET'])
def convert_string_to_int():
    db.weapons.update_many({}, [{'$set': {'rarity': {'$toInt': '$rarity'}}}])
    return 'done'