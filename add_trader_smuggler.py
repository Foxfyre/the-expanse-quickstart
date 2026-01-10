#!/usr/bin/env python3
"""Add Trader/Smuggler PDF content to the Foundry VTT database."""

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

# Trader Talent
trader_talent = {
    "_id": generate_id(),
    "name": "Trader",
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
        "description": "<p>Good merchants know how to identify a need and then profit from it, but if you aim to be a true master trader, you value finding a profit or benefit for all parties involved.</p>",
        "highest": "",
        "requirement": "Intelligence 2 or higher and the Intelligence (Business) focus.",
        "specialization": True,
        "ranks": {
            "novice": {
                "label": "novice",
                "effect": "<p>You're good at reading people, and you're excellent at understanding trends. Add +1 to Perception (Intuition) tests.</p>",
                "active": False
            },
            "expert": {
                "label": "expert",
                "effect": "<p>You're savvy when it comes to finances, loopholes, and opportunities. If you fail an Intelligence (Business) test, you can re-roll it, but must keep the result of the second roll.</p>",
                "active": False
            },
            "master": {
                "label": "master",
                "effect": "<p>Once per session when you succeed on an Intelligence (Business) test to buy or sell goods or bid for available jobs with a client, you may increase or decrease your Drama Die by 1 without spending Fortune (or increasing the Churn for altering the dice).</p>",
                "active": False
            }
        }
    },
    "ownership": {"default": 0},
    "_stats": BASE_STATS.copy()
}

# Smuggler Talent
smuggler_talent = {
    "_id": generate_id(),
    "name": "Smuggler",
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
        "description": "<p>You understand the calculus of risk. Understanding the opportunities and dangers in any transaction, you know how to prop up a mediocre payout with something a little extra.</p>",
        "highest": "",
        "requirement": "Communication 2 or higher and the Communication (Bargaining) focus.",
        "specialization": True,
        "ranks": {
            "novice": {
                "label": "novice",
                "effect": "<p>You know how to mitigate risks and maximize profits. Add +1 to all tests where the TN was increased by Risk.</p>",
                "active": False
            },
            "expert": {
                "label": "expert",
                "effect": "<p>Whenever you acquire cargo, whether by using the Merchants Buying rules in Sol System or by using the clients in Trades of the Expanse: Trader/Smuggler, you may choose to also take on a small amount of illicit cargo. Your overall flight gains +1 Risk, but if you complete the trade successfully you gain an additional +2 Temporary Income bonus.</p>",
                "active": False
            },
            "master": {
                "label": "master",
                "effect": "<p>When you attempt to bribe somebody with an Income test or a Communication (Bargaining) test, you may spend one Temporary Income to re-roll it, but must keep the result of the second roll.</p>",
                "active": False
            }
        }
    },
    "ownership": {"default": 0},
    "_stats": BASE_STATS.copy()
}

# Trader/Smuggler Stunts (Exploration - for trading activities)
trader_smuggler_stunts = [
    {
        "_id": generate_id(),
        "name": "Hot Market",
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
            "cost": "2",
            "repeatable": False,
            "description": "<p>Additional buyers are interested in your cargo. You break off your existing deal—possibly gaining a reputation or negatively impacting your previous contact's attitude toward you—to gain an additional +1 Temporary Income when the deal is complete with your new buyer.</p>"
        },
        "ownership": {"default": 0},
        "_stats": BASE_STATS.copy()
    },
    {
        "_id": generate_id(),
        "name": "Smooth Sailing",
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
            "cost": "2-4",
            "repeatable": True,
            "description": "<p>You've covered your tracks and chosen the safest routes. Reduce this mission's Risk by 1 for each two SP spent.</p>"
        },
        "ownership": {"default": 0},
        "_stats": BASE_STATS.copy()
    },
    {
        "_id": generate_id(),
        "name": "Primera Pinche Heroes",
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
            "description": "<p>When you're looking for a market to sell your goods, you identify a port or location that is in desperate need of what you have. Add +1 to the goods' Income Modifier, and the maximum sale value of the goods at that location is +4 (see Selling Goods in Sol System), but the Risk for taking the cargo there is increased by +2.</p>"
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

    # Add Trader talent
    if trader_talent['name'] not in existing_names:
        db['items'].append(trader_talent)
        items_added += 1
        print(f"Added talent: {trader_talent['name']}")
    else:
        print(f"Skipped (exists): {trader_talent['name']}")

    # Add Smuggler talent
    if smuggler_talent['name'] not in existing_names:
        db['items'].append(smuggler_talent)
        items_added += 1
        print(f"Added talent: {smuggler_talent['name']}")
    else:
        print(f"Skipped (exists): {smuggler_talent['name']}")

    # Add stunts
    for stunt in trader_smuggler_stunts:
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
