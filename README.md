Dungeons &amp; Dragons 5e Random Encounter Generator
====================================================

This is a full featured D&amp;D 5e random encounter generator built in Python 3.4. Encounters are built by creating
a XP budget. This budget is based on party size, average party level, and a difficulty selection.
Randomness is injected in two ways, first by selecting factors from an XP budget.
Second is by selecting a monster from an XP value near that random factor. This helps lend to lots of re-usability.


Features
--------
- Varying party sizes
- Average party levels
- Difficulty selection
- Input sanity checking

Usage
-----
Run this program with the following:

    python random_encounter_builder.py

The program will prompt you for your selections as such:

    Party size?> 4
    Party average level?> 5
    Select difficulty:
    Easy, [Medium], Hard, or Deadly> deadly
    Select monster type:'?' [All]> humanoid
    Randomized encounter based on:
    Party Size: 4
    Party Level: 5
    Difficulty: deadly
    5x Spy(s) found on Monster Manual page: 349
    Run again? Y/N
    [Y]>

Future Additions
----------------

- Seed monsters
- Encounter generation based on location