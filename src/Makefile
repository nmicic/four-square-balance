# Linux / GCC (default):
#     make            # builds foursquare
#     make check      # self-checks + independent b-file regression gate
# macOS / Apple Clang needs libomp (brew install libomp):
#     make CC=clang CFLAGS="-O3 -Wall -Xpreprocessor -fopenmp \
#         -I$(brew --prefix libomp)/include -L$(brew --prefix libomp)/lib -lomp"

CC      ?= cc
CFLAGS  ?= -O3 -Wall -march=native -flto -fopenmp
LDLIBS  ?= -lm

all: foursquare

foursquare: foursquare.c
	$(CC) $(CFLAGS) -o foursquare foursquare.c $(LDLIBS)

# Regression gate:
#   1. engine self-consistency,
#   2. independent check of a(n) against a committed A122921-prefix fixture.
check: foursquare
	./foursquare --check
	@echo "independent gate: a(n) engine vs committed b-file (n=1..50)"
	@for n in $$(seq 1 50); do \
	  got=`./foursquare $$n | sed -n 's/.*a(n)=\([0-9]*\).*/\1/p'`; \
	  want=`sed -n '/^[0-9]/p' ../data/a122921_prefix_50.txt | sed -n "$${n}p" | awk '{print $$2}'`; \
	  [ "$$got" = "$$want" ] || { echo "MISMATCH n=$$n got=$$got want=$$want"; exit 1; }; \
	done; echo "b-file gate OK (1..50)"

clean:
	rm -f foursquare

.PHONY: all check clean
