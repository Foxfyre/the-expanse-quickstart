#!/usr/bin/env python3
"""Add TUE Core weapons to the Foundry VTT database."""

import json
import random
import string

def generate_id(length=16):
    """Generate a random alphanumeric ID."""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

# Base stats template
BASE_STATS = {
    "systemId": "expanse",
    "systemVersion": "1.0.1",
    "coreVersion": "10.291",
    "createdTime": None,
    "modifiedTime": None,
    "lastModifiedBy": None
}

# Weapons from TUE Core Chapter 4
WEAPONS = [
    # Close Weapons - Light
    {
        "name": "Ceramic Tactical Knife",
        "type": "light_melee",
        "damage": 1,
        "dieFaces": 6,
        "cost": 8,
        "modifier": "Dexterity",
        "description": "<p>These combat knives are crafted of high strength ceramic and can easily pass through a metal detector if the hilt is only ceramic and plastic.</p>"
    },
    {
        "name": "Combat Knife",
        "type": "light_melee",
        "damage": 1,
        "dieFaces": 6,
        "cost": 6,
        "modifier": "Dexterity",
        "description": "<p>These double-sided blades are usually about 18 cm long and are crafted with high carbon steel for high durability and sharpness. They often have a serrated edge on one side, closest to the grip.</p>"
    },
    # Close Weapons - Heavy
    {
        "name": "Sword",
        "type": "heavy_melee",
        "damage": 2,
        "dieFaces": 6,
        "cost": 7,
        "modifier": "Strength",
        "description": "<p>This can be any long-bladed weapon that is designed for slashing and piercing.</p>"
    },
    {
        "name": "Stun Baton",
        "type": "light_melee",
        "damage": 1,
        "dieFaces": 6,
        "cost": 10,
        "modifier": "Strength",
        "description": "<p>This bludgeoning weapon discharges paralyzing electrical shocks in close combat. A stun baton has no effect on a target in armor. If it hits a target without armor, it paralyzes the individual for 1d6 rounds unless they succeed on a Constitution (Stamina) test with a TN of 10 + the damage inflicted by the weapon. Strength does not add to a stun baton's damage.</p>"
    },
    # Pistols
    {
        "name": "Automatic Machine Pistol",
        "type": "pistol",
        "damage": 2,
        "dieFaces": 6,
        "cost": 14,
        "modifier": "Perception",
        "rangemin": "10",
        "rangemax": "20",
        "description": "<p>Small, concealable machine guns are a popular weapon among covert forces. They have both the Automatic quality and the Concealable quality.</p>",
        "quality": "Automatic, Concealable"
    },
    {
        "name": "Flechette Pistol",
        "type": "pistol",
        "damage": 2,
        "dieFaces": 6,
        "cost": 12,
        "modifier": "Perception",
        "rangemin": "10",
        "rangemax": "20",
        "description": "<p>This gun shoots salvoes containing many small fragments of metal, ceramic shards, or other material, tearing jagged holes in flesh and other soft matter but inflicting minimal damage on harder structures. Fléchette guns have the Anti-Personnel quality.</p>",
        "quality": "Anti-Personnel"
    },
    {
        "name": "Semi-automatic Pistol",
        "type": "pistol",
        "damage": 2,
        "dieFaces": 6,
        "cost": 10,
        "modifier": "Perception",
        "rangemin": "10",
        "rangemax": "20",
        "description": "<p>A semi-automatic pistol automatically ejects and reloads a new cartridge with every shot. A semi-automatic only fires one shot per pull of the trigger. This is the most common type of handgun found in The Expanse.</p>"
    },
    {
        "name": "Revolver",
        "type": "pistol",
        "damage": 2,
        "dieFaces": 6,
        "cost": 9,
        "modifier": "Perception",
        "rangemin": "10",
        "rangemax": "20",
        "description": "<p>A revolver uses a revolving cylinder with multiple chambers (usually six). While limited in ammo capacity, they are extremely unlikely to jam.</p>"
    },
    {
        "name": "Stun Pistol",
        "type": "pistol",
        "damage": 1,
        "dieFaces": 6,
        "cost": 10,
        "modifier": "Perception",
        "rangemin": "6",
        "rangemax": "12",
        "description": "<p>A stun pistol is a ranged weapon that fires a pair of darts that carry a powerful electrical charge that inflicts penetrating damage but can only incapacitate the target.</p>",
        "quality": "Stunning"
    },
    # Rifles
    {
        "name": "Assault Rifle",
        "type": "rifle",
        "damage": 3,
        "dieFaces": 6,
        "cost": 12,
        "modifier": "Perception",
        "rangemin": "30",
        "rangemax": "60",
        "description": "<p>Extremely powerful and versatile, this rifle is fully capable of automatic fire while also being capable of several other modes (single shot, short burst, and fully automatic). This weapon has the Automatic Quality.</p>",
        "quality": "Automatic"
    },
    {
        "name": "Grenade Launcher",
        "type": "rifle",
        "damage": 0,
        "dieFaces": 6,
        "cost": 15,
        "modifier": "Perception",
        "rangemin": "20",
        "rangemax": "40",
        "description": "<p>A character can fire any kind of grenade from a grenade launcher instead of throwing it. Damage is the same as the equivalent thrown grenade.</p>"
    },
    {
        "name": "Riot Gun",
        "type": "rifle",
        "damage": 2,
        "dieFaces": 6,
        "cost": 11,
        "modifier": "Perception",
        "rangemin": "10",
        "rangemax": "20",
        "description": "<p>Frequently employed by security forces during times of particular strife, riot guns fire non-lethal crowd suppression rounds to immobilize targets instead of wounding them. They have the Suppression quality.</p>",
        "quality": "Suppression, Non-lethal"
    },
    {
        "name": "Shotgun",
        "type": "rifle",
        "damage": 2,
        "dieFaces": 6,
        "cost": 10,
        "modifier": "Perception",
        "rangemin": "8",
        "rangemax": "16",
        "description": "<p>The shotgun is a long-barreled firearm that fires a cartridge containing shot (smaller projectiles) or a single large slug. If using shot, the shotgun has the Spreading quality.</p>",
        "quality": "Spreading"
    },
    {
        "name": "Sniper Rifle",
        "type": "rifle",
        "damage": 4,
        "dieFaces": 6,
        "cost": 15,
        "modifier": "Perception",
        "rangemin": "60",
        "rangemax": "120",
        "description": "<p>This is an extremely accurate, long-range rifle intended to take out a target from far away. This weapon has the Long Range quality and inflicts +1d6 damage.</p>",
        "quality": "Long Range"
    },
    {
        "name": "Submachine Gun",
        "type": "rifle",
        "damage": 2,
        "dieFaces": 6,
        "cost": 13,
        "modifier": "Perception",
        "rangemin": "20",
        "rangemax": "40",
        "description": "<p>This automatic weapon fires rifle cartridges from a magazine. They are shorter and more compact than assault rifles but do not have the same range or stopping power. This weapon has the Automatic quality and the Ineffective flaw.</p>",
        "quality": "Automatic, Ineffective"
    },
    # Grenades
    {
        "name": "Frag Grenade",
        "type": "thrown",
        "damage": 3,
        "dieFaces": 6,
        "cost": 10,
        "modifier": "Accuracy",
        "rangemin": "4",
        "rangemax": "8",
        "description": "<p>A fragmentation grenade that explodes into deadly shrapnel. Affects all targets within the blast radius.</p>"
    },
    {
        "name": "Flash Grenade",
        "type": "thrown",
        "damage": 0,
        "dieFaces": 6,
        "cost": 8,
        "modifier": "Accuracy",
        "rangemin": "4",
        "rangemax": "8",
        "description": "<p>Also called a flashbang, this grenade produces a blinding flash and deafening bang that stuns targets. Affected targets are blinded and deafened for 1d6 rounds unless they make a successful Constitution (Stamina) test.</p>",
        "quality": "Non-lethal, Stunning"
    },
    {
        "name": "Smoke Grenade",
        "type": "thrown",
        "damage": 0,
        "dieFaces": 6,
        "cost": 6,
        "modifier": "Accuracy",
        "rangemin": "4",
        "rangemax": "8",
        "description": "<p>This grenade produces a thick cloud of smoke that obscures vision. The smoke provides concealment for anyone in the area.</p>"
    },
]


def create_folder(name, folder_type="Item", parent=None):
    """Create a folder entry."""
    return {
        "_id": generate_id(),
        "name": name,
        "type": folder_type,
        "folder": parent,
        "description": "",
        "sorting": "a",
        "sort": 0,
        "color": None,
        "flags": {}
    }


def create_weapon(weapon_data, folder_id, folder_name):
    """Create a weapon item entry."""
    # Get image based on type
    img_map = {
        "light_melee": "systems/expanse/ui/item-img/item-light_melee.png",
        "heavy_melee": "systems/expanse/ui/item-img/item-heavy_melee.png",
        "pistol": "systems/expanse/ui/item-img/item-pistol.png",
        "rifle": "systems/expanse/ui/item-img/item-rifle.png",
        "thrown": "systems/expanse/ui/item-img/item-improvised.png",
        "unarmed": "systems/expanse/ui/item-img/item-unarmed.png",
    }

    return {
        "_id": generate_id(),
        "name": weapon_data["name"],
        "type": "weapon",
        "img": img_map.get(weapon_data["type"], "systems/expanse/ui/item-img/item-improvised.png"),
        "effects": [],
        "folder": folder_id,
        "sort": 0,
        "flags": {
            "the-expanse-quickstart": {
                "initialization-folder": folder_name,
                "sort": 0
            }
        },
        "system": {
            "name": "",
            "type": weapon_data["type"],
            "group": "",
            "attack": "",
            "npcattack": "",
            "usefocus": False,
            "usefocusplus": False,
            "damage": weapon_data["damage"],
            "hasBonusDamage": False,
            "bonusDamage": 0,
            "rangemin": weapon_data.get("rangemin", "0"),
            "rangemax": weapon_data.get("rangemax", "0"),
            "range": "",
            "cost": weapon_data["cost"],
            "equipped": False,
            "description": weapon_data["description"],
            "modifier": weapon_data["modifier"],
            "bonusModifier": "",
            "tohitabil": "",
            "quality": weapon_data.get("quality", ""),
            "manualDamage": 0,
            "dieFaces": weapon_data["dieFaces"]
        },
        "ownership": {"default": 0},
        "_stats": BASE_STATS.copy()
    }


def main():
    # Read existing database
    with open('packs/the-expanse-quickstart.db', 'r') as f:
        db = json.load(f)

    # Get existing item names to avoid duplicates
    existing_names = {item['name'] for item in db.get('items', [])}
    existing_folder_names = {f['name'] for f in db.get('folders', [])}

    items_added = 0

    # Find the Weapons folder
    weapons_folder_id = None
    for folder in db.get('folders', []):
        if folder['name'] == 'Weapons':
            weapons_folder_id = folder['_id']
            break

    # Add weapons
    for weapon_data in WEAPONS:
        if weapon_data['name'] not in existing_names:
            weapon = create_weapon(weapon_data, weapons_folder_id, "Weapons")
            db['items'].append(weapon)
            items_added += 1
            existing_names.add(weapon_data['name'])
            print(f"Added weapon: {weapon_data['name']}")
        else:
            print(f"Skipped (exists): {weapon_data['name']}")

    # Write updated database
    with open('packs/the-expanse-quickstart.db', 'w') as f:
        json.dump(db, f, separators=(',', ':'))

    print(f"\nTotal weapons added: {items_added}")
    return items_added


if __name__ == '__main__':
    main()
