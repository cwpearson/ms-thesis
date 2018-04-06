
TARGETS = \
app-abstraction.pdf \
minsky-topo-hardware.pdf \
minsky-topo-cuda-simple.pdf \
minsky-topo-cuda-detail.pdf \
x86-kepler-bw.pdf \
x86-pascal-bw.pdf \
p8-pascal-bw.pdf \
p9-volta-bw.pdf \


all: $(TARGETS)

%.pdf: %.dot
	dot -Tpdf $< -o $@

%.pdf: %.svg
	inkscape -D -z --file=$< --export-pdf=$@
	# inkscape -D -z --file=$< --export-pdf=$@ --export-latex

clean:
	rm -f $(TARGETS)