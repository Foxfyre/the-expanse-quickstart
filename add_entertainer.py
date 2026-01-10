#!/usr/bin/env python3
"""Add Entertainer PDF content to the Foundry VTT database."""

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

# Entertainer Talent
entertainer_talent = {
    "_id": generate_id(),
    "name": "Entertainer",
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
        "description": "<p>Many people dream of lighting the hearts and minds of others afire with their art, but you've got the talent and training to make it happen.</p>",
        "highest": "",
        "requirement": "The type of art the character creates dictates the requirements. Writers and poets need Communication 2 or higher and Communication (Expression) focus; musicians, actors, singers, dancers, comedians, drag performers, and other live entertainers require Communication (Performance) focus; chefs, sculptors, painters, illustrators, makers, and other fabrication artists require Dexterity 2 or higher and Dexterity (Crafting) focus; a critic or reviewer might qualify with Communication (Expression) or Intelligence 2 or higher and Intelligence (Art) focus.",
        "specialization": True,
        "ranks": {
            "novice": {
                "label": "novice",
                "effect": "<p>You've got some raw potential, and you're starting to learn how to experiment with it. Sometimes that blows up in your face, but sometimes it finds brilliance in what was otherwise an average work of art. Whenever you roll a test to create or perform art, you may choose to re-roll the attempt but must keep the new roll even if it's worse. In addition, you should explain how a success transforms a performance that wasn't going well or how a failure results in a promising piece going off the rails.</p>",
                "active": False
            },
            "expert": {
                "label": "expert",
                "effect": "<p>You have developed a signature style, possibly even a signature piece such as a custom instrument or beloved persona, and it's something with which audiences strongly connect. Talk to the GM to develop a clear idea of what this entails, but it should be fairly narrow. Whenever you create using your signature, you can choose to either gain a +2 on the subsequent Income test or reduce the cost of Stunts while using it by 1 SP (minimum 1).</p>",
                "active": False
            },
            "master": {
                "label": "master",
                "effect": "<p>Your art is a part of you, and even those who aren't familiar with your medium can tell right away that you have a gift for it. You make the most challenging artistic feats look easy and attempt things other artists can't even dream of doing. Reduce the Test Difficulty by one category for all tests related to artistic creation and performance or by two categories if you can feature your signature. In addition, if the Drama Die is lower than 3 on a performance roll related to your art, treat it as though you rolled a 3 in terms of degrees of success.</p>",
                "active": False
            }
        }
    },
    "ownership": {"default": 0},
    "_stats": BASE_STATS.copy()
}

# Entertainer Stunts (Social)
entertainer_stunts = [
    {
        "_id": generate_id(),
        "name": "I'm With the Band!",
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
            "cost": "1-3",
            "repeatable": False,
            "description": "<p>By telling people you're a performer and implying—correctly or otherwise—that you are somehow part of the evening's entertainment, you can get into just about any club, bar, concert hall, theatre, or other entertainment venue immediately and at no cost, even if they're sold out. This also lets you get backstage, though it doesn't necessarily grant access to guarded celebrities or restricted areas you have no business visiting. The cost of this Stunt depends on how plausible your presence is (1 SP for very plausible, 2 SP for somewhat plausible, 3 SP for implausible).</p>"
        },
        "ownership": {"default": 0},
        "_stats": BASE_STATS.copy()
    },
    {
        "_id": generate_id(),
        "name": "Right in the Feels",
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
            "cost": "1-3",
            "repeatable": True,
            "description": "<p>You know how to read your audience and tune your performance for maximum impact. For each point spent on this Stunt, treat the number on the Drama Die as one higher for the purposes of determining the degree of success on a performance roll. Note that this does not change the actual die roll result, only the degree of success when relevant.</p>"
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

    if entertainer_talent['name'] not in existing_names:
        db['items'].append(entertainer_talent)
        items_added += 1
        print(f"Added talent: {entertainer_talent['name']}")
    else:
        print(f"Skipped (exists): {entertainer_talent['name']}")

    for stunt in entertainer_stunts:
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
