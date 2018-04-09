
TARGETS =

DATA_DIR = ../data
GEN_DIR = generated
CSV_FILES=$(wildcard $(DATA_DIR)/*.csv)
SVG_FILES=$(wildcard *.svg)
DOT_FILES=$(wildcard *.dot)

GEN_FILES := $(patsubst $(DATA_DIR)/%.csv, $(GEN_DIR)/%.pdf, ${CSV_FILES})
GEN_FILES += $(patsubst %.svg, $(GEN_DIR)/%.pdf, ${SVG_FILES})
GEN_FILES += $(patsubst %.dot, $(GEN_DIR)/%.pdf, ${DOT_FILES})
TARGETS += $(GEN_FILES)

all: $(TARGETS)

generated:
	mkdir -p generated

generated/%.pdf: %.dot generated
	dot -Tpdf $< -o $@

generated/%.pdf: %.svg generated
	inkscape -D -z --file=$< --export-pdf=$@

generated/%.pdf: $(DATA_DIR)/%.csv generated make_plot.py $(DATA_DIR)/plots.yml
	python make_plot.py $< $@

clean:
	rm -f $(TARGETS) $(GEN_DIR)/*.pdf