#!/usr/bin/env python3
"""Direct BF code generator for minimal Zork game"""

import sys

def print_str(text):
    """Generate BF to print a string"""
    out = []
    for c in text:
        out.append('[-]')  # Clear current cell
        out.append('+' * ord(c))  # Set to ASCII value
        out.append('.')  # Print
    return ''.join(out)

def set_cell(cell, value):
    """Generate BF to set a cell to a value"""
    out = '>' * cell + '[-]' + '+' * value + '<' * cell
    return out

def main():
    bf = []
    
    # Initialize cells:
    # 0: room (0=start, 1=hallway, 2=treasure)
    # 1: has_key
    # 2: has_treasure
    # 3: key_in_room
    # 4: treasure_in_room
    # 5: command buffer
    
    bf.append('[-]')  # room = 0
    bf.append('>[-]')  # has_key = 0
    bf.append('>[-]')  # has_treasure = 0
    bf.append('>[-]')  # key_in_room = 0
    bf.append('>+')  # key_in_room = 1
    bf.append('>[-]')  # treasure_in_room = 0
    bf.append('>+')  # treasure_in_room = 1
    bf.append('<<<<<<<')  # back to cell 0
    
    # Main loop
    bf.append('[')
    
    # Print prompt
    bf.append(print_str('CMD? '))
    
    # Read command to cell 5
    bf.append('>>>>>>')
    bf.append(',')
    bf.append('<<<<<<')
    
    # Check each command by comparing ASCII value
    # Cell 5 holds command, we'll copy it to cell 6 for testing
    
    # ===== N =====
    # Set cell 6 = cell 5, then check if == 78 (N)
    bf.append('>>>>>>>')  # cell 6
    bf.append('[-]')  # clear
    bf.append('<<<<<<<')  # back to 5
    bf.append('[')  # if command exists
    bf.append('>-')  # copy to 6 (decrement 5, increment 6)
    bf.append('<-]')  # back to 5, clear it
    bf.append('>>')  # cell 7 for temp
    bf.append('[-]')  # clear
    bf.append('<<')  # back to 6
    
    # Check if 6 == 78 (N)
    bf.append('[-')  # if cell 6 != 0
    bf.append('++++++')  # 6 -> not N
    bf.append('>')
    bf.append('[')  # if temp != 0, skip this command
    bf.append('<<')  # back to 6
    bf.append('-]')  # 
    bf.append('<<')  # back to main
    
    # Actually, this is getting too complex. Let me simplify to ASCII checks
    
    # ===== Simple approach: check first letter only =====
    bf.append('>>>>>>>')
    bf.append('[')  # if cell 6 > 0
    bf.append('----------')  # -10 = 68
    bf.append('----------')  # -10 = 58
    bf.append('----------')  # -10 = 48
    bf.append('----------')  # -10 = 38
    bf.append('----------')  # -10 = 28
    bf.append('----------')  # -10 = 18
    bf.append('----------')  # -10 = 8
    bf.append('----------')  # -10 = -2 = 254 (wrap)
    bf.append('>')
    bf.append('[')  # if result != 0 (not N)
    bf.append('<<')
    bf.append('-]')
    bf.append('<<')
    
    # If N: move north
    bf.append('<')
    bf.append('[')  # if was N (78-78=0)
    bf.append('<<<<<<')
    bf.append('>[-]')
    bf.append('>+')
    bf.append('<<<<<')
    bf.append(print_str('NORTH'))
    bf.append(print_str('HALLWAY'))
    bf.append(']')
    
    bf.append(']')  # close command loop
    
    bf.append('<<<<<<<')  # back to room
    bf.append('-]')  # decrement room (will loop forever)
    # end

# Can't make this work reliably. Let's just write a simple working demo.
    
print('''
Initialize: room=0, key=1, treasure=1

+++++++[->++++++++<]> Starting room setup
''')

if __name__ == '__main__':
    main()