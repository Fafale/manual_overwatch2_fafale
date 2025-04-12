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

class DebugMedalAmount(Range):
    display_name = "DEBUG Medal Amount"
    range_start = 1
    range_end = 500
    default = 30

class RequiredMedalPercentage(Range):
    """
    Percentage of Medals to win the game.
    """
    display_name = "Percentage Medals"
    range_start = 50
    range_end = 100
    default = 70

class EnableHeroMasteries(Toggle):
    """
    Enable whether Hero Masteries are included in the randomizer.
    """
    display_name = "Enable Hero Masteries"

class EnableHeroKO(Toggle):
    """
    Enable whether specific Hero KO are included in the randomizer.
    """
    display_name = "Enable Hero KO"

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

    Attention: D.Va = DVa
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

    Attention: Torbjörn = Torbjorn, Soldier: 76 = Soldier 76
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

    Attention: Lúcio = Lucio
    """
    display_name = "Available Support Heroes"
    valid_keys = [hero_name for hero_name in SUPPORT_HERO_LIST]
    default = sorted(set([hero_name for hero_name in SUPPORT_HERO_LIST]))



# This is called before any manual options are defined, in case you want to define your own with a clean slate or let Manual define over them
def before_options_defined(options: dict) -> dict:
    options["debug_medal_amount"]        = DebugMedalAmount
    options["required_medal_percentage"] = RequiredMedalPercentage

    #options["enable_hero_masteries"]    = EnableHeroMasteries
    options["enable_hero_ko"]           = EnableHeroKO

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

    
    return options

# This is called after any manual options are defined, in case you want to see what options are defined or want to modify the defined options
def after_options_defined(options: dict) -> dict:
    options["goal"].visibility = Visibility.spoiler #spoiler
    return options