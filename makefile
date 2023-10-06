CODE = executor\
       helper\
       intents\
       logger\
       rugpt3\
       tts

VENV = .venv
PYTHON_VERSION = 3.11

.create-venv:
	test -d $(VENV) || python$(PYTHON_VERSION) -m venv $(VENV)
	$(VENV)/bin/python -m pip install --upgrade pip
	$(VENV)/bin/python -m pip install poetry

init:
	make .create-venv
	$(VENV)/bin/python -m poetry install

lint:
	$(VENV)/bin/python -m black $(CODE)
	$(VENV)/bin/python -m isort $(CODE)
	$(VENV)/bin/python -m pylint disable=missing-module-docstring $(CODE)

start:
	$(VENV)/bin/python -m /voice_assistant/executor/run