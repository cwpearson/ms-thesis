
TARGETS = \
minsky-topo-actual.pdf \
minsky-topo-logical.pdf

all: $(TARGETS)

%.pdf: %.dot
	dot -Tpdf $< -o $@

clean:
	rm -f $(TARGETS)