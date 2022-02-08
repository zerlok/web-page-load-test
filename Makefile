GECKODRIVER_VERSION ?= v0.30.0
GECKODRIVER_ARCHIVE ?= geckodriver-$(GECKODRIVER_VERSION)-linux64.tar.gz
GECKODRIVER_DOWNLOAD_PATH ?= https://github.com/mozilla/geckodriver/releases/download/$(GECKODRIVER_VERSION)/$(GECKODRIVER_ARCHIVE)


geckodriver:
	wget -q $(GECKODRIVER_DOWNLOAD_PATH)
	tar xzf $(GECKODRIVER_ARCHIVE)
	rm $(GECKODRIVER_ARCHIVE)

install: geckodriver
	echo ok

.PHONY: clean
clean:
	rm geckodriver

.PHONY: all
all: clean install
