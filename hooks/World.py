# Object classes from AP core, to represent an entire MultiWorld and this individual World that's part of it
import random
from worlds.AutoWorld import World
from BaseClasses import MultiWorld, CollectionState

# Object classes from Manual -- extending AP core -- representing items and locations that are used in generation
from ..Items import ManualItem
from ..Locations import ManualLocation

# Raw JSON data from the Manual apworld, respectively:
#          data/game.json, data/items.json, data/locations.json, data/regions.json
#
from ..Data import game_table, item_table, location_table, region_table

# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_option_enabled, get_option_value

# calling logging.info("message") anywhere below in this file will output the message to both console and log file
import logging

########################################################################################
## Order of method calls when the world generates:
##    1. create_regions - Creates regions and locations
##    2. create_items - Creates the item pool
##    3. set_rules - Creates rules for accessing regions and locations
##    4. generate_basic - Runs any post item pool options, like place item/category
##    5. pre_fill - Creates the victory location
##
## The create_item method is used by plando and start_inventory settings to create an item from an item name.
## The fill_slot_data method will be used to send data to the Manual client for later use, like deathlink.
########################################################################################



# Use this function to change the valid filler items to be created to replace item links or starting items.
# Default value is the `filler_item_name` from game.json
def hook_get_filler_item_name(world: World, multiworld: MultiWorld, player: int) -> str | bool:
    return False

# Called before regions and locations are created. Not clear why you'd want this, but it's here. Victory location is included, but Victory event is not placed yet.
def before_create_regions(world: World, multiworld: MultiWorld, player: int):
    max_medals = get_option_value(multiworld, player, "debug_medal_amount")
    multiplier = get_option_value(multiworld, player, "required_medal_percentage")
    medals = round(max_medals * multiplier / 100)
    if medals == 0:
        medals = 1
    if medals == 1:
        goal_index = world.victory_names.index(f"Goal (Gather 1 Medal)")
    else:
        goal_index = world.victory_names.index(f"Goal (Gather {medals} Medals)")

    # Set goal location
    world.options.goal.value = goal_index

# Called after regions and locations are created, in case you want to see or modify that information. Victory location is included.
def after_create_regions(world: World, multiworld: MultiWorld, player: int):
    # Use this hook to remove locations from the world
    locationNamesToRemove = [] # List of location names

    # Add your code here to calculate which locations to remove

    for region in multiworld.regions:
        if region.player == player:
            for location in list(region.locations):
                if location.name in locationNamesToRemove:
                    region.locations.remove(location)
    if hasattr(multiworld, "clear_location_cache"):
        multiworld.clear_location_cache()

# The item pool before starting items are processed, in case you want to see the raw item pool at that stage
def before_create_items_starting(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    itemNamesToRemove = [] # List of item names

    include_tanks = is_option_enabled(multiworld, player, "include_tank_heroes")
    include_damages = is_option_enabled(multiworld, player, "include_damage_heroes")
    include_supports = is_option_enabled(multiworld, player, "include_support_heroes")

    tank_list = []
    if include_tanks is True:
        if len(get_option_value(multiworld, player, "available_tank_heroes")) > 0:
            tank_list.extend(get_option_value(multiworld, player, "available_tank_heroes"))
        else:
            tank_list.extend([
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
            ])
        
        num_included_tanks = get_option_value(multiworld, player, "tank_heroes_amount")
        num_excluded_tanks = len(tank_list) if len(tank_list) < num_included_tanks else len(tank_list) - num_included_tanks
        for _ in range(num_excluded_tanks):
            st_hero = random.choice(list(tank_list))
            item = next(i for i in item_pool if i.name == st_hero)
            item_pool.remove(item)
            tank_list.remove(st_hero)

    damage_list = []
    if include_damages is True:
        if len(get_option_value(multiworld, player, "available_damage_heroes")) > 0:
            damage_list.extend(get_option_value(multiworld, player, "available_damage_heroes"))
        else:
            damage_list.extend([
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
            ])

        num_included_damages = get_option_value(multiworld, player, "damage_heroes_amount")
        num_excluded_damages = len(damage_list) if len(damage_list) < num_included_damages else len(damage_list) - num_included_damages
        for _ in range(num_excluded_damages):
            st_hero = random.choice(list(damage_list))
            item = next(i for i in item_pool if i.name == st_hero)
            item_pool.remove(item)
            damage_list.remove(st_hero)
            
    
    support_list = []
    if include_supports is True:
        if len(get_option_value(multiworld, player, "available_support_heroes")) > 0:
            support_list.extend(get_option_value(multiworld, player, "available_support_heroes"))
        else:
            support_list.extend([
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
            ])
        
        num_included_supports = get_option_value(multiworld, player, "support_heroes_amount")
        num_excluded_supports = len(support_list) if len(support_list) < num_included_supports else len(support_list) - num_included_supports
        for _ in range(num_excluded_supports):
            st_hero = random.choice(list(support_list))
            item = next(i for i in item_pool if i.name == st_hero)
            item_pool.remove(item)
            support_list.remove(st_hero)

    num_starting_heroes = get_option_value(multiworld, player, "starting_hero_number")    
    
    hero_list = []
    hero_list.extend(tank_list)
    hero_list.extend(damage_list)
    hero_list.extend(support_list)
    
    for _ in range(min(num_starting_heroes, len(hero_list))):
        st_hero = random.choice(list(hero_list))
        item = next(i for i in item_pool if i.name == st_hero)
        item_pool.remove(item)
        multiworld.push_precollected(item)
        hero_list.remove(st_hero)

    max_medals = get_option_value(multiworld, player, "debug_medal_amount")
    multiplier = get_option_value(multiworld, player, "required_medal_percentage")
    medals = round(max_medals * multiplier / 100)
    if medals == 0:
        medals = 1
    
    bad_medals = 500 - max_medals
    for _ in range(bad_medals):
        itemNamesToRemove.append("Medal")
    
    # Get the victory item out of the pool:
    victory_item = next(i for i in item_pool if i.name == "Ultimate Medal (Victory)")
    item_pool.remove(victory_item)

    gather_loc_list = []
    if not hasattr(world.multiworld, "generation_is_fake"):
        # Get the victory location and place the victory item there
        gather_loc_list = ["Gather 1 Medal"] # A list of all the victory location names in order
        for i in range(2, 501):
            gather_loc_list.append(f"Gather {i} Medals")
        
        for i in range(len(gather_loc_list)):
            if str(medals) in gather_loc_list[i]:
                victory_id = i
                break

        gather_location_name = gather_loc_list[victory_id]
        gather_location = next(l for l in multiworld.get_unfilled_locations(player=player) if l.name == gather_location_name)
        gather_location.place_locked_item(victory_item)
    
    # Remove the extra gather locations
    for region in multiworld.regions:
        if region.player == player:
            for location in list(region.locations):
                if location.name in gather_loc_list and location.name != gather_location_name:
                    region.locations.remove(location)
                    pass
    
    # Remove items from the pool
    debug = True
    if debug:
        print("Removing items from pool:")
    for itemName in itemNamesToRemove:
        if debug:
            print(itemName)
        item = next(i for i in item_pool if i.name == itemName)
        item_pool.remove(item)
    
    return item_pool

# The item pool after starting items are processed but before filler is added, in case you want to see the raw item pool at that stage
def before_create_items_filler(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    # Use this hook to remove items from the item pool
    itemNamesToRemove = [] # List of item names

    # Add your code here to calculate which items to remove.
    #
    # Because multiple copies of an item can exist, you need to add an item name
    # to the list multiple times if you want to remove multiple copies of it.

    for itemName in itemNamesToRemove:
        item = next(i for i in item_pool if i.name == itemName)
        item_pool.remove(item)

    return item_pool

    # Some other useful hook options:

    ## Place an item at a specific location
    # location = next(l for l in multiworld.get_unfilled_locations(player=player) if l.name == "Location Name")
    # item_to_place = next(i for i in item_pool if i.name == "Item Name")
    # location.place_locked_item(item_to_place)
    # item_pool.remove(item_to_place)

# The complete item pool prior to being set for generation is provided here, in case you want to make changes to it
def after_create_items(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    return item_pool

# Called before rules for accessing regions and locations are created. Not clear why you'd want this, but it's here.
def before_set_rules(world: World, multiworld: MultiWorld, player: int):
    pass

# Called after rules for accessing regions and locations are created, in case you want to see or modify that information.
def after_set_rules(world: World, multiworld: MultiWorld, player: int):
    # Use this hook to modify the access rules for a given location

    def Example_Rule(state: CollectionState) -> bool:
        # Calculated rules take a CollectionState object and return a boolean
        # True if the player can access the location
        # CollectionState is defined in BaseClasses
        return True

    ## Common functions:
    # location = world.get_location(location_name, player)
    # location.access_rule = Example_Rule

    ## Combine rules:
    # old_rule = location.access_rule
    # location.access_rule = lambda state: old_rule(state) and Example_Rule(state)
    # OR
    # location.access_rule = lambda state: old_rule(state) or Example_Rule(state)

# The item name to create is provided before the item is created, in case you want to make changes to it
def before_create_item(item_name: str, world: World, multiworld: MultiWorld, player: int) -> str:
    return item_name

# The item that was created is provided after creation, in case you want to modify the item
def after_create_item(item: ManualItem, world: World, multiworld: MultiWorld, player: int) -> ManualItem:
    return item

# This method is run towards the end of pre-generation, before the place_item options have been handled and before AP generation occurs
def before_generate_basic(world: World, multiworld: MultiWorld, player: int) -> list:
    pass

# This method is run at the very end of pre-generation, once the place_item options have been handled and before AP generation occurs
def after_generate_basic(world: World, multiworld: MultiWorld, player: int):
    pass

# This is called before slot data is set and provides an empty dict ({}), in case you want to modify it before Manual does
def before_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    return slot_data

# This is called after slot data is set and provides the slot data at the time, in case you want to check and modify it after Manual is done with it
def after_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    return slot_data

# This is called right at the end, in case you want to write stuff to the spoiler log
def before_write_spoiler(world: World, multiworld: MultiWorld, spoiler_handle) -> None:
    pass

# This is called when you want to add information to the hint text
def before_extend_hint_information(hint_data: dict[int, dict[int, str]], world: World, multiworld: MultiWorld, player: int) -> None:
    
    ### Example way to use this hook: 
    # if player not in hint_data:
    #     hint_data.update({player: {}})
    # for location in multiworld.get_locations(player):
    #     if not location.address:
    #         continue
    #
    #     use this section to calculate the hint string
    #
    #     hint_data[player][location.address] = hint_string
    
    pass

def after_extend_hint_information(hint_data: dict[int, dict[int, str]], world: World, multiworld: MultiWorld, player: int) -> None:
    pass
