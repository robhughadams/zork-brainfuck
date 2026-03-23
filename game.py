# Game loop
room = 0
has_key = 0
has_treasure = 0
key_in_room = 1
treasure_in_room = 1

while room < 10:
    print("COMMAND? ")
    cmd = input()
    if cmd == "N":
        if room == 0:
            room = 1
            print("NORTH")
            print("HALLWAY")
        else:
            print("CANT GO NORTH")
    if cmd == "S":
        if room == 1:
            room = 2
            print("SOUTH")
            print("TREASURE ROOM")
        else:
            print("CANT GO SOUTH")
    if cmd == "W":
        if room == 1:
            room = 0
            print("WEST")
            print("DARK ROOM")
        else:
            print("CANT GO WEST")
    if cmd == "E":
        if room == 0:
            print("THERE IS A KEY")
        else:
            print("CANT GO EAST")
    if cmd == "LOOK":
        if room == 0:
            print("DARK ROOM")
            if key_in_room == 1:
                print("RUSTY KEY HERE")
        if room == 1:
            print("HALLWAY")
        if room == 2:
            print("TREASURE ROOM")
            if treasure_in_room == 1:
                print("GOLDEN TREASURE HERE")
    if cmd == "TAKE":
        if room == 0:
            if key_in_room == 1:
                if has_key == 0:
                    has_key = 1
                    key_in_room = 0
                    print("TOOK KEY")
                else:
                    print("ALREADY HAVE KEY")
            else:
                print("NO KEY HERE")
        if room == 2:
            if treasure_in_room == 1:
                has_treasure = 1
                treasure_in_room = 0
                print("YOU WIN!")
                print("GAME OVER")
                break
            else:
                print("NO TREASURE")
    if cmd == "QUIT":
        print("GOODBYE")
        break