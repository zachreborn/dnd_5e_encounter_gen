__author__ = 'zhill'
import monsters_by_challenge_rating
import random

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
        raise AssertionError('Party level should be between 1 and 20, while party size should be 1 or greater.')
    return (encounter_table[difficulty][party_level - 1]) * party_size


def xp_list_gen(xp):
    """Function to find factors of the XP budget integer."""
    # TODO return the random factor but also how many times said factor goes in so we know how many creatures to use
    random_gen_factor = random.choice([i for i in range(2, int(xp * 0.5) + 1) if xp % i == 0])
    return int(xp / random_gen_factor), random_gen_factor


def build_encounter(xp):
    """Function to return list of monsters for an encounter that have the XP value input
    List comprehension. Insert key into list so long as XP is equal to key value at index 2
    """
    # TODO this also needs to spit out n, where == n * factor = xp
    return random.choice([key for key, val in monsters_by_challenge_rating.cr_dict.items() if val[2] == xp])


########################################################################################################################
# Define encounter variables via user input
# TODO Might want to separate these out into their own functions and set the variables equal to that function.
# TODO Better input sanitation
party_size_input = int(input('Party size?\n'))
party_level_input = int(input('Party average level?\n'))
difficulty_input = str.lower(input('Select difficulty:\nEasy, Medium, Hard, or Deadly\n'))


########################################################################################################################
# Testing functions - party size, party level, difficulty
# print(build_encounter(int(xp_budget(party_size_input, party_level_input, difficulty_input))))
# print(int(xp_budget(party_size_input, party_level_input, difficulty_input)))
# print(build_encounter(7200))
# print(xp_list_gen(7200))