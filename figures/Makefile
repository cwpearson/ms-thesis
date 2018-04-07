
TARGETS = \
app-abstraction.pdf \
minsky-topo-hardware.pdf \
minsky-topo-cuda-simple.pdf \
minsky-topo-cuda-detail.pdf \
m2_um_cpu0-gpu0.pdf

all: $(TARGETS)

%.pdf: %.dot
	dot -Tpdf $< -o $@

%.pdf: %.svg
	inkscape -D -z --file=$< --export-pdf=$@
	# inkscape -D -z --file=$< --export-pdf=$@ --export-latex

%.pdf: ../data/%.csv
	python make_plot.py $< $@

clean:
	rm -f $(TARGETS)