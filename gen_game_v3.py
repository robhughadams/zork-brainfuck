#!/usr/bin/env python3
"""Generate working BF game directly - not using transpiler yet"""

def p(s):
    for c in s:
        print('[-]' + '+' * ord(c) + '.')

# Cell layout: 0=temp, 1=room, 2=has_key, 3=key_here, 4=treasure_here, 5=cmd

# Init
print('[-]')  # temp = 0
print('>[-]')  # room = 0
print('>[-]')  # has_key = 0
print('>[-]')  # key_here = 0
print('>+')  # key_here = 1
print('>[-]')  # treasure_here = 0
print('>+')  # treasure_here = 1

print('<<<<<<<')  # back to cell 0

# Main loop
print('[')

# Print prompt
p('CMD?')

# Read input
print('>>>>>>')
print(',')
print('<<<<<<')

# Check N (78) - simplified ASCII check
print('>>>>>')
print('[')
print('----------')  # -10
print('----------')  # -10  
print('----------')  # -10
print('----------')  # -10
print('----------')  # -10
print('----------')  # -10
print('----------')  # -10
print('>')
print('[')
print('<<-')
print(']')
print('<<')

# If N: go to room 1
print('<')
print('[')
print('<<<<<<')
print('>[-]')
print('>+')
print('<<<<<')
p('NORTH')
p('HALL')
print(']')

# Check S (83)
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

# If S: go to room 2
print('<')
print('[')
print('<<<<<<')
print('>[-]')
print('>++')
print('<<<<<')
p('SOUTH')
p('TREASURE')
print(']')

# Check L (LOOK)
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

# LOOK logic
print('<')
print('[')
# Room 0
print('<<<<<<<')
print('[')
p('DARK ROOM')
print('>>>')
print('[')
p('KEY HERE')
print('>>>-]')
print('<<<<<')
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
p('TREASURE RM')
print('<<<<<')
print('-]')

print(']')

# Check Q (QUIT)
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

# If Q
print('<')
print('[')
p('BYE')
print(']')

# End loop
print('<<<<<<<')
print('-]')
print(']')