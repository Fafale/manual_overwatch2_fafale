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
    locationNamesToRemove = [] # List of location names
    itemNamesToRemove = [] # List of item names

    MAX_HERO_KO_CHECKS = 6
    enable_hero_ko = is_option_enabled(multiworld, player, "enable_hero_elimination_checks")
    hero_ko_checks = get_option_value(multiworld, player, "hero_elimination_check_amount")

    MAX_HERO_MASTERY_CHECKS = 6
    include_mastery_mode = get_option_value(multiworld, player, "include_hero_masteries")
    enable_masteries = include_mastery_mode >= 1

    mastery_list = []
    if enable_masteries is True:
        mastery_check_amount = get_option_value(multiworld, player, "hero_mastery_check_amount")

        all_mastery_list = [
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

        available_mastery_list = []
        if len(get_option_value(multiworld, player, "available_hero_masteries")) > 0:
            available_mastery_list.extend(get_option_value(multiworld, player, "available_hero_masteries"))
        else:
            available_mastery_list.extend(all_mastery_list)
        
        num_included_masteries = min(get_option_value(multiworld, player, "hero_masteries_amount"), len(available_mastery_list))

        for _ in range(num_included_masteries):
            hero_name = random.choice(list(available_mastery_list))

            mastery_list.append(hero_name)

            available_mastery_list.remove(hero_name)
            all_mastery_list.remove(hero_name)

            for i in range(mastery_check_amount+1, MAX_HERO_MASTERY_CHECKS):
                locationNamesToRemove.append(f"Hero Mastery - {hero_name} - Recruit - Check {i}")
                locationNamesToRemove.append(f"Hero Mastery - {hero_name} - Agent - Check {i}")
                locationNamesToRemove.append(f"Hero Mastery - {hero_name} - Veteran - Check {i}")
        
        for hero_name in all_mastery_list:
            itemNamesToRemove.append(f"Hero Mastery - {hero_name}")
            itemNamesToRemove.append(f"Hero Mastery - {hero_name}")
            itemNamesToRemove.append(f"Hero Mastery - {hero_name}")
            for i in range(1, MAX_HERO_MASTERY_CHECKS):
                locationNamesToRemove.append(f"Hero Mastery - {hero_name} - Recruit - Check {i}")
                locationNamesToRemove.append(f"Hero Mastery - {hero_name} - Agent - Check {i}")
                locationNamesToRemove.append(f"Hero Mastery - {hero_name} - Veteran - Check {i}")
        
        progressive_masteries = (include_mastery_mode == 1)

        if progressive_masteries is False:
            for hero_name in mastery_list:
                itemNamesToRemove.append("Hero Mastery - " + hero_name)
                itemNamesToRemove.append("Hero Mastery - " + hero_name)


    include_tanks = is_option_enabled(multiworld, player, "include_tank_heroes")
    include_damages = is_option_enabled(multiworld, player, "include_damage_heroes")
    include_supports = is_option_enabled(multiworld, player, "include_support_heroes")


    #Handling Tank list
    tank_list = []
    if include_tanks is True:
        all_tank_list = [
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

        available_tank_list = []
        if len(get_option_value(multiworld, player, "available_tank_heroes")) > 0:
            available_tank_list.extend(get_option_value(multiworld, player, "available_tank_heroes"))
        else:
            available_tank_list.extend(all_tank_list)
        
        num_included_tanks = min(get_option_value(multiworld, player, "tank_heroes_amount"), len(available_tank_list))
        
        for _ in range(num_included_tanks):
            st_hero = random.choice(list(available_tank_list))
            tank_list.append(st_hero)
            available_tank_list.remove(st_hero)
            all_tank_list.remove(st_hero)

            if enable_hero_ko is True:
                for i in range(hero_ko_checks+1, MAX_HERO_KO_CHECKS):
                    locationNamesToRemove.append(f"{st_hero} - Get Eliminations ({i})")
        
        for hero in all_tank_list:
            item = next(i for i in item_pool if i.name == hero)
            item_pool.remove(item)

            if enable_hero_ko is True:
                locationNamesToRemove.append(f"{hero} - Get Eliminations (1)")
                locationNamesToRemove.append(f"{hero} - Get Eliminations (2)")
                locationNamesToRemove.append(f"{hero} - Get Eliminations (3)")
                locationNamesToRemove.append(f"{hero} - Get Eliminations (4)")
                locationNamesToRemove.append(f"{hero} - Get Eliminations (5)")    



    #Handling Damage list
    damage_list = []
    if include_damages is True:
        all_damage_list = [
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

        available_damage_list = []
        if len(get_option_value(multiworld, player, "available_damage_heroes")) > 0:
            available_damage_list.extend(get_option_value(multiworld, player, "available_damage_heroes"))
        else:
            available_damage_list.extend(all_damage_list)
        
        num_included_damages = min(get_option_value(multiworld, player, "damage_heroes_amount"), len(available_damage_list))
        
        for _ in range(num_included_damages):
            st_hero = random.choice(list(available_damage_list))
            damage_list.append(st_hero)
            available_damage_list.remove(st_hero)
            all_damage_list.remove(st_hero)
            
            if enable_hero_ko is True:
                for i in range(hero_ko_checks+1, MAX_HERO_KO_CHECKS):
                    locationNamesToRemove.append(f"{st_hero} - Get Eliminations ({i})")
                    
        for hero in all_damage_list:
            item = next(i for i in item_pool if i.name == hero)
            item_pool.remove(item)

            if enable_hero_ko is True:
                locationNamesToRemove.append(f"{hero} - Get Eliminations (1)")
                locationNamesToRemove.append(f"{hero} - Get Eliminations (2)")
                locationNamesToRemove.append(f"{hero} - Get Eliminations (3)")
                locationNamesToRemove.append(f"{hero} - Get Eliminations (4)")
                locationNamesToRemove.append(f"{hero} - Get Eliminations (5)")     
            
    
    #Handling Support list
    support_list = []
    if include_supports is True:
        all_support_list = [
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

        available_support_list = []
        if len(get_option_value(multiworld, player, "available_support_heroes")) > 0:
            available_support_list.extend(get_option_value(multiworld, player, "available_support_heroes"))
        else:
            available_support_list.extend(all_support_list)
        
        num_included_supports = min(get_option_value(multiworld, player, "support_heroes_amount"), len(available_support_list))
        
        for _ in range(num_included_supports):
            st_hero = random.choice(list(available_support_list))
            support_list.append(st_hero)
            available_support_list.remove(st_hero)
            all_support_list.remove(st_hero)

            if enable_hero_ko is True:
                for i in range(hero_ko_checks+1, MAX_HERO_KO_CHECKS):
                    locationNamesToRemove.append(f"{st_hero} - Get Eliminations ({i})")
        
        for hero in all_support_list:
            item = next(i for i in item_pool if i.name == hero)
            item_pool.remove(item)

            if enable_hero_ko is True:
                locationNamesToRemove.append(f"{hero} - Get Eliminations (1)")
                locationNamesToRemove.append(f"{hero} - Get Eliminations (2)")
                locationNamesToRemove.append(f"{hero} - Get Eliminations (3)")
                locationNamesToRemove.append(f"{hero} - Get Eliminations (4)")
                locationNamesToRemove.append(f"{hero} - Get Eliminations (5)")   

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

    MAX_DEATHMATCH_CHECKS = 6
    include_deathmatch = get_option_value(multiworld, player, "include_deathmatch_checks")

    if include_deathmatch > 0:
        deathmatch_check_amount = get_option_value(multiworld, player, "deathmatch_check_amount")

        include_solo_deathmatch = ((include_deathmatch == 1) or (include_deathmatch == 3))
        include_team_deathmatch = ((include_deathmatch == 2) or (include_deathmatch == 3))

        if include_solo_deathmatch:
            for i in range(deathmatch_check_amount+1, MAX_DEATHMATCH_CHECKS):
                    locationNamesToRemove.append(f"Solo Deathmatch - Check {i}")
        else:
            for i in range(1, MAX_DEATHMATCH_CHECKS):
                locationNamesToRemove.append(f"Solo Deathmatch - Check {i}")
        
        if include_team_deathmatch:
            for i in range(deathmatch_check_amount+1, MAX_DEATHMATCH_CHECKS):
                    locationNamesToRemove.append(f"Team Deathmatch - Check {i}")
        else:
            for i in range(1, MAX_DEATHMATCH_CHECKS):
                locationNamesToRemove.append(f"Team Deathmatch - Check {i}")

    

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
    debug = False
    if debug:
        print("Removing items from pool:")
    for itemName in itemNamesToRemove:
        if debug:
            print(itemName)
        item = next(i for i in item_pool if i.name == itemName)
        item_pool.remove(item)
    
    for region in multiworld.regions:
        if region.player == player:
            for location in list(region.locations):
                if location.name in locationNamesToRemove:
                    region.locations.remove(location)
    if hasattr(multiworld, "clear_location_cache"):
        multiworld.clear_location_cache()

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
