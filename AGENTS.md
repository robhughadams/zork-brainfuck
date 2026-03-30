# Agent Workflow

This document describes the agents and workflows used in this project.

## Main Agent (opencode)

The primary agent handles all software engineering tasks including:
- Writing and modifying code
- Running tests
- Committing and pushing changes
- Searching the codebase

## Workflow Rules

1. **Always use TDD** - Tests must pass before committing
2. **Commit after each verification gate** - Don't batch multiple changes
3. **Use Python virtual environment** - Always use `venv/bin/python` or `venv/bin/pytest`
4. **Keep intermediate files** - Preserve .bf and .pre.py files in repo
5. **Default branch is main** - Not master
6. **Update docs when stopping** - Document progress/findings in PLAN.md before ending session

## Build Pipeline

```
game.py → src/preprocess.py → game.pre.py → [py_compile verify] → src/transpile.py → game.bf
```

## Commands

```bash
# Run tests
make test
# or: venv/bin/pytest tests/ -v

# Build game
make build

# Preprocess only (no transpile)
make preprocess

# Run game (uses beef interpreter)
make run

# Build/run vendor zork-py game
make build-zorkpy
make run-zorkpy

# Clean generated files
make clean
```

## Testing

- Tests are in `tests/` directory
- Use `venv/bin/pytest` for running tests
- New features require tests before commit

## Git Workflow

1. Make changes
2. Run tests to verify
3. Commit with descriptive message
4. Push to origin/main

## Known Limitations

- If statements in Brainfuck are complex (require equality comparison)
- While loops must decrement counter in body
- Some Python features require lowering in preprocessor

## Active TODOs (from PLAN.md)

### High Priority (In Progress)
- Implement `if/elif/else` statements - preprocessor support added, BF equality check pending
- Support `while x == n:` comparison in loop condition - preprocessor support added
- **String handling**: Phase 1 in progress - debugging string storage/print pointer navigation

### Medium Priority
- Support string methods like `.lower()`
- Support `input("prompt")` with prompt argument
- Support `input().lower()` chaining
- Support string equality `s == "text"`

### Lower Priority
- Support `break` statement
- Support nested input in conditionals
- Optimize BF output size

### Recent Progress (2026-03-29)
- Fixed preprocess.py bugs: tab vs space indentation causing build crashes
- Full toolchain works: `make build build-zorkpy test` passes (30 tests)
- Created tests/test_strings.py with 20 TDD test cases across 4 phases
- Started implementing string handling in src/transpile.py

### String Implementation Progress (2026-03-29)

**Phase 1 COMPLETE** - String literal variables (8/8 tests passing):
- Fixed `self.var_count` bug in transpile.py (line 242)
- Fixed pointer navigation for `print(s)` 
- All TestStringLiterals tests pass

**Phase 2-4**: Not yet implemented:
- Phase 2: String concatenation (`"a" + "b"`) - needs preprocessor support
- Phase 3: `len(s)`, `s[0]` - needs transpiler support
- Phase 4: String input - needs transpiler support

**Current test status**: 9/20 passing (Phase 1 + 1 other)

---

## Session 2026-03-29 (continued)

### Completed Fixes

1. **Fixed `chr(n + 48)` support** (transpile.py):
   - Added patterns for `print(chr(var + n))` and `print(chr(n + var))`
   - This fixed test_len_simple and test_len_empty

2. **Fixed string concat with variable** (preprocess.py):
   - Added handler for `print("literal" + var)` and `print(var + "literal")`
   - Converts to two separate print statements
   - This fixed test_input_echo

3. **Fixed base_cell bug** (transpile.py):
   - Changed `current_pos = var_count + 1` to `current_pos = 0`
   - After initialization, pointer should return to cell 0
   - This fixed 12 failing tests (numeric operations)

4. **Fixed input() type inference** (transpile.py):
   - Added two-pass variable collection
   - First pass: collect explicit variables (strings, numbers)
   - Second pass: analyze input() usage to determine type (string vs numeric)
   - Handles both `x = input(); print(chr(x))` (numeric) and `s = input(); print(s)` (string)

### Bstr Structure (ASCII only)

Current bstr format (length-prefixed, ASCII):
```
Cell X:   length (n)
Cell X+1: char[0]
Cell X+2: char[1]
...
Cell X+n: char[n-1]
```

Verified working for lengths: 20, 100, 2000 chars.

**ASCII only**: Uses `ord(char)` which naturally handles ASCII (0-127). 
Strings with non-ASCII chars will have unexpected behavior (UTF-8 encoding not handled).

### Test Status

**All 61 tests passing**, 12 skipped:
- 20/20 string tests passing
- All numeric tests passing
- 12 tests skipped (feature not yet implemented)
