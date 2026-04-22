separator = "---------------------------------------------------------"

loop = 4
mailbox_open = 0
leaflet_visible = 0
leaflet_taken = 0
print(separator)
print("Welcome to Zork - The Unofficial BrainFuck Version.")

running = 1
while running > 0:
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
            _c_handled_eq_0 = 1
            _c_eq_match_0_0 = 1
            _c_eq_cmp_0_0 = loop
            _c_eq_cmp_0_0 = _c_eq_cmp_0_0 - 4
            if _c_eq_cmp_0_0 > 0:
                _c_eq_match_0_0 = 0
            _c_eq_cmp_rev_0_0 = 4
            _c_eq_cmp_rev_0_0 = _c_eq_cmp_rev_0_0 - loop
            if _c_eq_cmp_rev_0_0 > 0:
                _c_eq_match_0_0 = 0
            if _c_handled_eq_0 > 0:
                if _c_eq_match_0_0 > 0:
                    _c_handled_eq_0 = 0
                    print(separator)
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
                print(separator)
                print("It is securely anchored.")
            # LOWERED_RUNTIME_STRING_EQ
            if second == "open mailbox":
                _handled_second_0 = 0
                print(separator)
                _c_handled_eq_5 = 1
                _c_eq_match_5_0 = 1
                _c_eq_cmp_5_0 = mailbox_open
                _c_eq_cmp_5_0 = _c_eq_cmp_5_0 - 1
                if _c_eq_cmp_5_0 > 0:
                    _c_eq_match_5_0 = 0
                _c_eq_cmp_rev_5_0 = 1
                _c_eq_cmp_rev_5_0 = _c_eq_cmp_rev_5_0 - mailbox_open
                if _c_eq_cmp_rev_5_0 > 0:
                    _c_eq_match_5_0 = 0
                if _c_handled_eq_5 > 0:
                    if _c_eq_match_5_0 > 0:
                        _c_handled_eq_5 = 0
                        print("The small mailbox is already open.")
                if _c_handled_eq_5 > 0:
                    mailbox_open = 1
                    leaflet_visible = 1
                    print("Opening the small mailbox reveals a leaflet.")
            # LOWERED_RUNTIME_STRING_EQ
            if second == "take leaflet":
                _handled_second_0 = 0
                print(separator)
                _c_handled_eq_6 = 1
                _c_eq_match_6_0 = 1
                _c_eq_cmp_6_0 = leaflet_visible
                _c_eq_cmp_6_0 = _c_eq_cmp_6_0 - 0
                if _c_eq_cmp_6_0 > 0:
                    _c_eq_match_6_0 = 0
                _c_eq_cmp_rev_6_0 = 0
                _c_eq_cmp_rev_6_0 = _c_eq_cmp_rev_6_0 - leaflet_visible
                if _c_eq_cmp_rev_6_0 > 0:
                    _c_eq_match_6_0 = 0
                if _c_handled_eq_6 > 0:
                    if _c_eq_match_6_0 > 0:
                        _c_handled_eq_6 = 0
                        print("You do not see any leaflet here.")
                _c_eq_match_6_1 = 1
                _c_eq_cmp_6_1 = leaflet_taken
                _c_eq_cmp_6_1 = _c_eq_cmp_6_1 - 1
                if _c_eq_cmp_6_1 > 0:
                    _c_eq_match_6_1 = 0
                _c_eq_cmp_rev_6_1 = 1
                _c_eq_cmp_rev_6_1 = _c_eq_cmp_rev_6_1 - leaflet_taken
                if _c_eq_cmp_rev_6_1 > 0:
                    _c_eq_match_6_1 = 0
                if _c_handled_eq_6 > 0:
                    if _c_eq_match_6_1 > 0:
                        _c_handled_eq_6 = 0
                        print("You already have the leaflet.")
                if _c_handled_eq_6 > 0:
                    leaflet_taken = 1
                    print("Taken.")
            # LOWERED_RUNTIME_STRING_EQ
            if second == "read leaflet":
                _handled_second_0 = 0
                print(separator)
                _c_handled_eq_7 = 1
                _c_eq_match_7_0 = 1
                _c_eq_cmp_7_0 = leaflet_taken
                _c_eq_cmp_7_0 = _c_eq_cmp_7_0 - 1
                if _c_eq_cmp_7_0 > 0:
                    _c_eq_match_7_0 = 0
                _c_eq_cmp_rev_7_0 = 1
                _c_eq_cmp_rev_7_0 = _c_eq_cmp_rev_7_0 - leaflet_taken
                if _c_eq_cmp_rev_7_0 > 0:
                    _c_eq_match_7_0 = 0
                if _c_handled_eq_7 > 0:
                    if _c_eq_match_7_0 > 0:
                        _c_handled_eq_7 = 0
                        print("Welcome to the Unofficial Python Version of Zork. Your mission is to find a Jade Statue.")
                _c_eq_match_7_1 = 1
                _c_eq_cmp_7_1 = leaflet_visible
                _c_eq_cmp_7_1 = _c_eq_cmp_7_1 - 1
                if _c_eq_cmp_7_1 > 0:
                    _c_eq_match_7_1 = 0
                _c_eq_cmp_rev_7_1 = 1
                _c_eq_cmp_rev_7_1 = _c_eq_cmp_rev_7_1 - leaflet_visible
                if _c_eq_cmp_rev_7_1 > 0:
                    _c_eq_match_7_1 = 0
                if _c_handled_eq_7 > 0:
                    if _c_eq_match_7_1 > 0:
                        _c_handled_eq_7 = 0
                        print("You need to take the leaflet first.")
                if _c_handled_eq_7 > 0:
                    print("You do not have any leaflet to read.")
            # LOWERED_RUNTIME_STRING_EQ
            if second == "go east":
                _handled_second_0 = 0
                print(separator)
                print("The door is boarded and you cannot remove the boards.")
            # LOWERED_RUNTIME_STRING_EQ
            if second == "open door":
                _handled_second_0 = 0
                print(separator)
                print("The door cannot be opened.")
            # LOWERED_RUNTIME_STRING_EQ
            if second == "take boards":
                _handled_second_0 = 0
                print(separator)
                print("The boards are securely fastened.")
            # LOWERED_RUNTIME_STRING_EQ
            if second == "look at house":
                _handled_second_0 = 0
                print(separator)
                print("The house is a beautiful colonial house which is painted white. It is clear that the owners must have been extremely wealthy.")
            # LOWERED_RUNTIME_STRING_EQ
            if second == "go southwest":
                _handled_second_0 = 0
                loop = 8
            if _handled_second_0 > 0:
                print(separator)
                print("That is not a valid command here.")
                _c_handled_eq_8 = 1
                _c_eq_match_8_0 = 1
                _c_eq_cmp_8_0 = leaflet_visible
                _c_eq_cmp_8_0 = _c_eq_cmp_8_0 - 1
                if _c_eq_cmp_8_0 > 0:
                    _c_eq_match_8_0 = 0
                _c_eq_cmp_rev_8_0 = 1
                _c_eq_cmp_rev_8_0 = _c_eq_cmp_rev_8_0 - leaflet_visible
                if _c_eq_cmp_rev_8_0 > 0:
                    _c_eq_match_8_0 = 0
                if _c_handled_eq_8 > 0:
                    if _c_eq_match_8_0 > 0:
                        _c_handled_eq_8 = 0
                        print("Options: take mailbox, open mailbox, go east, open door, take boards, look at house, go southwest, take leaflet, read leaflet")
                if _c_handled_eq_8 > 0:
                    print("Options: take mailbox, open mailbox, go east, open door, take boards, look at house, go southwest")


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
            _c_handled_eq_1 = 1
            _c_eq_match_1_0 = 1
            _c_eq_cmp_1_0 = loop
            _c_eq_cmp_1_0 = _c_eq_cmp_1_0 - 8
            if _c_eq_cmp_1_0 > 0:
                _c_eq_match_1_0 = 0
            _c_eq_cmp_rev_1_0 = 8
            _c_eq_cmp_rev_1_0 = _c_eq_cmp_rev_1_0 - loop
            if _c_eq_cmp_rev_1_0 > 0:
                _c_eq_match_1_0 = 0
            if _c_handled_eq_1 > 0:
                if _c_eq_match_1_0 > 0:
                    _c_handled_eq_1 = 0
                    print(separator)
                    print("This is a forest, with trees in all directions. To the east, there appears to be sunlight.")
                    forest_inp = input("What do you do? ")

            # LOWERED_STRING_CHAIN
            forest_inp = forest_inp.lower()
            _handled_forest_inp_1 = 1
            # LOWERED_RUNTIME_STRING_EQ
            if forest_inp == "go west":
                _handled_forest_inp_1 = 0
                print(separator)
                print("You would need a machete to go further west.")
            # LOWERED_RUNTIME_STRING_EQ
            if forest_inp == "go north":
                _handled_forest_inp_1 = 0
                print(separator)
                print("The forest becomes impenetrable to the North.")
            # LOWERED_RUNTIME_STRING_EQ
            if forest_inp == "go south":
                _handled_forest_inp_1 = 0
                print(separator)
                print("Storm-tossed trees block your way.")
            # LOWERED_RUNTIME_STRING_EQ
            if forest_inp == "go east":
                _handled_forest_inp_1 = 0
                loop = 9
            if _handled_forest_inp_1 > 0:
                print(separator)
                print("That is not a valid command here.")
                print("Options: go west, go north, go south, go east")


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
            _c_handled_eq_2 = 1
            _c_eq_match_2_0 = 1
            _c_eq_cmp_2_0 = loop
            _c_eq_cmp_2_0 = _c_eq_cmp_2_0 - 9
            if _c_eq_cmp_2_0 > 0:
                _c_eq_match_2_0 = 0
            _c_eq_cmp_rev_2_0 = 9
            _c_eq_cmp_rev_2_0 = _c_eq_cmp_rev_2_0 - loop
            if _c_eq_cmp_rev_2_0 > 0:
                _c_eq_match_2_0 = 0
            if _c_handled_eq_2 > 0:
                if _c_eq_match_2_0 > 0:
                    _c_handled_eq_2 = 0
                    print(separator)
                    print("You are in a clearing, with a forest surrounding you on all sides. A path leads south.")
                    print("There is an open grating, descending into darkness.")
                    grating_inp = input("What do you do? ")

            # LOWERED_STRING_CHAIN
            grating_inp = grating_inp.lower()
            _handled_grating_inp_2 = 1
            # LOWERED_RUNTIME_STRING_EQ
            if grating_inp == "go south":
                _handled_grating_inp_2 = 0
                print(separator)
                print("You see a large ogre and turn around.")
            # LOWERED_RUNTIME_STRING_EQ
            if grating_inp == "descend grating":
                _handled_grating_inp_2 = 0
                loop = 10
            if _handled_grating_inp_2 > 0:
                print(separator)
                print("That is not a valid command here.")
                print("Options: go south, descend grating")


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
            _c_handled_eq_3 = 1
            _c_eq_match_3_0 = 1
            _c_eq_cmp_3_0 = loop
            _c_eq_cmp_3_0 = _c_eq_cmp_3_0 - 10
            if _c_eq_cmp_3_0 > 0:
                _c_eq_match_3_0 = 0
            _c_eq_cmp_rev_3_0 = 10
            _c_eq_cmp_rev_3_0 = _c_eq_cmp_rev_3_0 - loop
            if _c_eq_cmp_rev_3_0 > 0:
                _c_eq_match_3_0 = 0
            if _c_handled_eq_3 > 0:
                if _c_eq_match_3_0 > 0:
                    _c_handled_eq_3 = 0
                    print(separator)
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
                print(separator)
                print("Why would you do that? Are you some sort of sicko?")
            # LOWERED_RUNTIME_STRING_EQ
            if cave_inp == "smash skeleton":
                _handled_cave_inp_3 = 0
                print(separator)
                print("Sick person. Have some respect mate.")
            # LOWERED_RUNTIME_STRING_EQ
            if cave_inp == "light up room":
                _handled_cave_inp_3 = 0
                print(separator)
                print("You would need a torch or lamp to do that.")
            # LOWERED_RUNTIME_STRING_EQ
            if cave_inp == "break skeleton":
                _handled_cave_inp_3 = 0
                print(separator)
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
                print(separator)
                print("You throw yourself down the staircase as an attempt at suicide. You die.")
                print(separator)
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
                    mailbox_open = 0
                    leaflet_visible = 0
                    leaflet_taken = 0
            if _handled_cave_inp_3 > 0:
                print(separator)
                print("That is not a valid command here.")
                print("Options: descend staircase, go down staircase, scale staircase, take skeleton, smash skeleton, light up room, break skeleton, suicide")


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
            _c_handled_eq_4 = 1
            _c_eq_match_4_0 = 1
            _c_eq_cmp_4_0 = loop
            _c_eq_cmp_4_0 = _c_eq_cmp_4_0 - 11
            if _c_eq_cmp_4_0 > 0:
                _c_eq_match_4_0 = 0
            _c_eq_cmp_rev_4_0 = 11
            _c_eq_cmp_rev_4_0 = _c_eq_cmp_rev_4_0 - loop
            if _c_eq_cmp_rev_4_0 > 0:
                _c_eq_match_4_0 = 0
            if _c_handled_eq_4 > 0:
                if _c_eq_match_4_0 > 0:
                    _c_handled_eq_4 = 0
                    print(separator)
                    print("You have entered a mud-floored room.")
                    print("Lying half buried in the mud is an old trunk, bulging with jewels.")
                    last_inp = input("What do you do? ")

            # LOWERED_STRING_CHAIN
            last_inp = last_inp.lower()
            _handled_last_inp_4 = 1
            # LOWERED_RUNTIME_STRING_EQ
            if last_inp == "open trunk":
                _handled_last_inp_4 = 0
                print(separator)
                print("You have found the Jade Statue and have completed your quest!")
            if _handled_last_inp_4 > 0:
                print(separator)
                print("That is not a valid command here.")
                print("Options: open trunk")

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
                mailbox_open = 0
                leaflet_visible = 0
                leaflet_taken = 0
