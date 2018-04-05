
TARGETS = \
minsky-topo-hardware.pdf \
minsky-topo-cuda-simple.pdf \
minsky-topo-cuda-detail.pdf \

all: $(TARGETS)

%.pdf: %.dot
	dot -Tpdf $< -o $@

clean:
	rm -f $(TARGETS)