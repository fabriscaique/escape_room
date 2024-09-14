import time
import sys
import random

def slow_print(text, delay=0.01, color_code=""):
    if color_code:
        text = color_code + text + "\033[0m"  # Apply color and reset to default
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# Define rooms and items

couch = {
    "name": "couch",
    "type": "furniture",
}

door_a = {
    "name": "door a",
    "type": "door",
}

door_d = {
    "name": "door d",
    "type": "door",
}

key_a = {
    "name": "key for door a",
    "type": "key",
    "target": door_a,
}

piano = {
    "name": "piano",
    "type": "furniture",
}

game_room = {
    "name": "game room",
    "type": "room",
}

outside = {
  "name": "outside"
}

queen_bed = {
    "name": "queen bed",
    "type": "furniture",
}

door_b = {
    "name": "door b",
    "type": "door",
}

key_b = {
    "name": "key for door b",
    "type": "key",
    "target": door_b,
}

door_c = {
    "name": "door c",
    "type": "door",
}

bedroom_1 = {
    "name": "bedroom 1",
    "type": "room",
}

double_bed = {
    "name": "double bed",
    "type": "furniture",
}

dresser = {
    "name": "dresser",
    "type": "furniture",
}

key_c = {
    "name": "key for door c",
    "type": "key",
    "target": door_c,
}

key_d = {
    "name": "key for door d",
    "type": "key",
    "target": door_d,
}

bedroom_2 = {
    "name": "bedroom 2",
    "type": "room",
}

dining_table = {
    "name": "dining table",
    "type": "furniture"
}

living_room = {
    "name": "living room",
    "type": "room",
}

all_rooms = [game_room, bedroom_1, bedroom_2, living_room, outside]

all_doors = [door_a, door_b, door_c, door_d]

# Define which items/rooms are related

object_relations = {
    "game room": [couch, piano, door_a],
    "piano": [key_a],
    "outside": [door_a],
    "door a": [game_room, bedroom_1],
    "bedroom 1": [queen_bed, door_a, door_b, door_c],
    "door b": [bedroom_1, bedroom_2],
    "door c": [bedroom_1, living_room],
    "queen bed": [key_b],
    "bedroom 2": [double_bed, dresser, door_b],
    "double bed": [key_c],
    "dresser": [key_d],
    "living room": [dining_table, door_c, door_d],
    "door d": [living_room, outside],
}

# Define game state. Do not directly change this dict.
# Instead, when a new game starts, make a copy of this
# dict and use the copy to store gameplay state. This
# way you can replay the game multiple times.

INIT_GAME_STATE = {
    "current_room": game_room,
    "keys_collected": [],
    "target_room": outside
}

def linebreak():
    """
    Print a line break
    """
    slow_print("\n\n")

def start_game():
    """
    Start the game
    """
    slow_print("You wake up on a couch and find yourself in a strange house with no windows which you have never been to before. You don't remember why you are here and what had happened before. You feel some unknown danger is approaching and you must get out of the house, NOW!")
    play_room(game_state["current_room"])

def play_room(room):
    """
    Play a room. First check if the room being played is the target room.
    If it is, the game will end with success. Otherwise, let player either
    explore (list all items in this room) or examine an item found here.
    """
    game_state["current_room"] = room
    if game_state["current_room"] == game_state["target_room"]:
        slow_print("Congrats! You escaped the room!")
    else:
        print()
        slow_print("You are now in " + room["name"])
        try:
            intended_action = int(input("Press [1] to explore the room\nPress [2] to examine something\n"))
            if intended_action == 1:
                explore_room(room)
                play_room(room)
            elif intended_action == 2:
                examine_item(input("What would you like to examine?\n").strip())
            else:
                slow_print("Please, use your numerical keyboard.")
                play_room(room)
            linebreak()
        except ValueError:
            slow_print("Please, use your numerical keyboard.")
            play_room(room)

def explore_room(room):
    """
    Explore a room. List all items belonging to this room.
    """
    items = [i["name"] for i in object_relations[room["name"]]]
    print()
    slow_print("You explore the room. This is " + room["name"] + ". You find " + ", ".join(items))

def get_next_room_of_door(door, current_room):
    """
    From object_relations, find the two rooms connected to the given door.
    Return the room that is not the current_room.
    """
    connected_rooms = object_relations[door["name"]]
    for room in connected_rooms:
        if not current_room == room:
            return room

def last_puzzle():
    slow_print("This door holds a puzzle.")
    password = "MXPPTLOA"  # Defining password. 

    while True: 
        try:
            user_input = input("HINT is EFKQ\nPASSWORD is:\n").lower().replace(" ", "")
            if user_input == password:
                print("Password correct!")
                break
            else: 
                print("Password incorrect, please try again.")
        except ValueError: 
            print("Invalid input, please try again")

def number_sequence_puzzle():
    slow_print("You have unlocked Door A, but there's a puzzle to solve before you proceed.")
    slow_print("A sequence of numbers will flash briefly. Try to memorize it!")
    
    # Generate a random sequence of numbers
    sequence = [random.randint(0, 9) for _ in range(4)]
    
    while True:
        # Display the sequence briefly
        print("Memorize this sequence: ", sequence)
        time.sleep(3)  # Show for 3 seconds
        print("\033c", end='')  # Clear the screen (works in some terminals)

        # Ask the player to input the sequence
        user_input = input("Enter the sequence you saw: ").strip()

        # Check if the player's input matches the sequence
        if user_input == ''.join(map(str, sequence)):
            slow_print("Correct! You may proceed to the next room.")
            return True
        else:
            slow_print("Incorrect sequence. Try again.")

def examine_item(item_name):
    """
    Examine an item which can be a door or furniture.
    First make sure the intended item belongs to the current room.
    Then check if the item is a door. Tell player if key hasn't been
    collected yet. Otherwise ask player if they want to go to the next
    room. If the item is not a door, then check if it contains keys.
    Collect the key if found and update the game state. At the end,
    play either the current or the next room depending on the game state
    to keep playing.
    """
    current_room = game_state["current_room"]
    next_room = ""
    output = None

    for item in object_relations[current_room["name"]]:
        if item["name"] == item_name:
            print()
            output = "You examine " + item_name + ". "
            if item["type"] == "door":
                have_key = False
                for key in game_state["keys_collected"]:
                    if key["target"] == item:
                        have_key = True
                if have_key:
                    if item["name"] == "door a":
                        output += "You unlock it with a key you have."
                        slow_print(output)
                        if number_sequence_puzzle():  # Trigger the puzzle for Door A
                            next_room = get_next_room_of_door(item, current_room)
                    elif item["name"] == "door d":
                        output += "Woow!!." 
                        slow_print(output)
                        last_puzzle()
                    
                    next_room = get_next_room_of_door(item, current_room)
                else:
                    output += "It is locked but you don't have the key."
            else:
                if item["name"] in object_relations and len(object_relations[item["name"]]) > 0:
                    item_found = object_relations[item["name"]].pop()
                    game_state["keys_collected"].append(item_found)
                    output += "You find " + item_found["name"] + "."
                else:
                    output += "There isn't anything interesting about it."
            slow_print(output)
            break

    if output is None:
        slow_print("The item you requested is not found in the current room.")

    if next_room and input("Do you want to go to the next room? Enter 'yes' or 'no'").strip() == 'yes':
        play_room(next_room)
    else:
        play_room(current_room)

game_state = INIT_GAME_STATE.copy()

start_game()