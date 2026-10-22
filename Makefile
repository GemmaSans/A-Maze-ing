NAME = a_maze_ing

GREEN = \033[0;32m
BLUE = \033[0;34m
RESET = \033[0m

VENV = maze_env
PYTHON = ${VENV}/bin/python3
PIP = ${VENV}/bin/pip
FLAKE8 = ${VENV}/bin/flake8
MYPY = ${VENV}/bin/mypy

MYPY_FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

all: install-package

venv:
	@python3 -m venv maze_env
	@echo "${GREEN}${VENV} successfully created${RESET}"

install: venv
	@${PIP} install -r requirements.txt
	@echo "${GREEN}Requirements successfully installed${RESET}"

build:
	@rm -rf dist/
	@${PYTHON} -m build
	@echo "${GREEN}Mazegen successfully packaged${RESET}"

install-package: install build
	@${PIP} install dist/mazegen-*.whl
	@echo "${GREEN}Mazegen package successfully installed${RESET}"

run:
	@echo "${BLUE}Generating maze...${RESET}"
	@${PYTHON} a_maze_ing.py config.txt

debug:
	@echo "${BLUE}Debugging...${RESET}"
	@${PYTHON} -m pdb a_maze_ing.py config.txt

clean:
	@rm -rf .mypy_cache
	@rm -rf __pycache__
	@rm -rf mazegen/__pycache__
	@rm -rf mazegen/.mypy_cache
	@rm -rf dist/ 
	@rm -rf build/ 
	@rm -rf mazegen.egg-info
	@echo "${BLUE}Cache and extra directories successfully deleted${RESET}"

fclean: clean
	@rm -rf maze_env
	@echo "${BLUE}${VENV} successfully deleted${RESET}"

lint:
	@${FLAKE8} .
	@${MYPY} . ${MYPY_FLAGS}
	@echo "${GREEN}Flake8 and mypy successfully checked${RESET}"

lint-strict: lint
	@${MYPY} . --strict
	@echo "${GREEN}Flake8 and mypy strict successfully checked${RESET}"

.PHONY: all venv install build install-package run debug clean lint lint-strict
