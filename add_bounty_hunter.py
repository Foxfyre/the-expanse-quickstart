#!/usr/bin/env python3
"""Add Bounty Hunter PDF content to the Foundry VTT database."""

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

# Base stats template
BASE_STATS = {
    "systemId": "expanse",
    "systemVersion": "1.0.1",
    "coreVersion": "10.291",
    "createdTime": None,
    "modifiedTime": None,
    "lastModifiedBy": None
}

# Bounty Hunter Talent
bounty_hunter_talent = {
    "_id": generate_id(),
    "name": "Bounty Hunter",
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
        "description": "<p>You're a dogged tracker and bounty hunter.</p>",
        "highest": "",
        "requirement": "Perception 2 or higher and at least one Perception focus.",
        "specialization": True,
        "ranks": {
            "novice": {
                "label": "novice",
                "effect": "<p>You can designate someone or something as your \"quarry\" after spending at least an hour on the job investigating them. You can only have one active quarry at a time. You're considered to always have the tangential focus necessary to investigate your quarry, and if you have the primary or tangential focus, you gain a +1 bonus on your tests to investigate them. You also gain the benefits of the Dexterity (Initiative) and Perception (Intuition) focuses with regard to your designated quarry. If you already have these focuses, you gain an additional +1 bonus from them regarding your quarry.</p>",
                "active": False
            },
            "expert": {
                "label": "expert",
                "effect": "<p>You can prepare a major action in relation to your quarry. Whenever you roll initiative against your quarry, you can perform your prepared action first before your quarry acts regardless of the initiative order; you then take your normal actions on your turn. Prepared actions may include things like a Run or Charge towards your quarry, an Attack against them, an attempt to hide from them, or a Stunt Attack directed at them.</p>",
                "active": False
            },
            "master": {
                "label": "master",
                "effect": "<p>When you surprise your quarry, you are automatically considered to have them dead-to-rights. You have a +2 bonus for any tests to see if you surprise your quarry. Also, if you fail an ability test to unlock a clue related to your quarry, you can re-roll the test and use the result of the second roll instead.</p>",
                "active": False
            }
        }
    },
    "ownership": {"default": 0},
    "_stats": BASE_STATS.copy()
}

# Bounty Hunting Stunts
bounty_hunting_stunts = [
    {
        "_id": generate_id(),
        "name": "The Upper Hand (Bounty)",
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
            "cost": "1-4",
            "repeatable": False,
            "description": "<p>During the making contact encounter, you gain a bonus to your initiative test against your target equal to the SP spent (up to +4). This is a version of The Upper Hand exploration stunt unique to bounty hunting.</p>"
        },
        "ownership": {"default": 0},
        "_stats": BASE_STATS.copy()
    },
    {
        "_id": generate_id(),
        "name": "What Makes Them Tick",
        "type": "stunt",
        "img": "systems/expanse/ui/item-img/stunt.png",
        "effects": [],
        "folder": FOLDERS["Social Stunts"],
        "sort": 0,
        "flags": {
            "the-expanse-quickstart": {
                "initialization-folder": "Social Stunts",
                "sort": 0
            }
        },
        "system": {
            "type": "Social",
            "name": "",
            "cost": "2-6",
            "repeatable": False,
            "description": "<p>You get a real sense for your target and what motivates them; for your next social encounter with the target, you gain a bonus to all interaction tests equal to half the SP spent (up to +3 for 6 SP).</p>"
        },
        "ownership": {"default": 0},
        "_stats": BASE_STATS.copy()
    },
    {
        "_id": generate_id(),
        "name": "Saw That Coming",
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
            "cost": "5",
            "repeatable": False,
            "description": "<p>When you make contact with your target, you can choose one thing that they do in response to you, when it happens, and retroactively declare you had previously prepared for it. So, for example, if the target ducks out the back exit, you can use this stunt to declare you have an ally waiting there for them. The GM approves your choice, and it can only involve resources reasonably at your disposal during the hunt.</p>"
        },
        "ownership": {"default": 0},
        "_stats": BASE_STATS.copy()
    }
]

# Equipment items - need to check if there's an "item" type or use a generic approach
# For now, we'll add them as items with type "item" if that exists, or create journal entries
bounty_hunting_equipment = [
    {
        "_id": generate_id(),
        "name": "Bypass",
        "type": "item",
        "img": "systems/expanse/ui/item-img/item.png",
        "effects": [],
        "folder": None,  # Will create Equipment folder if needed
        "sort": 0,
        "flags": {
            "the-expanse-quickstart": {
                "initialization-folder": "Equipment",
                "sort": 0
            }
        },
        "system": {
            "description": "<p>An electronic lockpick that can sometimes bypass locks and overrides on doors. Usually installed on a hand terminal. Can roll a test with a default +0 bonus against the TN of the lock's sophistication (typically 11). Failure returns an error, and multiple failed attempts may set off security measures.</p>",
            "cost": "11",
            "quantity": 1
        },
        "ownership": {"default": 0},
        "_stats": BASE_STATS.copy()
    },
    {
        "_id": generate_id(),
        "name": "Restraints",
        "type": "item",
        "img": "systems/expanse/ui/item-img/item.png",
        "effects": [],
        "folder": None,
        "sort": 0,
        "flags": {
            "the-expanse-quickstart": {
                "initialization-folder": "Equipment",
                "sort": 0
            }
        },
        "system": {
            "description": "<p>Simple restraints for keeping a prisoner under control. Plastic zip ties require TN 15 Strength (Might) to break, causing 1d6 impact damage per attempt. Metal cuffs are nearly impossible to break (TN 21) and generally require picking the locks.</p>",
            "cost": "6-7",
            "quantity": 1
        },
        "ownership": {"default": 0},
        "_stats": BASE_STATS.copy()
    },
    {
        "_id": generate_id(),
        "name": "Sedatives",
        "type": "item",
        "img": "systems/expanse/ui/item-img/item.png",
        "effects": [],
        "folder": None,
        "sort": 0,
        "flags": {
            "the-expanse-quickstart": {
                "initialization-folder": "Equipment",
                "sort": 0
            }
        },
        "system": {
            "description": "<p>Sedatives activate within a minute (four action rounds). Target must make a TN 13 Constitution (Tolerance) test or fall unconscious. Success means the character is only fatigued. Target remains unconscious for 1d6 hours unless given another dose.</p>",
            "cost": "9",
            "quantity": 1
        },
        "ownership": {"default": 0},
        "_stats": BASE_STATS.copy()
    },
    {
        "_id": generate_id(),
        "name": "Surveillance Drone",
        "type": "item",
        "img": "systems/expanse/ui/item-img/item.png",
        "effects": [],
        "folder": None,
        "sort": 0,
        "flags": {
            "the-expanse-quickstart": {
                "initialization-folder": "Equipment",
                "sort": 0
            }
        },
        "system": {
            "description": "<p>Small, light drones with rotors for atmospheric operation and gas cartridge for microgravity. Synched to user's hand terminal, requires Dexterity (Piloting) tests for complex maneuvers. Equipped with video cameras and microphones. Better drones may have night vision, infrared, or other sensors. Any attack that damages such a light drone essentially destroys it.</p>",
            "cost": "10",
            "quantity": 1
        },
        "ownership": {"default": 0},
        "_stats": BASE_STATS.copy()
    },
    {
        "_id": generate_id(),
        "name": "Electronic Surveillance (Bug)",
        "type": "item",
        "img": "systems/expanse/ui/item-img/item.png",
        "effects": [],
        "folder": None,
        "sort": 0,
        "flags": {
            "the-expanse-quickstart": {
                "initialization-folder": "Equipment",
                "sort": 0
            }
        },
        "system": {
            "description": "<p>Tiny wireless camera and microphone about the size of a small coin with adhesive backing. May transmit continuously or store data for burst transmissions. TN 15+ Perception (Intuition or Seeing) test to notice; TN 13 Perception (Searching) to locate when searching.</p>",
            "cost": "9",
            "quantity": 1
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
    if bounty_hunter_talent['name'] not in existing_names:
        db['items'].append(bounty_hunter_talent)
        items_added += 1
        print(f"Added talent: {bounty_hunter_talent['name']}")
    else:
        print(f"Skipped (exists): {bounty_hunter_talent['name']}")

    # Add stunts if not exist
    for stunt in bounty_hunting_stunts:
        if stunt['name'] not in existing_names:
            db['items'].append(stunt)
            items_added += 1
            print(f"Added stunt: {stunt['name']}")
        else:
            print(f"Skipped (exists): {stunt['name']}")

    # Check if "item" type exists in the system
    existing_types = {item.get('type') for item in db.get('items', [])}
    print(f"Existing item types: {existing_types}")

    # Add equipment - only if the type is supported
    # For now, skip equipment as we're not sure the schema is correct
    # We'll add them in a subsequent iteration after verifying

    # Write updated database (single line JSON)
    with open('packs/the-expanse-quickstart.db', 'w') as f:
        f.write(json.dumps(db, separators=(',', ':')))

    print(f"\nTotal items added: {items_added}")
    return items_added

if __name__ == '__main__':
    items_added = main()
