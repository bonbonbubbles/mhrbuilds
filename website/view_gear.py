from flask_pymongo import PyMongo
from flask import Blueprint, render_template, request, flash, redirect, url_for, Flask, session
import os
from .database import db

view_gear = Blueprint('view_gear', __name__)

@view_gear.route('/')
@view_gear.route('/overview')
def overview():
    if 'email' in session:
        return render_template('overview.html', email=session['email'])
    return render_template('overview.html')

@view_gear.route('/weapon_overview', methods=['GET'])
def weapon_overview():
    if 'email' in session:
        return render_template('weapon_overview.html', email=session['email'])
    return render_template('weapon_overview.html')

@view_gear.route('/view_helmets', methods=['GET'])
def view_helmets():
        helmets = db.helmets.find()
        skills = db.skills.find()

        if 'email' in session:
            user = db.users.find_one({'email': session['email']})
            gearsets = db.gearsets.find({'user_id': user['_id']})
            return render_template('view_gear.html', gear_type="Helmets", gearsets=gearsets, gear_list=helmets, skills=skills, email=session['email'])

        return render_template('view_gear.html', gear_type="Helmets", gear_list=helmets, skills=skills)

@view_gear.route('/view_chest', methods=['GET'])
def view_chest():
    armor = db.armor.find()
    skills = db.skills.find()

    if 'email' in session:
        user = db.users.find_one({'email': session['email']})
        gearsets = db.gearsets.find({'user_id': user['_id']})
        return render_template('view_gear.html', gear_type="Chest", gearsets=gearsets, gear_list=armor, skills=skills, email=session['email'])

    return render_template('view_gear.html', gear_type="Chest", gear_list=armor, skills=skills)

@view_gear.route('/view_gloves', methods=['GET'])
def view_gloves():
    gloves = db.gloves.find()
    skills = db.skills.find()

    if 'email' in session:
        user = db.users.find_one({'email': session['email']})
        gearsets = db.gearsets.find({'user_id': user['_id']})
        return render_template('view_gear.html', gear_type="Gloves", gearsets=gearsets, gear_list=gloves, skills=skills, email=session['email'])

    return render_template('view_gear.html', gear_type="Gloves", gear_list=gloves, skills=skills)

@view_gear.route('/view_belts', methods=['GET'])
def view_belts():
    belts = db.belts.find()
    skills = db.skills.find()

    if 'email' in session:
        user = db.users.find_one({'email': session['email']})
        gearsets = db.gearsets.find({'user_id': user['_id']})
        return render_template('view_gear.html', gear_type="Belts", gearsets=gearsets, gear_list=belts, skills=skills, email=session['email'])
    return render_template('view_gear.html', gear_type="Belts", gear_list=belts, skills=skills)

@view_gear.route('/view_legs', methods=['GET'])
def view_legs():
    legs = db.legs.find()
    skills = db.skills.find()

    if 'email' in session:
        user = db.users.find_one({'email': session['email']})
        gearsets = db.gearsets.find({'user_id': user['_id']})
        return render_template('view_gear.html', gear_type="Legs", gearsets=gearsets, gear_list=legs, skills=skills, email=session['email'])

    return render_template('view_gear.html', gear_type="Legs", gear_list=legs, skills=skills)

@view_gear.route('/view_greatswords', methods=['GET'])
def greatswords():
    greatswords = db.weapons.find({'weapon_type': 'Greatsword'}).sort('rarity', -1)

    if 'email' in session:
        user = db.users.find_one({'email': session['email']})
        gearsets = db.gearsets.find({'user_id': user['_id']})
        return render_template('view_weapon_list.html', gearsets=gearsets, weapon_type='Greatswords', weapon_list=greatswords, email=session['email'])

    return render_template('view_weapon_list.html', weapon_type='Greatswords', weapon_list=greatswords)

@view_gear.route('/view_longswords', methods=['GET'])
def longswords():
    longswords = db.weapons.find({'weapon_type': 'Long Sword'}).sort('rarity', -1)

    if 'email' in session:
        user = db.users.find_one({'email': session['email']})
        gearsets = db.gearsets.find({'user_id': user['_id']})
        return render_template('view_weapon_list.html', weapon_type='Long Swords', gearsets=gearsets, weapon_list=longswords, email=session['email'])

    return render_template('view_weapon_list.html', weapon_type='Long Swords', weapon_list=longswords)

@view_gear.route('/view_swordshields', methods=['GET'])
def sword_and_shields():
    sword_and_shields = db.weapons.find({'weapon_type': 'Sword and Shield'}).sort('rarity', -1)

    if 'email' in session:
        user = db.users.find_one({'email': session['email']})
        gearsets = db.gearsets.find({'user_id': user['_id']})
        return render_template('view_weapon_list.html', weapon_type='Sword and Shields', gearsets=gearsets, weapon_list=sword_and_shields, email=session['email'])

    return render_template('view_weapon_list.html', weapon_type='Sword and Shields', weapon_list=sword_and_shields)

@view_gear.route('/view_dualblades', methods=['GET'])
def dual_blades():
    dual_blades = db.weapons.find({'weapon_type': 'Dual Blades'}).sort('rarity', -1)

    if 'email' in session:
        user = db.users.find_one({'email': session['email']})
        gearsets = db.gearsets.find({'user_id': user['_id']})
        return render_template('view_weapon_list.html', weapon_type='Dual Blades', gearsets=gearsets, weapon_list=dual_blades, email=session['email'])

    return render_template('view_weapon_list.html', weapon_type='Dual Blades', weapon_list=dual_blades)

@view_gear.route('/view_hammers', methods=['GET'])
def hammers():
    hammers = db.weapons.find({'weapon_type': 'Hammer'})

    if 'email' in session:
        user = db.users.find_one({'email': session['email']})
        gearsets = db.gearsets.find({'user_id': user['_id']})
        return render_template('view_weapon_list.html', weapon_type='Hammers', gearsets=gearsets, weapon_list=hammers, email=session['email'])

    return render_template('view_weapon_list.html', weapon_type='Hammers', weapon_list=hammers)

@view_gear.route('/view_huntinghorns', methods=['GET'])
def hunting_horns():
    hunting_horns = db.weapons.find({'weapon_type': 'Hunting Horn'})

    if 'email' in session:
        user = db.users.find_one({'email': session['email']})
        gearsets = db.gearsets.find({'user_id': user['_id']})
        return render_template('view_weapon_list_hh.html', weapon_type='Hunting Horns', gearsets=gearsets, weapon_list=hunting_horns, email=session['email'])

    return render_template('view_weapon_list_hh.html', weapon_type='Hunting Horns', weapon_list=hunting_horns)

@view_gear.route('/view_lances', methods=['GET'])
def lance():
    lance = db.weapons.find({'weapon_type': 'Lance'})

    if 'email' in session:
        user = db.users.find_one({'email': session['email']})
        gearsets = db.gearsets.find({'user_id': user['_id']})
        return render_template('view_weapon_list.html', weapon_type='Lances', gearsets=gearsets, weapon_list=lance, email=session['email'])

    return render_template('view_weapon_list.html', weapon_type='Lances', weapon_list=lance)

@view_gear.route('/view_gunlances', methods=['GET'])
def gunlances():
    gunlances = db.weapons.find({'weapon_type': 'Gunlance'})

    if 'email' in session:
        user = db.users.find_one({'email': session['email']})
        gearsets = db.gearsets.find({'user_id': user['_id']})
        return render_template('view_weapon_list.html', weapon_type='Gunlances', gearsets=gearsets, weapon_list=gunlances, email=session['email'])

    return render_template('view_weapon_list.html', weapon_type='Gunlances', weapon_list=gunlances)

@view_gear.route('/view_switchaxes', methods=['GET'])
def switch_axes():
    switch_axes = db.weapons.find({'weapon_type': 'Switch Axe'})

    if 'email' in session:
        user = db.users.find_one({'email': session['email']})
        gearsets = db.gearsets.find({'user_id': user['_id']})
        return render_template('view_weapon_list.html', weapon_type='Switch Axes', gearsets=gearsets, weapon_list=switch_axes, email=session['email'])

    return render_template('view_weapon_list.html', weapon_type='Switch Axes', weapon_list=switch_axes)

@view_gear.route('/view_chargeblades', methods=['GET'])
def charge_blades():
    charge_blades = db.weapons.find({'weapon_type': 'Charge Blade'})

    if 'email' in session:
        user = db.users.find_one({'email': session['email']})
        gearsets = db.gearsets.find({'user_id': user['_id']})
        return render_template('view_weapon_list.html', weapon_type='Charge Blades', gearsets=gearsets, weapon_list=charge_blades, email=session['email'])

    return render_template('view_weapon_list.html', weapon_type='Charge Blades', weapon_list=charge_blades)

@view_gear.route('/view_insectglaives', methods=['GET'])
def insect_glaives():
    insect_glaives = db.weapons.find({'weapon_type': 'Insect Glaive'})

    if 'email' in session:
        user = db.users.find_one({'email': session['email']})
        gearsets = db.gearsets.find({'user_id': user['_id']})
        return render_template('view_weapon_list.html', weapon_type='Insect Glaives', gearsets=gearsets, weapon_list=insect_glaives, email=session['email'])

    return render_template('view_weapon_list.html', weapon_type='Insect Glaives', weapon_list=insect_glaives)

@view_gear.route('/view_bows', methods=['GET'])
def bows():
    bows = db.weapons.find({'weapon_type': 'Bow'})

    if 'email' in session:
        user = db.users.find_one({'email': session['email']})
        gearsets = db.gearsets.find({'user_id': user['_id']})
        return render_template('view_weapon_list_bow.html', weapon_type='Bows', gearsets=gearsets, weapon_list=bows, email=session['email'])

    return render_template('view_weapon_list_bow.html', weapon_type='Bows', weapon_list=bows)

@view_gear.route('/view_heavybowguns', methods=['GET'])
def heavy_bowguns():
    heavy_bowguns = db.weapons.find({'weapon_type': 'Heavy Bowgun'})

    if 'email' in session:
        user = db.users.find_one({'email': session['email']})
        gearsets = db.gearsets.find({'user_id': user['_id']})
        return render_template('view_weapon_list.html', weapon_type='Heavy Bowguns', gearsets=gearsets, weapon_list=heavy_bowguns, email=session['email'])

    return render_template('view_weapon_list.html', weapon_type='Heavy Bowguns', weapon_list=heavy_bowguns)

@view_gear.route('/view_lightbowguns', methods=['GET'])
def light_bowguns():
    light_bowguns = db.weapons.find({'weapon_type': 'Light Bowgun'})

    if 'email' in session:
        user = db.users.find_one({'email': session['email']})
        gearsets = db.gearsets.find({'user_id': user['_id']})
        return render_template('view_weapon_list.html', weapon_type='Light Bowguns', gearsets=gearsets, weapon_list=light_bowguns, email=session['email'])

    return render_template('view_weapon_list.html', weapon_type='Light Bowguns', weapon_list=light_bowguns)

@view_gear.route('/view_decorations', methods=['GET'])
def decorations():
    decorations = db.decorations.find()

    if 'email' in session:
        user = db.users.find_one({'email': session['email']})
        gearsets = db.gearsets.find({'user_id': user['_id']})
        return render_template('view_decorations.html', gearsets=gearsets, decorations=decorations, email=session['email'])

    return render_template('view_decorations.html', decorations=decorations, weapon_list=decorations)

@view_gear.route('/view_rampage_decorations', methods=['GET'])
def rampage_decorations():
    rampage_decorations = db.rampage_decorations.find()

    if 'email' in session:
        user = db.users.find_one({'email': session['email']})
        gearsets = db.gearsets.find({'user_id': user['_id']})
        return render_template('view_rampage_decos.html', gearsets=gearsets, decorations=rampage_decorations, email=session['email'])

    return render_template('view_rampage_decos.html', decorations=rampage_decorations)