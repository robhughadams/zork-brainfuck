.PHONY: all test build run clean preprocess build-zorkpy run-zorkpy

PYTHON = python3
VENV_PY = venv/bin/python
TEST = venv/bin/pytest

all: build

test:
	$(TEST) tests/ -v

build: game/game.pre.py
	$(VENV_PY) -m src.transpile < game/game.pre.py > game.bf

preprocess: game/game.pre.py

game/game.pre.py: game/game.py src/preprocess.py
	$(VENV_PY) src/preprocess.py game/game.py

run: game.bf
	beef game.bf

build-zorkpy: vendor/zork-py/zork.pre.py
	$(VENV_PY) -m src.transpile < vendor/zork-py/zork.pre.py > vendor/zork-py/zork.bf

vendor/zork-py/zork.pre.py: vendor/zork-py/zork.py src/preprocess.py
	$(VENV_PY) src/preprocess.py vendor/zork-py/zork.py

run-zorkpy: vendor/zork-py/zork.bf
	beef vendor/zork-py/zork.bf

clean:
	rm -f game/game.pre.py game.bf vendor/zork-py/zork.pre.py vendor/zork-py/zork.bf
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
