#!/usr/bin/env python3
"""Simple game test - just print something"""
def p(s):
    for c in s:
        print('[-]')
        print('+' * ord(c))
        print('.')

p('HI')
print('[,]')  # Simple input loop