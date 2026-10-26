VENV = src/.venv
PIP = $(VENV)/bin/pip
RUFF = $(VENV)/bin/ruff

.PHONY: check format run

$(RUFF): src/pyproject.toml
	python3 -m venv $(VENV)
	$(PIP) install ./src
	@touch $(RUFF)

check: $(RUFF)
	$(RUFF) check src
	$(RUFF) format --check src

format: $(RUFF)
	$(RUFF) check --fix src
	$(RUFF) format src

run: $(RUFF)
	cd src && .venv/bin/uvicorn app.main:app --reload
