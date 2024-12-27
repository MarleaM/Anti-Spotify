VENV = .venv
REQUIREMENTS = requirements.txt

ifeq ($(OS),Windows_NT)
  PYTHON = $(VENV)\\Scripts\\python.exe
  PIP = $(VENV)\\Scripts\\pip.exe
  RM = del /Q
  RMDIR = rmdir /S /Q
else
  PYTHON = $(VENV)/bin/python
  PIP = $(VENV)/bin/pip
  RM = rm -f
  RMDIR = rm -rf
endif

.PHONY: all
all: run

$(VENV)/bin/activate: 
	python3 -m venv $(VENV)

.PHONY: install
install: $(VENV)/bin/activate
	$(PIP) install -r $(REQUIREMENTS)

.PHONY: run
run: $(VENV)/bin/activate
	$(PYTHON) backend.py $(RUN_ARGS)

.PHONY: clean
clean:
	$(RMDIR) $(VENV)
	$(RM) *.pyc
	$(RM) -r __pycache__
