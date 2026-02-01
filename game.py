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
    },
    "hallway": {
        "name": "the Hallway",
        "desc": "A narrow corridor with flickering torches. You hear distant dripping water.",
        "exits": {"west": "training_room", "north": "armory"},
    },
    "armory": {
        "name": "the Armory",
        "desc": "Rusty training weapons line the walls. One sword looks *almost* usable.",
        "exits": {"south": "hallway"},
    },
}


def look(state):
    room = WORLD[state["location"]]
    print(f"\nYou are in {room['name']}.")
    print(room["desc"])

    exits = ", ".join(sorted(room["exits"].keys()))
    print(f"Exits: {exits}\n")


def go_direction(state, direction: str):
    direction = direction.strip().lower()
    room = WORLD[state["location"]]
    exits = room["exits"]

    if direction in exits:
        state["location"] = exits[direction]
        look(state)
    else:
        print(f"You can't go {direction} from here.")


def main():
    state = {
        "location": "training_room",
        "is_running": True,
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
        else:
            print(f"I don't understand '{raw}'. Type 'help'.")


if __name__ == "__main__":
    main()
