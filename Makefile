NAME = a_maze_ing

GREEN = \033[0;32m
BLUE = \033[0;34m
RESET = \033[0m

VENV = maze_env
PYTHON = ${VENV}/bin/python3
PIP = ${VENV}/bin/pip
STAMP = ${VENV}/.installed
FLAKE8 = ${VENV}/bin/flake8
MYPY = ${VENV}/bin/mypy

FLAKE8_EXCLUDE = --extend-exclude=${VENV},build,dist
MYPY_EXCLUDE = --exclude '^(${VENV}|build|dist)/'
MYPY_FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

all: install-package

${VENV}:
	@python3 -m venv ${VENV}
	@echo "${GREEN}${VENV} successfully created${RESET}"

${STAMP}: requirements.txt | ${VENV}
	@echo "${BLUE}Installing requirements in $$(${PYTHON} -c 'import sys; print(sys.prefix)')${RESET}"
	@${PIP} install -r requirements.txt
	@touch ${STAMP}
	@echo "${GREEN}Requirements successfully installed/checked${RESET}"

install: ${STAMP}

build: install
	@rm -rf dist/
	@rm -f mazegen-*.whl mazegen-*.tar.gz
	@${PYTHON} -m build
	@cp dist/mazegen-*.whl .
	@echo "${GREEN}Mazegen successfully packaged${RESET}"

install-package: build
	@${PIP} install mazegen-*.whl
	@echo "${GREEN}Mazegen package successfully installed at: $$(${PIP} show mazegen | grep Location | cut -d' ' -f2)${RESET}"

run: install
	@echo "${BLUE}Using Python in ${VENV}: $$(${PYTHON} -c 'import sys; print(sys.prefix)')${RESET}"
	@echo "${BLUE}Generating maze...${RESET}"
	@${PYTHON} a_maze_ing.py config.txt

debug: install
	@echo "${BLUE}Debugging...${RESET}"
	@${PYTHON} -m pdb a_maze_ing.py config.txt

clean:
	@rm -rf .mypy_cache
	@rm -rf __pycache__
	@rm -rf mazegen/__pycache__
	@rm -rf mazegen/.mypy_cache
	@echo "${BLUE}Cache and extra directories successfully deleted${RESET}"

fclean: clean
	@rm -rf dist/ 
	@rm -rf build/ 
	@rm -rf mazegen.egg-info
	@rm -rf ${VENV}
	@rm -f maze.txt
	@echo "${BLUE}${VENV}, build artifacts and outputs successfully deleted${RESET}"

re: fclean all

lint: install
	@${FLAKE8} . ${FLAKE8_EXCLUDE}
	@${MYPY} . ${MYPY_EXCLUDE} ${MYPY_FLAGS}
	@echo "${GREEN}Flake8 and mypy successfully checked${RESET}"

lint-strict: install
	@${FLAKE8} . ${FLAKE8_EXCLUDE}
	@${MYPY} . ${MYPY_EXCLUDE} --strict
	@echo "${GREEN}Flake8 and mypy strict successfully checked${RESET}"

.PHONY: all install build install-package run debug clean fclean re lint lint-strict
