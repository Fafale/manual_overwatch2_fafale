<h1>Manual Overwatch 2 for Archipelago</h1>

A really basic Overwatch implementation for Archipelago. It works just like [League of Legends AP](https://github.com/gaithernOrg/LoLAP) and similars.

It's a _Mcguffin game_[^1], so generation can sometimes fail if you disable too many locations AND using [Universal Tracker](https://github.com/FarisTheAncient/Archipelago/releases) is **extremely** recommended to avoid breaking the already simplistic logic.

<h2>Important Points</h2>

- It's advised to only play Unranked matches while doing this randomizer if you intend to lock yourself out of certain heroes. However, you can still play matches normally (using locked heroes) if you use the post-game hero-specific stats screen to only consider info about unlocked heroes. 

- I'd appreciate if anyone has some ideas for logic improvements or more checks/items to receive as well. It's hard to think of anything since you can't choose to specifically play an "Escort" match, for instance, so you end up abandoned to RNG.

- It's important to notice that some checks/locations are _kinda_ generic/repetitive, such as `Solo Deathmatch - Check 1` up to `Solo Deathmatch - Check 5`, so you could define them as either "win a different match" or "kill X enemies in a single match", whichever suits you better.

<h2>Items and Locations</h2>

Items you can receive:

- Access to all 42 Heroes, or only some roles (individual heroes can be toggled on/off)
- Access to all 14 Hero Masteries, if enabled (individual Masteries can be toggled on/off)
- Access to Deathmatch gamemodes, if enabled

Locations you can send:

- Win each gamemode as each enabled role (6 checks currently forced enabled for all included roles)
- Eliminate X enemies with each unlocked character, if enabled (up to 5 checks per Hero)
- Complete each course from Hero Mastery mode, if enabled (up to 5 checks per course, 15 per Hero)
- Win Solo/Team Deathmatch matches, if enabled (up to 5 checks each)

<h2>Yaml Options</h2>
There's a fair number of yaml options, so here they are organized into groups:

<h3>Mcguffin Goal Setting</h3>

- `required_medal_percentage` - Define the percentage of Mcguffin items needed to goal.

<h3>Hero Inclusion Settings</h3>

- `starting_hero_number` - Define the number of unlocked heroes to start with.
- For each role, there are 3 repeated options:
  - `include_ROLE_heroes` - If this role's items and locations are added at all.
  - `available_ROLE_heroes` - Change this list to exclude some heroes with this role from appearing.
  - `ROLE_heroes_amount` - Number of heroes with this role to enter the item pool, chosen from the above list.

<h3>Hero Eliminations</h3>

- `enable_hero_elimination_checks` - Enable checks for eliminating enemies for ALL included heroes.
- `hero_elimination_check_amount` - How many checks each hero has.

For this one, you could either define "send all checks once reaching X eliminations" or "send a check for each X enemies eliminated", since all checks are in logic once you unlock the hero to play with.

<h3>Hero Masteries</h3>

- `include_hero_masteries` - Enable checks for completing Hero Mastery courses.
- `available_hero_masteries` - Change this list to exclude some heroes from appearing.
- `hero_masteries_amount` - Number of heroes with this role to enter the item pool, chosen from the above list.
- `hero_mastery_check_amount` - How many checks each course has. (Keep in mind each hero has 3 courses)

Please keep in mind that heroes you unlock to play are **different items** from heroes you unlock to do their Hero Mastery courses. So receiving a `DVa` **doesn't** mean you're logically able to do her Hero Mastery, but receiving a `Hero Mastery - DVa` does, and vice versa.

<h3>Deathmatch Checks</h3>

- `include_deathmatch_checks` - Enable checks for Solo and/or Team Deathmatch modes.
- `deathmatch_check_amount` - How many checks each gamemode has.


[^1]: Archipelago games where you need to receive a certain quantity of an item to goal them.
