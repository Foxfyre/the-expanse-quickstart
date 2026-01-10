#!/usr/bin/env python3
"""Add Scout PDF content to the Foundry VTT database."""

import json
import random
import string

def generate_id(length=16):
    """Generate a random alphanumeric ID."""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

# Folder IDs from existing database
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

# Scout Talent
scout_talent = {
    "_id": generate_id(),
    "name": "Scout",
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
        "description": "<p>You're skilled at understanding an area of space and finding what you're looking for.</p>",
        "highest": "",
        "requirement": "Intelligence 2 or higher and the Intelligence (Astronomy) focus.",
        "specialization": True,
        "ranks": {
            "novice": {
                "label": "novice",
                "effect": "<p>You are adept at making the most of your instruments when looking for something. If you fail an Intelligence (Technology) test when using sensors, you can re-roll it but must keep the result of the second roll.</p>",
                "active": False
            },
            "expert": {
                "label": "expert",
                "effect": "<p>Your astronomical abilities are unrivaled. When you make an Intelligence (Astronomy) test as part of an advanced test, you gain a +1 bonus to the result of each Drama Die. This increases your total roll and allows you to reach the success threshold faster.</p>",
                "active": False
            },
            "master": {
                "label": "master",
                "effect": "<p>When you perform tests using ship sensors, treat them as if their Sensors rating is 1 higher.</p>",
                "active": False
            }
        }
    },
    "ownership": {"default": 0},
    "_stats": BASE_STATS.copy()
}

# Scout Stunts (Vehicle Combat - Ship Sensors)
scout_stunts = [
    {
        "_id": generate_id(),
        "name": "Eye Patch",
        "type": "stunt",
        "img": "systems/expanse/ui/item-img/stunt.png",
        "effects": [],
        "folder": FOLDERS["Combat Stunts"],
        "sort": 0,
        "flags": {
            "the-expanse-quickstart": {
                "initialization-folder": "Combat Stunts",
                "sort": 0
            }
        },
        "system": {
            "type": "Combat",
            "name": "",
            "cost": "1+",
            "repeatable": True,
            "description": "<p>Reduce the TN of a damage control test to repair a loss to Sensors by 1 for each SP spent.</p>"
        },
        "ownership": {"default": 0},
        "_stats": BASE_STATS.copy()
    },
    {
        "_id": generate_id(),
        "name": "Eat Static",
        "type": "stunt",
        "img": "systems/expanse/ui/item-img/stunt.png",
        "effects": [],
        "folder": FOLDERS["Combat Stunts"],
        "sort": 0,
        "flags": {
            "the-expanse-quickstart": {
                "initialization-folder": "Combat Stunts",
                "sort": 0
            }
        },
        "system": {
            "type": "Combat",
            "name": "",
            "cost": "1+",
            "repeatable": True,
            "description": "<p>You adjust your ship's active emissions in a way that makes it harder to target, adding +SP to your ship's next electronic warfare test.</p>"
        },
        "ownership": {"default": 0},
        "_stats": BASE_STATS.copy()
    },
    {
        "_id": generate_id(),
        "name": "Exploitable Terrain",
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
            "description": "<p>If you are near appropriate exploitable terrain (asteroid field, dust cloud), you spot a path near or through it that the pilot (whether you or another character) can use as protective cover. Immediately trigger either the Evasive Maneuver or Follow the Leader chase stunt.</p>"
        },
        "ownership": {"default": 0},
        "_stats": BASE_STATS.copy()
    }
]

def main():
    # Read existing database
    with open('packs/the-expanse-quickstart.db', 'r') as f:
        db = json.loads(f.read().strip())

    # Get existing item names to avoid duplicates
    existing_names = {item['name'] for item in db.get('items', [])}

    items_added = 0

    # Add talent if not exists
    if scout_talent['name'] not in existing_names:
        db['items'].append(scout_talent)
        items_added += 1
        print(f"Added talent: {scout_talent['name']}")
    else:
        print(f"Skipped (exists): {scout_talent['name']}")

    # Add stunts if not exist
    for stunt in scout_stunts:
        if stunt['name'] not in existing_names:
            db['items'].append(stunt)
            items_added += 1
            print(f"Added stunt: {stunt['name']}")
        else:
            print(f"Skipped (exists): {stunt['name']}")

    # Write updated database (single line JSON)
    with open('packs/the-expanse-quickstart.db', 'w') as f:
        f.write(json.dumps(db, separators=(',', ':')))

    print(f"\nTotal items added: {items_added}")
    return items_added

if __name__ == '__main__':
    items_added = main()
