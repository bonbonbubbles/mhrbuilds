from .database import db
from bson import ObjectId

def get_skill_names_from_gear(gear):
    skills = gear['skills']
    skills_list = []
    for skill in skills:
        if skill[0] != "" and skill[0] is not None:
            skill_name = skill[0]
            skill_level = int(skill[1])
                # get max of skill from db
            skill_info = db.skills.find_one({'name': skill_name})
            skills_list.append([skill_name, int(skill_info['max']), skill_level])
    return skills_list

def get_slot_info_from_gearlist(gearset):
    try:
        weapon_slot1 = gearset['weaponslot1']
    except KeyError:
        weapon_slot1 = ["", ""]
    try:
        weapon_slot2 = gearset['weaponslot2']
    except KeyError:
        weapon_slot2 = ["", ""]
    try:
        weapon_slot3 = gearset['weaponslot3']
    except KeyError:
        weapon_slot3 = ["", ""]
    try:
        helmet_slot1 = gearset['helmetslot1']
    except KeyError:
        helmet_slot1 = ["", ""]
    try:
        helmet_slot2 = gearset['helmetslot2']
    except KeyError:
        helmet_slot2 = ["", ""]
    try:
        helmet_slot3 = gearset['helmetslot3']
    except KeyError:
        helmet_slot3 = ["", ""]
    try:
        armor_slot1 = gearset['armorslot1']
    except KeyError:
        armor_slot1 = ["", ""]
    try:
        armor_slot2 = gearset['armorslot2']
    except KeyError:
        armor_slot2 = ["", ""]
    try:
        armor_slot3 = gearset['armorslot3']
    except KeyError:
        armor_slot3 = ["", ""]
    try:
        gloves_slot1 = gearset['glovesslot1']
    except KeyError:
        gloves_slot1 = ["", ""]
    try:
        gloves_slot2 = gearset['glovesslot2']
    except KeyError:
        gloves_slot2 = ["", ""]
    try:
        gloves_slot3 = gearset['glovesslot3']
    except KeyError:
        gloves_slot3 = ["", ""]
    try:
        belt_slot1 = gearset['beltslot1']
    except KeyError:
        belt_slot1 = ["", ""]
    try:
        belt_slot2 = gearset['beltslot2']
    except KeyError:
        belt_slot2 = ["", ""]
    try:
        belt_slot3 = gearset['beltslot3']
    except KeyError:
        belt_slot3 = ["", ""]
    try:
        legs_slot1 = gearset['legsslot1']
    except KeyError:
        legs_slot1 = ["", ""]
    try:
        legs_slot2 = gearset['legsslot2']
    except KeyError:
        legs_slot2 = ["", ""]
    try:
        legs_slot3 = gearset['legsslot3']
    except KeyError:
        legs_slot3 = ["", ""]

    # make a dictionary of slot grade : name
    slot_info = {'weaponslot1': weapon_slot1, 'weaponslot2': weapon_slot2, 'weaponslot3': weapon_slot3, 'helmetslot1': helmet_slot1, 'helmetslot2': helmet_slot2, 'helmetslot3': helmet_slot3,
                'armorslot1': armor_slot1, 'armorslot2': armor_slot2, 'armorslot3': armor_slot3, 'glovesslot1': gloves_slot1, 'glovesslot2':gloves_slot2, 'glovesslot3': gloves_slot3,
                'beltslot1': belt_slot1, 'beltslot2': belt_slot2, 'beltslot3': belt_slot3, 'legsslot1': legs_slot1, 'legsslot2': legs_slot2, 'legsslot3': legs_slot3}

    for slot in slot_info:
        # match decoration name to decoration skill
        if slot_info[slot][1] != "":
            decoration_info = db.decorations.find_one({'name': slot_info[slot][1]})
            try:
                slot_info[slot].append(decoration_info['skill'])
            except TypeError:
                slot_info[slot].append("")
        else:
            slot_info[slot].append("")

    for slot in slot_info:
        # append skill maximum value to slot info
        if slot_info[slot][1] != "":
            try:
                slot_info[slot].append(db.skills.find_one({'name': slot_info[slot][2]})['max'])
            except TypeError:
                slot_info[slot].append('')

    return slot_info
