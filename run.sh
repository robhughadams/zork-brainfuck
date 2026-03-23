#!/bin/bash
# Zork in Brainfuck - Runner Script
# Requires a Brainfuck interpreter

echo "Installing brainfuck interpreter..."

# Try to install brainfuck
if command -v apt-get &> /dev/null; then
    sudo apt-get update 2>/dev/null || true
    sudo apt-get install -y brainfuck 2>/dev/null || true
fi

# Check for brainfuck interpreter
if command -v bf &> /dev/null; then
    echo "Running Zork in Brainfuck..."
    bf game.bf
else
    echo "Brainfuck interpreter not found."
    echo "Install with: sudo apt-get install brainfuck"
    echo "Or try an online interpreter at https://brainfuck.org/"
fi