#!/usr/bin/env python3
"""Add Planetary Surveyor PDF content to the Foundry VTT database."""

import json
import random
import string

def generate_id(length=16):
    """Generate a random alphanumeric ID."""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

FOLDERS = {
    "Talents": "IU20IoXryabm8l17",
    "Combat Stunts": "L2Y3hw8oETegMcjg",
    "Exploration Stunts": "5kPoA2WkyKYaHcnq",
    "Social Stunts": "3nR4S7LWhxjIWXGn",
}

BASE_STATS = {
    "systemId": "expanse",
    "systemVersion": "1.0.1",
    "coreVersion": "10.291",
    "createdTime": None,
    "modifiedTime": None,
    "lastModifiedBy": None
}

# Planetary Surveyor Talent
planetary_surveyor_talent = {
    "_id": generate_id(),
    "name": "Planetary Surveyor",
    "type": "talent",
    "img": "systems/expanse/ui/item-img/talent-tablet.png",
    "effects": [],
    "folder": FOLDERS["Talents"],
    "sort": 0,
    "flags": {
        "the-expanse-quickstart": {
            "initialization-folder": "Talents",
            "sort": 0
        }
    },
    "system": {
        "description": "<p>Whether you were born on one or not, you are an expert on planets.</p>",
        "highest": "",
        "requirement": "Intelligence 2 or higher and the Intelligence (Planetary Sciences) focus.",
        "specialization": True,
        "ranks": {
            "novice": {
                "label": "novice",
                "effect": "<p>You know all about the planetary sciences. Add +1 to Intelligence (Planetary Sciences) tests.</p>",
                "active": False
            },
            "expert": {
                "label": "expert",
                "effect": "<p>You know what to look out for when you're on a planet (or in the water, or even the atmosphere). Subtract 2 from the TN to avoid planetary hazards.</p>",
                "active": False
            },
            "master": {
                "label": "master",
                "effect": "<p>You have a variety of skills that help you explore. Gain two of the following focuses if you don't have them already: Constitution (Stamina), Dexterity (Driving), Dexterity (Piloting), Perception (Survival), Perception (Tracking). If you already have all of these, pick two and add +1 to all rolls made using them.</p>",
                "active": False
            }
        }
    },
    "ownership": {"default": 0},
    "_stats": BASE_STATS.copy()
}

# Planetary Surveyor Stunts (Exploration - Survival)
surveyor_stunts = [
    {
        "_id": generate_id(),
        "name": "Dead Reckoning",
        "type": "stunt",
        "img": "systems/expanse/ui/item-img/stunt.png",
        "effects": [],
        "folder": FOLDERS["Exploration Stunts"],
        "sort": 0,
        "flags": {
            "the-expanse-quickstart": {
                "initialization-folder": "Exploration Stunts",
                "sort": 0
            }
        },
        "system": {
            "type": "Exploration",
            "name": "",
            "cost": "1+",
            "repeatable": True,
            "description": "<p>Your survival skills help you get the lay of the land, granting you a bonus of +1 per SP spent on your next use of Intelligence (Navigation) in the area.</p>"
        },
        "ownership": {"default": 0},
        "_stats": BASE_STATS.copy()
    },
    {
        "_id": generate_id(),
        "name": "Survivor's Mindset",
        "type": "stunt",
        "img": "systems/expanse/ui/item-img/stunt.png",
        "effects": [],
        "folder": FOLDERS["Exploration Stunts"],
        "sort": 0,
        "flags": {
            "the-expanse-quickstart": {
                "initialization-folder": "Exploration Stunts",
                "sort": 0
            }
        },
        "system": {
            "type": "Exploration",
            "name": "",
            "cost": "1+",
            "repeatable": True,
            "description": "<p>Your survivalist attitude steels your mind, giving you a bonus of +1 per SP spent on your next use of any Willpower focus in the area.</p>"
        },
        "ownership": {"default": 0},
        "_stats": BASE_STATS.copy()
    },
    {
        "_id": generate_id(),
        "name": "Frontier Medicine",
        "type": "stunt",
        "img": "systems/expanse/ui/item-img/stunt.png",
        "effects": [],
        "folder": FOLDERS["Exploration Stunts"],
        "sort": 0,
        "flags": {
            "the-expanse-quickstart": {
                "initialization-folder": "Exploration Stunts",
                "sort": 0
            }
        },
        "system": {
            "type": "Exploration",
            "name": "",
            "cost": "2+",
            "repeatable": True,
            "description": "<p>You use natural or makeshift remedies, or a first aid kit, to restore 1 Fortune point for every 2 SP spent.</p>"
        },
        "ownership": {"default": 0},
        "_stats": BASE_STATS.copy()
    },
    {
        "_id": generate_id(),
        "name": "Snakebite Kit",
        "type": "stunt",
        "img": "systems/expanse/ui/item-img/stunt.png",
        "effects": [],
        "folder": FOLDERS["Exploration Stunts"],
        "sort": 0,
        "flags": {
            "the-expanse-quickstart": {
                "initialization-folder": "Exploration Stunts",
                "sort": 0
            }
        },
        "system": {
            "type": "Exploration",
            "name": "",
            "cost": "3",
            "repeatable": False,
            "description": "<p>Using emergency techniques or some sort of antivenom, remove a condition caused by naturally occurring poison or venom.</p>"
        },
        "ownership": {"default": 0},
        "_stats": BASE_STATS.copy()
    },
    {
        "_id": generate_id(),
        "name": "Makeshift Sling",
        "type": "stunt",
        "img": "systems/expanse/ui/item-img/stunt.png",
        "effects": [],
        "folder": FOLDERS["Exploration Stunts"],
        "sort": 0,
        "flags": {
            "the-expanse-quickstart": {
                "initialization-folder": "Exploration Stunts",
                "sort": 0
            }
        },
        "system": {
            "type": "Exploration",
            "name": "",
            "cost": "4",
            "repeatable": False,
            "description": "<p>By using a splint or brace from the environment to reinforce an injury, reduce the penalty from an injured or wounded condition by 1 (to -0 or -1 respectively).</p>"
        },
        "ownership": {"default": 0},
        "_stats": BASE_STATS.copy()
    }
]

def main():
    with open('packs/the-expanse-quickstart.db', 'r') as f:
        db = json.loads(f.read().strip())

    existing_names = {item['name'] for item in db.get('items', [])}
    items_added = 0

    if planetary_surveyor_talent['name'] not in existing_names:
        db['items'].append(planetary_surveyor_talent)
        items_added += 1
        print(f"Added talent: {planetary_surveyor_talent['name']}")
    else:
        print(f"Skipped (exists): {planetary_surveyor_talent['name']}")

    for stunt in surveyor_stunts:
        if stunt['name'] not in existing_names:
            db['items'].append(stunt)
            items_added += 1
            print(f"Added stunt: {stunt['name']}")
        else:
            print(f"Skipped (exists): {stunt['name']}")

    with open('packs/the-expanse-quickstart.db', 'w') as f:
        f.write(json.dumps(db, separators=(',', ':')))

    print(f"\nTotal items added: {items_added}")
    return items_added

if __name__ == '__main__':
    main()
