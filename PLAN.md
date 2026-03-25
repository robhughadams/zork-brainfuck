# Zork in Brainfuck

A Zork-style text adventure game written entirely in Brainfuck, built via a Python-to-BF transpiler.

## License

GPL v3 - see LICENSE file

## Overview

- **Transpiler**: Python subset → Brainfuck
- **Pre-processor**: Converts `for` loops to `while` loops
- **Game**: 3-room adventure with key, door, treasure

## Build Pipeline

```
game.py → src/preprocess.py → game.pre.py → [py_compile verify] → src/transpile.py → game.bf
```

## Project Structure

```
zork-bf/
├── LICENSE                    # GPL v3
├── PLAN.md                    # This plan
├── README.md
├── .gitignore
├── game.bf                    # Compiled game
├── game/
│   ├── __init__.py
│   ├── game.py              # Game source
│   └── game.pre.py          # Preprocessed
├── src/
│   ├── __init__.py
│   ├── bf.py               # BF interpreter
│   ├── preprocess.py        # For loop → while
│   └── transpile.py         # Main transpiler
└── tests/
    └── ... (test files)
```

## Features

### Transpiler
- `print("text")` - string literals
- `print(chr(x))` / `print(chr(65))` - char output
- `x = 5`, `x = x + 1`, `x = x - 1` - variables
- `x = input()` - character input
- `while x > 0:` - loops (body must decrement)
- `for i in range(n):` - via preprocessor

### Known Limitations
- If statements cause infinite loops (not implemented)
- While loops require body to decrement counter

## TODO: Features Needed to Compile zork-py

### High Priority
- [ ] **TODO**: Implement `if/elif/else` statements - current implementation causes infinite loops
- [ ] **TODO**: Support `while x == n:` comparison in loop condition
- [ ] **TODO**: Support `while True:` infinite loop
- [ ] **TODO**: Support `exit()` function call

### Medium Priority
- [ ] **TODO**: Support string methods like `.lower()`
- [ ] **TODO**: Support `input("prompt")` with prompt argument
- [ ] **TODO**: Support `input().lower()` chaining
- [ ] **TODO**: Support string equality `s == "text"`

### Lower Priority
- [ ] **TODO**: Support `break` statement
- [ ] **TODO**: Support nested input in conditionals
- [ ] **TODO**: Optimize BF output size (current: 226KB for simple game)

## Tests

28 tests passing

## Usage

```bash
# Pre-process
python src/preprocess.py game/game.py

# Verify valid Python
python -m py_compile game/game.pre.py

# Transpile
python src/transpile.py < game/game.pre.py > game.bf

# Run
python src/bf.py game.bf
```
