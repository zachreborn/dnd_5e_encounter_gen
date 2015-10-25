__author__ = 'Zachary Hill'
## TODO move this to an easier to write file YAML or XML then import with a class.
# Monsters by CR
# 'Monster Name': [Monster Manual Page, 'Challenge Rating number', Experience Points, Size, Type]
# 'Key'         :       [0],                       [1],                      [2]      [3]   [4]
cr_dict = {
    # CR 0 is 10 XP
    'Awakened shrub': [317, '0', 10, 'Small', 'Plant'],
    'Baboon': [318, '0', 10, 'Small', 'Beast'],
    'Badger': [318, '0', 10, 'Tiny', 'Beast'],
    'Bat': [318, '0', 10, 'Tiny', 'Beast'],
    'Cat': [320, '0', 10, 'Tiny', 'Beast'],
    'Commoner': [345, '0', 10, 'Medium', 'Humanoid'],
    'Crab': [320, '0', 10, 'Tiny', 'Beast'],
    'Crawling claw': [44, '0', 10, 'Tiny', 'Undead'],
    'Deer': [321, '0', 10, 'Medium', 'Beast'],
    'Eagle': [322, '0', 10, 'Small', 'Beast'],
    'Frog': [322, '0', 10, 'Tiny', 'Beast'],
    'Giant fire beetle': [325, '0', 10, 'Small', 'Beast'],
    'Goat': [330, '0', 10, 'Medium', 'Beast'],
    'Hawk': [330, '0', 10, 'Tiny', 'Beast'],
    'Homunculus': [188, '0', 10, 'Tiny', 'Construct'],
    'Hyena': [331, '0', 10, 'Medium', 'Beast'],
    'Jackal': [331, '0', 10, 'Small', 'Beast'],
    'Lemure': [76, '0', 10, 'Medium', 'Fiend'],
    'Lizard': [332, '0', 10, 'Tiny', 'Beast'],
    'Myconid sprout': [230, '0', 10, 'Small', 'Plant'],
    'Octopus': [333, '0', 10, 'Small', 'Beast'],
    'Owl': [333, '0', 10, 'Tiny', 'Beast'],
    'Quipper': [335, '0', 10, 'Tiny', 'Beast'],
    'Rat': [335, '0', 10, 'Tiny', 'Beast'],
    'Raven': [335, '0', 10, 'Tiny', 'Beast'],
    'Scorpion': [337, '0', 10, 'Tiny', 'Beast'],
    'Sea horse': [337, '0', 10, 'Tiny', 'Beast'],
    'Shrieker': [138, '0', 10, 'Medium', 'Plant'],
    'Spider': [337, '0', 10, 'Tiny', 'Beast'],
    'Vulture': [339, '0', 10, 'Medium', 'Beast'],
    'Weasel': [340, '0', 10, 'Tiny', 'Beast'],
    # CR 1/8 - 25XP
    'Bandit': [343, '1/8', 25, 'Medium', 'Humanoid'],
    'Blood hawk': [319, '1/8', 25, 'Small', 'Beast'],
    'Camel': [320, '1/8', 25, 'Large', 'Beast'],
    'Cultist': [345, '1/8', 25, 'Medium', 'Humanoid'],
    'Flumph': [135, '1/8', 25, 'Small', 'Aberration'],
    'Flying snake': [322, '1/8', 25, 'Tiny', 'Beast'],
    'Giant crab': [324, '1/8', 25, 'Medium', 'Beast'],
    'Giant rat': [327, '1/8', 25, 'Small', 'Beast'],
    'Giant weasel': [329, '1/8', 25, 'Medium', 'Beast'],
    'Guard': [347, '1/8', 25, 'Medium', 'Humanoid'],
    'Kobold': [195, '1/8', 25, 'Small', 'Humanoid'],
    'Manes': [60, '1/8', 25, 'Small', 'Fiend'],
    'Mastiff': [332, '1/8', 25, 'Medium', 'Beast'],
    'Merfolk': [218, '1/8', 25, 'Medium', 'Humanoid'],
    'Monodrone': [224, '1/8', 25, 'Medium', 'Construct'],
    'Mule': [333, '1/8', 25, 'Medium', 'Beast'],
    'Noble': [348, '1/8', 25, 'Medium', 'Humanoid'],
    'Poisonous snake': [334, '1/8', 25, 'Tiny', 'Beast'],
    'Pony': [335, '1/8', 25, 'Medium', 'Beast'],
    'Slaad tadpole': [276, '1/8', 25, 'Tiny', 'Aberration'],
    'Stirge': [284, '1/8', 25, 'Tiny', 'Beast'],
    'Tribal warrior': [350, '1/8', 25, 'Medium', 'Humanoid'],
    'Twig blight': [32, '1/8', 25, 'small', 'Plant'],
    # CR 1/4 - 50XP
    'Aarakocra': [12, '1/4', 50, 'Medium', 'Humanoid'],
    'Acolyte': [342, '1/4', 50, 'Medium', 'Humanoid'],
    'Axe beak': [317, '1/4', 50, 'Large', 'Beast'],
    'Blink dog': [318, '1/4', 50, 'Medium', 'Fey'],
    'Boar': [319, '1/4', 50, 'Medium', 'Beast'],
    'Bullywug': [35, '1/4', 50, 'Medium', 'Humanoid'],
    'Constrictor snake': [320, '1/4', 50, 'Large', 'Beast'],
    'Draft horse': [321, '1/4', 50, 'Large', 'Beast'],
    'Dretch': [57, '1/4', 50, 'Small', 'Fiend'],
    'Drow': [128, '1/4', 50, 'Medium', 'Humanoid'],
    'Duodrone': [225, '1/4', 50, 'Medium', 'Construct'],
    'Elk': [322, '1/4', 50, 'Large', 'Beast'],
    'Flying sword': [20, '1/4', 50, 'Small', 'Construct'],
    'Giant badger': [323, '1/4', 50, 'Medium', 'Beast'],
    'Giant bat': [323, '1/4', 50, 'Large', 'Beast'],
    'Giant centipede': [323, '1/4', 50, 'Small', 'Beast'],
    'Giant frog': [325, '1/4', 50, 'Medium', 'Beast'],
    'Giant lizard': [326, '1/4', 50, 'Large', 'Beast'],
    'Giant owl': [327, '1/4', 50, 'Large', 'Beast'],
    'Giant poisonous snake': [327, '1/4', 50, 'Medium', 'Beast'],
    'Giant wolf spider': [330, '1/4', 50, 'Medium', 'Beast'],
    'Goblin': [166, '1/4', 50, 'Small', 'Humanoid'],
    'Grimlock': [175, '1/4', 50, 'Medium', 'Humanoid'],
    'Kenku': [194, '1/4', 50, 'Medium', 'Humanoid'],
    'Kuo-toa': [199, '1/4', 50, 'Medium', 'Humanoid'],
    'Leonin': ['MaD 31', '1/4', 50, 'Medium', 'Humanoid'],
    'Luck Dragon': ['MaD 21', '1/4', 50, 'Tiny', 'Dragon'],
    'Mud mephit': [216, '1/4', 50, 'Small', 'Elemental'],
    'Myr': ['MaD 10', '1/4', 50, 'Small', 'Construct'],
    'Needle blight': [32, '1/4', 50, 'Medium', 'Plant'],
    'Panther': [333, '1/4', 50, 'Medium', 'Beast'],
    'Pixie': [253, '1/4', 50, 'Tiny', 'Fey'],
    'Pseudodragon': [254, '1/4', 50, 'Tiny', 'Dragon'],
    'Pteranodon': [80, '1/4', 50, 'Medium', 'Beast'],
    'Riding horse': [336, '1/4', 50, 'Large', 'Beast'],
    'Skeleton': [272, '1/4', 50, 'Medium', 'Undead'],
    'Smoke mephit': [217, '1/4', 50, 'Small', 'Elemental'],
    'Sprite': [283, '1/4', 50, 'Tiny', 'Fey'],
    'Steam mephit': [217, '1/4', 50, 'Small', 'Elemental'],
    'Swarm of bats': [337, '1/4', 50, 'Medium', 'Beast'],
    'Swarm of rats': [339, '1/4', 50, 'Medium', 'Beast'],
    'Swarm of ravens': [339, '1/4', 50, 'Medium', 'Beast'],
    'Troglodyte': [290, '1/4', 50, 'Medium', 'Humanoid'],
    'Violet fungus': [138, '1/4', 50, 'Medium', 'Plant'],
    'Winged kobold': [195, '1/4', 50, 'Small', 'Humanoid'],
    'Wolf': [341, '1/4', 50, 'Medium', 'Beast'],
    'Zombie': [316, '1/4', 50, 'Medium', 'Undead'],
    # CR 1/2 is 100XP
    'Ape': [317, '1/2', 100, 'Medium', 'Beast'],
    'Baneling': ['MaD 28', '1/2', 100, 'Small', 'Fiend'],
    'Black bear': [318, '1/2', 100, 'Medium', 'Beast'],
    'Cockatrice': [42, '1/2', 100, 'Small', 'Monstrosity'],
    'Crocodile': [320, '1/2', 100, 'Large', 'Beast'],
    'Darkmantle': [46, '1/2', 100, 'Small', 'Monstrosity'],
    'Deep gnome': [164, '1/2', 100, 'Small', 'Humanoid'],
    'Dust mephit': [215, '1/2', 100, 'Small', 'Elemental'],
    'Fern Lizard': ['MaD 20', '1/2', 100, 'Small', 'Beast'],
    'Gas spore': [138, '1/2', 100, 'Large', 'Plant'],
    'Gazellean': ['MaD 35', '1/2', 100, 'Medium', 'Humanoid'],
    'Giant goat': [326, '1/2', 100, 'Large', 'Beast'],
    'Giant sea horse': [328, '1/2', 100, 'Large', 'Beast'],
    'Giant wasp': [329, '1/2', 100, 'Medium', 'Beast'],
    'Gnoll': [163, '1/2', 100, 'Medium', 'Humanoid'],
    'Gray ooze': [243, '1/2', 100, 'Medium', 'Ooze'],
    'Hobgoblin': [186, '1/2', 100, 'Medium', 'Humanoid'],
    'Ice mephit': [215, '1/2', 100, 'Small', 'Elemental'],
    'Jackalwere': [193, '1/2', 100, 'Medium', 'Humanoid'],
    'Lizardfolk': [204, '1/2', 100, 'Medium', 'Humanoid'],
    'Magma mephit': [216, '1/2', 100, 'Small', 'Elemental'],
    'Magmin': [212, '1/2', 100, 'Small', 'Elemental'],
    'Myconid adult': [232, '1/2', 100, 'Medium', 'Plant'],
    'Orc': [246, '1/2', 100, 'Medium', 'Humanoid'],
    'Piercer': [252, '1/2', 100, 'Medium', 'Monstrosity'],
    'Reef shark': [336, '1/2', 100, 'Medium', 'Beast'],
    'Rust monster': [262, '1/2', 100, 'Medium', 'Monstrosity'],
    'Sahuagin': [263, '1/2', 100, 'Medium', 'Humanoid'],
    'Satyr': [267, '1/2', 100, 'Medium', 'Fey'],
    'Scout': [349, '1/2', 100, 'Medium', 'Humanoid'],
    'Shadow': [269, '1/2', 100, 'Medium', 'Undead'],
    'Sliver': ['MaD 15', '1/2', 100, 'Medium', 'Monstrosity'],
    'Spider Skull': ['MaD 52', '1/2', 100, 'Tiny', 'Undead'],
    'Spirit': ['MaD 27', '1/2', 100, 'Medium', 'Undead'],
    'Swarm of insects': [338, '1/2', 100, 'Medium', 'Beast'],
    'Thug': [350, '1/2', 100, 'Medium', 'Humanoid'],
    'Tridrone': [225, '1/2', 100, 'Medium', 'Construct'],
    'Verdalin': ['MaD 55', '1/2', 100, 'Small', 'Fey'],
    'Vine blight': [32, '1/2', 100, 'Medium', 'Plant'],
    'Warhorse': [340, '1/2', 100, 'Large', 'Beast'],
    'Warhorse skeleton': [273, '1/2', 100, 'Large', 'Undead'],
    'Worg': [341, '1/2', 100, 'Large', 'Monstrosity'],
    # CR 1 is 200XP
    'Animated armor': [19, '1', 200, 'Medium', 'Construct'],
    'Arcanamite': ['MaD 34', '1', 200, 'Small', 'Monstrosity'],
    'Brass dragon wyrmling': [106, '1', 200, 'Medium', 'Dragon'],
    'Brown bear': [319, '1', 200, 'Large', 'Beast'],
    'Bugbear': [33, '1', 200, 'Medium', 'Humanoid'],
    'Burning Skeleton': ['MaD 42', '1', 200, 'Medium', 'Undead'],
    'Copper dragon wyrmling': [112, '1', 200, 'Medium', 'Dragon'],
    'Death dog': [321, '1', 200, 'Medium', 'Monstrosity'],
    'Dire wolf': [321, '1', 200, 'Large', 'Beast'],
    'Dryad': [121, '1', 200, 'Medium', 'Fey'],
    'Duergar': [122, '1', 200, 'Medium', 'Humanoid'],
    'Eldrazi Scion': ['MaD 43', '1', 200, 'Large', 'Aberration'],
    'Fire snake': [265, '1', 200, 'Medium', 'Elemental'],
    'Ghoul': [148, '1', 200, 'Medium', 'Undead'],
    'Giant eagle': [324, '1', 200, 'Large', 'Beast'],
    'Giant hyena': [326, '1', 200, 'Large', 'Beast'],
    'Giant octopus': [326, '1', 200, 'Large', 'Beast'],
    'Giant spider': [328, '1', 200, 'Large', 'Beast'],
    'Giant toad': [329, '1', 200, 'Large', 'Beast'],
    'Giant vulture': [329, '1', 200, 'Large', 'Beast'],
    'Goblin boss': [166, '1', 200, 'Small', 'Humanoid'],
    'Half-ogre': [238, '1', 200, 'Large', 'Giant'],
    'Harpy': [181, '1', 200, 'Medium', 'Monstrosity'],
    'Hippogriff': [184, '1', 200, 'Large', 'Monstrosity'],
    'Imp': [76, '1', 200, 'Tiny', 'Fiend'],
    'Kobold Bully': ['MaD 24', '1', 200, 'Small', 'Humanoid'],
    'Kuo-toa whip': [199, '1', 200, 'Medium', 'Humanoid'],
    'Lion': [331, '1', 200, 'Large', 'Beast'],
    'Pustuloid': ['MaD 6', '1', 200, 'Small', 'Fiend'],
    'Quadrone': [226, '1', 200, 'Medium', 'Construct'],
    'Quaggoth spore servant': [230, '1', 200, 'Medium', 'Plant'],
    'Quasit': [63, '1', 200, 'Tiny', 'Fiend'],
    'Scarecrow': [268, '1', 200, 'Medium', 'Construct'],
    'Silverpaw Dog': ['MaD 39', '1', 200, 'Medium', 'Fey'],
    'Specter': [279, '1', 200, 'Medium', 'Undead'],
    'Spy': [349, '1', 200, 'Medium', 'Humanoid'],
    'Swarm of quippers': [338, '1', 200, 'Medium', 'Beast'],
    'Thri-kreen': [288, '1', 200, 'Medium', 'Humanoid'],
    'Tiger': [339, '1', 200, 'Large', 'Beast'],
    'Winter Sprite': ['MaD 58', '1', 200, 'Tiny', 'Fey'],
    'Young faerie dragon': [133, '1', 200, 'Tiny', 'Dragon'],
    'Yuan-ti pureblood': [310, '1', 200, 'Medium', 'Humanoid'],
    # CR2 = 450XP
    'Adult faerie dragon': [133, '2', 450, 'Tiny', 'Dragon'],
    'Allosaurus': [79, '2', 450, 'Large', 'Beast'],
    'Ankheg': [21, '2', 450, 'Large', 'Monstrosity'],
    'Awakened tree': [317, '2', 450, 'Huge', 'Plant'],
    'Azer': [22, '2', 450, 'Medium', 'Elemental'],
    'Bandit captain': [344, '2', 450, 'Medium', 'Humanoid'],
    'Berserker': [344, '2', 450, 'Medium', 'Humanoid'],
    'Black dragon wyrmling': [88, '2', 450, 'Medium', 'Dragon'],
    'Bronze dragon wyrmling': [109, '2', 450, 'Medium', 'Dragon'],
    'Carrion crawler': [37, '2', 450, 'Large', 'Monstrosity'],
    'Cave bear': [334, '2', 450, 'Large', 'Beast'],
    'Centaur': [38, '2', 450, 'Large', 'Monstrosity'],
    'Cult fanatic': [345, '2', 450, 'Medium', 'Humanoid'],
    'Druid': [346, '2', 450, 'Medium', 'Humanoid'],
    'Ettercap': [131, '2', 450, 'Medium', 'Monstrosity'],
    'Fiendish Hyena': ['MaD 23', '2', 450, 'Large', 'Fiend'],
    'Gargoyle': [140, '2', 450, 'Medium', 'Elemental'],
    'Gelatinous cube': [242, '2', 450, 'Large', 'Ooze'],
    'Ghast': [148, '2', 450, 'Medium', 'Undead'],
    'Giant boar': [323, '2', 450, 'Large', 'Beast'],
    'Giant constrictor snake': [324, '2', 450, 'Huge', 'Beast'],
    'Giant elk': [325, '2', 450, 'Huge', 'Beast'],
    'Gibbering mouther': [157, '2', 450, 'Medium', 'Aberration'],
    'Githzerai monk': [161, '2', 450, 'Medium', 'Humanoid'],
    'Gnoll pack lord': [163, '2', 450, 'Medium', 'Humanoid'],
    'Green dragon wyrmling': [95, '2', 450, 'Medium', 'Dragon'],
    'Grick': [173, '2', 450, 'Medium', 'Monstrosity'],
    'Griffon': [174, '2', 450, 'Large', 'Monstrosity'],
    'Hunter shark': [330, '2', 450, 'Large', 'Beast'],
    'Intellect devourer': [191, '2', 450, 'Tiny', 'Aberration'],
    'Kobold Shaman': ['MaD 25', '2', 450, 'Small', 'Humanoid'],
    'Lizardfolk shaman': [205, '2', 450, 'Medium', 'Humanoid'],
    'Merrow': [219, '2', 450, 'Large', 'Monstrosity'],
    'Might Sliver': ['MaD 16', '2', 450, 'Large', 'Monstrosity'],
    'Mimic': [220, '2', 450, 'Medium', 'Monstrosity'],
    'Minotaur skeleton': [273, '2', 450, 'Large', 'Undead'],
    'Morphlit': ['MaD 3', '2', 450, 'Small', 'Aberration'],
    'Myconid sovereign': [232, '2', 450, 'Large', 'Plant'],
    'Nothic': [236, '2', 450, 'Medium', 'Aberration'],
    'Ochre jelly': [243, '2', 450, 'Large', 'Ooze'],
    'Ogre': [237, '2', 450, 'Large', 'Giant'],
    'Ogre zombie': [316, '2', 450, 'Large', 'Undead'],
    'Orc eye of Gruumsh': [247, '2', 450, 'Medium', 'Humanoid'],
    'Orog': [247, '2', 450, 'Medium', 'Humanoid'],
    'Pegasus': [250, '2', 450, 'Large', 'Celestial'],
    'Pentadrone': [226, '2', 450, 'Large', 'Construct'],
    'Peryton': [251, '2', 450, 'Medium', 'Monstrosity'],
    'Plesiosaurus': [80, '2', 450, 'Large', 'Beast'],
    'Polar bear': [334, '2', 450, 'Large', 'Beast'],
    'Poltergeist': [279, '2', 450, 'Medium', 'Undead'],
    'Priest': [348, '2', 450, 'Medium', 'Humanoid'],
    'Quaggoth': [256, '2', 450, 'Medium', 'Humanoid'],
    'Rhinoceros': [336, '2', 450, 'Large', 'Beast'],
    'Rug of smothering': [20, '2', 450, 'Large', 'Construct'],
    'Saber-toothed tiger': [336, '2', 450, 'Large', 'Beast'],
    'Sahuagin priestess': [264, '2', 450, 'Medium', 'Humanoid'],
    'Screecher': ['MaD 50', '2', 450, 'Large', 'Monstrosity'],
    'Sea hag': [179, '2', 450, 'Medium', 'Fey'],
    'Silver dragon wyrmling': [118, '2', 450, 'Medium', 'Dragon'],
    'Spined devil': [78, '2', 450, 'Small', 'Fiend'],
    'Spitting Sliver': ['MaD 18', '2', 450, 'Large', 'Monstrosity'],
    'Swarm of poisonous snakes': [338, '2', 450, 'Medium', 'Beast'],
    'Swarm of Squirrels': ['MaD 53', '2', 450, 'Medium', 'Beast'],
    'Wererat': [209, '2', 450, 'Medium', 'Humanoid'],
    'White dragon wyrmling': [102, '2', 450, 'Medium', 'Dragon'],
    'Will-o-wisp': [301, '2', 450, 'Tiny', 'Undead'],
    # CR3 is 700XP
    'Ankylosaurus': [79, '3', 700, 'Huge', 'Beast'],
    'Armour Sliver': ['MaD 16', '3', 700, 'Large', 'Monstrosity'],
    'Basilisk': [24, '3', 700, 'Medium', 'Monstrosity'],
    'Bearded devil': [70, '3', 700, 'Medium', 'Fiend'],
    'Blue dragon wyrmling': [91, '3', 700, 'Medium', 'Dragon'],
    'Bugbear chief': [33, '3', 700, 'Medium', 'Humanoid'],
    'Death Widow': ['MaD 49', '3', 700, 'Large', 'Monstrosity'],
    'Displacer beast': [81, '3', 700, 'Large', 'Monstrosity'],
    'Doppelganger': [82, '3', 700, 'Medium', 'Monstrosity'],
    'Fire Spire Initiate': ['MaD 9', '3', 700, 'Medium', 'Humanoid'],
    'Gladeborn Trapper': ['MaD 51', '3', 700, 'Medium', 'Humanoid'],
    'Giant scorpion': [327, '3', 700, 'Large', 'Beast'],
    'Githyanki warrior': [160, '3', 700, 'Medium', 'Humanoid'],
    'Gold dragon wyrmling': [115, '3', 700, 'Medium', 'Dragon'],
    'Green hag': [177, '3', 700, 'Medium', 'Fey'],
    'Grell': [172, '3', 700, 'Medium', 'Aberration'],
    'Hell hound': [182, '3', 700, 'Medium', 'Fiend'],
    'Hobgoblin captain': [186, '3', 700, 'Medium', 'Humanoid'],
    'Hook horror': [189, '3', 700, 'Large', 'Monstrosity'],
    'Killer whale': [331, '3', 700, 'Huge', 'Beast'],
    'Knight': [347, '3', 700, 'Medium', 'Humanoid'],
    'Kuo-toa monitor': [199, '3', 700, 'Medium', 'Humanoid'],
    'Manticore': [213, '3', 700, 'Large', 'Monstrosity'],
    'Minotaur': [223, '3', 700, 'Large', 'Monstrosity'],
    'Mummy': [228, '3', 700, 'Medium', 'Undead'],
    'Nightmare': [235, '3', 700, 'Large', 'Fiend'],
    'Owlbear': [249, '3', 700, 'Large', 'Monstrosity'],
    'Phase spider': [334, '3', 700, 'Large', 'Monstrosity'],
    'Quaggoth thonot': [256, '3', 700, 'Medium', 'Humanoid'],
    'Rat Hermit': ['MaD 2', '3', 700, 'Medium', 'Humanoid'],
    'Spectator': [30, '3', 700, 'Medium', 'Aberration'],
    'Snow Spider': ['MaD 57', '3', 700, 'Large', 'Beast'],
    'Tentaghoul': ['MaD 48', '3', 700, 'Large', 'Undead'],
    'Troll Boar': ['MaD 37', '3', 700, 'Large', 'Monstrosity'],
    'Truesong Dancer': ['MaD 30', '3', 700, 'Medium', 'Humanoid'],
    'Veteran': [350, '3', 700, 'Medium', 'Humanoid'],
    'Virulent Sliver': ['MaD 17', '3', 700, 'Large', 'Monstrosity'],
    'Water weird': [299, '3', 700, 'Large', 'Elemental'],
    'Werewolf': [211, '3', 700, 'Medium', 'Humanoid'],
    'Wight': [300, '3', 700, 'Medium', 'Undead'],
    'Winged Sliver': ['MaD 17', '3', 700, 'Large', 'Monstrosity'],
    'Winter wolf': [340, '3', 700, 'Large', 'Monstrosity'],
    'Yeti': [305, '3', 700, 'Large', 'Monstrosity'],
    'Yuan-ti malison': [309, '3', 700, 'Medium', 'Monstrosity'],
    # CR4 is 1100XP
    'Banshee': [23, '4', 1100, 'Medium', 'Undead'],
    'Black pudding': [241, '4', 1100, 'Large', 'Ooze'],
    'Bone naga': [233, '4', 1100, 'Large', 'Undead'],
    'Chuul': [40, '4', 1100, 'Large', 'Aberration'],
    'Couatl': [43, '4', 1100, 'Medium', 'Celestial'],
    'Crystalline Sliver': ['MaD 18', '4', 1100, 'Large', 'Monstrosity'],
    'Elephant': [322, '4', 1100, 'Huge', 'Beast'],
    'Ettin': [132, '4', 1100, 'Large', 'Giant'],
    'Flameskull': [134, '4', 1100, 'Tiny', 'Undead'],
    'Ghost': [147, '4', 1100, 'Medium', 'Undead'],
    'Gnoll fang of Yeenoghu': [163, '4', 1100, 'Medium', 'Fiend'],
    'Helmed horror': [183, '4', 1100, 'Medium', 'Construct'],
    'Incubus': [284, '4', 1100, 'Medium', 'Fiend'],
    'Kobold Hero': ['MaD 26', '4', 1100, 'Small', 'Humanoid'],
    'Lamia': [201, '4', 1100, 'Large', 'Monstrosity'],
    'Lizard king/queen': [205, '4', 1100, 'Medium', 'Humanoid'],
    'Orc war chief': [246, '4', 1100, 'Medium', 'Humanoid'],
    'Red dragon wyrmling': [98, '4', 1100, 'Medium', 'Dragon'],
    'Sea hag (in coven)': [179, '4', 1100, 'Medium', 'Fey'],
    'Shadow demon': [64, '4', 1100, 'Medium', 'Fiend'],
    'Silverpaw Paladin': ['MaD 39', '4', 1100, 'Small', 'Humanoid'],
    'Succubus': [285, '4', 1100, 'Medium', 'Fiend'],
    'Wereboar': [209, '4', 1100, 'Medium', 'Humanoid'],
    'Weretiger': [210, '4', 1100, 'Medium', 'Humanoid'],
    # CR5 is 1800XP
    'Air elemental': [124, '5', 1800, 'Large', 'Elemental'],
    'Barbed devil': [70, '5', 1800, 'Medium', 'Fiend'],
    'Barlgura': [56, '5', 1800, 'Large', 'Fiend'],
    'Beholder zombie': [316, '5', 1800, 'Large', 'Undead'],
    'Bulette': [34, '5', 1800, 'Large', 'Monstrosity'],
    'Cambion': [36, '5', 1800, 'Medium', 'Fiend'],
    'Drow elite warrior': [128, '5', 1800, 'Medium', 'Humanoid'],
    'Earth elemental': [124, '5', 1800, 'Large', 'Elemental'],
    'Fire elemental': [125, '5', 1800, 'Large', 'Elemental'],
    'Flesh golem': [169, '5', 1800, 'Medium', 'Construct'],
    'Giant crocodile': [324, '5', 1800, 'Huge', 'Beast'],
    'Giant shark': [328, '5', 1800, 'Huge', 'Beast'],
    'Gladeborn Hunter': ['MaD 51', '5', 1800, 'Medium', 'Humanoid'],
    'Gladiator': [346, '5', 1800, 'Medium', 'Humanoid'],
    'Gorgon': [171, '5', 1800, 'Large', 'Monstrosity'],
    'Green hag (coven)': [177, '5', 1800, 'Medium', 'Fey'],
    'Grove Guardian': ['MaD 38', '5', 1800, 'Large', 'Fey'],
    'Half-red dragon veteran': [180, '5', 1800, 'Medium', 'Humanoid'],
    'Hill giant': [155, '5', 1800, 'Huge', 'Giant'],
    'Mezzoloth': [313, '5', 1800, 'Medium', 'Fiend'],
    'Myr Battlesphere': ['MaD 11', '5', 1800, 'Huge', 'Construct'],
    'Night hag': [178, '5', 1800, 'Medium', 'Fiend'],
    'Otyugh': [248, '5', 1800, 'Large', 'Aberration'],
    'Owlbear Matron': ['MaD 56', '5', 1800, 'Large', 'Monstrosity'],
    'Red slaad': [276, '5', 1800, 'Large', 'Aberration'],
    'Revenant': [259, '5', 1800, 'Medium', 'Undead'],
    'Roper': [261, '5', 1800, 'Large', 'Monstrosity'],
    'Sahuagin baron': [264, '5', 1800, 'Large', 'Humanoid'],
    'Salamander': [266, '5', 1800, 'Large', 'Elemental'],
    'Shambling mound': [270, '5', 1800, 'Large', 'Plant'],
    'Spellskite': ['MaD 36', '5', 1800, 'Large', 'Construct'],
    'Triceratops': [80, '5', 1800, 'Huge', 'Beast'],
    'Troll': [291, '5', 1800, 'Large', 'Giant'],
    'Truesong Dirge': ['MaD 30', '5', 1800, 'Medium', 'Humanoid'],
    'Umber hulk': [292, '5', 1800, 'Large', 'Monstrosity'],
    'Unicorn': [294, '5', 1800, 'Large', 'Celestial'],
    'Vampire spawn': [298, '5', 1800, 'Medium', 'Undead'],
    'Water elemental': [125, '5', 1800, 'Large', 'Elemental'],
    'Werebear': [208, '5', 1800, 'Medium', 'Humanoid'],
    'Wraith': [302, '5', 1800, 'Medium', 'Undead'],
    'Xorn': [304, '5', 1800, 'Medium', 'Elemental'],
    'Young remorhaz': [258, '5', 1800, 'Large', 'Monstrosity'],
    # CR6 is 2300XP
    'Chasme': [57, '6', 2300, 'Large', 'Fiend'],
    'Chimera': [39, '6', 2300, 'Large', 'Monstrosity'],
    'Cyclops': [45, '6', 2300, 'Huge', 'Giant'],
    'Drider': [120, '6', 2300, 'Large', 'Monstrosity'],
    'Galeb duhr': [139, '6', 2300, 'Medium', 'Elemental'],
    'Githzerai zerth': [161, '6', 2300, 'Medium', 'Humanoid'],
    'Gnoll Deathknight': ['MaD 22', '6', 2300, 'Medium', 'Humanoid'],
    'Herald of Rot': ['MaD 7', '6', 2300, 'Large', 'Fiend'],
    'Hobgoblin warlord': [187, '6', 2300, 'Medium', 'Humanoid'],
    'Invisible stalker': [192, '6', 2300, 'Medium', 'Elemental'],
    'Kuo-toa archpriest': [200, '6', 2300, 'Medium', 'Humanoid'],
    'Mage': [347, '6', 2300, 'Medium', 'Humanoid'],
    'Mammoth': [332, '6', 2300, 'Huge', 'Beast'],
    'Medusa': [214, '6', 2300, 'Medium', 'Monstrosity'],
    'Vrock': [64, '6', 2300, 'Large', 'Fiend'],
    'Wyvern': [303, '6', 2300, 'Large', 'Dragon'],
    'Young brass dragon': [105, '6', 2300, 'Large', 'Dragon'],
    'Young white dragon': [101, '6', 2300, 'Large', 'Dragon'],
    # CR7 is 2900XP
    'Blue slaad': [276, '7', 2900, 'Large', 'Aberration'],
    'Brood Monitor': ['MaD 44', '7', 2900, 'Huge', 'Aberration'],
    'Drow mage': [129, '7', 2900, 'Medium', 'Humanoid'],
    'Giant ape': [323, '7', 2900, 'Huge', 'Beast'],
    'Gnoll Deathmage': ['MaD 23', '7', 2900, 'Medium', 'Humanoid'],
    'Grick alpha': [173, '7', 2900, 'Large', 'Monstrosity'],
    'Mind flayer': [222, '7', 2900, 'Medium', 'Aberration'],
    'Night hag (coven)': [178, '7', 2900, 'Medium', 'Fey'],
    'Oni': [239, '7', 2900, 'Large', 'Giant'],
    'Shield guardian': [271, '7', 2900, 'Large', 'Construct'],
    'Stone giant': [156, '7', 2900, 'huge', 'Giant'],
    'Young black dragon': [88, '7', 2900, 'Large', 'Dragon'],
    'Young copper dragon': [111, '7', 2900, 'Large', 'Dragon'],
    'Yuan-ti abomination': [308, '7', 2900, 'Large', 'Monstrosity'],
    # CR8 is 3900XP
    'Assassin': [343, '8', 3900, 'Medium', 'Humanoid'],
    'Chain devil': [72, '8', 3900, 'Medium', 'Fiend'],
    'Cloaker': [41, '8', 3900, 'Large', 'Aberration'],
    'Drow priestess of Lolth': [129, '8', 3900, 'Medium', 'Humanoid'],
    'Fomorian': [136, '8', 3900, 'Huge', 'Giant'],
    'Frost giant': [155, '8', 3900, 'Huge', 'Giant'],
    'Githyanki knight': [160, '8', 3900, 'Medium', 'Humanoid'],
    'Green slaad': [277, '8', 3900, 'Large', 'Aberration'],
    'Hezrou': [60, '8', 3900, 'Large', 'Fiend'],
    'Hydra': [190, '8', 3900, 'Huge', 'Monstrosity'],
    'Master of the Five Spires': ['MaD 9', '8', 3900, 'Medium', 'Humanoid'],
    'Mind flayer arcanist': [222, '8', 3900, 'Medium', 'Aberration'],
    'Priest of Blight': ['MaD 8', '8', 3900, 'Medium', 'Humanoid'],
    'Selachian': ['MaD 4', '8', 3900, 'Large', 'Humanoid'],
    'Spirit naga': [234, '8', 3900, 'Large', 'Monstrosity'],
    'Tyrannosaurus rex': [80, '8', 3900, 'Huge', 'Beast'],
    'Young bronze dragon': [108, '8', 3900, 'Large', 'Dragon'],
    'Young green dragon': [94, '8', 3900, 'Large', 'Dragon'],
    # CR9 is 5000XP
    'Abominable yeti': [306, '9', 5000, 'Huge', 'Monstrosity'],
    'Bone devil': [71, '9', 5000, 'Large', 'Fiend'],
    'Bone Golem': ['MaD 14', '9', 5000, 'Large', 'Construct'],
    'Brood Butcher': ['MaD 45', '9', 5000, 'Huge', 'Aberration'],
    'Clay golem': [168, '9', 5000, 'Large', 'Construct'],
    'Cloud giant': [154, '9', 5000, 'Huge', 'Giant'],
    'Coven Horror': ['MaD 41', '9', 5000, 'Large', 'Monstrosity'],
    'Fire giant': [154, '9', 5000, 'Huge', 'Giant'],
    'Glabrezu': [58, '9', 5000, 'Large', 'Fiend'],
    'Gray slaad': [277, '9', 5000, 'Medium', 'Aberration'],
    'Nycaloth': [314, '9', 5000, 'Large', 'Fiend'],
    'Pact Devil': ['MaD 29', '9', 5000, 'Large', 'Fiend'],
    'Treant': [289, '9', 5000, 'Huge', 'Plant'],
    'Young blue dragon': [91, '9', 5000, 'Large', 'Dragon'],
    'Young silver dragon': [118, '9', 5000, 'Large', 'Dragon'],
    # CR10 is 5900XP
    'Aboleth': [13, '10', 5900, 'Large', 'Aberration'],
    'Death slaad': [278, '10', 5900, 'Medium', 'Aberration'],
    'Deva': [16, '10', 5900, 'Medium', 'Celestial'],
    'Dream Eater': ['MaD 40', '10', 5900, 'Large', 'Aberration'],
    'Fallen Angel': ['MaD 13', '10', 5900, 'Medium', 'Celestial'],
    'Grave Titan': ['MaD 1', '10', 5900, 'Huge', 'Undead'],
    'Guardian naga': [234, '10', 5900, 'Large', 'Monstrosity'],
    'Stone golem': [170, '10', 5900, 'Large', 'Construct'],
    'Tuskaloth': ['MaD 32', '10', 5900, 'Gargantuan', 'Beast'],
    'Yochlol': [65, '10', 5900, 'Medium', 'Fiend'],
    'Young gold dragon': [115, '10', 5900, 'Large', 'Dragon'],
    'Young red dragon': [98, '10', 5900, 'Large', 'Dragon'],
    # CR11 is 7200XP
    'Behir': [25, '11', 7200, 'Huge', 'Monstrosity'],
    'Dao': [143, '11', 7200, 'Large', 'Elemental'],
    'Djinni': [144, '11', 7200, 'Large', 'Elemental'],
    'Efreeti': [145, '11', 7200, 'Large', 'Elemental'],
    'Gynosphinx': [282, '11', 7200, 'Large', 'Monstrosity'],
    'Horned devil': [74, '11', 7200, 'Large', 'Fiend'],
    'Marid': [146, '11', 7200, 'Large', 'Elemental'],
    'Remorhaz': [258, '11', 7200, 'Huge', 'Monstrosity'],
    'Roc': [260, '11', 7200, 'gargantuan', 'Monstrosity'],
    # CR12 is 8400XP
    'Arcanaloth': [313, '12', 8400, 'Medium', 'Fiend'],
    'Archmage': [342, '12', 8400, 'Medium', 'Humanoid'],
    'Erinyes': [73, '12', 8400, 'Medium', 'Fiend'],
    'Kraken Hatchling': ['MaD 5', '12', 8400, 'Huge', 'Monstrosity'],
    # CR 13 is 10000XP
    'Adult brass dragon': [105, '13', 10000, 'Huge', 'Dragon'],
    'Adult white dragon': [101, '13', 10000, 'Huge', 'Dragon'],
    'Beholder': [28, '13', 10000, 'Large', 'Aberration'],
    'Nalfeshnee': [62, '13', 10000, 'Large', 'Fiend'],
    'Rakshasa': [257, '13', 10000, 'Medium', 'Fiend'],
    'Sliver Queen': ['MaD 19', '13', 10000, 'Huge', 'Monstrosity'],
    'Storm giant': [156, '13', 10000, 'Huge', 'Giant'],
    'Ultroloth': [314, '13', 10000, 'Medium', 'Fiend'],
    'Vampire': [297, '13', 10000, 'Medium', 'Undead'],
    'Young red shadow dragon': [85, '13', 10000, 'Large', 'Dragon'],
    # CR14 is 11500XP
    'Adult black dragon': [98, '14', 11500, 'Huge', 'Dragon'],
    'Adult copper dragon': [111, '14', 11500, 'Huge', 'Dragon'],
    'Beholder (lair)': [28, '14', 11500, 'Large', 'Aberration'],
    'Clockwork Dragon': ['MaD 33', '14', 11500, 'Huge', 'Construct'],
    'Death tyrant': [29, '14', 11500, 'Large', 'Undead'],
    'Ice devil': [75, '14', 11500, 'Large', 'Fiend'],
    # CR15 is 13000XP
    'Adult bronze dragon': [108, '15', 13000, 'Huge', 'Dragon'],
    'Adult green dragon': [94, '15', 13000, 'Huge', 'Dragon'],
    'Death tyrant (lair)': [29, '15', 13000, 'Large', 'Undead'],
    'Fusion Elemental': ['MaD 12', '15', 13000, 'Huge', 'Elemental'],
    'Mummy lord': [229, '15', 13000, 'Medium', 'Undead'],
    'Purple worm': [255, '15', 13000, 'Gargantuan', 'Monstrosity'],
    'Vampire (spellcaster)': [297, '15', 13000, 'Medium', 'Undead'],
    'Vampire (warrior)': [297, '15', 13000, 'Medium', 'Undead'],
    # CR16 is 15000
    'Adult blue dragon': [91, '16', 15000, 'Huge', 'Dragon'],
    'Adult silver dragon': [117, '16', 15000, 'Huge', 'Dragon'],
    'Ginormous Squirrel': ['MaD 54', '16', 15000, 'Gargantuan', 'Beast'],
    'Iron golem': [170, '16', 15000, 'Large', 'Construct'],
    'Marilith': [61, '16', 15000, 'Large', 'Fiend'],
    'Mummy lord (lair)': [229, '16', 15000, 'Medium', 'Undead'],
    'Planetar': [17, '16', 15000, 'Large', 'Celestial'],
    # CR17 is 18000XP
    'Adult blue dracolich': [84, '17', 18000, 'Huge', 'Undead'],
    'Adult gold dragon': [114, '17', 18000, 'Huge', 'Dragon'],
    'Adult red dragon': [98, '17', 18000, 'Huge', 'Dragon'],
    'Androsphinx': [281, '17', 18000, 'Large', 'Monstrosity'],
    'Death knight': [47, '17', 18000, 'Medium', 'Undead'],
    'Dragon turtle': [119, '17', 18000, 'Gargantuan', 'Dragon'],
    'Goristro': [59, '17', 18000, 'Huge', 'Fiend'],
    'Sire of Stagnation': ['MaD 46', '17', 18000, 'Gargantuan', 'Aberration'],
    # CR18 is 20000XP
    'Demilich': [48, '18', 20000, 'Tiny', 'Undead'],
    # CR19 is 22000XP
    'Balor': [55, '19', 22000, 'Huge', 'Fiend'],
    # CR20 is 25000XP
    'Ancient brass dragon': [104, '20', 25000, 'Gargantuan', 'Dragon'],
    'Ancient white dragon': [100, '20', 25000, 'Gargantuan', 'Dragon'],
    'Demilich (lair)': [48, '20', 25000, 'Tiny', 'Undead'],
    'Pit fiend': [77, '20', 25000, 'Large', 'Fiend'],
    # CR21 is 33000XP
    'Ancient black dragon': [87, '21', 33000, 'Gargantuan', 'Dragon'],
    'Ancient copper dragon': [110, '21', 33000, 'Gargantuan', 'Dragon'],
    'Lich': [202, '21', 33000, 'Medium', 'Undead'],
    'Solar': [18, '21', 33000, 'Large', 'Celestial'],
    # CR22 is 41000XP
    'Ancient bronze dragon': [107, '22', 41000, 'Gargantuan', 'Dragon'],
    'Ancient green dragon': [93, '22', 41000, 'Gargantuan', 'Dragon'],
    'Lich (lair)': [202, '22', 41000, 'Medium', 'Undead'],
    # CR23 is 50000XP
    'Ancient blue dragon': [90, '23', 50000, 'Gargantuan', 'Dragon'],
    'Ancient silver dragon': [116, '23', 50000, 'Gargantuan', 'Dragon'],
    'Empyrean': [130, '23', 50000, 'Huge', 'Celestial'],
    'Kraken': [197, '23', 50000, 'Gargantuan', 'Monstrosity'],
    # CR24 is 62000XP
    'Ancient gold dragon': [113, '24', 62000, 'Gargantuan', 'Dragon'],
    'Ancient red dragon': [97, '24', 62000, 'Gargantuan', 'Dragon'],
    # CR30 is 155000XP
    'Tarrasque': [286, '30', 155000, 'Gargantuan', 'Monstrosity'],
    'Ulamog': ['MaD 47', '30', 155000, 'Colossal', 'Aberration'],
    }
