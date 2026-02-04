import random

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
        "items": ["bandage"],

    },
    "armory": {
        "name": "the Armory",
        "desc": "Rusty training weapons line the walls. One sword looks *almost* usable.",
        "exits": {"south": "hallway"},
        "items": ["rusty sword"],
    },
}


def look(state):
    print(f"(HP: {state['hp']}/{state['max_hp']})")

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
        maybe_spawn_enemy(state)

    else:
        print(f"You can't go {direction} from here.")

def show_inventory(state):
    inv = state["inventory"]
    if not inv:
        print("Your inventory is empty.")
    else:
        print("You are carrying: " + ", ".join(inv))

    weapon = state.get("weapon")
    if weapon:
        print(f"Equipped weapon: {weapon}")


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
    
def use_item(state, item_name: str):
    item_name = item_name.strip().lower()
    if not item_name:
        print("Use what?")
        return

    # Find exact item in inventory (case-insensitive)
    match = None
    for it in state["inventory"]:
        if it.lower() == item_name:
            match = it
            break

    if match is None:
        print(f"You don't have '{item_name}'.")
        return

    if match.lower() == "map":
        room = WORLD[state["location"]]
        exits = ", ".join(sorted(room["exits"].keys()))
        print(f"The map shows exits from here: {exits}")
        print("(Pro tip: maps are mostly confidence with better branding.)")
    elif match.lower() == "rusty sword":
        state["weapon"] = match
        print(f"You equip the {match}. It feels... questionably heroic.")
    elif match.lower() == "bandage":
        if state["hp"] >= state["max_hp"]:
            print("You're already at full health.")
            return

        heal_amount = 3
        state["hp"] = min(state["max_hp"], state["hp"] + heal_amount)
        state["inventory"].remove(match)
        print(f"You use a bandage and heal +{heal_amount} HP.")
        print(f"(HP: {state['hp']}/{state['max_hp']})")

    else:
        print(f"You try to use {match}, but nothing happens.")


def maybe_spawn_enemy(state):
    # Only spawn in the hallway, and only if no enemy already exists
    if state["location"] != "hallway" or state["enemy"] is not None:
        return

    # 40% chance
    if random.random() < 0.40:
        state["enemy"] = {"name": "rat", "hp": 3}
        print("\nA nasty RAT scurries out of the shadows! 🐀")
        print("Type 'attack' to fight it (or 'go west/north' to run).\n")
        
        

def attack(state):
    enemy = state.get("enemy")
    if not enemy:
        print("There is nothing to attack.")
        return

    weapon = state.get("weapon")
    damage = 2 if weapon else 1
    # 25% miss chance
    MISS_CHANCE = 0.25

    if random.random() < MISS_CHANCE:
        print("You swing... and miss!")
        print("The rat squeaks mockingly.\n")
        return
    
    CRIT_CHANCE = 0.1
    if random.random() < CRIT_CHANCE:
        damage *= 2
        print("Critical hit!")
    
    enemy["hp"] -= damage
    if weapon:
        print(f"You swing your {weapon} and deal {damage} damage!")
        if damage is 0 :
            print('You have missed')
            state["attack"] = 1
    else:
        print(f"You punch wildly and deal {damage} damage!")
        state["attack"] = 1

    if enemy["hp"] <= 0:
        print("The rat collapses. The hallway is safe... for now.")
        state["enemy"] = None
    else:
        print(f"The {enemy['name']} is still up! (HP: {enemy['hp']})")
        # simple counter-attack flavor (no player HP yet)
        state["hp"] -= 1
        print("It bites your boot and hisses. Rude.\n")
        if state["hp"] <= 0:
            print("\nYou collapse dramatically. Game over.")
            state["is_running"] = False
        else:
            print(f"(HP: {state['hp']}/{state['max_hp']})\n")

def status(state):
    print(f"HP: {state['hp']}/{state['max_hp']}")
    weapon = state.get("weapon") or "none"
    print(f"Weapon: {weapon}")


def main():
    state = {
        "location": "training_room",
        "is_running": True,
        "inventory": [],
        "weapon": None,
        "enemy": None,
        "hp": 10,
        "max_hp": 10,
        "attack": 1

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
        elif cmd.startswith("use "):
            use_item(state, raw[4:])
        elif cmd == "use":
            use_item(state, "")
        elif cmd in ("attack", "hit"):
            attack(state)
        elif cmd == "status":
            status(state)

        else:
            print(f"I don't understand '{raw}'. Type 'help'.")


if __name__ == "__main__":
    main()
