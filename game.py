def show_help():
    print("""
Commands:
  help                 Show this help
  look                 Describe where you are
  go <north|south|east|west>   Move to another room
  quit                 Exit the game
""".strip())


WORLD = {
    "training_room": {
        "name": "the Training Room",
        "desc": "A small stone room with a chalkboard. Someone wrote: 'Ship small. Ship often.'",
        "exits": {"east": "hallway"},
        "items": ["map"],
    },
    "hallway": {
        "name": "the Hallway",
        "desc": "A narrow corridor with flickering torches. You hear distant dripping water.",
        "exits": {"west": "training_room", "north": "armory"},
        "items": [],
    },
    "armory": {
        "name": "the Armory",
        "desc": "Rusty training weapons line the walls. One sword looks *almost* usable.",
        "exits": {"south": "hallway"},
        "items": ["rusty sword"],
    },
}


def look(state):
    room = WORLD[state["location"]]
    print(f"\nYou are in {room['name']}.")
    print(room["desc"])

    exits = ", ".join(sorted(room["exits"].keys()))
    print(f"Exits: {exits}\n")
    
    items = room.get("items", [])
    if items:
        print("You see: " + ", ".join(items))
    else:
        print("You see: nothing useful.")
    print()



def go_direction(state, direction: str):
    direction = direction.strip().lower()
    room = WORLD[state["location"]]
    exits = room["exits"]

    if direction in exits:
        state["location"] = exits[direction]
        look(state)
    else:
        print(f"You can't go {direction} from here.")

def show_inventory(state):
    inv = state["inventory"]
    if not inv:
        print("Your inventory is empty.")
    else:
        print("You are carrying: " + ", ".join(inv))

def take_item(state, item_name: str):
    item_name = item_name.strip().lower()
    if not item_name:
        print("Take what?")
        return

    room = WORLD[state["location"]]
    room_items = room.get("items", [])

    # match case-insensitively
    match = None
    for it in room_items:
        if it.lower() == item_name:
            match = it
            break

    if match is None:
        print(f"There is no '{item_name}' here.")
        return

    room_items.remove(match)
    state["inventory"].append(match)
    print(f"You picked up: {match}")


def main():
    state = {
        "location": "training_room",
        "is_running": True,
        "inventory": [],
    }

    print("Welcome to Dungeon Dash (text edition)!")
    print("Type 'help' to see commands.\n")
    look(state)

    while state["is_running"]:
        raw = input("> ").strip()

        if not raw:
            continue

        cmd = raw.lower()

        if cmd == "help":
            show_help()
        elif cmd == "look":
            look(state)
        elif cmd.startswith("go "):
            direction = raw[3:]  # keep original spacing; we'll strip inside function
            go_direction(state, direction)
        elif cmd in ("quit", "exit"):
            print("Goodbye! 👋")
            state["is_running"] = False
        elif cmd in ("inventory", "inv"):
            show_inventory(state)
        elif cmd.startswith("take "):
            take_item(state, raw[5:])
        elif cmd == "take":
            take_item(state, "")

        else:
            print(f"I don't understand '{raw}'. Type 'help'.")


if __name__ == "__main__":
    main()
