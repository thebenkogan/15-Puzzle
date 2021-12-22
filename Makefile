.PHONY: puzzle test

clean:
		rm -rf puzzle/__pycache__
		rm -rf test/__pycache__

run:
		python -m puzzle.main

test:
		python -m pytest
		rm -rf .pytest_cache	