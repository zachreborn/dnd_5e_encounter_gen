__author__ = 'zhill'
import monsters
import random
from bisect import bisect_left

########################################################################################################################
# Encounter Table
# Table filled with encounter data for difficulties and XP budgets. Useful data can be derived
encounter_table = {
    'easy': [25, 50, 75, 125, 250, 300, 350, 450, 550, 600, 800, 1000,
             1100, 1250, 1400, 1600, 2000, 2100, 2400, 2800],
    'medium': [50, 100, 150, 250, 500, 600, 750, 900, 1100, 1200, 1600,
               2000, 2200, 2500, 2800, 3200, 3900, 4200, 4900, 5700],
    'hard': [75, 150, 225, 375, 750, 900, 1100, 1400, 1600, 1900, 2400,
             3000, 3400, 3800, 4300, 4800, 5900, 6300, 7300, 8500],
    'deadly': [100, 200, 400, 500, 1100, 1400, 1700, 2100, 2400, 2800,
               3600, 4500, 5100, 5700, 6400, 7200, 8800, 9500, 10900, 12700],
}


def xp_budget(party_size, party_level, difficulty):
    """Function which takes the party size, average party level, and desired difficulty to return the correct XP budget
    within the encounter_table dictionary.
    """
    if party_level > 20 or party_level < 1 or party_size < 1:
        raise ValueError('Party level should be between 1 and 20, while party size should be 1 or greater.')
    return (encounter_table[difficulty][party_level - 1]) * party_size


def xp_list_gen(xp):
    """Function to find factors of the XP budget integer. Returns a random factor,
    so long as that factor pairing is < 30. This keeps the number of monsters manageable.
    """
    random_gen_factor = 0
    while random_gen_factor == 0 or (xp / random_gen_factor) > 30:
        random_gen_factor = random.choice([i for i in range(10, xp + 1) if xp % i == 0])
    return random_gen_factor


def rnd_select_monster(xp):
    """Function to return a randomly selected monster for an encounter that have the XP nearest the xp
    value input without going over. Pulls random monster from the monsters.cr_dict dictionary.
    """
    nearest_monster_xp = min([val[2] for val in monsters.cr_dict.values() if val[2] <= xp], key=lambda x: abs(x - xp))
    return random.choice([key for key, val in monsters.cr_dict.items() if val[2] == nearest_monster_xp])


def build_encounter_size(party_size, monster_xp, xp):
    """Function returns number of monsters in encounter based on previous function outputs.
    The number of monsters depends upon the party size, and xp budget.
    """
    monster_count = [1, 2, 6, 10, 14]
    encounter_multiplier = [1.0, 0.67, 0.50, 0.40, 0.33, 0.25]
    num_monsters = xp // monster_xp
    """Use monster_count table to find correct index in encounter_multiplier."""
    index_table = bisect_left(monster_count, num_monsters)
    if party_size <= 2 and index_table != len(encounter_multiplier) - 1:
        index_table += 1
    if num_monsters == 1:
        return num_monsters
    return int(num_monsters * encounter_multiplier[index_table])  # number, xp value


def get_user_input_str(prompt, choices=None):
    result = None
    while result is None:
        val = input(prompt).lower()
        if choices and val not in choices:
            print(' Error: must choose one: {0}'.format(choices,))
        else:
            result = val
    return result


def get_user_input_int(prompt):
    result = None
    while result is None:
        try:
            result = int(input(prompt))
        except ValueError:
            print(' not an integer, try again...')
    return result


########################################################################################################################
# Define encounter variables via user input. Loop through input and output until N is entered or CTRL-C is pressed.
script_repeat = 'y'
while script_repeat == 'y':
    party_size_input = get_user_input_int('Party size?> ')
    party_level_input = get_user_input_int('Party average level?> ')
    difficulty_input = get_user_input_str('Select difficulty:\nEasy, Medium, Hard, or Deadly> ',
                                          choices=['easy', 'medium', 'hard', 'deadly'])

########################################################################################################################
# Define run variables to output data
    encounter_xp = xp_budget(party_size_input, party_level_input, difficulty_input)
    xp_per_monster = xp_list_gen(encounter_xp)
    output_monster = rnd_select_monster(xp_per_monster)
    output_encounter = build_encounter_size(party_size_input, monsters.cr_dict[output_monster][2], encounter_xp)

    print('Randomized encounter based on:\nParty Size: {0}\nParty Level: {1}\n'
          'Difficulty: {2}\n'
          '{3}x {4}(s) found on Monster Manual page: {5}'.format(
              party_size_input, party_level_input, difficulty_input,
              output_encounter, output_monster, monsters.cr_dict[output_monster][0]))

    script_repeat = get_user_input_str('Run again? Y/N> ', choices=['y', 'n'])