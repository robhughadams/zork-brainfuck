#!/usr/bin/env python3
"""Generate working BF game - using the correct print method"""

def p(s):
    """Print string: clear cell, set value, print"""
    for c in s:
        print('[-]')  # clear
        print('+' * ord(c))  # set value
        print('.')  # print

# Cell layout: 0=temp, 1=room, 2=has_key, 3=key_here, 4=treasure_here, 5=cmd, 6=unused

# Initialize
print('[-]')  # temp = 0
print('>[-]')  # room = 0
print('>[-]')  # has_key = 0
print('>[-]')  # key_here = 0
print('>+')   # key_here = 1
print('>[-]')  # treasure_here = 0
print('>+')   # treasure_here = 1

print('<<<<<<<')  # back to cell 0

# Main loop
print('[')

# Print "CMD? "
p('CMD?')

# Read input to cell 5 (command)
print('>>>>>>')
print(',')
print('<<<<<<')

# ===== Check N =====
print('>>>>>')  # cell 5
print('[')      # if command != 0
print('----------')  # -10
print('----------')  
print('----------')  
print('----------')  
print('----------')  
print('----------')  
print('----------')  
print('>')      # cell 6
print('[')      # if temp != 0 (not N)
print('<<-')    # clear and continue
print(']')
print('<<')     # back to cell 5

print('<')      # cell 4
print('[')      # if was N (now 0)
print('<<<<<<')  # to room
print('>[-]')    # clear
print('>+')      # room = 1
print('<<<<<')   # back
p('NORTH')
p('HALL')
print(']')

# ===== Check S =====
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

print('<')
print('[')
print('<<<<<<')
print('>[-]')
print('>++')
print('<<<<<')
p('SOUTH')
p('TREASURE')
print(']')

# ===== Check L (LOOK) =====
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

print('<')
print('[')
# Room 0
print('<<<<<<<')  # to room
print('[')         # if room == 0
p('DARK ROOM')
print('>>>')       # to key_here (cell 3)
print('[')         # if key here
p('KEY')
print('>>>-]')     # consume flag
print('<<<<<')     # back
print('-]')

# Room 1
print('<')
print('[')
p('HALLWAY')
print('<<<<<')
print('-]')

# Room 2
print('<')
print('[')
p('TREASURE')
print('<<<<<')
print('-]')

print(']')

# ===== Check Q =====
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

print('<')
print('[')
p('BYE')
print(']')

# End loop
print('<<<<<<<')
print('-]')
print(']')