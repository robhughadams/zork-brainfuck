#!/usr/bin/env python3
"""Generate working Zork BF game"""

def p(s):
    """Print string helper"""
    for c in s:
        print('[-]' + '+' * ord(c) + '.')

# Init cells
print('[-]')  # room = 0
print('>[-]')  # has_key = 0
print('>[-]')  # has_treasure = 0
print('>[-]')  # key_here = 0
print('>+')  # key_here = 1
print('>[-]')  # treasure_here = 0
print('>+')  # treasure_here = 1
print('<<<<<<<')  # back to cell 0

# Main loop
print('[')

# Print prompt
p('CMD?')

# Read input to cell 5
print('>>>>>>')
print(',')
print('<<<<<<')

# Check command = 'N' (78)
print('>>>>>')  # cell 5
print('[')  # if input
print('----------')  # -10 -> 68
print('----------')  # -10 -> 58
print('----------')  # -10 -> 48
print('----------')  # -10 -> 38
print('----------')  # -10 -> 28
print('----------')  # -10 -> 18
print('----------')  # -10 -> 8
print('>')  # cell 6
print('[')  # if != 0 (not N)
print('<<-')  # clear and continue
print(']')
print('<<')  # back to 5

# If N: room = 1
print('<')  # cell 4
print('[')  # if was N
print('<<<<<<')  # to room
print('>[-]')  # clear
print('>+')  # room = 1
print('<<<<<')  # back
p('NORTH')
p('HALL')
print(']')

# Check command = 'S' (83)
print('>>>>>')
print('[')
print('----------')
print('----------')
print('----------')
print('----------')
print('----------')
print('----------')
print('----------')
print('---')
print('>')
print('[')
print('<<-')
print(']')
print('<<')

# If S: room = 2
print('<')
print('[')
print('<<<<<<')
print('>[-]')
print('>++')
print('<<<<<')
p('SOUTH')
p('TREASURE RM')
print(']')

# Check command = 'L' (LOOK)
print('>>>>>')
print('[')
print('----------')
print('----------')
print('----------')
print('----------')
print('----------')
print('----')
print('>')
print('[')
print('<<-')
print(']')
print('<<')

# LOOK: show current room
print('<')
print('[')
print('<<<<<<<')  # go to room 0
print('[')  # if room == 0
p('DARK ROOM')
print('>>>')  # cell 3
print('[')  # if key here
p('KEY HERE')
print('>>>-]')  # consume flag
print('<<<<<')  # back to room 0
print('-]')

print('<')  # room 1
print('[')
p('HALLWAY')
print('<<<<<')  # back
print('-]')

print('<')  # room 2  
print('[')
p('TREASURE ROOM')
print('<<<<<')  # back
print('-]')

print(']')

# Check command = 'Q' (QUIT)
print('>>>>>')
print('[')
print('----------')
print('----------')
print('----------')
print('----------')
print('----------')
print('--')
print('>')
print('[')
print('<<-')
print(']')
print('<<')

# Quit
print('<')
print('[')
p('BYE')
print(']')

# End main loop
print('<<<<<<<')
print('-]')
print(']')