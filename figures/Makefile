
TARGETS =

CSV_FILES =

GEN_DIR = generated

PLOT_DIR = ../data/plot
CSV_FILES += $(wildcard $(PLOT_DIR)/*.csv)

REGPLOT_DIR = ../data/regplot
CSV_FILES += $(wildcard $(REGPLOT_DIR)/*.csv)


GEN_FILES := $(patsubst $(PLOT_DIR)/%.csv, $(GEN_DIR)/%.pdf, ${CSV_FILES})
GEN_FILES := $(patsubst $(REGPLOT_DIR)/%.csv, $(GEN_DIR)/%.pdf, ${GEN_FILES})


SVG_FILES=$(wildcard *.svg)
DOT_FILES=$(wildcard *.dot)


GEN_FILES += $(patsubst %.svg, $(GEN_DIR)/%.pdf, ${SVG_FILES})
GEN_FILES += $(patsubst %.dot, $(GEN_DIR)/%.pdf, ${DOT_FILES})
TARGETS += $(GEN_FILES)

all: $(TARGETS)

$(GEN_DIR):
	mkdir -p $(GEN_DIR)

$(GEN_DIR)/%.pdf: %.dot $(GEN_DIR)
	dot -Tpdf $< -o $@

$(GEN_DIR)/%.pdf: %.svg $(GEN_DIR)
	inkscape -D -z --file=$< --export-pdf=$@

$(GEN_DIR)/%.pdf: $(PLOT_DIR)/%.csv $(GEN_DIR) $(PLOT_DIR)/plot.py $(PLOT_DIR)/plots.yml
	python $(PLOT_DIR)/plot.py $< $@

$(GEN_DIR)/%.pdf: $(REGPLOT_DIR)/%.csv $(GEN_DIR) $(REGPLOT_DIR)/plot.py
	python $(REGPLOT_DIR)/plot.py $< $@

clean:
	rm -f $(TARGETS) $(GEN_DIR)/*.pdf