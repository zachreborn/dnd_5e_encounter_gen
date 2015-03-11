# dnd_5e_encounter_gen
Dungeons &amp; Dragons 5e random encounter generator
====================================================

This is a full featured D&amp;Dragons 5e random encounter generator. It primarily makes use of a dictionary
with each monster and associated XP values. Randomness is injected in two ways, first by selecting factors
from an XP budget. This XP budget is defined by your party size, average party level, and difficulty selection.
The second is by selecting a monster from an XP value near that random factor. This helps lend to lots of re-usability.



Features
--------
- Varying party sizes
- Average party levels
- Difficulty selection


Usage
-----
Presently this program can be run by the following:

    python random_encounter_builder.py

The program will prompt you for your selections as such:

    Party size?> 4
    Party average level?> 5
    Select difficulty:
    Easy, Medium, Hard, or Deadly> deadly
    Randomized encounter based on:
    Party Size: 4
    Party Level: 5
    Difficulty: deadly
    5x Spy(s) found on Monster Manual page: 349
    Run again? Y/N>

Future Additions
----------------

My primary next goal will be to add monster groupings to either a separate dictionary or the same dictionary.
This will allow for monster groupings outside of a single monster type using a more iterative approach of
selecting monsters from the dictionaries.