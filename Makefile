# Makefile for creating the Complete Greek Bible

PYTHON := python3
REPO_URL := https://github.com/eliranwong/SBLGNT-add-ons.git
REPO_DIR := SBLGNT-add-ons
SCRIPT := merge_bible.py

.PHONY: all clean complete-bible

all: complete-bible

complete-bible: $(REPO_DIR)
	@echo "Starting merge process..."
	$(PYTHON) $(SCRIPT)
	@echo "Done. Output file: CompleteGreekBible.SQLite3"

$(REPO_DIR):
	@echo "Cloning SBLGNT repository..."
	git clone $(REPO_URL)

clean:
	@echo "Cleaning up..."
	rm -f CompleteGreekBible.SQLite3
	@echo "Note: SBLGNT-add-ons directory was preserved. Remove manually if needed: rm -rf $(REPO_DIR)"