# Interactive Zork - with input pauses
# Uses input but simple processing

print("================================")
print("         ZORK in Brainfuck")
print("================================")
print("")

# First room
print("You are in a DARK ROOM.")
print("There is a rusty KEY here.")
print("")
print("Press Enter to look around...")
pause = input()

print("You see a rusty key on the floor.")
print("")
print("Press Enter to take the key...")
pause = input()

print("You pick up the rusty key.")
has_key = 1
key_in_room = 0
print("")

# Second room
print("You walk NORTH to a hallway.")
print("A locked DOOR blocks the way.")
print("")
print("Press Enter to unlock the door...")
pause = input()

print("You use the rusty key to unlock it.")
print("The door creaks open!")
print("")

# Third room
print("You enter the TREASURE ROOM!")
print("A GOLDEN CHEST sits in the center!")
print("")
print("Press Enter to open the chest...")
pause = input()

print("You open the chest and find...")
print("DIAMONDS! RUBIES! GOLD!")
print("")
print("You take the treasure!")
print("")

# Win
print("********************************")
print("        YOU WIN!")
print("********************************")
print("")
print("Thanks for playing ZORK in Brainfuck!")
print("")
print("Press Enter to quit...")
pause = input()
print("Goodbye!")
