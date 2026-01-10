#!/usr/bin/env python3
"""Add Ships of The Expanse stunts to the Foundry VTT database."""

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

# Command Stunts from Ships of The Expanse p.28
COMMAND_STUNTS = [
    {
        "name": "Down With the Ship",
        "cost": "2",
        "description": "<p>In an act of heroism, the commander can expend their own Fortune to remove damage taken by other characters (as the result of a Collateral Loss) on board the ship.</p>"
    },
    {
        "name": "Calculation",
        "cost": "3+",
        "description": "<p>You can bank the SP you just spent for this stunt +1 and use them on a later stunt. You can also combine these SP with future SP earned.</p>"
    },
    {
        "name": "Rapid Reload",
        "cost": "4",
        "description": "<p>Your ship can fire one additional torpedo (in excess of its number of torpedo tubes) this round. Each additional SP spent allows you to fire one more torpedo. You can never fire more than double the number of torpedo tubes on your ship.</p>"
    },
    {
        "name": "Skimming",
        "cost": "4",
        "description": "<p>If a space battle takes place near a planet with an atmosphere, you can dive into the planet's atmosphere to avoid being targeted and perhaps even lose your pursuer completely. Your pilot must make an opposed TN 17 Dexterity (Piloting) test to succeed. If successful, the pursuing ship loses track of your ship in the atmosphere, at least temporarily. On following rounds, the pursuing ship can make opposed TN 11 Intelligence (Technology) + Sensors tests to reacquire a target on your ship.</p>"
    },
    {
        "name": "Too Close",
        "cost": "4",
        "description": "<p>To perform this stunt, you must be engaged against multiple enemy ships and at close range to one that is of at least one size class larger. A space station can also count as a larger ship. The pilot maneuvers into a position that makes it difficult for enemies to target your ship without risking damage to the other ship. During the Maneuver phase, the pilot must make a successful opposed TN 15 Dexterity (Piloting) test against the larger ship at -2. The difficulty is reduced by 1 for every additional size class greater the enemy ship is than the crew's ship. If successful, the pilot gains a +2 to their evasion test against any ships other than the ship they are using for cover. In addition, any attacks that miss the crew's ship hit the larger ship if the pilot rolls a 5 or 6 on the Drama Die. If both ships fail the piloting test, the ships collide, causing 2d6 damage to the larger ship and 4d6 damage to the smaller ship.</p>"
    },
    {
        "name": "Burn Them",
        "cost": "5",
        "description": "<p>An Epstein drive emits a powerful drive plume that can, in a pinch, be used as a weapon. To do this successfully, the ship must be at close range and perform a sudden flip and burn that points the drive plume directly at the enemy ship. The ships must be at extremely close range, so this maneuver can't be used in normal engagements - only if circumstances have dictated that the ships are very close (under 1 km). Unfortunately, this maneuver leaves the crew's ship vulnerable and open to attack. To successfully perform this maneuver, the pilot must also make a successful opposed TN 19 Dexterity (Piloting) test against the other ship at -2. If successful, the other ship is engulfed in your drive plume, causing 6d6 damage. The downside is that only rear-facing weapons can fire while the ship performs this maneuver, and enemy ships have a +2 to their evasion tests. Also, due to being in an exposed position, all evasion tests are at -2. If the pilot fails this test, they fail to engulf the enemy ship with the drive plume but still suffer all of the associated penalties.</p>"
    },
    {
        "name": "Weapon Online",
        "cost": "5",
        "description": "<p>One of the crew can temporarily bring a damaged weapon, or a weapon that has run out of ammo, (possibly the result of the GM using a Churn effect) back online. A character can attempt a TN 14 Intelligence (Engineering) or Dexterity (Gunnery) test to bring a weapon back online. The weapon can make 1d3 shots before giving up the ghost for good, requiring a proper repair. The weapon cannot be brought back online again without the ship receiving full maintenance at a spaceport.</p>"
    },
    {
        "name": "Quick Start",
        "cost": "6",
        "description": "<p>The crew can attempt to make a quick repair and restart the ship's reactor. This requires two characters to work together; one must make a TN 14 Intelligence (Technology) test and another must make a TN 14 Intelligence (Engineering) test, and they must reach a threshold of 15.</p>"
    },
    {
        "name": "Misdirect",
        "cost": "7",
        "description": "<p>When attempting to outrun a torpedo, you can fly close to another ship to try to get the torpedo to hit that ship instead of your own. You perform a flip and burn when near another ship. The pilot must make a successful opposed Dexterity (Piloting) test against the other ship and another member of the crew must make a TN 17 Technology (Intelligence) test. If both are successful, the torpedo impacts the other ship instead.</p>"
    },
]

# Fleet Command Stunts from Ships of The Expanse p.28
FLEET_STUNTS = [
    {
        "name": "Combined Fire",
        "cost": "1+",
        "description": "<p>You coordinate fire with an allied ship, increasing the likelihood that both of you hit the target. Every 1 SP you spend increases the TN of tests made to evade your ship's attack by +1. Both captains must spend this SP.</p>"
    },
    {
        "name": "Draw Fire",
        "cost": "2+",
        "description": "<p>You manage to draw fire from an enemy's intended target. For every 2 SP spent, an attacker that was going to attack an ally attacks your ship instead.</p>"
    },
    {
        "name": "Good Advice",
        "cost": "2+",
        "description": "<p>This stunt allows one commander to aid another, either by giving them a bonus to their next command test or giving them SP. Every 2 SP you spend gives an allied Commander +1 on their next test or 1 SP to spend.</p>"
    },
]

# Pilot Stunts from Ships of The Expanse p.29
PILOT_STUNTS = [
    {
        "name": "Steady as She Goes",
        "cost": "2+",
        "description": "<p>When performing high-g maneuvers the pilot can lessen the potential damage to passengers by making a smooth transition. For every 2 SP spent the TN for the Constitution (Stamina) test is reduced by 1.</p>"
    },
    {
        "name": "Blockade (Ship)",
        "cost": "4",
        "description": "<p>The pilot maneuvers the ship to make it difficult for an enemy ship to fire on or pursue its chosen target (unless that target is the pilot's ship). The enemy ship suffers a -2 penalty to any maneuver test to pursue or attack its original target. Or the targeted ship gets a +2 to its evasion test.</p>"
    },
    {
        "name": "Dauntless",
        "cost": "5",
        "description": "<p>The pilot aims their ship at an enemy ship as if to ram it, to cause it to veer off course and miss their attack opportunity. This maneuver can only be used when the ships are already at close range. The enemy ship must make a successful TN 15 Dexterity (Piloting) test or not be able to take any other action as they recover from the threat of being rammed. If the enemy ship doesn't flinch, the pilot must make a successful TN 17 Dexterity (Piloting) test to avoid hitting the ship they were aiming at although their ship still gets to take other actions.</p>"
    },
]

# Electronic Warfare Stunts from Ships of The Expanse p.29
EW_STUNTS = [
    {
        "name": "Turnabout is Fair Play",
        "cost": "2+",
        "description": "<p>Most torpedoes have their own internal guidance systems, making them impossible to hack. However, if a torpedo is being manually controlled, the sensors operator can attempt to wrest control of the torpedo from the other ship. If there is more than one torpedo, 2 SP can be spent to attempt to control each. See Electronic Warfare under Ship Maneuvers for details.</p>"
    },
    {
        "name": "Hack the System",
        "cost": "4",
        "description": "<p>While scanning the enemy ship for weaknesses, the sensors operator detects an opening in the enemy ship's computer system. They can attempt to hack the enemy's ship to temporarily disable one or more systems. See Electronic Warfare under Ship Maneuvers for details.</p>"
    },
]

# Engineer Stunts from Ships of The Expanse p.29
ENGINEER_STUNTS = [
    {
        "name": "Not My Ship!",
        "cost": "1+",
        "description": "<p>The Engineer can spend Fortune to reduce damage taken by the ship just as if it were part of the hull. The engineer can spend 1d6 Fortune to reduce damage to the ship for every SP spent.</p>"
    },
    {
        "name": "Quick Fix",
        "cost": "3+",
        "description": "<p>Every 3 SP spent allows the engineer to instantly repair a single loss to Maneuverability, Sensors, or Weapons.</p>"
    },
    {
        "name": "Patch",
        "cost": "4",
        "description": "<p>The ship's engineer can apply a quick weld job to temporarily reinforce hull damage. Attempt a TN 17 Intelligence (Engineering) test to make the patch. If successful, temporarily remove hull losses up to the number rolled on the Drama Die by the engineer. This patch only lasts until the end of the combat, and the ship must then receive proper maintenance at a spaceport.</p>"
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


def create_stunt(stunt_data, stunt_type, folder_id, folder_name):
    """Create a stunt item entry."""
    return {
        "_id": generate_id(),
        "name": stunt_data["name"],
        "type": "stunt",
        "img": "systems/expanse/ui/item-img/stunt.png",
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
            "type": stunt_type,
            "name": "",
            "cost": stunt_data["cost"],
            "repeatable": False,
            "description": stunt_data["description"]
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
    folders_added = 0

    # Find the parent "Stunts" folder
    stunts_parent_id = None
    for folder in db.get('folders', []):
        if folder['name'] == 'Stunts':
            stunts_parent_id = folder['_id']
            break

    # Define stunt categories
    stunt_categories = [
        ("Ship Command Stunts", "Ship Command", COMMAND_STUNTS),
        ("Fleet Command Stunts", "Fleet Command", FLEET_STUNTS),
        ("Pilot Stunts", "Pilot", PILOT_STUNTS),
        ("Electronic Warfare Stunts", "Electronic Warfare", EW_STUNTS),
        ("Engineer Stunts", "Engineer", ENGINEER_STUNTS),
    ]

    for folder_name, stunt_type, stunts in stunt_categories:
        # Create folder if it doesn't exist
        folder_id = None
        if folder_name not in existing_folder_names:
            folder = create_folder(folder_name, parent=stunts_parent_id)
            folder_id = folder['_id']
            db['folders'].append(folder)
            folders_added += 1
            print(f"Created folder: {folder_name}")
        else:
            for folder in db.get('folders', []):
                if folder['name'] == folder_name:
                    folder_id = folder['_id']
                    break

        # Add stunts
        for stunt_data in stunts:
            if stunt_data['name'] not in existing_names:
                stunt = create_stunt(stunt_data, stunt_type, folder_id, folder_name)
                db['items'].append(stunt)
                items_added += 1
                existing_names.add(stunt_data['name'])  # Track newly added names
                print(f"Added {stunt_type} stunt: {stunt_data['name']}")
            else:
                print(f"Skipped (exists): {stunt_data['name']}")

    # Write updated database
    with open('packs/the-expanse-quickstart.db', 'w') as f:
        json.dump(db, f, separators=(',', ':'))

    print(f"\nTotal folders added: {folders_added}")
    print(f"Total stunts added: {items_added}")
    return items_added


if __name__ == '__main__':
    main()
