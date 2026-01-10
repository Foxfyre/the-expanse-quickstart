#!/usr/bin/env python3
"""Add Journalist PDF content to the Foundry VTT database."""

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

# Journalist Talent
journalist_talent = {
    "_id": generate_id(),
    "name": "Journalist",
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
        "description": "<p>You have a knack for getting the story, whatever it takes.</p>",
        "highest": "",
        "requirement": "Based on the type of journalism the character practices, they need either Communication 2 or higher and the Communication (Research) or Communication (Expression) focus, or Intelligence 2 or higher and the Intelligence (Research) or Intelligence (Current Affairs) focus.",
        "specialization": True,
        "ranks": {
            "novice": {
                "label": "novice",
                "effect": "<p>You've learned to use your status as a journalist to get your foot in the door both literally and figuratively. Whenever you use the Press Pass stunt successfully to gain access to a situation, gain +2 to your next social test directly related to conducting journalistic activity.</p>",
                "active": False
            },
            "expert": {
                "label": "expert",
                "effect": "<p>You've developed a few specific techniques as part of your journalistic arsenal. Select three stunts from the General Social Stunts list in The Expanse RPG—halve the SP cost of these stunts, rounded up (minimum 1). This reduction only applies when you're using a stunt as part of your journalistic work; while they're encouraged to give it a fair amount of latitude, the GM has the final say on whether it applies to a particular situation.</p>",
                "active": False
            },
            "master": {
                "label": "master",
                "effect": "<p>You've got a knack for finding the right angle to make a story catch on and have developed enough of an audience following to get it started. Once per session, you may use the Go Viral stunt for free, provided you have some way of broadcasting the relevant events.</p>",
                "active": False
            }
        }
    },
    "ownership": {"default": 0},
    "_stats": BASE_STATS.copy()
}

# Journalist Stunts (Social)
journalist_stunts = [
    {
        "_id": generate_id(),
        "name": "Hardball",
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
            "cost": "1+",
            "repeatable": True,
            "description": "<p>You are adept at asking tough questions and getting honest answers, even if it ruffles some feathers. You may spend SP to impose a -1 penalty on Deception tests for anyone who tries to lie to you during questioning. You may also force an opponent to re-roll a Deception test, but you must abide by this new result, and their Attitude shifts a degree less favorable toward you afterward.</p>"
        },
        "ownership": {"default": 0},
        "_stats": BASE_STATS.copy()
    },
    {
        "_id": generate_id(),
        "name": "Fourth Estate",
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
            "cost": "2+",
            "repeatable": False,
            "description": "<p>You temporarily gain a rank of Membership in an organization you've been covering or researching, with the rank equal to the SP spent -1. This lasts for the rest of the session. You are not actually a member, but you've gained enough trust of those in the organization that as long as you don't violate their rules, they will take you under their wing for a time.</p>"
        },
        "ownership": {"default": 0},
        "_stats": BASE_STATS.copy()
    },
    {
        "_id": generate_id(),
        "name": "Press Pass",
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
            "cost": "3",
            "repeatable": False,
            "description": "<p>By announcing yourself as a member of the press and presenting appropriate credentials, you can gain access to a restricted area or situation where a member of the press might plausibly be admitted (even if it's unlikely). You probably can't convince the MCRN to let you waltz onto a battleship currently preparing for battle, for example, but you might be able to get on base to speak to a commander during an alert.</p>"
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

    if journalist_talent['name'] not in existing_names:
        db['items'].append(journalist_talent)
        items_added += 1
        print(f"Added talent: {journalist_talent['name']}")
    else:
        print(f"Skipped (exists): {journalist_talent['name']}")

    for stunt in journalist_stunts:
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
