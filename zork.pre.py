# Introduction narration of game


loop = 4
print("---------------------------------------------------------")
print("Welcome to Zork - The Unofficial Python Version.")

running = 1
while running > 0:
    # Room 1: Open Field (loop == 4)
    _run = 1
    while _run > 0:
        _c_loop = 4
        _c_loop = _c_loop - loop
        if _c_loop > 0:
            _run = 0
        if _run > 0:
            print("---------------------------------------------------------")
            print("You are standing in an open field west of a white house, with a boarded front door.")
            print("(A secret path leads southwest into the forest.)")
            print("There is a Small Mailbox.")
            second = input("What do you do? ")
            loop = 8
            _run = 0


    # Room 2: Forest (loop == 8)
    _run = 1
    while _run > 0:
        _c_loop = 8
        _c_loop = _c_loop - loop
        if _c_loop > 0:
            _run = 0
        if _run > 0:
            print("---------------------------------------------------------")
            print("This is a forest, with trees in all directions. To the east, there appears to be sunlight.")
            forest_inp = input("What do you do? ")
            loop = 9
            _run = 0


    # Room 3: Clearing with Grating (loop == 9)
    _run = 1
    while _run > 0:
        _c_loop = 9
        _c_loop = _c_loop - loop
        if _c_loop > 0:
            _run = 0
        if _run > 0:
            print("---------------------------------------------------------")
            print("You are in a clearing, with a forest surrounding you on all sides. A path leads south.")
            print("There is an open grating, descending into darkness.")
            grating_inp = input("What do you do? ")
            loop = 10
            _run = 0


    # Room 4: Cave (loop == 10)
    _run = 1
    while _run > 0:
        _c_loop = 10
        _c_loop = _c_loop - loop
        if _c_loop > 0:
            _run = 0
        if _run > 0:
            print("---------------------------------------------------------")
            print("You are in a tiny cave with a dark, forbidding staircase leading down.")
            print("There is a skeleton of a human male in one corner.")
            cave_inp = input("What do you do? ")
            loop = 11
            _run = 0


    # Room 5: End of game (loop == 11)
    _run = 1
    while _run > 0:
        _c_loop = 11
        _c_loop = _c_loop - loop
        if _c_loop > 0:
            _run = 0
        if _run > 0:
            print("---------------------------------------------------------")
            print("You have entered a mud-floored room.")
            print("Lying half buried in the mud is an old trunk, bulging with jewels.")
            last_inp = input("What do you do? ")
            print("---------------------------------------------------------")
            exit_inp = input("Do you want to continue? Y/N ")
            running = 0
            _run = 0
