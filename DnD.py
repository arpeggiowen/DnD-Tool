# -*- coding: utf-8 -*-
"""
A console-based tool for Dungeons & Dragons with several features for rolling
dice, stats and generating random characters.

"""

import random as ra

# read in list of races
file1 = open("DnD_races.txt","r")
races = file1.read().splitlines()
file1.close()

# read in list of classes
file2 = open("DnD_classes.txt","r")
classes = file2.read().splitlines()
file2.close()

# read in list of subclasses
file3 = open("DnD_subclasses.txt","r")
sub_classes = file3.read().splitlines()
file3.close()

# read in list of backgrounds
file4 = open("DnD_backgrounds.txt","r")
backgrounds = file4.read().splitlines()
file4.close()

#-----------------------------------Dice rolls--------------------------------#

# dice roller
def roll(dice):
    # check validity of input
    if not isinstance(dice,int):
        print(f'Error: input must be integer [4,6,8,10,12,20,100]')
        
    else:
        return ra.randint(1,dice)

# weighted d6
def wroll():
    wd = [1]*5 + [2]*10 + [3]*15 + [4]*20 + [5]*15 + [6]*10
    return ra.choice(wd)

# d20 roll with advantage
def advantage():
    d1 = roll(20)
    d2 = roll(20)
    return max(d1,d2)

# d20 roll with disadvantage
def disadvantage():
    d1 = roll(20)
    d2 = roll(20)
    return min(d1,d2)

#----------------------------------Character----------------------------------#

# return a random race
def random_race():
    return races[ra.randint(0,len(races)-1)]

# return a random class
def random_class():
    return classes[ra.randint(0,len(classes)-1)]

# return subclasses
def subclasses(char_class):
    # read through list of subclasses to determine relevant entries
    # start read after base class name in subclasses list
    start = sub_classes.index(char_class) + 1   
    
    # stop at end of list...
    if char_class == classes[-1]:
        stop = len(sub_classes)-1
    # ... or next base class has been reached
    else:
        stop = sub_classes.index(classes[classes.index(char_class)+1])-1
        
    # copy relevant subclasses to new list and return
    subs = []
    for sub in range(start,stop):
        subs.append(sub_classes[sub])
    return subs

# return a random subclass
def random_subclass(char_class):
    class_subs = subclasses(char_class)
    return class_subs[ra.randint(0,len(class_subs)-1)]

# return a random background
def random_background():
    return backgrounds[ra.randint(0, len(classes) - 1)]

#---------------------------------Stat rolls----------------------------------#

# roll a set number of dice then take the specified number of highest or lowest rolls
def sum_roll(num_dice, dice_val, to_total, high):
    d_roll = []
    for r in range(num_dice):
        d_roll.append(roll(dice_val))

    if high == True:
        d_roll.sort(reverse=True)
    else:
        d_roll.sort()

    return sum(d_roll[:to_total])

# roll for character stats
def stat_roll():
    stats = []

    for i in range(6):
        stat_roll = [roll(6),roll(6),roll(6),roll(6)]
        stat_roll.sort(reverse=True)
        stats.append(sum(stat_roll[:3]))

    return stats

# return greatest of three stat rolls
def max_roll():
    roll1, roll2, roll3 = stat_roll(), stat_roll(), stat_roll()
    if sum(roll1) > max(sum(roll2), sum(roll3)):
        return roll1
    elif sum(roll2) > max(sum(roll1),sum(roll3)):
        return roll2
    else:
        return roll3

# keep rolling until stat sum is at/above specified value
def min_roll(minimum):
    roll = stat_roll()
    while sum(roll) < minimum:
        roll = stat_roll()
    return roll

# make a stat roll where all values are above a minimum threshold
def avg_roll(minimum):
    d_roll = stat_roll()
    for stat in d_roll:
        if stat < minimum:
            re_roll = sum_roll(4,6,3,True)
            while re_roll < minimum:
                re_roll = sum_roll(4,6,3,True)
            d_roll[d_roll.index(stat)] = re_roll
    return d_roll

# stat roll in players' favour
def weighted_roll():
    wr = [wroll(),wroll(),wroll(),wroll()]
    wr.sort(reverse=True)
    return sum(wr[:3])

#----------------------------Background details-------------------------#

def parents(race):
    roll1 = roll(100)
    if roll1 < 96:
        # extra roll for mixed races
        if race == 'Half-Elf':
            roll1 = roll(8)
            if roll1 < 6:
                return 'An elf and a human.'
            elif roll1 == 6:
                return 'An elf and a half-elf.'
            elif roll1 == 7:
                return 'A human and a half-elf.'
            else:
                return 'Half-elves.'
        
        elif race == 'Half-Orc':
            roll1 = roll(8)
            if roll1 < 4:
                return 'An orc and a human'
            elif roll1 in (4,5):
                return 'An orc and a half-orc.'
            elif roll1 in (6,7):
                return 'A human and a half-orc.'
            else:
                return 'Half-orcs.'

        elif race == 'Tiefling':
            roll1 = roll(8)
            if roll1 < 5:
                return 'Humans.'
            elif roll1 in (5,6):
                return 'A tiefling and a human.'
            elif roll1 == 7:
                return 'A tiefling and a devil.'
            else:
                return 'A human and a devil.'

        return 'Known.'

    else:
        return 'Unknown.'

def birthplace():
    roll1 = roll(100)
    if roll1 <= 50:
        return 'Home.'
    elif roll1 in range(51,56):
        return 'Home of a family friend.'
    elif roll1 in range(56,64):
        return 'Home of a healer or midwife.'
    elif roll1 in (64,65):
        return 'Carriage, cart, or wagon.'
    elif roll1 in range(66,69):
        return 'Barn, shed, or other outbuilding.'
    elif roll1 in (69,70):
        return 'Cave.'
    elif roll1 in (71,72):
        return 'Field.'
    elif roll1 in (73,74):
        return 'Forest.'
    elif roll1 in range(75,78):
        return 'Temple.'
    elif roll1 == 78:
        return 'Battlefield.'
    elif roll1 in (79,80):
        return 'Alley or street.'
    elif roll1 in (81,82):
        return 'Brothel, tavern, or inn.'
    elif roll1 in (83,84):
        return 'Castle, keep, tower, or palace.'
    elif roll1 == 85:
        return 'Sewer or rubbish heap.'
    elif roll1 in range(86,89):
        return 'Among people of a different race.'
    elif roll1 in range(89,92):
        return 'On board a boat or a ship.'
    elif roll1 in (92,93):
        return 'In a prison or in the headquarters of a secret organisation.'
    elif roll1 in (94,95):
        return 'In a sage\'s laboratory.'
    elif roll1 == 96:
        return 'In the Feywild.'
    elif roll1 == 97:
        return 'In the shadowfell.'
    elif roll1 == 98:
        return 'On the Astral Plane or the Ethereal Plane.'
    elif roll1 == 99:
        return 'On an Inner Plane of your choice.'
    else:
        return 'On an Outer Plane of your choice.'

def siblings():
    sibling = 0
    order = 'Only child.'
    
    # number of siblings
    roll1 = roll(10)    
    if roll1 < 3:
        sibling = 0
        order = 'Only child.'
    elif roll1 in (3,4):
        sibling = roll(3)
    elif roll1 in (5,6):
        sibling = roll(4) + 1
    elif roll1 in (7,8):
        sibling = wroll() + 2
    else:
        sibling = roll(8) + 3

    #  birth order
    if roll1 >= 3:
        roll1 = wroll() + wroll()
        if roll1 == 2:
            order = 'Twin, triplet, or quadruplet.'
        elif roll1 in range(3,8):
            order = 'Older.'
        else:
            order = 'Younger.'

    return sibling, order

def family(cha):
    # family
    roll1 = roll(100)
    if roll1 == 1:
        family = 'None.'
    elif roll1 == 2:
        family = 'Instituion, such as an asylum.'
    elif roll1 == 3:
        family = "Temple."
    elif roll1 in (4,5):
        family = 'Orphanage.'
    elif roll1 in (6,7):
        family = 'Guardian.'
    elif roll1 in range(8,16):
        family = 'Paternal or maternal aunt, uncle, or both; or extended family such as a tribe or clan.'
    elif roll1 in range(16,26):
        family = 'Paternal or maternal grandparent(s).'
    elif roll1 in range(26,36):
        family = 'Adoptive family (same or different race).'
    elif roll1 in range(36,56):
        family = 'Single father or stepfather.'
    elif roll1 in range(56,76):
        family = 'Single mother or stepmother.'
    else:
        family = 'Mother and father.'

    
    # absent parent
    roll1 = roll(4)
    if roll1 == 1:
        absent = cause_of_death()
    elif roll1 == 2:
        absent = 'Parent was imprisoned, enslaved, or otherwise taken away.'
    elif roll1 == 3:
        absent = 'Abandoned by parents.'
    else:
        absent = 'Parent disappeared to an unknown fate.'

    # family lifestyle
    roll1 = wroll() + wroll() + wroll()
    if roll1 == 3:
        lifestyle = 'Wretched.'
        lmod = -40
    elif roll1 in (4,5):
        lifestyle = 'Squalid.'
        lmod = -20
    elif roll1 in range(6,9):
        lifestyle = 'Poor.'
        lmod = -10
    elif roll1 in range(9,13):
        lifestyle = 'Modest.'
        lmod = 0
    elif roll1 in range(13,16):
        lifestyle = 'Comfortable.'
        lmod = 10
    elif roll1 in (16,17):
        lifestyle = 'Wealthy.'
        lmod = 20
    else:
        lifestyle = 'Aristocratic.'
        lmod = 40

    # childhood home
    roll2 = roll(100)
    if roll2 + lmod <= 0:
        home = 'On the streets.'
    elif roll2 + lmod in range(1,21):
        home = 'No permanent residence; moved around a lot.'
    elif roll2 + lmod in range(31,41):
        home = 'Encampment or village in the wilderness.'
    elif roll2 + lmod in range(41,51):
        home = 'Apartment in a rundown neighbourhood.'
    elif roll2 + lmod in range(51,71):
        home = 'Small house.'
    elif roll2 in range(71,91):
        home = 'Large house.'
    elif roll2 in range(91,111):
        home = 'Mansion.'
    else:
        home = 'Palace or castle.'

    # childhood memories
    if roll1 + cha <= 3:
        memory = 'Haunted by the mistreatment of peers in childhood.'
    elif roll1 + cha in (4,5):
        memory = 'Spent most of childhood alone, with no close friends.'
    elif roll1 + cha in range(6,9):
        memory = 'Others saw as being different or strange, and so had few companions.'
    elif roll1 + cha in range(9,13):
        memory = 'Had a few close friends and lived and ordinary childhood.'
    elif roll1 + cha in range(13,16):
        memory = 'Had several friends and a generally happy childhood.'
    elif roll1 + cha in (16,17):
        memory = 'Always found it easy to make friends and loved being around people.'
    else:
        memory = 'Was known to everyone and had friends everywhere they went.'

    return family, absent, home, memory, lifestyle

def cause_of_death():
    roll1 = roll(12)
    if roll1 == 1:
        return 'Unknown.'
    elif roll1 == 2:
        return 'Murdured.'
    elif roll1 == 3:
        return 'Killed in battle.'
    elif roll1 == 4:
        return 'Accident related to class or occupaton.'
    elif roll1 == 5:
        return 'Accident unrelated to class or occupation.'
    elif roll1 in (6,7):
        return 'Natural causes, such as disease or old age.'
    elif roll1 == 8:
        return 'Apparent suicide.'
    elif roll1 == 9:
        return 'Torn apart by an animal or a natural disaster.'
    elif roll1 == 10:
        return 'Consumed by a monster.'
    elif roll1 == 11:
        return 'Executed for a crime or tortured to death.'
    else:
        return (f'Bizarre event, such as being hit by a meteorite, '
                f'struck down by an angry god, or killed by a hatching '
                f'slaad egg.')

def alignment():
    roll1 = roll(6) + roll(6) + roll(6)
    
    if roll1 == 3:
        return 'Chaotic Evil / Neutral'
    elif roll1 in (4,5):
        return 'Lawful Evil'
    elif roll1 in range(6,9):
        return 'Neutral Evil'
    elif roll1 in range(9,13):
        return 'Neutral'
    elif roll1 in range(13,16):
        return 'Neutral Good'
    elif roll1 in (16,17):
        return 'Lawful Good / Neutral'
    else:
        return 'Chaotic Good / Neutral'

def origins():
    race = random_race()
    c_class = random_class()
    sub_c = random_subclass(c_class)
    bg = random_background()
    parent = parents(race)
    birth_place = birthplace()
    sib, b_order = siblings()
    fam, absent, home, memory, lifestyle = family(wroll()-1)
    align = alignment()

    print(f'Race: {race}\n'
          f'Class: {c_class}\n'
          f'Subclass: {sub_c}\n'
          f'Background: {bg}\n'
          f'Parents: {parent}\n'
          f'Birthplace: {birth_place}\n'
          f'Home: {home}\n'
          f'Siblings: {sib}. {b_order}\n'
          f'Family: {fam} {absent} {memory}\n'
          f'Alignment: {align}\n'
          f'Lifestyle: {lifestyle}')
    
    
    

def main():
    repeat = True
    while repeat == True:
        print(f'[Q]uick character, [F]ull backstory, '
              f'[S]tat roll, or [D]ice roll: ')
        roll_type = input()
        
        # check for valid input
        while roll_type.upper() not in ['Q','F','S','D']:
            print(f'Please enter Q, F, S or R: ')
            roll_type = input()
            
        if roll_type.upper() == 'Q':
            race = random_race()
            c_class = random_class()
            sub = random_subclass(c_class)
            bg = random_background()
            print(f'{race} {c_class} ({sub}) {bg}')
        elif roll_type.upper() == 'F':
            origins()
        elif roll_type.upper() == 'S':
            print(stat_roll())
        elif roll_type.upper() == 'D':
            print(f'Dice (4, 6, 8, 10, 12, 20, 100): ')
            dice = int(input())
            while dice not in [4,6,8,10,12,20,100]:
                print(f'Enter valid dice (4, 6, 8, 10, 12, 20, 100): ')
                dice = int(input())
            
            if dice == 20:
                print(f'[N]ormal, with [a]dvantage or [d]isadvantage? ')
                adv = input()
                if adv.lower() == 'a':
                    print(advantage())
                elif adv.lower() == 'd':
                    print(disadvantage())
                else:
                    print(roll(20))
            else:
                print(roll(dice))
            
        print(f'Roll again? [Y/N]')
        rep_roll = input()
        if rep_roll.upper() != 'Y':
            repeat = False
    
main()