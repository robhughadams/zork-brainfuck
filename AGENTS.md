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

# Run game
make run
# or: make run-python

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
