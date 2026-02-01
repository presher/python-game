def show_help():
    print("""
Commands:
  help         Show this help
  look         Describe where you are
  quit         Exit the game
""".strip())

def look(state):
    # We'll expand this later into real rooms/maps.
    print(f"You are in {state['location']}. It's quiet... too quiet.")

def main():
    state = {
        "location": "the Training Room",
        "is_running": True,
    }

    print("Welcome to Dungeon Dash (text edition)!")
    print("Type 'help' to see commands.\n")

    while state["is_running"]:
        cmd = input("> ").strip().lower()

        if cmd == "help":
            show_help()
        elif cmd == "look":
            look(state)
        elif cmd in ("quit", "exit"):
            print("Goodbye! 👋")
            state["is_running"] = False
        elif cmd == "":
            # User just pressed Enter
            continue
        else:
            print(f"I don't understand '{cmd}'. Type 'help'.")

if __name__ == "__main__":
    main()
