# Object classes from AP that represent different types of options that you can create
from Options import FreeText, NumericOption, Toggle, DefaultOnToggle, Choice, TextChoice, Range, OptionSet, NamedRange, Visibility

# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_option_enabled, get_option_value


TANK_HERO_LIST = [
    "DVa",
    "Doomfist",
    "Hazard",
    "Junker Queen",
    "Mauga",
    "Orisa",
    "Ramattra",
    "Reinhardt",
    "Roadhog",
    "Sigma",
    "Winston",
    "Wrecking Ball",
    "Zarya"
]
TANK_HERO_AMOUNT = len(TANK_HERO_LIST)

DAMAGE_HERO_LIST = [
    "Ashe",
    "Bastion",
    "Cassidy",
    "Echo",
    "Freja",
    "Genji",
    "Hanzo",
    "Junkrat",
    "Mei",
    "Pharah",
    "Reaper",
    "Sojourn",
    "Soldier 76",
    "Sombra",
    "Symmetra",
    "Torbjorn",
    "Tracer",
    "Venture",
    "Widowmaker"
]
DAMAGE_HERO_AMOUNT = len(DAMAGE_HERO_LIST)

SUPPORT_HERO_LIST = [
    "Ana",
    "Baptiste",
    "Brigitte",
    "Illari",
    "Juno",
    "Kiriko",
    "Lifeweaver",
    "Lucio",
    "Mercy",
    "Moira",
    "Zenyatta"
]
SUPPORT_HERO_AMOUNT = len(SUPPORT_HERO_LIST)

HERO_MASTERY_LIST = [
    "Mercy",
    "Reinhardt",
    "Tracer",
    "Sojourn",
    "Winston",
    "DVa",
    "Echo",
    "Genji",
    "Lucio",
    "Mei",
    "Soldier 76",
    "Kiriko",
    "Cassidy",
    "Brigitte"
]
HERO_MASTERY_AMOUNT = len(HERO_MASTERY_LIST)

####################################################################
# NOTE: At the time that options are created, Manual has no concept of the multiworld or its own world.
#       Options are defined before the world is even created.
#
# Example of creating your own option:
#
#   class MakeThePlayerOP(Toggle):
#       """Should the player be overpowered? Probably not, but you can choose for this to do... something!"""
#       display_name = "Make me OP"
#
#   options["make_op"] = MakeThePlayerOP
#
#
# Then, to see if the option is set, you can call is_option_enabled or get_option_value.
#####################################################################


# To add an option, use the before_options_defined hook below and something like this:
#   options["total_characters_to_win_with"] = TotalCharactersToWinWith
#

class RequiredMedalPercentage(Range):
    """
    Percentage of Medals to win the game.
    """
    display_name = "Percentage Medals"
    range_start = 50
    range_end = 100
    default = 70

class EnableHeroEliminationChecks(DefaultOnToggle):
    """
    Enable whether getting Eliminations with specific heroes are included in the randomizer.
    """
    display_name = "Enable Hero Elimination Checks"

class HeroEliminationCheckAmount(Range):
    """
    Can be ignored if enable_hero_elimination_checks is false

    Choose how many "Get X Eliminations" checks each hero has.
    """
    display_name = "Hero Elimination Check Amount"
    range_start = 1
    range_end = 5
    default = 3

class StartingHeroNumber(Range):
    """
    Number of Heroes to start the multiworld with.
    """
    display_name = "Starting Hero Number"
    range_start = 1
    range_end = 42
    default = 3

class IncludeTankHeroes(DefaultOnToggle):
    """
    Whether Tank heroes are included in the randomizer.
    """
    display_name = "Include Tank Heroes"
    
class TankHeroesAmount(Range):
    """
    Can be ignored if include_tank_heroes is false.

    Total amount of Tank heroes that can appear in the item pool.
    """
    display_name = "Tank Heroes Amount"
    range_start = 1
    range_end = TANK_HERO_AMOUNT
    default = TANK_HERO_AMOUNT

class AvailableTankHeroes(OptionSet):
    """
    Can be ignored if include_tank_heroes is false.
    
    List of available heroes that can appear in the item pool.
    To avoid errors, emptying this list will work the same as if it's complete.

    Attention: "D.Va" = "DVa"
    """
    display_name = "Available Tank Heroes"
    valid_keys = [hero_name for hero_name in TANK_HERO_LIST]
    default = sorted(set([hero_name for hero_name in TANK_HERO_LIST]))

class IncludeDamageHeroes(DefaultOnToggle):
    """
    Whether Damage heroes are included in the randomizer.
    """
    display_name = "Include Damage Heroes"

class DamageHeroesAmount(Range):
    """
    Can be ignored if include_damage_heroes is false.

    Total amount of Damage heroes that can appear in the item pool.
    """
    display_name = "Damage Heroes Amount"
    range_start = 1
    range_end = DAMAGE_HERO_AMOUNT
    default = DAMAGE_HERO_AMOUNT

class AvailableDamageHeroes(OptionSet):
    """
    Can be ignored if include_damage_heroes is false.
    
    List of available heroes that can appear in the item pool.
    To avoid errors, emptying this list will work the same as if it's complete.

    Attention: "Torbjörn" = "Torbjorn", "Soldier: 76" = "Soldier 76"
    """
    display_name = "Available Damage Heroes"
    valid_keys = [hero_name for hero_name in DAMAGE_HERO_LIST]
    default = sorted(set([hero_name for hero_name in DAMAGE_HERO_LIST]))

class IncludeSupportHeroes(DefaultOnToggle):
    """
    Whether Support heroes are included in the randomizer.
    """
    display_name = "Include Support Heroes"

class SupportHeroesAmount(Range):
    """
    Can be ignored if include_support_heroes is false.

    Total amount of Support heroes that can appear in the item pool.
    """
    display_name = "Support Heroes Amount"
    range_start = 1
    range_end = SUPPORT_HERO_AMOUNT
    default = SUPPORT_HERO_AMOUNT

class AvailableSupportHeroes(OptionSet):
    """
    Can be ignored if include_support_heroes is false.
    
    List of available heroes that can appear in the item pool.
    To avoid errors, emptying this list will work the same as if it's complete.

    Attention: "Lúcio" = "Lucio"
    """
    display_name = "Available Support Heroes"
    valid_keys = [hero_name for hero_name in SUPPORT_HERO_LIST]
    default = sorted(set([hero_name for hero_name in SUPPORT_HERO_LIST]))

class IncludeHeroMasteries(Choice):
    """
    Choose how Hero Masteries are included in the randomizer.

    Disabled: Hero Masteries aren't included in the randomizer.
    Progressive: 3 Mastery items per hero, each one unlocks a course (Recruit -> Agent -> Veteran).
    Complete: Only 1 Mastery item per hero, which unlocks all 3 courses for that hero.
    """
    display_name = "Include Hero Masteries"
    option_disabled = 0
    option_progressive = 1
    option_complete = 2
    default = 0

class HeroMasteriesAmount(Range):
    """
    Can be ignored if include_hero_masteries is disabled.


    Total amount of Hero Masteries that can appear in the item pool.
    """
    display_name = "Hero Masteries Amount"
    range_start = 1
    range_end = HERO_MASTERY_AMOUNT
    default = HERO_MASTERY_AMOUNT

class AvailableHeroMasteries(OptionSet):
    """
    Can be ignored if include_hero_masteries is disabled.

    
    List of available heroes that can appear in the item pool.
    To avoid errors, emptying this list will work the same as if it's complete.

    Attention: "D.Va" = "DVa", "Soldier: 76" = "Soldier 76", "Lúcio" = "Lucio"
    """
    display_name = "Available Hero Masteries"
    valid_keys = [hero_name for hero_name in HERO_MASTERY_LIST]
    default = sorted(set([hero_name for hero_name in HERO_MASTERY_LIST]))

class HeroMasteryCheckAmount(Range):
    """
    Can be ignored if include_hero_masteries is disabled.

    Number of locations on each course from each included Hero Mastery.
    For example, if check amount is 5, each included Hero Mastery will have 15 checks in total.
    """
    display_name = "Hero Mastery Check Amount"
    range_start = 1
    range_end = 5
    default = 3

class IncludeDeathmatchChecks(Choice):
    """
    Choose how the Deathmatch gamemodes are included in the randomizer.

    Disabled: Deathmatch gamemodes aren't included in the randomizer.
    Solo Only: Only the Solo Deathmatch is included in the randomizer.
    Team Only: Only the Team Deathmatch is included in the randomizer.
    Both: Both Solo and Team Deathmatch are included in the randomizer.
    """
    display_name = "Include Deathmatch Checks"
    option_disabled = 0
    option_solo_only = 1
    option_team_only = 2
    option_both = 3
    default = 0

class DeathmatchCheckAmount(Range):
    """
    Can be ignored if include_deathmatch_checks is disabled.

    Number of locations on each included Deathmatch gamemode.
    """
    display_name = "Deathmatch Check Amount"
    range_start = 1
    range_end = 5
    default = 3

# This is called before any manual options are defined, in case you want to define your own with a clean slate or let Manual define over them
def before_options_defined(options: dict) -> dict:
    options["required_medal_percentage"] = RequiredMedalPercentage

    options["starting_hero_number"]     = StartingHeroNumber

    options["include_tank_heroes"]      = IncludeTankHeroes     #Toggle
    options["available_tank_heroes"]    = AvailableTankHeroes   #OptionSet
    options["tank_heroes_amount"]       = TankHeroesAmount      #Range

    options["include_damage_heroes"]    = IncludeDamageHeroes   #Toggle
    options["available_damage_heroes"]  = AvailableDamageHeroes #OptionSet
    options["damage_heroes_amount"]     = DamageHeroesAmount    #Range

    options["include_support_heroes"]   = IncludeSupportHeroes  #Toggle
    options["available_support_heroes"] = AvailableSupportHeroes#OptionSet
    options["support_heroes_amount"]    = SupportHeroesAmount   #Range

    options["enable_hero_elimination_checks"]   = EnableHeroEliminationChecks   #Toggle
    options["hero_elimination_check_amount"]    = HeroEliminationCheckAmount    #Range

    options["include_hero_masteries"]       = IncludeHeroMasteries      #Choice
    options["available_hero_masteries"]     = AvailableHeroMasteries    #OptionSet
    options["hero_masteries_amount"]        = HeroMasteriesAmount       #Range
    options["hero_mastery_check_amount"]    = HeroMasteryCheckAmount    #Range
    
    options["include_deathmatch_checks"] = IncludeDeathmatchChecks  #Choice
    options["deathmatch_check_amount"]   = DeathmatchCheckAmount    #Range
    return options

# This is called after any manual options are defined, in case you want to see what options are defined or want to modify the defined options
def after_options_defined(options: dict) -> dict:
    options["goal"].visibility = Visibility.spoiler #spoiler
    return options