topdir = $(shell pwd)
prefix ?= /usr/local

TEST_OUTPUT_FILE = $(topdir)/tests/test.output

SKULLFT_BINPATH=$(topdir)/src
export SKULLFT_BINPATH

check:
	./src/skull-ft ./tests > $(TEST_OUTPUT_FILE) 2>&1
	diff -u tests/expect.output $(TEST_OUTPUT_FILE) && echo "Test Done"

install:
	cp src/skull-ft src/skull-case-executor.py $(prefix)/bin

clean:
	rm -f $(TEST_OUTPUT_FILE)
