# Zork in Brainfuck - Transpiler Plan

## Overview
Build a Python-to-Brainfuck transpiler that targets a minimal Zork-style game.

## Selected Approach
- **Transpiler**: Python subset → Brainfuck (minimal: while loops, arrays, no functions)
- **Game scope**: 2-3 rooms, 1-2 items, basic navigation
- **Verification**: Run generated BF and verify output matches expected behavior

---

## Phase 1: Transpiler Infrastructure

### Goal
Create a working transpiler that can generate valid, runnable Brainfuck code.

### Python Subset to Support
- Integer variables (byte cells, 0-255)
- While loops with [ ]
- Print statements (ASCII output via .)
- Input via ,
- Array access with index
- Simple arithmetic: +, -, assignment

### Transpiler Components
1. **Lexer** - Tokenize subset Python
2. **Parser** - Build AST (very simple)
3. **Code Generator** - Emit Brainfuck

### Verification Gate 1: Hello World
- [x] Transpiler accepts `print("Hello")` 
- [x] Generates valid BF that runs without errors
- [x] Output is "Hello"
- [x] **COMMIT** (done: 935a731)

### Current Status
- Transpiler: print() works
- BF Interpreter: Python-based bf.py works
- Game Generator: gen_game_v4.py produces BF but has logic issues

---

## Phase 2: Game Logic in Python Subset

### Goal
Express the Zork game logic in the Python subset.

### Game Design (Minimal)
```
Rooms (3):
- Room 0: Start (Dark Room) - has rusty key
- Room 1: Hallway (connects to 0 and 2)  
- Room 2: Treasure Room - has golden treasure

Commands:
- N/S/E/W - movement
- LOOK - describe current room
- TAKE [item] - pick up item
- QUIT - exit game

Win condition: Take treasure from room 2
```

### Implementation as Python Subset
```python
# Memory layout:
# cell 0: current_room (0-2)
# cell 1: has_key (0/1)
# cell 2: has_treasure (0/1)
# cell 3: key_in_room (0/1) - for room 0
# cell 4: treasure_in_room (0/1) - for room 2

while running:
    print("COMMAND? ")
    cmd = input()
    if cmd == "N":
        # Move north logic
    elif cmd == "S":
        # Move south logic
```

### Verification Gate 2: Game Logic
- [ ] Transpiler handles while loops, if-else, print, input
- [ ] Generated BF runs without crashes
- [ ] Game starts and shows prompt
- [ ] **COMMIT**

---

## Phase 3: Game Feature Tests

### Verification Gate 3: Navigation
- [ ] Player can type "N" to move from room 0 to room 1
- [ ] Player can type "S" to move from room 1 to room 2
- [ ] Player can type "W" to go back
- [ ] Room descriptions appear correctly

### Verification Gate 4: Items
- [ ] LOOK shows "rusty key" in room 0
- [ ] TAKE KEY picks up key
- [ ] TAKE TREASURE in room 2 triggers win message
- [ ] Items disappear after taken

### Verification Gate 5: Win Condition
- [ ] Taking treasure prints "YOU WIN!"
- [ ] Game can be quit with QUIT
- [ ] **COMMIT**

---

## File Structure
```
zork-bf/
├── PLAN.md                    # This plan
├── transpiler/
│   ├── __init__.py
│   ├── lexer.py              # Tokenizer
│   ├── parser.py             # AST builder  
│   └── codegen.py            # BF code generator
├── game.py                   # Game in Python subset
└── run.py                    # CLI entry point
```

## Success Criteria
1. Transpiler generates valid BF (no bracket errors)
2. All 5 verification gates pass
3. Game is playable with 3 rooms, 2 items, 5 commands
4. Win condition reachable