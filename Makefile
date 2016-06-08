topdir = $(shell pwd)
prefix ?= /usr/local

TEST_RUN_FOLDER = $(topdir)/tests/run
TEST_OUTPUT_FILE = $(topdir)/tests/run/case1/output.txt
EXPECT_OUTPUT_TEMPLATE = $(topdir)/tests/expect_template.output
EXPECT_OUTPUT_FILE = $(topdir)/tests/expect.output

SKULLFT_BINPATH=$(topdir)/src
export SKULLFT_BINPATH

check:
	./src/skull-ft ./tests
	cd tests && sed 's|$${prefix}|$(topdir)|g' $(EXPECT_OUTPUT_TEMPLATE) > $(EXPECT_OUTPUT_FILE)
	diff -u $(EXPECT_OUTPUT_FILE) $(TEST_OUTPUT_FILE) && echo "Test Done"

install:
	cp src/skull-ft src/skull-case-executor.py $(prefix)/bin

clean:
	rm -rf $(TEST_RUN_FOLDER) $(EXPECT_OUTPUT_FILE)
