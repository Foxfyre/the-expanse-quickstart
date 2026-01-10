#!/usr/bin/env python3
"""Add Sol System Organization Stunts to the Foundry VTT database."""

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

# Organization Growth Stunts from Sol System p.105
GROWTH_STUNTS = [
    {
        "name": "Rebuild/Expand",
        "cost": "1+",
        "description": "<p>Add Stability at the cost of 1 per SP spent.</p>"
    },
    {
        "name": "Kit",
        "cost": "1",
        "description": "<p>Supply one character with an important or significant piece of equipment or 1d3 minor items.</p>"
    },
    {
        "name": "Discovery",
        "cost": "2",
        "description": "<p>The organization learns something scientific or about rival groups. Learn 2 exact ability scores or focuses of any threat or project.</p>"
    },
    {
        "name": "High Morale",
        "cost": "2",
        "description": "<p>Gain a +2 bonus on the next plot action the organization undertakes.</p>"
    },
    {
        "name": "Repairs",
        "cost": "2",
        "description": "<p>Remove a single organization condition.</p>"
    },
    {
        "name": "Contacts",
        "cost": "3",
        "description": "<p>The organization forms a connection that will provide useful information from time to time.</p>"
    },
    {
        "name": "New Hire",
        "cost": "3",
        "description": "<p>A skilled or influential NPC joins the organization. Select one Growth or Plot Stunt and reduce its cost by 1 SP. If this character dies or leaves, the organization loses this benefit.</p>"
    },
    {
        "name": "Redundancies",
        "cost": "3",
        "description": "<p>Increase Resolve by 1.</p>"
    },
    {
        "name": "Trade Network",
        "cost": "3",
        "description": "<p>The organization attracts the attention of a trading ship or group, which makes new or better equipment available from time to time.</p>"
    },
    {
        "name": "New Assets",
        "cost": "4",
        "description": "<p>Increase an ability rated 5 or less by 1.</p>"
    },
    {
        "name": "Significant Growth",
        "cost": "4",
        "description": "<p>Increase the Size of the organization from local to regional.</p>"
    },
    {
        "name": "New Focus (Organization)",
        "cost": "4",
        "description": "<p>Add a Focus to the organization.</p>"
    },
    {
        "name": "New Talent (Organization)",
        "cost": "5",
        "description": "<p>A skilled and influential NPC joins the organization. Select two Growth or Plot Stunts and reduce their cost by 1 SP. If this character dies or leaves, the organization loses this benefit.</p>"
    },
    {
        "name": "Organization Effort",
        "cost": "5",
        "description": "<p>Increase the organization's size from regional to system wide.</p>"
    },
    {
        "name": "Major Industry",
        "cost": "6",
        "description": "<p>Increase an ability rated 6 or more by 1.</p>"
    },
    {
        "name": "Rampant Growth",
        "cost": "6",
        "description": "<p>Increase the organization's size from system wide to interstellar.</p>"
    },
]

# Plot Stunts from Sol System p.106
PLOT_STUNTS = [
    {
        "name": "Reinforce",
        "cost": "1+",
        "description": "<p>Add extra Stability equal to the number of SP spent.</p>"
    },
    {
        "name": "Create an Opening",
        "cost": "1",
        "description": "<p>Gain a +2 bonus on your next plot action against this same operation.</p>"
    },
    {
        "name": "Analysts",
        "cost": "2",
        "description": "<p>You uncover valuable insight or intelligence about the target operation. Select one ability. The target suffers a -1 penalty to tests with that ability until they roll doubles on a growth check.</p>"
    },
    {
        "name": "Countermeasures",
        "cost": "2",
        "description": "<p>Pick a focus. The operation cannot use that Focus in their next plot action.</p>"
    },
    {
        "name": "Preparations",
        "cost": "2",
        "description": "<p>You reinforce against this danger's usual avenues of attack. This threat or rival receives a -2 penalty to their next plot action against your organization.</p>"
    },
    {
        "name": "Exploit an Opportunity",
        "cost": "3",
        "description": "<p>Add +1d6 Stability loss to an operation.</p>"
    },
    {
        "name": "Precise Efforts",
        "cost": "3",
        "description": "<p>Ignore the operation's Resolve when determining their Stability loss.</p>"
    },
    {
        "name": "Uncover Assets",
        "cost": "3",
        "description": "<p>You gain some valuables as part of your plot action, stealing supplies from another organization or returning from the mines with a strange artifact.</p>"
    },
    {
        "name": "Domino Effect",
        "cost": "4",
        "description": "<p>Use the results from your plot action to immediately target a second operation. The two operations affected should be linked in some way. Each operation rolls and resists separately.</p>"
    },
    {
        "name": "Policy Shift",
        "cost": "4",
        "description": "<p>Pick a focus. Your target operation permanently loses that Focus.</p>"
    },
    {
        "name": "Second Team",
        "cost": "4",
        "description": "<p>Immediately roll a second plot action against the same operation. This must use a different ability than the current plot action.</p>"
    },
    {
        "name": "Double Shifts",
        "cost": "5",
        "description": "<p>Immediately roll a second plot action against the same operation. This test uses the same ability as the current plot action.</p>"
    },
    {
        "name": "Make the Most",
        "cost": "5",
        "description": "<p>Add +2d6 Stability loss to an operation.</p>"
    },
    {
        "name": "Unexpected Insights",
        "cost": "5",
        "description": "<p>You learn from your struggles. Your organization gains a new Focus, determined by the GM. This Focus must be for the same ability the target operation used to roll its plot check.</p>"
    },
    {
        "name": "Power Shift",
        "cost": "6",
        "description": "<p>Reduce one of the target operation's abilities by 1, and raise the same ability for your organization by 1.</p>"
    },
    {
        "name": "Turn the Tables",
        "cost": "6",
        "description": "<p>The target operation loses one focus, while your organization gains a new Focus determined by the GM (the same, if possible). This may be an important NPC defecting from a rival organization or learning to harness the deadly lightning strikes from seasonal storms.</p>"
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

    # Create Organization Growth Stunts folder if it doesn't exist
    growth_folder_name = "Organization Growth Stunts"
    growth_folder_id = None
    if growth_folder_name not in existing_folder_names:
        growth_folder = create_folder(growth_folder_name, parent=stunts_parent_id)
        growth_folder_id = growth_folder['_id']
        db['folders'].append(growth_folder)
        folders_added += 1
        print(f"Created folder: {growth_folder_name}")
    else:
        for folder in db.get('folders', []):
            if folder['name'] == growth_folder_name:
                growth_folder_id = folder['_id']
                break

    # Create Plot Stunts folder if it doesn't exist
    plot_folder_name = "Plot Stunts"
    plot_folder_id = None
    if plot_folder_name not in existing_folder_names:
        plot_folder = create_folder(plot_folder_name, parent=stunts_parent_id)
        plot_folder_id = plot_folder['_id']
        db['folders'].append(plot_folder)
        folders_added += 1
        print(f"Created folder: {plot_folder_name}")
    else:
        for folder in db.get('folders', []):
            if folder['name'] == plot_folder_name:
                plot_folder_id = folder['_id']
                break

    # Add Organization Growth Stunts
    for stunt_data in GROWTH_STUNTS:
        if stunt_data['name'] not in existing_names:
            stunt = create_stunt(stunt_data, "Organization Growth", growth_folder_id, growth_folder_name)
            db['items'].append(stunt)
            items_added += 1
            print(f"Added growth stunt: {stunt_data['name']}")
        else:
            print(f"Skipped (exists): {stunt_data['name']}")

    # Add Plot Stunts
    for stunt_data in PLOT_STUNTS:
        if stunt_data['name'] not in existing_names:
            stunt = create_stunt(stunt_data, "Plot", plot_folder_id, plot_folder_name)
            db['items'].append(stunt)
            items_added += 1
            print(f"Added plot stunt: {stunt_data['name']}")
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
