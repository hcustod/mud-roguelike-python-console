import random
from explore_map import start_explore_map
import functions
from functions import load_game
from user import User
from partyGenerator.partyCreation import generate_party
from fightSystem import run_combat
from partyGenerator.models import Monster
from dreamLevels import run_dream_levels


def get_valid_input(prompt, valid_range, error_message):
    while True:
        user_input = input(prompt)
        if user_input.isdigit() and int(user_input) in valid_range:
            return int(user_input)
        else:
            print(error_message)


def main_game(current_user):

    
    small_dice_options = list(range(1, 7))
    big_dice_options = list(range(1, 21))

    weapons = ["Fist", "Knife", "Club", "Gun", "Bomb", "Nuclear Bomb"]
    loot_options = ["Health Potion", "Poison Potion", "Secret Note", "Leather Boots", "Flimsy Gloves"]
    monster_powers = { "Fire Magic": 2, "Freeze Time": 4, "Super Hearing": 6 }


    party = generate_party()
    first_hero = party[0]
    monster = Monster()
    belt = []

    monsters_killed = functions.load_game()

    print(f"Total monsters killed so far: {monsters_killed}\n")

    for _ in range(2):
        _, belt = functions.collect_loot(loot_options, belt)


    # Loot bag
    print("    ------------------------------------------------------------------")
    print("    |    !!You find a loot bag!! You look inside to find 2 items:")
    input("    |    Roll for first item (Press enter)")
    _, belt = functions.collect_loot(loot_options, belt)
    input("    |    Roll for second item (Press enter)")
    _, belt = functions.collect_loot(loot_options, belt)
    print("    |    You're super neat, so you organize your belt alphabetically:")
    belt.sort()
    current_user.update_stats("loot", belt[:])
    belt, first_hero.health_points = functions.use_loot(belt, first_hero.health_points)

    # Weapon roll
    print("    ------------------------------------------------------------------")
    print("    |", end="    ")
    input("Roll the dice for your weapon (Press enter)")
    ascii_image5 = """
              , %               .           
   *      @./  #         @  &.(         
  @        /@   (      ,    @       # @ 
  @        ..@#% @     @&*#@(         % 
   &   (  @    (   / /   *    @  .   /  
     @ % #         /   .       @ ( @    
                 %   .@*                
               #         .              
             /     # @   *              
                 ,     %                
            @&@           @&@        
    """
    print(ascii_image5)

    weapon_roll = random.choice(small_dice_options)
    weapon_name = weapons[weapon_roll - 1]

    # Only the first hero will get the weapon.
    first_hero.combat_strength = min(first_hero.combat_strength + weapon_roll, 6)
    print("    |    The hero's weapon is " + weapon_name)
    print("    |    Hero's combat strength is now", first_hero.combat_strength)

    # TODO; should we pick up the stats from first_hero instead?
    current_user.update_stats("weapon", weapon_name)

    # Analyze weapon roll
    input("    | Analyze the Weapon roll (Press enter)")
    print("    |", end="    ")
    if weapon_name == "Fist":
        print("    |    --- Oh no... you rolled the Fist.")

    first_hero.combat_strength, monster.combat_strength = functions.adjust_combat_strength(
        first_hero.combat_strength, monster.combat_strength
    )

    if weapon_name != "Fist":
        print("    |    --- Thank goodness you didn't roll the Fist...")
    if weapon_roll <= 2:
        print("    |    --- You rolled a weak weapon, friend")
    elif weapon_roll <= 4:
        print("    |    --- Your weapon is meh")
    else:
        print("    |    --- Nice weapon, friend!")

    # Monster magic roll
    print("    |", end="    ")
    input("Roll for Monster's Magic Power (Press enter)")
    print("""
                @%   @                      
         @     @                        
             &                          
      @      .                          

     @       @                    @     
              @                  @      
      @         @              @  @     
       @            ,@@@@@@@     @      
         @                     @        
            @               @           
                 @@@@@@@                
        """)
    power_roll = random.choice(list(monster_powers.keys()))
    monster.combat_strength += min(6, monster.combat_strength + monster_powers[power_roll])

    print("    |    The monster's combat strength is now " + str(
        monster.combat_strength) + " using the " + power_roll + " magic power")

    print("    ------------------------------------------------------------------")
    print("    |", end="    ")

    # Analyze monster vs character
    input("Analyze the roll (Press enter)")
    print("\n    |    You are matched in strength: " + str(monster.combat_strength == first_hero.combat_strength))
    print("    |    You have a strong first hero: " + str((first_hero.combat_strength + first_hero.health_points) >= 15))
    print("    |", end="    ")

    # Dream levels
    print("\n    ------------------------------------------------------------------")
    print("    |    Just before you engage in combat, a dreamy haze falls upon you...")
    num_dream_lvls = run_dream_levels(party, monster)
    if num_dream_lvls > 0:
        print("    |    You feel yourself spiraling into a dream within a dream...")
        _ = functions.inception_dream(num_dream_lvls)

    # Start combat
    winner, num_stars, monsters_killed = run_combat(party, monster, belt)

    # Removed how stars were saved from lab here due to conflicts w new save system.

    # Post combat updates
    current_user.update_stats("winner", winner)
    current_user.update_stats("stars", num_stars)

    functions.save_game_all(current_user, monsters_killed)
    

if __name__ == "__main__":

    print(r"""**************************************************************************************

     ____                             _   _                                     
    |  _ \ _ __ ___  __ _ _ __ ___   | | | | __ _ _ __ ___  _ __ ___   ___ _ __ 
    | | | | '__/ _ \/ _` | '_ ` _ \  | |_| |/ _` | '_ ` _ \| '_ ` _ \ / _ \ '__|
    | |_| | | |  __/ (_| | | | | | | |  _  | (_| | | | | | | | | | | |  __/ |   
    |____/|_|  \___|\__,_|_| |_| |_| |_| |_|\__,_|_| |_| |_|_| |_| |_|\___|_|      

**************************************************************************************""")

    print("\n1. Play Now!")
    print("2. Sign in")
    print("3. Create an account\n")
    menu_selection = str(input("Please select an option [1, 2, 3]: "))

    match menu_selection:
        case "1":
            current_user = User("Guest", "")

        case "2":
            current_user = functions.sign_in()

        case "3":
            current_user = functions.create_account()

    # Debug for current_user not being created
    if not current_user:
        print("Failed to create a user.")
        exit(1)

    while True:

        print("\n=== Main Menu ===")
        print("1. Start Battle")
        print("2. Explore Map")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            main_game(current_user)
        elif choice == "2":
            start_explore_map()
        elif choice == "3":
            print("Thanks for playing!")
            break
        else:
            print("Invalid choice. Try again.")
