#!/usr/bin/env python3
"""Add Pirate PDF content to the Foundry VTT database."""

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

# Pirate Talent
pirate_talent = {
    "_id": generate_id(),
    "name": "Pirate",
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
        "description": "<p>For better or worse, you have thrown in your lot with pirates. Your name is known by law enforcement, and a poster with your face on it might very well hang in the local Star Helix office. Your die is cast, and you have little choice except to be the very best pirate you can be. This isn't a day job, matey. It's called \"living the life\" for a reason.</p>",
        "highest": "",
        "requirement": "Communication 2 or higher.",
        "specialization": True,
        "ranks": {
            "novice": {
                "label": "novice",
                "effect": "<p>Your past deeds have become known and your symbols, be they flags, songs, or catchphrases, herald your impending approach. You gain the Intimidation focus and can use your Communication rather than Strength Ability for tests that use it.</p>",
                "active": False
            },
            "expert": {
                "label": "expert",
                "effect": "<p>Your name is recognized in the far corners of the system and beyond the Ring gate. While people may not always fear you, they certainly respect you both as a celebrity and a known criminal. You gain +2 to all tests to identify prize ships in social situations and +2 to recruit new crew members.</p>",
                "active": False
            },
            "master": {
                "label": "master",
                "effect": "<p>Whether through economic disruption, tales of your derring-do, or by atrocities you've committed, it's hard to go anywhere you aren't known. While it's harder to keep a low profile, there are distinct financial benefits to your notoriety. You gain a +2 to all tests to sell stolen cargo.</p>",
                "active": False
            }
        }
    },
    "ownership": {"default": 0},
    "_stats": BASE_STATS.copy()
}

def main():
    with open('packs/the-expanse-quickstart.db', 'r') as f:
        db = json.loads(f.read().strip())

    existing_names = {item['name'] for item in db.get('items', [])}
    items_added = 0

    if pirate_talent['name'] not in existing_names:
        db['items'].append(pirate_talent)
        items_added += 1
        print(f"Added talent: {pirate_talent['name']}")
    else:
        print(f"Skipped (exists): {pirate_talent['name']}")

    with open('packs/the-expanse-quickstart.db', 'w') as f:
        f.write(json.dumps(db, separators=(',', ':')))

    print(f"\nTotal items added: {items_added}")
    return items_added

if __name__ == '__main__':
    main()
