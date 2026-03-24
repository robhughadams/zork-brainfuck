# Zork in Brainfuck - Transpiler Plan

## Overview
Build a Python-to-Brainfuck transpiler that targets a minimal Zork-style game.

## Selected Approach
- **Transpiler**: Python subset → Brainfuck (minimal: while loops, arrays, no functions)
- **Pre-processor**: Converts `for` loops to `while` loops as intermediate step
- **Game scope**: 2-3 rooms, 1-2 items, basic navigation
- **Verification**: Run generated BF and verify output matches expected behavior

---

## Phase 1: Transpiler Infrastructure

### Goal
Create a working transpiler that can generate valid, runnable Brainfuck code.

### Python Subset to Support
- Integer variables (byte cells, 0-255)
- While loops with [ ]
- For loops (pre-processed to while)
- Print statements (ASCII output via .)
- Input via ,
- Array access with index
- Simple arithmetic: +, -, assignment

### Build Pipeline
```
game.py → [preprocess.py] → game.pre.py → [verify py_compile] → [transpile.py] → game.bf
```

### Pre-processor: for loops → while loops
- **Input:** `for i in range(3):`
- **Output:**
  ```python
  i = 3
  while i > 0:
      # body
      i = i - 1
  ```
- **Intermediate file:** `game.pre.py` (for inspection)
- **Build gate:** `python -m py_compile game.pre.py` must pass

### Transpiler Components
1. **Pre-processor** - Convert for loops to while loops
2. **Verifier** - py_compile check (BUILD GATE)
3. **Transpiler** - Python subset → Brainfuck

### Verification Gate 1: Hello World
- [x] Transpiler accepts `print("Hello")` 
- [x] Generates valid BF that runs without errors
- [x] Output is "Hello"
- [x] **COMMIT** (done: 935a731)

---

## Phase 2: For Loop Pre-processor

### Goal
Add `for i in range(n):` support via pre-processing.

### Implementation
1. Create `preprocess.py`
2. Parse source for `for (\w+) in range\((\d+)\):` pattern
3. Convert to: `i = n` + `while i > 0:` + body + `i = i - 1`
4. Write intermediate `.pre.py` file
5. Verify with `python -m py_compile` (BUILD GATE)

### Verification Gate 2: For Loops
- [x] Pre-processor converts for → while correctly
- [x] Intermediate .pre.py is valid Python (py_compile passes)
- [x] Generated BF runs correctly
- [ ] **COMMIT**

---

## Phase 3: Game Logic in Python Subset

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
- [x] Transpiler handles while loops, print, input
- [x] Generated BF runs without crashes
- [x] Game starts and shows prompt
- [x] **COMMIT** (done: 59362cc)

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