# Introduction narration of game


loop = 4
print("---------------------------------------------------------")
print("Welcome to Zork - The Unofficial Python Version.")

running = 1
while running > 0:
    # First Input Loop
    _run = 1
    while _run > 0:
        _c_loop_0 = loop
        _c_loop_0 = _c_loop_0 - 4
        if _c_loop_0 > 0:
            _run = 0
        _c_loop_rev_0 = 4
        _c_loop_rev_0 = _c_loop_rev_0 - loop
        if _c_loop_rev_0 > 0:
            _run = 0
        if _run > 0:
            # if x == n: (simplified)
            print("---------------------------------------------------------")
            print("You are standing in an open field west of a white house, with a boarded front door.")
            print("(A secret path leads southwest into the forest.)")
            print("There is a Small Mailbox.")
            second = input("What do you do? ")

            # LOWERED_STRING_CHAIN
            second = second.lower()
            _handled_second_0 = 1
            # LOWERED_RUNTIME_STRING_EQ
            if second == "take mailbox":
                _handled_second_0 = 0
                print("---------------------------------------------------------")
                print("It is securely anchored.")
            # LOWERED_RUNTIME_STRING_EQ
            if second == "open mailbox":
                _handled_second_0 = 0
                print("---------------------------------------------------------")
                print("Opening the small mailbox reveals a leaflet.")
            # LOWERED_RUNTIME_STRING_EQ
            if second == "go east":
                _handled_second_0 = 0
                print("---------------------------------------------------------")
                print("The door is boarded and you cannot remove the boards.")
            # LOWERED_RUNTIME_STRING_EQ
            if second == "open door":
                _handled_second_0 = 0
                print("---------------------------------------------------------")
                print("The door cannot be opened.")
            # LOWERED_RUNTIME_STRING_EQ
            if second == "take boards":
                _handled_second_0 = 0
                print("---------------------------------------------------------")
                print("The boards are securely fastened.")
            # LOWERED_RUNTIME_STRING_EQ
            if second == "look at house":
                _handled_second_0 = 0
                print("---------------------------------------------------------")
                print("The house is a beautiful colonial house which is painted white. It is clear that the owners must have been extremely wealthy.")
            # LOWERED_RUNTIME_STRING_EQ
            if second == "go southwest":
                _handled_second_0 = 0
                loop = 8
            # LOWERED_RUNTIME_STRING_EQ
            if second == "read leaflet":
                _handled_second_0 = 0
                print("---------------------------------------------------------")
                print("Welcome to the Unofficial Python Version of Zork. Your mission is to find a Jade Statue.")
            if _handled_second_0 > 0:
                print("---------------------------------------------------------")
    


    # Southwest Loop
    _run = 1
    while _run > 0:
        _c_loop_1 = loop
        _c_loop_1 = _c_loop_1 - 8
        if _c_loop_1 > 0:
            _run = 0
        _c_loop_rev_1 = 8
        _c_loop_rev_1 = _c_loop_rev_1 - loop
        if _c_loop_rev_1 > 0:
            _run = 0
        if _run > 0:
            # if x == n: (simplified)
            print("---------------------------------------------------------")
            print("This is a forest, with trees in all directions. To the east, there appears to be sunlight.")
            forest_inp = input("What do you do? ")

            # LOWERED_STRING_CHAIN
            forest_inp = forest_inp.lower()
            _handled_forest_inp_1 = 1
            # LOWERED_RUNTIME_STRING_EQ
            if forest_inp == "go west":
                _handled_forest_inp_1 = 0
                print("---------------------------------------------------------")
                print("You would need a machete to go further west.")
            # LOWERED_RUNTIME_STRING_EQ
            if forest_inp == "go north":
                _handled_forest_inp_1 = 0
                print("---------------------------------------------------------")
                print("The forest becomes impenetrable to the North.")
            # LOWERED_RUNTIME_STRING_EQ
            if forest_inp == "go south":
                _handled_forest_inp_1 = 0
                print("---------------------------------------------------------")
                print("Storm-tossed trees block your way.")
            # LOWERED_RUNTIME_STRING_EQ
            if forest_inp == "go east":
                _handled_forest_inp_1 = 0
                loop = 9
            if _handled_forest_inp_1 > 0:
                print("---------------------------------------------------------")
    


    # East Loop and Grating Input
    _run = 1
    while _run > 0:
        _c_loop_2 = loop
        _c_loop_2 = _c_loop_2 - 9
        if _c_loop_2 > 0:
            _run = 0
        _c_loop_rev_2 = 9
        _c_loop_rev_2 = _c_loop_rev_2 - loop
        if _c_loop_rev_2 > 0:
            _run = 0
        if _run > 0:
            # if x == n: (simplified)
            print("---------------------------------------------------------")
            print("You are in a clearing, with a forest surrounding you on all sides. A path leads south.")
            print("There is an open grating, descending into darkness.")
            grating_inp = input("What do you do? ")

            # LOWERED_STRING_CHAIN
            grating_inp = grating_inp.lower()
            _handled_grating_inp_2 = 1
            # LOWERED_RUNTIME_STRING_EQ
            if grating_inp == "go south":
                _handled_grating_inp_2 = 0
                print("---------------------------------------------------------")
                print("You see a large ogre and turn around.")
            # LOWERED_RUNTIME_STRING_EQ
            if grating_inp == "descend grating":
                _handled_grating_inp_2 = 0
                loop = 10
            if _handled_grating_inp_2 > 0:
                print("---------------------------------------------------------")    



    # Grating Loop and Cave Input
    _run = 1
    while _run > 0:
        _c_loop_3 = loop
        _c_loop_3 = _c_loop_3 - 10
        if _c_loop_3 > 0:
            _run = 0
        _c_loop_rev_3 = 10
        _c_loop_rev_3 = _c_loop_rev_3 - loop
        if _c_loop_rev_3 > 0:
            _run = 0
        if _run > 0:
            # if x == n: (simplified)
            print("---------------------------------------------------------")
            print("You are in a tiny cave with a dark, forbidding staircase leading down.")
            print("There is a skeleton of a human male in one corner.")
            cave_inp = input("What do you do? ")

            # LOWERED_STRING_CHAIN
            cave_inp = cave_inp.lower()
            _handled_cave_inp_3 = 1
            # LOWERED_RUNTIME_STRING_EQ
            if cave_inp == "descend staircase":
                _handled_cave_inp_3 = 0
                loop = 11
            # LOWERED_RUNTIME_STRING_EQ
            if cave_inp == "take skeleton":
                _handled_cave_inp_3 = 0
                print("---------------------------------------------------------")
                print("Why would you do that? Are you some sort of sicko?")
            # LOWERED_RUNTIME_STRING_EQ
            if cave_inp == "smash skeleton":
                _handled_cave_inp_3 = 0
                print("---------------------------------------------------------")
                print("Sick person. Have some respect mate.")
            # LOWERED_RUNTIME_STRING_EQ
            if cave_inp == "light up room":
                _handled_cave_inp_3 = 0
                print("---------------------------------------------------------")
                print("You would need a torch or lamp to do that.")
            # LOWERED_RUNTIME_STRING_EQ
            if cave_inp == "break skeleton":
                _handled_cave_inp_3 = 0
                print("---------------------------------------------------------")
                print("I have two questions: Why and With What?")
            # LOWERED_RUNTIME_STRING_EQ
            if cave_inp == "go down staircase":
                _handled_cave_inp_3 = 0
                loop = 11
            # LOWERED_RUNTIME_STRING_EQ
            if cave_inp == "scale staircase":
                _handled_cave_inp_3 = 0
                loop = 11
            # LOWERED_RUNTIME_STRING_EQ
            if cave_inp == "suicide":
                _handled_cave_inp_3 = 0
                print("---------------------------------------------------------")
                print("You throw yourself down the staircase as an attempt at suicide. You die.")
                print("---------------------------------------------------------")
                suicide_inp = input("Do you want to continue? Y/N ")
                # LOWERED_STRING_CHAIN
                suicide_inp = suicide_inp.lower()
                _handled_suicide_inp_6 = 1
                # LOWERED_RUNTIME_STRING_EQ
                if suicide_inp == "n":
                    _handled_suicide_inp_6 = 0
                    running = 0
                    _run = 0
                # LOWERED_RUNTIME_STRING_EQ
                if suicide_inp == "y":
                    _handled_suicide_inp_6 = 0
                    loop = 4
            # LOWERED_RUNTIME_STRING_EQ
            if cave_inp == "scale staircase":
                _handled_cave_inp_3 = 0
                loop = 11
            if _handled_cave_inp_3 > 0:
                print("---------------------------------------------------------")



    # End of game
    _run = 1
    while _run > 0:
        _c_loop_4 = loop
        _c_loop_4 = _c_loop_4 - 11
        if _c_loop_4 > 0:
            _run = 0
        _c_loop_rev_4 = 11
        _c_loop_rev_4 = _c_loop_rev_4 - loop
        if _c_loop_rev_4 > 0:
            _run = 0
        if _run > 0:
            # if x == n: (simplified)
            print("---------------------------------------------------------")
            print("You have entered a mud-floored room.")
            print("Lying half buried in the mud is an old trunk, bulging with jewels.")
            last_inp = input("What do you do? ")

            # LOWERED_STRING_CHAIN
            last_inp = last_inp.lower()
            _handled_last_inp_4 = 1
            # LOWERED_RUNTIME_STRING_EQ
            if last_inp == "open trunk":
                _handled_last_inp_4 = 0
                print("---------------------------------------------------------")
                print("You have found the Jade Statue and have completed your quest!")
            if _handled_last_inp_4 > 0:
                print("---------------------------------------------------------")
        
            # Exit loop at the end of game
            exit_inp = input("Do you want to continue? Y/N ")
            # LOWERED_STRING_CHAIN
            exit_inp = exit_inp.lower()
            _handled_exit_inp_5 = 1
            # LOWERED_RUNTIME_STRING_EQ
            if exit_inp == "n":
                _handled_exit_inp_5 = 0
                running = 0
                _run = 0
            # LOWERED_RUNTIME_STRING_EQ
            if exit_inp == "y":
                _handled_exit_inp_5 = 0
                loop = 4