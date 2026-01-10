#!/usr/bin/env python3
"""Add TUE Core stunts to the Foundry VTT database."""

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

# Chase Stunts (page 114)
CHASE_STUNTS = [
    {"name": "Punch It", "cost": "1+", "description": "<p>You gain a +1 bonus on your next chase test for each 1 SP you spend.</p>"},
    {"name": "Evasive Maneuver", "cost": "2", "description": "<p>Until your next turn, attacks against you and your vehicle (if any) suffer a −2 penalty.</p>"},
    {"name": "Follow the Leader", "cost": "2", "description": "<p>Make a test with a TN you choose and an ability focus you work out with the GM for pulling off a tricky maneuver. If you fail, you crash. Anyone following you using the same method of transport must make the same test or crash.</p>"},
    {"name": "Attack on the Move", "cost": "3", "description": "<p>You can make a bonus melee or ranged attack, use the bonus Activate action to use an in-built weapon system, or make a bonus Ram attack against an enemy within range and line of sight, at a −2 penalty to the roll.</p>"},
    {"name": "Keep It Steady", "cost": "3", "description": "<p>Until the beginning of your next turn, passengers gain a +1 bonus when making attacks or making other ability tests that would benefit from stable platform.</p>"},
    {"name": "Interference", "cost": "4", "description": "<p>A character of your choice suffers a −2 penalty on their next chase test.</p>"},
    {"name": "Short Cut", "cost": "5", "description": "<p>Add an additional +2 to your chase total.</p>"},
]

# General Combat Stunts (page 114)
COMBAT_STUNTS = [
    {"name": "Adrenaline Rush", "cost": "1-3", "description": "<p>Regain lost Fortune equal to the SP spent. You cannot exceed your character's max Fortune.</p>"},
    {"name": "Momentum", "cost": "1-3", "description": "<p>Gain +3 to initiative per SP spent, changing your place in the initiative order.</p>"},
    {"name": "Take Cover", "cost": "1-3", "description": "<p>If there is cover in your immediate vicinity, gain a cover rating equal to SP spent, up to the maximum rating available.</p>"},
    {"name": "Guardian Angel", "cost": "1+", "description": "<p>Choose an ally within 5 meters of you. If they would take damage before your next turn, 1 damage point per SP spent transfers to you instead as you interpose yourself in front of the attack.</p>"},
    {"name": "Whatever's Handy", "cost": "1", "description": "<p>Immediately arm yourself with anything in your environment you can reasonably wield as a makeshift weapon.</p>"},
    {"name": "Group Tactics", "cost": "2+", "description": "<p>Choose one ally to move 2 meters in a direction of their choosing for each 2 SP spent.</p>"},
    {"name": "Injure", "cost": "2", "description": "<p>If your target has lost half or more of their Fortune, your attack imposes an injured condition so long as its damage exceeds the target's Toughness.</p>"},
    {"name": "Overcome Toughness", "cost": "2", "description": "<p>Against this attack's damage, the target's Toughness is considered to be half its normal value, rounded down.</p>"},
    {"name": "Bodyguard", "cost": "3", "description": "<p>Move up to 3 meters, positioning yourself between a foe and a target. Until the start of your next turn, the foe must succeed on a minor action Dexterity (Acrobatics) or Strength (Might) test vs. your Defense to reach the target you're protecting.</p>"},
    {"name": "Expose", "cost": "3", "description": "<p>Destroy or move any one object in weapon range, such as a door or crate, that could provide cover. This can take out small sections of larger objects like pillars or walls.</p>"},
    {"name": "Knock Out", "cost": "4", "description": "<p>If your target has lost half or more of their Fortune, your attack imposes an unconscious condition so long as its damage exceeds the target's Toughness.</p>"},
    {"name": "Lethal Blow", "cost": "5", "description": "<p>Inflict an extra 2d6 damage on this attack.</p>"},
    {"name": "Wound", "cost": "5", "description": "<p>If your target has lost half or more of their Fortune, your attack imposes a wounded condition so long as its damage exceeds the target's Toughness.</p>"},
]

# Gun Stunts (page 115)
GUN_STUNTS = [
    {"name": "Overwatch (Gun)", "cost": "1-3", "description": "<p>Your opponent suffers −1 to attack rolls per SP spent until the start of your next turn.</p>"},
    {"name": "Precision Marksmanship", "cost": "1-4", "description": "<p>If you make an attack with a firearm that benefits from an Aim bonus before the end of your next turn, increase the aim bonus by +1 per SP spent.</p>"},
    {"name": "Ricochet", "cost": "1-3", "description": "<p>Make a trick shot that ignores (SP spent) of the armor rating of a target behind cover.</p>"},
    {"name": "Short Burst", "cost": "1-3", "description": "<p>Automatic weapons only. Ignore one point of your opponent's Toughness per SP spent.</p>"},
    {"name": "Strafe", "cost": "1-3", "description": "<p>Automatic weapons only. Immediately move up to (SP spent) meters in any direction, and apply this attack to anyone within (SP spent) meters of your original target. Halve the damage dealt to the additional targets.</p>"},
    {"name": "Suppressive Fire", "cost": "1-5", "description": "<p>Automatic weapons only. At the end of each character's turn until the start of your next turn, make a new attack against that character if they're within (SP) meters of the spot where your target stands.</p>"},
    {"name": "Rapid Reload", "cost": "1", "description": "<p>Next time you miss with a firearm, immediately reload without checking against Capacity.</p>"},
    {"name": "Efficient Gunner", "cost": "2+", "description": "<p>Next time you miss with a firearm, subtract 1 from the Drama Die's result for each 2 SP spent, for purposes of checking against Capacity.</p>"},
    {"name": "Long Burst", "cost": "2", "description": "<p>Automatic weapons only. Make a second attack against the same target or a different one within 5 meters of the first; take a −2 to this attack roll, but gain a +2 to the damage roll if you hit.</p>"},
    {"name": "Pistol Whip", "cost": "3", "description": "<p>Pistols only. If the attack hits an opponent adjacent to you, make a second attack to club them with the gun, inflicting 1d6 + Strength damage.</p>"},
    {"name": "Called Shot", "cost": "4", "description": "<p>You target an exposed part of your opponent's body. The attack's damage becomes penetrating.</p>"},
    {"name": "Sniper's Perch", "cost": "4", "description": "<p>You find high ground or another advantageous shooting position. If you attack with a firearm on your next turn, double your weapon's short and long ranges for that turn.</p>"},
    {"name": "Spray and Pray", "cost": "5", "description": "<p>Automatic weapons only. Apply this attack to every target within a 5-meter radius of your original target, including allies. All additional targets gain +1 to Defense against this attack.</p>"},
]

# Grappling Stunts (page 115)
GRAPPLING_STUNTS = [
    {"name": "Hinder", "cost": "1-3", "description": "<p>Melee attacks your opponent makes before the start of your next turn reduce their damage by 2 per SP spent.</p>"},
    {"name": "Grapple", "cost": "1", "description": "<p>You and your target make opposed Fighting (Grappling) rolls; if you win, they can't move from where they are on their next turn. You and the target both take a −2 Defense penalty until the beginning of your next turn.</p>"},
    {"name": "Takedown", "cost": "2", "description": "<p>You and your target make opposed Fighting (Grappling) rolls; if you win, you and your target fall prone; your target takes an additional 1d6 damage and can't stand up until you do.</p>"},
    {"name": "Human Shield", "cost": "3", "description": "<p>You and your target make opposed Fighting (Grappling) rolls; if you win, any failed ranged attack against you hits your target instead, and ranged attacks against you take a −2 penalty until the beginning of your next turn.</p>"},
    {"name": "Strangle", "cost": "3", "description": "<p>Roll Fighting (Grappling) vs. your target's Constitution (Stamina); if you win, the target loses their minor action catching their breath on their next turn.</p>"},
    {"name": "Hostage", "cost": "4", "description": "<p>You and your target make opposed Fighting (Grappling) rolls; if you win, you maneuver them into a vulnerable position. If they do anything other than a free action on their next turn, you may make an immediate attack against your target with a +2 bonus to the Drama Die.</p>"},
    {"name": "Pin", "cost": "4", "description": "<p>You and your target make opposed Fighting (Grappling) rolls; if you win, they can't do anything other than a free action on their next turn. You and the target both take a −4 Defense penalty until the beginning of your next turn.</p>"},
    {"name": "Restrain", "cost": "5", "description": "<p>If you have appropriate equipment in hand, like handcuffs or rope, you and your target make opposed Fighting (Grappling) rolls; if you win, they become restrained and can't do anything other than try to escape.</p>"},
]

# Melee Stunts (page 116)
MELEE_STUNTS = [
    {"name": "Parry", "cost": "1-3", "description": "<p>Your opponent suffers −1 to Defense per SP spent until your next turn, as you guide their limb or weapon off-center, throwing off their balance.</p>"},
    {"name": "Footwork", "cost": "1+", "description": "<p>You maneuver effortlessly. Gain +1 per SP spent to one combat-related test of your choice before the end of your next turn.</p>"},
    {"name": "Feint", "cost": "1", "description": "<p>Reduce your target's initiative by 1 (to a minimum of 1) for the rest of the encounter.</p>"},
    {"name": "Disarm", "cost": "2", "description": "<p>You and your target make opposed melee attack rolls; if you win, knock your enemy's weapon 1d6 + Strength meters away in a direction of your choice.</p>"},
    {"name": "Hamstring", "cost": "3", "description": "<p>Cumulatively reduce your target's Speed by 3 for the rest of the encounter. If it's reduced to 0, they become restrained for the rest of the encounter and cannot move.</p>"},
    {"name": "Bind Weapon", "cost": "3", "description": "<p>You and your opponent make opposed melee attack rolls; if you win, your opponent's next melee attack against you automatically misses.</p>"},
    {"name": "Armor Crush", "cost": "4", "description": "<p>Convert up to 3 points of damage you would inflict on your foe with this attack into a penalty to their worn armor instead. This penalty lasts for 1d6 rounds or until they take a major action to readjust their armor.</p>"},
    {"name": "Break Weapon", "cost": "5", "description": "<p>You and your opponent make opposed melee attack rolls; if you win, you destroy your opponent's weapon, rendering it unusable.</p>"},
]

# Vehicle Combat Stunts (page 116)
VEHICLE_STUNTS = [
    {"name": "System Damage", "cost": "1-3", "description": "<p>Your attack damages the vehicle's Handling, Sensors, or Weapons. Impose a −1 penalty per SP spent to the damaged ability. This penalty remains until the vehicle is repaired.</p>"},
    {"name": "Penetrate Hull", "cost": "1+", "description": "<p>Your attack overcomes the vehicle's resistance to damage. If a vehicle has a Hull rating, you must spend SP equal to it on this stunt before spending SP on other stunts.</p>"},
    {"name": "Off-Course", "cost": "2", "description": "<p>The vehicle is thrown off-course and the operator must make a TN 15 test to maintain control. A new test can be made each round to regain control if it is lost.</p>"},
    {"name": "Scuttle", "cost": "2", "description": "<p>Your attack destroys the target vehicle. This stunt is only available against a helpless vehicle.</p>"},
    {"name": "Shrapnel", "cost": "2+", "description": "<p>The attack causes a damaging explosion in the vehicle's interior. The operator and all passengers in the same compartment suffer 1d6 damage for 2 SP or 2d6 damage for 4 SP.</p>"},
    {"name": "Hull Breach", "cost": "3+", "description": "<p>You inflict significant damage to the vehicle, reducing its Hull rating by 1 per 3 SP spent. The loss of Hull rating lasts until repaired.</p>"},
    {"name": "Slowdown", "cost": "3", "description": "<p>You damage the vehicle's propulsion, dropping its Speed class by one category. If it drops to Slow or less, the operator must make a TN 15 test to maintain control.</p>"},
    {"name": "Disable Drive", "cost": "4", "description": "<p>Your attack disables the vehicle's propulsion. The operator must make a TN 15 test to maintain control and the vehicle can no longer move or maneuver under its own power. The vehicle is helpless.</p>"},
    {"name": "Skewer", "cost": "4+", "description": "<p>Your attack is in just the right place to do serious damage inside the vehicle: One character suffers 4d6 damage for 4 SP, or 6d6 damage for 6 SP, or the full damage of your weapon +2d6, whichever is less.</p>"},
    {"name": "Rupture", "cost": "5", "description": "<p>Your attack ruptures a fuel line or power conduit, causing an internal explosion. This deals 3d6 penetrating damage to everyone in a particular compartment of the vehicle.</p>"},
    {"name": "Disable Engine", "cost": "6", "description": "<p>Your attack disables the vehicle's engine or main power, such as a ship's reactor, leaving the vehicle completely without power other than emergency back-ups and essentially helpless.</p>"},
]

# Exploration Stunts (page 118)
EXPLORATION_STUNTS = [
    {"name": "A Stitch in Time", "cost": "1+", "description": "<p>You put in the effort to do it right the first time. Gain +1 per SP spent on your next test related to this one during this encounter so long as this roll was part of an advanced test.</p>"},
    {"name": "Pay Dirt", "cost": "1+", "description": "<p>In the course of your endeavor, you discover something valuable. Temporarily gain +1 Income per SP spent; this increase lasts until you next fail an Income test.</p>"},
    {"name": "Jury Rig", "cost": "2", "description": "<p>You find or improvise a piece of equipment you need to be more effective. For the rest of the encounter, negate any situational penalties you would suffer for lacking proper equipment.</p>"},
    {"name": "Frugal", "cost": "5", "description": "<p>You use only what you must to get the job done, saving resources for a rainy day. This Income test doesn't deplete your Income even if it normally would.</p>"},
]

# Infiltration Stunts (page 118)
INFILTRATION_STUNTS = [
    {"name": "Just a Shadow", "cost": "1+", "description": "<p>Gain +1 per SP spent to your next test during this encounter as long as you remain unnoticed.</p>"},
    {"name": "Good Instincts", "cost": "1", "description": "<p>Make a Perception test using an appropriate focus (GM's choice) with the same TN as the test you just made to learn the most likely immediate consequence of the action you just performed.</p>"},
    {"name": "Calming the Waters", "cost": "1+", "description": "<p>Reduce the current Churn Pool by the SP spent.</p>"},
    {"name": "Bravery", "cost": "1", "description": "<p>Your success bolsters your courage, granting you 1d6 extra Toughness against the next damaging hazard you face in this encounter.</p>"},
    {"name": "Over Here!", "cost": "2", "description": "<p>Your flashy action makes you the center of attention. Each of your allies gains +1 to their next test to hide or pass scrutiny in this encounter. Any action an opponent takes until then automatically targets you.</p>"},
    {"name": "Take One for the Team", "cost": "2", "description": "<p>When you successfully avoid damage from a hazard but an ally doesn't, you may take the damage for that ally instead.</p>"},
    {"name": "Cover Your Tracks", "cost": "3", "description": "<p>Whether you're hacking into a network, evading the cops, or infiltrating a military base, you impose a −2 on all future rolls to follow your trail related to this test.</p>"},
    {"name": "High Tech Hustle", "cost": "3", "description": "<p>With an injection of technobabble or a quick mod to a device, you sidestep one minor complication impeding your current goal.</p>"},
    {"name": "It Wasn't Me", "cost": "4", "description": "<p>You leave evidence another character is responsible for the results of your test. All failed tests to investigate the truth reveal that person as the culprit, and such tests suffer a −2 penalty.</p>"},
    {"name": "Fancy Meeting You Here", "cost": "5", "description": "<p>Choose a focus or talent your character doesn't possess. An NPC of the GM's choice with that focus or talent appears in the scene within a few minutes.</p>"},
]

# Social Stunts (pages 124-125)
SOCIAL_STUNTS = [
    {"name": "Cards on the Table", "cost": "1", "description": "<p>If you were completely honest when making this test, your target must be completely honest in the next social test they make against you during this encounter.</p>"},
    {"name": "Making an Entrance", "cost": "1", "description": "<p>If this is your first action of the encounter, gain +1 to your next opposed roll against one character who witnessed it. You can choose this stunt multiple times per roll.</p>"},
    {"name": "Sway the Crowd", "cost": "2", "description": "<p>Your words affect one additional person of your choice. You may choose this stunt multiple times per roll.</p>"},
    {"name": "Good Cop/Bad Cop", "cost": "3", "description": "<p>Choose an ally to immediately make a test in seeming opposition to the one you just made, with the same target. If they succeed, they prompt the target to give up a secret you didn't already know.</p>"},
    {"name": "Let's Make a Deal", "cost": "3", "description": "<p>Your action turns out to benefit a character you didn't target, who now owes you a favor—no matter how much they protest.</p>"},
    {"name": "Flirt", "cost": "4", "description": "<p>Roll Communication (Seduction) vs. your target's Willpower (Self-Discipline) against a character whose Attitude toward you is Open or better; if you win, they become enamored with your character.</p>"},
    {"name": "From the Heart", "cost": "4", "description": "<p>You believe wholeheartedly in what you say. Choose one Willpower focus. If you don't have it already, gain it for the rest of the encounter. If you do, it adds +3 instead of +2 to rolls you make with it.</p>"},
    {"name": "Sleep With One Eye Open", "cost": "4", "description": "<p>Applies to a test targeting someone you have a negative Relationship with. The next attack you make against that target in this session is automatically a surprise attack so long as they weren't already in combat.</p>"},
    {"name": "Enrage", "cost": "5", "description": "<p>Choose one character present whose Attitude toward you is Neutral or worse. They must immediately either attack you or storm out of the scene.</p>"},
    {"name": "Patter", "cost": "5", "description": "<p>Your rapid-fire words confuse your target, who must succeed at a Perception (Empathy) roll vs. your Communication (Deception), or automatically fail their next non-attack test against you.</p>"},
    {"name": "My Word Is My Bond", "cost": "7", "description": "<p>Applies to a test relevant to completing a task you've promised someone you have a Relationship with. Gain +2 to tests directly related to completing this task until the end of the session.</p>"},
]

# Attitude Stunts (page 125)
ATTITUDE_STUNTS = [
    {"name": "Making an Offer", "cost": "1-3", "description": "<p>Your test implies a promise or olive branch, temporarily shifting the target's Attitude toward you up by one per SP spent; it shifts back by the same amount as soon as you fail a social test against them.</p>"},
    {"name": "Read the Room", "cost": "1", "description": "<p>The GM reveals the current Attitude, or an intention or mood indicator, for one character present of your choice. You can choose this stunt multiple times per roll.</p>"},
    {"name": "On the Fence", "cost": "2", "description": "<p>Choose a character you didn't target who's Standoffish, Neutral, or Open toward you. They're convinced to take your side in the conflict.</p>"},
    {"name": "Bad Form", "cost": "3", "description": "<p>Immediately regain the SP you spent on this stunt, plus 1 more. Then choose any character present; they now consider you a rival, threat, or enemy.</p>"},
    {"name": "Cast Out", "cost": "3", "description": "<p>Your action shames or embarrasses another character present, imposing a −2 penalty on their next social roll against anyone but you in this encounter.</p>"},
    {"name": "Risky Business", "cost": "4", "description": "<p>Your action reveals a secret or contains a significant lie, shifting your target's Attitude toward another character in the scene from Neutral or worse to Very Hostile.</p>"},
    {"name": "Meddle", "cost": "5", "description": "<p>Your action brings others together or drives a wedge between them. Choose two other characters present and shift their Attitudes toward each other up or down by one.</p>"},
]

# Membership & Reputation Stunts (page 125)
REPUTATION_STUNTS = [
    {"name": "Bon Mot", "cost": "1", "description": "<p>You tag the perfect witty remark onto the end of your action. For the rest of the session, gain a temporary honorific you can use for passive Reputation only.</p>"},
    {"name": "Stick Your Neck Out", "cost": "1", "description": "<p>Your test puts your own Reputation in jeopardy to help someone else. An ally of your choice gains a +2 bonus to their next social test in this encounter; if they fail, you lose all Reputation bonuses from one honorific for the rest of the session.</p>"},
    {"name": "In Good Standing", "cost": "2", "description": "<p>When targeting a member of an organization in which you have Membership, treat your rank as one higher for purposes of gaining access to resources for the rest of this encounter.</p>"},
    {"name": "Benefit of the Doubt", "cost": "3", "description": "<p>Your action impresses or charms any one character present. Increase all relevant Membership and Reputation bonuses by +1 while interacting with that character for the rest of the session.</p>"},
    {"name": "Go Viral", "cost": "3", "description": "<p>Whether via you or others sharing a video or audio recording, news gets out quickly about what you've just done. For the rest of the session, the honorific most related to this test applies even in situations where it seems unrelated.</p>"},
    {"name": "Oozing Confidence", "cost": "4", "description": "<p>Your action impresses or fools all the right people. Gain one temporary Reputation honorific or rank of Membership for the rest of the session.</p>"},
    {"name": "Name-Dropping", "cost": "5", "description": "<p>Your action displays your affiliation with someone whose Membership rank is higher than yours. You may use their Reputation or Membership benefits as your own for the rest of the session.</p>"},
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
        ("Chase Stunts", "Chase", CHASE_STUNTS),
        ("Combat Stunts", "Combat", COMBAT_STUNTS),
        ("Gun Stunts", "Gun", GUN_STUNTS),
        ("Grappling Stunts", "Grappling", GRAPPLING_STUNTS),
        ("Melee Stunts", "Melee", MELEE_STUNTS),
        ("Vehicle Combat Stunts", "Vehicle", VEHICLE_STUNTS),
        ("Exploration Stunts", "Exploration", EXPLORATION_STUNTS),
        ("Infiltration Stunts", "Infiltration", INFILTRATION_STUNTS),
        ("Social Stunts", "Social", SOCIAL_STUNTS),
        ("Attitude Stunts", "Attitude", ATTITUDE_STUNTS),
        ("Reputation Stunts", "Reputation", REPUTATION_STUNTS),
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
                existing_names.add(stunt_data['name'])
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
