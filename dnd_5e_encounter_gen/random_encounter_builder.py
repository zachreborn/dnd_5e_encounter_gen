import random
import monsters
import encounter_tables
from bisect import bisect_left

__author__ = 'Zachary Hill'

monsters_dict = {}


class Monster:
    """Class used to rename values in the monsters.cr_dict dictionary."""
    def __init__(self, name, manpage, cr, xp, size, monster_type):
        self.name = name
        self.manpage = manpage
        self.cr = cr
        self.xp = xp
        self.size = size
        self.monster_type = monster_type


def xp_budget(party_size, party_level, difficulty):
    """Function which takes the party size, average party level, and desired difficulty to return the correct XP budget
    within the encounter_table dictionary.
    """
    if party_level > 20 or party_level < 1 or party_size < 1:
        raise ValueError('Party level should be between 1 and 20, while party size should be 1 or greater.')
    return (encounter_tables.xp_difficulties[difficulty][party_level - 1]) * party_size


def xp_list_gen(xp):
    """Function to find factors of the XP budget integer. Returns a random factor,
    so long as that factor pairing is < 21. This keeps the number of monsters output manageable.
    """
    xp_factors = [i for i in range(10, xp + 1) if xp % i == 0]
    random_gen_factor = 0
    while random_gen_factor == 0 or (xp / random_gen_factor) > 20:
        random_gen_factor = random.choice(xp_factors)
    return random_gen_factor


def rnd_select_monster(xp, monster_type, input_monster_dict):
    """Function to return a randomly selected monster for an encounter that have the XP nearest the xp
    value input without going over. First checks to see if monster_type filter is set or not then
    pulls random monster from the monsters_dict dictionary.
    """
    if monster_type == 'all':
        nearest_monster_xp = min(list_monster_xp(input_monster_dict, xp), key=lambda x: abs(x - xp))
        monster_selections = [key for key in input_monster_dict if input_monster_dict[key].xp == nearest_monster_xp]
        output_monster = random.choice(monster_selections)
        return output_monster
    else:
        monster_type_dict = {key for key in input_monster_dict if input_monster_dict[key].monster_type == monster_type.capitalize()}
        nearest_monster_xp = min([input_monster_dict[key].xp for key in monster_type_dict if input_monster_dict[key].xp <= xp], key=lambda x: abs(x - xp))
        monster_selections = [key for key in monster_type_dict if input_monster_dict[key].xp == nearest_monster_xp and input_monster_dict[key].monster_type == monster_type.capitalize()]
        output_monster = random.choice(monster_selections)
        return output_monster


def list_monster_xp(input_monster_dict, xp):
    monster_xp_list = []
    for key in input_monster_dict:
        if input_monster_dict[key].xp <= xp:
            monster_xp_list.append(input_monster_dict[key].xp)
    return monster_xp_list


def build_encounter_size(party_size, monster_xp, xp):
    """Function returns number of monsters in encounter based on previous function outputs.
    The number of monsters depends upon the party size, and xp budget.
    """
    ## TODO need to rebuild this function. Function should subtract from the XP pool to determine encounter size. Will allow for encounters that are closer to the proper difficulty.
    monster_count = [1, 2, 6, 10, 14]
    encounter_multiplier = [1.0, 0.67, 0.50, 0.40, 0.33, 0.25]
    num_monsters = xp // monster_xp
    # Use monster_count table to find correct index in encounter_multiplier.
    index_table = bisect_left(monster_count, num_monsters)
    if party_size <= 2 and index_table != len(encounter_multiplier) - 1:
        index_table += 1
    if num_monsters == 1:
        return num_monsters
    return int(num_monsters * encounter_multiplier[index_table])  # number, xp value


def get_user_input_str(prompt, default_choice, choices=None):
    """Function returns a string based on input with exception check, so long as the input is one of a few choices."""
    result = None
    while result is None:
        val = input(prompt).lower()
        if val is '':
            result = default_choice
        elif choices and val not in choices:
            print(' Error: must choose one: {0}'.format(choices,))
        else:
            result = val
    return result


def get_user_input_int(prompt):
    """Function returns an integer based on input with exception checking."""
    result = None
    while result is None:
        try:
            result = int(input(prompt))
        except ValueError:
            print(' not an integer, try again...')
    return result


def get_user_input_vars():
    """Function grabs user input and returns formatted output for encounter building.
    User input selection is: Prompt text, default option, list of choices."""
    party_size_input = get_user_input_int('Party size?> ')
    party_level_input = get_user_input_int('Party average level?> ')
    difficulty_input = get_user_input_str('Select difficulty:\nEasy, [Medium], Hard, or Deadly> ',
                                          default_choice='medium', choices=['easy', 'medium', 'hard', 'deadly'])
    monster_type = get_user_input_str("Select monster type:'?' [All]> ", default_choice='all', choices=encounter_tables.monster_types_list)
    return party_size_input, party_level_input, difficulty_input, monster_type


def script_run():
    """Define encounter variables via user input. Loop through input and output
    until N or No is entered or CTRL-C is pressed.
    """
    # TODO restructure code so that it uses friendly names. ie current_encounter[1] should be current_encounter.avg_level
    current_encounter = get_user_input_vars()
    script_repeat = 'y'
    while script_repeat == 'y' or script_repeat == 'yes':
        """Define run variables to output data."""
        encounter_xp = xp_budget(current_encounter[0], current_encounter[1], current_encounter[2])
        xp_per_monster = xp_list_gen(encounter_xp)
        output_monster = rnd_select_monster(xp_per_monster, current_encounter[3], monsters_dict)
        output_encounter = build_encounter_size(current_encounter[0], monsters_dict[output_monster].xp, encounter_xp)

        print('Randomized encounter based on:\nParty Size: {0}\nParty Level: {1}\nDifficulty: {2}\nMonster type: {3}\n'
              '{4}x {5}(s) found on Monster Manual page: {6}'.format(
                  current_encounter[0], current_encounter[1], current_encounter[2], current_encounter[3],
                  output_encounter, output_monster, monsters_dict[output_monster].manpage))

        script_repeat = get_user_input_str('Run again? Y/N\n[Y]> ', default_choice='y', choices=['y', 'yes', 'n', 'no'])


def main():
    for key in monsters.cr_dict:
        monsters_dict[key] = Monster(key, *monsters.cr_dict[key])

    script_run()


if __name__ == '__main__':
    main()