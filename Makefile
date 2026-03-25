.PHONY: all test build run clean preprocess

PYTHON = python3
VENV_PY = venv/bin/python
TEST = venv/bin/pytest

all: build

test:
	$(TEST) tests/ -v

build: game/game.pre.py
	$(VENV_PY) -m src.transpile game/game.pre.py

preprocess: game/game.pre.py

game/game.pre.py: game/game.py src/preprocess.py
	$(VENV_PY) src/preprocess.py game/game.py

run: game.bf
	brainfuck game.bf

run-python: game.bf
	$(VENV_PY) src/bf.py game.bf

clean:
	rm -f game/game.pre.py game.bf
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
