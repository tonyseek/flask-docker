COMMANDS = help test release build clean
.PHONY: $(COMMANDS)

help:
	@echo "# You may need to 'pip install tox twine'."
	@echo
	@echo "available commands: $(COMMANDS)"

test:
	tox

release: clean build
	twine upload dist/*.{tar.gz,whl}

build:
	python setup.py sdist bdist_wheel

clean:
	rm -rf dist
