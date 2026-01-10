#!/usr/bin/env python3
"""Add TUE Core talents to the Foundry VTT database."""

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

# Core Talents from TUE Core (pages 46-58)
CORE_TALENTS = [
    {
        "name": "Affluent",
        "requirements": "None",
        "description": "You have access to greater resources than most.",
        "novice": "When you select this talent, increase your Income by +2.",
        "expert": "When you gain this degree, increase your Income by +1. You may add 2 to your Income score when comparing your score with an item's cost to purchase it automatically, without a test, or to determine whether the purchase will deplete your Income. You enjoy this benefit only once per game session.",
        "master": "When you gain this degree, increase your Income by +1. You can re-roll a failed Income test but must keep the result of the second roll."
    },
    {
        "name": "Agility",
        "requirements": "Dexterity 2, Dexterity (Acrobatics) focus",
        "description": "You move with grace, speed, and ease.",
        "novice": "Every move you make is part of one fluid motion. Using the Move action to stand up, climb, dismount, etc. does not reduce your Speed.",
        "expert": "When you move, terrain-based hazards do not reduce your Speed. When you fall, if you succeed at a Dexterity (Acrobatics) test with a TN determined by the GM based on height and nearby surfaces, you suffer only half damage.",
        "master": "Impressive acrobatics are just the way you naturally move. You can re-roll any die result of 1 on each die for Dexterity (Acrobatics), Stamina (Running), and Strength (Climbing, Jumping) tests, but must keep the results of the second roll."
    },
    {
        "name": "Artistry",
        "requirements": "Communication 1+ and the Dexterity (Crafting) focus or Communication (Expression) focus",
        "description": "You can create fine works of art. For the performing arts, see the Performance talent.",
        "novice": "You can use the Dexterity (Crafting) or Communication (Expression) focuses to create works of art. Choose a field of visual or literary arts. The GM determines the time and TN of the test, and the Drama Die determines your work's quality if you succeed.",
        "expert": "You grow as an artist, deepening your mastery of your craft or diversifying your talents. You learn the tools and tricks of a new artistic field or gain a +1 bonus to ability tests to create works of art in a field you are trained in.",
        "master": "You become an undisputed master of your craft. You learn the tools and tricks of a number of artistic fields equal to your Communication, or select one field and add your Willpower to the Drama Die to determine the quality of your work."
    },
    {
        "name": "Attractive",
        "requirements": "None",
        "description": "You have that special something that catches and holds people's attention and interest.",
        "novice": "Your presence is as stunning upon the second impression as it is on the first. You can use the Making an Entrance social stunt a second time at any point of an encounter. Also, if an NPC could be attracted to you, their initial attitude is one step more favorable towards you.",
        "expert": "You know how to best exploit your appearance. You can perform the Flirt social stunt for 3 SP instead of its normal cost, and the target of your efforts can have a Neutral attitude instead of Open.",
        "master": "Every move you make captures the attention and interest of others. When interacting with characters who would be attracted to you, you can re-roll a failed Communication (Deception, Performing, Persuasion, or Seduction) test, but must keep the result of the second roll."
    },
    {
        "name": "Burglary",
        "requirements": "Dexterity 2+",
        "description": "You know how to bypass security to enter a place and take anything that strikes your fancy.",
        "novice": "You know your way around security systems. When you succeed at an Intelligence (Security) test to study a lock, alarm, guards, or any part of a security system or protocol, the GM provides you with one more piece of information.",
        "expert": "Security measures cannot stop you. If you fail an Intelligence (Technology) test involving a security measure, you can re-roll it, but must keep the results of the second roll.",
        "master": "No valuable escapes your notice. If you fail a Perception (Searching) test, you can re-roll it, but must keep the results of the second roll."
    },
    {
        "name": "Command",
        "requirements": "Communication 2 or higher",
        "description": "You are a skilled and capable leader.",
        "novice": "Your presence inspires allies. If you take a major action to offer guidance, your allies gain a +1 bonus to Willpower (Courage) and Willpower (Morale) tests for the rest of the encounter. You can do this once per encounter.",
        "expert": "Your allies follow your lead. Any NPCs or PCs you lead gain a +1 bonus when rolling for initiative.",
        "master": "When you stand firm, your allies stand with you. When you lead NPCs or PCs in an encounter, they do not have to make a Willpower (Morale) test until more than two-thirds of your side's combatants are out of the fight. PCs also gain a +2 to Willpower (Courage) tests."
    },
    {
        "name": "Doctor",
        "requirements": "Intelligence (Medicine) focus",
        "description": "You can heal wounds and treat illness and other conditions.",
        "novice": "You're skilled in treating patients. You can re-roll any dice with a result of 1 or 2 when making an Intelligence (Medicine) test.",
        "expert": "With access to medical supplies and tools, you can treat some conditions. With an hour and a basic TN 11 Intelligence (Medicine) test you can remove a wounded condition, leaving the patient only injured.",
        "master": "You can perform complex medical procedures to restore a patient to a normal, healthy condition, and you can re-roll any failed Intelligence (Medicine) test, but must keep the result of the second roll."
    },
    {
        "name": "Dual Weapon Style",
        "requirements": "Dexterity 2+",
        "description": "You can fight in hand-to-hand combat with a weapon in your primary hand and another in your offhand.",
        "novice": "While wielding two close combat weapons, if you take the Activate action, you gain either a +1 bonus on your melee attack rolls or a +1 Defense bonus vs. melee attacks until the end of the encounter. You can switch the bonus with another Activate action.",
        "expert": "You can perform the Lightning Attack stunt for 2 SP instead of the usual 3, but the extra attack must come from your secondary weapon.",
        "master": "You can overwhelm opponents with attacks from both weapons. If you make a Melee Attack with your primary weapon and you are not charging, you can make another attack with your secondary weapon as a minor action."
    },
    {
        "name": "Know-It-All",
        "requirements": "Intelligence 2+",
        "description": "You can bring your considerable knowledge to bear on any situation.",
        "novice": "You can attempt a test using an Intelligence focus somehow related to the test at hand rather than the called-for ability, but with a −1 penalty.",
        "expert": "You leverage every bit of information available to you. You can perform the Breakthrough exploration stunt for 2 SP.",
        "master": "When you succeed at an ability test with a knowledge focus, you gain a +1 bonus to the result of each Drama Die on tests using related focuses for the duration of the encounter."
    },
    {
        "name": "Linguistics",
        "requirements": "Intelligence 1+",
        "description": "You pick up new languages easily. When you learn a new language, you learn to both speak and read it.",
        "novice": "You learn an additional language.",
        "expert": "You learn two additional languages for a total of three plus your native language(s). You can also imitate a specific dialect with a successful Communication (Performance) test.",
        "master": "You learn three additional languages for a total of six plus your native language(s). You can also pick any one additional language you know and speak it like a native—without any trace of an accent."
    },
    {
        "name": "Observation",
        "requirements": "Perception 2+",
        "description": "You have an eye for detail.",
        "novice": "Choose a Perception focus. If you fail a Perception test with your chosen focus, you can re-roll it but must keep the result of the second roll.",
        "expert": "Analysis of your observation often leads to insight. On a successful Perception test, you can spend 2 SP to make a second, immediate Perception test with the same TN but with a different focus than the first.",
        "master": "Nothing escapes your scrutiny. On a successful Perception test, you can spend 2 SP and gain a +2 bonus to all Perception tests involving the same object or subject as the first test for the duration of the encounter."
    },
    {
        "name": "Oratory",
        "requirements": "Communication (Persuasion) focus",
        "description": "You are a skilled and charismatic public speaker.",
        "novice": "You know how to work a crowd. If you fail a Communication (Persuasion) test when trying to convince a group (not an individual), you can re-roll it but must keep the results of the second roll.",
        "expert": "Each time you perform the Sway the Crowd social stunt, you affect three additional people instead of one.",
        "master": "You can agitate a crowd. If you make a successful Communication (Persuasion) test when addressing a group and the result of your Drama Die is 5 or 6, you rouse them to immediate action."
    },
    {
        "name": "Overwhelm Style",
        "requirements": "Fighting 2+",
        "description": "You are relentless and overwhelming in melee combat.",
        "novice": "When you make a close combat attack, you can take up to a −3 penalty on your attack roll to receive a corresponding bonus to your damage roll.",
        "expert": "Your expertise makes you dangerous. When you succeed with a close combat attack, you can add your focus bonus for that attack to your damage total.",
        "master": "You break through your opponent's defense with brutal or relentless attacks. By spending 3 SP after a successful attack, your target must make an opposed Strength (Might) test against your attack roll. If they fail, they suffer a −2 penalty to Defense until the end of your next turn."
    },
    {
        "name": "Performance",
        "requirements": "Communication (Performing) focus",
        "description": "You have a talent for the performing arts.",
        "novice": "Choose a form of performance art. You are an accomplished performer in your chosen art. In addition, you may perform the From the Heart and Sway the Crowd stunts for 1 SP less than their normal cost.",
        "expert": "You can add an additional form of performance to your repertoire. If you have at least 15 minutes to observe a crowd before performing, you gain a +1 bonus to any Communication-based tests to persuade or entertain them.",
        "master": "You can add an additional form of performance to your repertoire. When performing, you exude confidence and style. You may perform the With a Flourish stunt while performing in front of an audience for 3 SP, and its effects last until the end of the day."
    },
    {
        "name": "Pinpoint Accuracy",
        "requirements": "Accuracy or Fighting 1+, and Dexterity 1+",
        "description": "If you can see it, you can hit it. Hard.",
        "novice": "You strike where it hurts the most. Once per round, you can add 1d6 to the damage of a successful attack if your Dexterity is greater than your target's.",
        "expert": "Your instinct is as sharp as your eyes. When you take the Aim action, the attack bonus you gain is +2 instead of +1.",
        "master": "You can perform the Called Shot stunt for 3 SP. You can also use it with any weapon, not just guns."
    },
    {
        "name": "Protect",
        "requirements": "Perception and Willpower 1+",
        "description": "You are the shield that protects your friends.",
        "novice": "Your desire to protect others lends you speed. When you perform the Bodyguard action stunt, you can move up to 6 meters instead of 3.",
        "expert": "You react quickly to put yourself in harm's way. When you perform the Guardian Angel action stunt, the amount of damage you take instead of your ally is equal to the number of SP spent +2.",
        "master": "You become the shadow of those who would hurt others. If you are standing next to an opponent and that opponent moves within 2 meters of one of your allies, you can move adjacent to the opponent before they finish their turn, even if it would surpass your Speed."
    },
    {
        "name": "Quick Reflexes",
        "requirements": "Dexterity 2+",
        "description": "You react to threats instantly and instinctually.",
        "novice": "You can prepare yourself for action in an instant. Once per round, on your turn, you can use Ready as a free action.",
        "expert": "You can go prone or stand up as a free action rather than as part of a Move action.",
        "master": "It is very hard for an opponent to get the drop on you. You may re-roll your initiative roll at the start of a combat encounter but must keep the results of the second roll."
    },
    {
        "name": "Rifle Style",
        "requirements": "Accuracy (Rifles) focus",
        "description": "A rifle is far more dangerous in your hands.",
        "novice": "You can assume a high ready stance; as long as you do not move more than half your Speed, you can make an attack with a loaded rifle you are holding as a reaction before rolling initiative, even if surprised.",
        "expert": "You skillfully leverage your weapon's ability to punch through cover. You ignore 2 points of any armor bonus provided by cover when using a longarm or assault rifle.",
        "master": "Penalties to the attack roll due to range do not apply to your attacks with a rifle."
    },
    {
        "name": "Scouting",
        "requirements": "Dexterity 2+",
        "description": "You are skilled in reconnaissance and infiltration.",
        "novice": "If you fail a Dexterity (Stealth) test, you can re-roll it but must keep the results of the second roll.",
        "expert": "You know how to get the drop on opponents. You can perform the Seize the Initiative stunt for 2 SP.",
        "master": "You are a skilled observer. If you fail a Perception (Seeing) test, you can re-roll it but must keep the results of the second roll."
    },
    {
        "name": "Self-Defense Style",
        "requirements": "Fighting (Brawling) focus",
        "description": "You are trained in martial arts focused on defense and deflection.",
        "novice": "You use your opponent's momentum against them. When a melee attack misses you, you can use the Grapple action stunt as a reaction without spending any SP. In addition, you can perform the Knock Prone action stunt for 1 SP instead of the usual 2 against an opponent you have grappled.",
        "expert": "Your grip is difficult to break. If you fail a Fighting (Grappling) test, you can re-roll it but must keep the results of the second roll.",
        "master": "You counter an opponent with grace and skill. When you perform the Disarm stunt, you can retain hold of the weapon. In addition, when you spend SP on Knock Prone after making a Fighting (Grappling) attack, you may automatically move your opponent 2 meters for no additional SP cost."
    },
    {
        "name": "Single Weapon Style",
        "requirements": "Perception 2+",
        "description": "You can fight more effectively wielding a single-handed melee weapon.",
        "novice": "Fighting with a single-handed weapon demands increased awareness. If you take the Activate action, you gain a +1 Defense bonus until the end of the encounter while fighting in this style.",
        "expert": "You can wield your weapon to block and parry attacks. Your bonus to Defense increases to +2 while fighting in this style.",
        "master": "You know how to fight several enemies at once. Opponents making melee attacks against you never gain a bonus on their attack rolls for outnumbering you."
    },
    {
        "name": "Tactical Awareness",
        "requirements": "Dexterity and Perception 1+",
        "description": "You move calmly and expertly while in combat.",
        "novice": "You can take the Melee Attack or Ranged Attack action at any point during your movement. Normally you have to finish your movement before attacking.",
        "expert": "You seem to have eyes in the back of your head. When you perform the Take One for the Team exploration stunt, you only take half the damage from a trap or hazard and your ally remains unscathed.",
        "master": "You are hard to pin down in combat. Opponents do not gain an attack bonus for outnumbering you in melee."
    },
    {
        "name": "Thrown Weapon Style",
        "requirements": "None",
        "description": "You are adept with weapons thrown by hand.",
        "novice": "You gain a +1 bonus on attack rolls with thrown weapons.",
        "expert": "You can Ready a throwing weapon or grenade as a free action instead of a minor action.",
        "master": "Add your Accuracy score in meters to the range of throwing weapons and grenades when you throw them."
    },
    {
        "name": "Two-Handed Style",
        "requirements": "Strength 3+ and Fighting 1+",
        "description": "With heavy melee weapon in your hands, you are a truly formidable opponent.",
        "novice": "Your weapon and the power of your attacks force foes to yield ground. When you hit with a melee attack with a heavy weapon, you can move the target 2 meters in any direction like the Skirmish stunt.",
        "expert": "You strike fearsome blows with your weapon. You can perform the Vicious Blow stunt for 1 SP when wielding a heavy weapon.",
        "master": "You and your weapon are as one. When you are wielding a heavy weapon and gain SP, you gain +2 SP to use exclusively for the following stunts: Expose, Knock Prone, Shock and Awe, Skirmish, and Wound."
    },
]

# Specializations from TUE Core (pages 59-65)
SPECIALIZATIONS = [
    {
        "name": "Academic",
        "requirements": "Intelligence 2+ and the Intelligence (Research) focus",
        "description": "You are trained in all modern methods of finding information and putting it to use.",
        "novice": "You have a real skill in not only finding facts, but knowing where to look. If you fail an Intelligence (Research) test, you can re-roll it but must keep the result of the second roll.",
        "expert": "You have become adept at recalling relevant information. When you perform the A-Ha! stunt, you gain one free extra use of it.",
        "master": "Your fact-finding abilities are unparalleled. When you make an Intelligence (Research) test as part of an advanced test, you gain a +1 bonus to the result of each Drama Die."
    },
    {
        "name": "Ace",
        "requirements": "Dexterity 3+, and the Dexterity (Piloting) focus",
        "description": "Few can fly like you do.",
        "novice": "You can coax more out of your ship than most. When you perform the Punch It chase stunt, you gain an extra +1 bonus on your next chase test.",
        "expert": "Add +2 to the Drama Die when making tests using the Dexterity (Piloting) focus.",
        "master": "You are a peerless pilot. Add +1 to tests made using Dexterity (Piloting), and you may re-roll a failed test, but you don't get the bonus on the re-roll and must take the result of the second roll."
    },
    {
        "name": "Agent",
        "requirements": "Perception 2+ and the Perception (Empathy) and Communication (Deception) focuses",
        "description": "You're a skilled spy and infiltrator.",
        "novice": "You built your life on lies. If you fail a Communication (Deception) test, you can re-roll it but must keep the result of the second roll.",
        "expert": "You are also adept at seeing through deception. When you use the Read the Room stunt, add +3 to your Perception (Empathy) roll when the stunt is opposed.",
        "master": "You are a masterful spy. You gain two of the following focuses if you don't have them already: Communication (Disguise), Communication (Investigation), Dexterity (Stealth), Intelligence (Cryptography), and Intelligence (Security)."
    },
    {
        "name": "Commando",
        "requirements": "Constitution 2+, Willpower (Self-Discipline) focus",
        "description": "You are trained to fight, and to win, no matter the odds.",
        "novice": "If you fail a Constitution or Willpower (Self-Discipline) test, you can re-roll, but must keep the result of the second roll.",
        "expert": "You know how to work with a team to get things done. At this degree, you gain an intensity 1 Relationship with your team, whoever that may be.",
        "master": "You can overcome the effects of some conditions through sheer grit. When you acquire the exhausted, fatigued, injured, or wounded conditions, make a TN 13 Constitution (Stamina) or Willpower (Self-Discipline) test; if you succeed, you ignore the effects of the condition for the remainder of the encounter."
    },
    {
        "name": "Executive",
        "requirements": "Communication 2+ and the Communication (Persuasion) focus",
        "description": "You claim authority and leadership in an organization.",
        "novice": "You have experience in negotiating the byways of your organization. You acquire a Membership in a new organization or advance to the next rank with an existing Membership.",
        "expert": "Your authority extends to calling in a subordinate to support you. Once per day you may make a Communication (Persuasion) test to call in a subordinate from your organization.",
        "master": "Because you have influence in your organization, you have constant access to resources. Add your Membership rank to your Income whenever you can call upon your organization."
    },
    {
        "name": "Gunfighter",
        "requirements": "Dexterity 2 and Accuracy 2+",
        "description": "No one shoots as quickly or as accurately as you.",
        "novice": "Your accuracy is instinctive. Pick Accuracy (Pistols) or Accuracy (Rifles). You gain a +1 to attack and damage rolls for attacks made using your chosen focus.",
        "expert": "You're fast and precise. You may pick the other focus from the Novice degree and apply the Novice benefit to it, or improve the bonus for the focus you picked at Novice rank to +2.",
        "master": "You're one with the gun. Choose one of the following stunts: Lightning Attack, Overwatch, Lethal Blow, or Instant Kill. You can perform the chosen stunt for 1 SP less than usual when wielding a firearm."
    },
    {
        "name": "Hacker (Specialization)",
        "requirements": "Intelligence 2+ and the Intelligence (Technology) focus",
        "description": "You excel at the use and abuse of computer systems.",
        "novice": "You are skilled in navigating computer systems. Add +1 to Intelligence (Technology) tests.",
        "expert": "When things go wrong or don't work quite how you want them to, you're skilled in finding backdoors and loopholes. You can perform the High Tech Hustle stunt for 2 SP.",
        "master": "Breaking into a system is one thing, but getting out without getting caught is another. While using a computer system, you may perform the Cover Your Tracks stunt for 1 SP."
    },
    {
        "name": "Investigator",
        "requirements": "Perception and Intelligence 2+, at least one Perception focus",
        "description": "You're a skilled detective.",
        "novice": "You can always make a test to unlock a lead, even if you don't have a primary or tangential focus relevant to the investigation.",
        "expert": "The real trick to being a great investigator isn't in finding clues, it's in how you use them. You may use the Intuition stunt for 1 SP.",
        "master": "When all the evidence is gathered, it only needs a flash of inspiration to put it together and find the solution. You can use the Breakthrough stunt on an investigation for only 3 SP."
    },
    {
        "name": "Martial Artist",
        "requirements": "Fighting 2 or better and at least Novice rank in one hand-to-hand combat style",
        "description": "You are a master of hand-to-hand combat.",
        "novice": "When you make a Fighting-based attack roll, add +1 to damage on a successful hit.",
        "expert": "You have excellent speed and timing. When you perform the Momentum stunt with SP gained from a Fighting attack roll, you gain a bonus to your initiative as if you spent one more SP than you have.",
        "master": "You are a master of many close combat techniques. When you perform the Stunt Attack action with a Fighting attack roll, you automatically generate 3 SP."
    },
    {
        "name": "Overwatch",
        "requirements": "Communication 2+, Intelligence (Tactics) focus, and either Communication (Leadership) or Communication (Persuasion) focus",
        "description": "You do not need to be there in person to assist your crew.",
        "novice": "You can make an Intelligence (Tactics) test instead of a normal attack when performing a Stunt Attack, with the target's Defense as the TN. The Group Tactics, Double Team, Shock and Awe, and Over Here! Stunts cost 1 SP less when you use this talent.",
        "expert": "As long as you can see your crew you can lend a hand. You can cooperate in advanced tests even beyond the maximum number of characters who can cooperate in the test.",
        "master": "You can quickly make up for your crew's mistakes. When an ally you can perceive fails a test, you can make an Intelligence (Tactics) test with a TN equal to the original test's TN +2. If you succeed, it counts as if your ally had succeeded."
    },
    {
        "name": "Sniper",
        "requirements": "Accuracy 3 or better and the Accuracy (Rifles) focus",
        "description": "You are a crack shot.",
        "novice": "You know how to quietly set up a decisive shot. If you're hidden from your target, you can re-roll your first Accuracy (Rifles) attack during an encounter, but must keep the results of the second roll.",
        "expert": "You know how to wait for a perfect shot to present itself. If you use the Aim action for an Accuracy (Rifles) attack, add a bonus to damage equal to the attack roll bonus your Aim provides.",
        "master": "You are a deadly shot. When you are using the Accuracy (Rifles) focus, you can perform the Called Shot stunt for 2 SP."
    },
    {
        "name": "Socialite",
        "requirements": "Communication and Perception 2+",
        "description": "You know people and how to get what you want from them.",
        "novice": "Your natural charm causes people to like you. You may perform the On the Fence stunt for 1 SP.",
        "expert": "When you attempt a detailed social maneuver, you require one fewer shift (to a minimum of 1) to succeed. If the situation only requires a simple social maneuver, add +1 to your roll.",
        "master": "Wherever you go, you fit in with ease. When you interact with people who would have an attitude of Neutral or worse toward you, they automatically shift it one step in your favor."
    },
    {
        "name": "Spin Doctor",
        "requirements": "Communication 2+, Perception (Insight) focus, and either Communication (Expression) or Communication (Persuasion) focus",
        "description": "You can shape the hearts and minds of the masses.",
        "novice": "You can create fake news or expose the truth. When you witness a news story or statement, you can make a Communication test to present an alternate point of view that people believe.",
        "expert": "Your words can build or destroy reputations. Pick an individual to compliment or smear, and make a Communication test. If you win, you can impose a Reputation honorific or remove one the target already has.",
        "master": "Your ability to shape and mold people's opinions is strong. You may re-roll a failed Communication (Persuasion) or Communication (Expression) test but must keep the re-rolled result."
    },
    {
        "name": "Star",
        "requirements": "Communication 2+ and the Communication (Performing) focus",
        "description": "You can sway people with your performance, charisma, and fame.",
        "novice": "When using the Communication (Performing) focus, you may perform the Sway the Crowd stunt for 1 SP.",
        "expert": "A good performance opens doors and makes people want to know you. You can perform the Oozing Confidence stunt for 2 SP.",
        "master": "When you need to, you can pull out all of the stops with a performance. When you attempt a social grand gesture, your success threshold for each shift is one less than it would normally be."
    },
    {
        "name": "Thief",
        "requirements": "Dexterity 2+, the Dexterity (Sleight of Hand) and Dexterity (Stealth) focuses",
        "description": "You are adept at stealing things and avoiding getting caught.",
        "novice": "The first thing a skilled thief perfects is the ability to work unnoticed. You add +1 to all tests made with the Dexterity (Stealth) or the Dexterity (Sleight of Hand) focuses. Choose which focus receives this benefit.",
        "expert": "When you make a Dexterity test to hide or steal an object, you can re-roll the test if you choose, but must keep the result of the second roll. You may perform the It Wasn't Me stunt for 2 SP.",
        "master": "Add another +1 to tests using either Dexterity (Sleight of Hand) or Dexterity (Stealth), selecting the focus when you attain this degree."
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


def create_talent(talent_data, folder_id, folder_name, is_specialization=False):
    """Create a talent item entry."""
    # Build HTML description with tiers
    desc = f"<p><strong>Requirements:</strong> {talent_data['requirements']}</p>"
    desc += f"<p>{talent_data['description']}</p>"
    desc += f"<p><strong>Novice:</strong> {talent_data['novice']}</p>"
    desc += f"<p><strong>Expert:</strong> {talent_data['expert']}</p>"
    desc += f"<p><strong>Master:</strong> {talent_data['master']}</p>"

    talent_type = "Specialization" if is_specialization else "General"

    return {
        "_id": generate_id(),
        "name": talent_data["name"],
        "type": "talent",
        "img": "systems/expanse/ui/item-img/talent.png",
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
            "type": talent_type,
            "name": "",
            "description": desc
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

    # Find the parent "Talents" folder
    talents_parent_id = None
    for folder in db.get('folders', []):
        if folder['name'] == 'Talents':
            talents_parent_id = folder['_id']
            break

    # Create Core Talents folder if needed
    core_folder_name = "Core Talents"
    core_folder_id = None
    if core_folder_name not in existing_folder_names:
        core_folder = create_folder(core_folder_name, parent=talents_parent_id)
        core_folder_id = core_folder['_id']
        db['folders'].append(core_folder)
        folders_added += 1
        print(f"Created folder: {core_folder_name}")
    else:
        for folder in db.get('folders', []):
            if folder['name'] == core_folder_name:
                core_folder_id = folder['_id']
                break

    # Create Specializations folder if needed
    spec_folder_name = "Specializations"
    spec_folder_id = None
    if spec_folder_name not in existing_folder_names:
        spec_folder = create_folder(spec_folder_name, parent=talents_parent_id)
        spec_folder_id = spec_folder['_id']
        db['folders'].append(spec_folder)
        folders_added += 1
        print(f"Created folder: {spec_folder_name}")
    else:
        for folder in db.get('folders', []):
            if folder['name'] == spec_folder_name:
                spec_folder_id = folder['_id']
                break

    # Add Core Talents
    for talent_data in CORE_TALENTS:
        if talent_data['name'] not in existing_names:
            talent = create_talent(talent_data, core_folder_id, core_folder_name, is_specialization=False)
            db['items'].append(talent)
            items_added += 1
            existing_names.add(talent_data['name'])
            print(f"Added talent: {talent_data['name']}")
        else:
            print(f"Skipped (exists): {talent_data['name']}")

    # Add Specializations
    for talent_data in SPECIALIZATIONS:
        if talent_data['name'] not in existing_names:
            talent = create_talent(talent_data, spec_folder_id, spec_folder_name, is_specialization=True)
            db['items'].append(talent)
            items_added += 1
            existing_names.add(talent_data['name'])
            print(f"Added specialization: {talent_data['name']}")
        else:
            print(f"Skipped (exists): {talent_data['name']}")

    # Write updated database
    with open('packs/the-expanse-quickstart.db', 'w') as f:
        json.dump(db, f, separators=(',', ':'))

    print(f"\nTotal folders added: {folders_added}")
    print(f"Total talents added: {items_added}")
    return items_added


if __name__ == '__main__':
    main()
