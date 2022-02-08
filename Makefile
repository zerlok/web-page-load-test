SHELL := /bin/bash

DRIVERS_DIR ?= drivers

GECKODRIVER_VERSION ?= v0.30.0
GECKODRIVER_ARCHIVE ?= geckodriver-$(GECKODRIVER_VERSION)-linux64.tar.gz
GECKODRIVER_DOWNLOAD_PATH ?= https://github.com/mozilla/geckodriver/releases/download/$(GECKODRIVER_VERSION)/$(GECKODRIVER_ARCHIVE)

$(DRIVERS_DIR):
	mkdir $(DRIVERS_DIR)

$(DRIVERS_DIR)/geckodriver: $(DRIVERS_DIR)
	wget -q $(GECKODRIVER_DOWNLOAD_PATH)
	tar xzf $(GECKODRIVER_ARCHIVE) -C $(DRIVERS_DIR)
	rm $(GECKODRIVER_ARCHIVE)
	chmod +x $(DRIVERS_DIR)/geckodriver

.venv/:
	poetry install

install: $(DRIVERS_DIR)/geckodriver .venv/

.PHONY: clean
clean:
	if [[ -d $(DRIVERS_DIR) ]]; then rm -r $(DRIVERS_DIR); fi

.PHONY: benchmark
benchmark:
	PATH=$(PATH):$(DRIVERS_DIR) poetry run pytest --benchmark-only

.PHONY: all
all: clean install benchmark
