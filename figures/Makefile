
TARGETS =

CSV_FILES =

GEN_DIR = generated

# handle SVGs
SVG_FILES=$(wildcard *.svg)
GEN_FILES := $(patsubst %.svg, $(GEN_DIR)/%.pdf, ${SVG_FILES})

# handle DOT
DOT_FILES=$(wildcard *.dot)
GEN_FILES += $(patsubst %.dot, $(GEN_DIR)/%.pdf, ${DOT_FILES})


TARGETS += $(GEN_FILES)


# Handle Plot3 YMLs
PLOT3_CSVS = $(wildcard ../data/plot3/*.csv)
PLOT3_YMLS = $(wildcard ../data/plot3/*.yml)
PLOT3_PDFS = $(patsubst ../data/plot3/%.yml, $(GEN_DIR)/%.pdf, ${PLOT3_YMLS})
TARGETS += $(PLOT3_PDFS)

# Handle microbench YMLs
MICRO_JSONS = $(wildcard ../data/microbench/*.json)
MICRO_YMLS = $(wildcard ../data/microbench/*.yml)
MICRO_PDFS = $(patsubst ../data/microbench/%.yml, $(GEN_DIR)/%.pdf, ${MICRO_YMLS})
TARGETS += $(MICRO_PDFS)

all: $(TARGETS)

$(GEN_DIR):
	[ -d $(GEN_DIR)] || mkdir -p $(GEN_DIR)

$(GEN_DIR)/%.pdf: %.dot $(GEN_DIR)
	dot -Tpdf $< -o $@

$(GEN_DIR)/%.pdf: %.svg $(GEN_DIR)
	inkscape -D -z --file=$< --export-pdf=$@

$(GEN_DIR)/%.pdf: $(REGPLOT_DIR)/%.csv $(GEN_DIR) $(REGPLOT_DIR)/plot.py
	python $(REGPLOT_DIR)/plot.py $< $@

#plot3
$(GEN_DIR)/%.pdf: ../data/plot3/%.yml $(GEN_DIR) ../data/plot3/plot.py $(PLOT3_CSVS)
	python ../data/plot3/plot.py $@ $<

# microbench
$(GEN_DIR)/%.pdf: ../data/microbench/%.yml $(GEN_DIR) ../data/microbench/plot.py $(MICRO_JSONS)
	../data/microbench/plot.py $@ $<

clean:
	rm -f $(TARGETS) $(GEN_DIR)/*.pdf