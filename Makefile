.PHONY: all clean install  help

PYTHON = python
VENV_DIR = .cip

ifeq ($(OS),Windows_NT)
    VENV_PY = $(VENV_DIR)/Scripts/python.exe
else
    VENV_PY = $(VENV_DIR)/bin/python
endif


all : help

help :
	@echo "Available target :"
	@echo "  make install             - Install project dependencies and set up environment"

install :
	@echo "Installing project dependencies and setting up environment..."
	@echo "Creating virtual environment..."
	@$(PYTHON) -m venv $(VENV_DIR)
	@echo "Installing dependencies into virtual environment..."
	@$(VENV_PY) -m pip install --upgrade pip
	@$(VENV_PY) -m pip install .
	@echo "Installation completed successfully!"
ifeq ($(OS),Windows_NT)
	@echo "To activate the virtual environment, run: .cip\Scripts\activate"
else
	@echo "To activate the virtual environment, run: source .cip/bin/activate"
endif

