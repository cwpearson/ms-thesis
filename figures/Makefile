
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

PLOT2_TARGETS = \
../data/plot2/pageable_cpu0-gpu0.pdf \
../data/plot2/pinned_cpu0-gpu0.pdf \
../data/plot2/wc_cpu0-gpu0.pdf \
../data/plot2/minsky_pageable_cpu0-gpus.pdf \
../data/plot2/minsky_pageable_cpu1-gpus.pdf \
../data/plot2/minsky_pageable_cpu1-gpu01.pdf \
../data/plot2/minsky_memcpy_local.pdf \
../data/plot2/hal_peer_local.pdf \
../data/plot2/hal_peer_remote.pdf \
../data/plot2/minsky_nopeer_remote.pdf \
../data/plot2/minsky_path_gpu2-gpu0.pdf \
../data/plot2/minsky_path_gpu0-gpu2.pdf \
../data/plot2/hal_nopeer_remote.pdf \
../data/plot2/hal_nopeer_identical-local.pdf \
../data/plot2/hal_nopeer_identical-remote.pdf \
../data/plot2/minsky_nopeer_identical-local.pdf \
../data/plot2/minsky_nopeer_identical-remote.pdf \
../data/plot2/minsky_pinned_cpu0-local.pdf \
../data/plot2/minsky_wc_cpu0-local.pdf \
../data/plot2/minsky_pageable_affinity.pdf \
../data/plot2/hal_pageable_affinity.pdf \
../data/plot2/minsky_pinned_affinity_cpu0.pdf \
../data/plot2/minsky_pinned_affinity_cpu1.pdf \
../data/plot2/hal_pinned_affinity.pdf \
../data/plot2/minsky_pageable_cpu0-gpus.pdf \
../data/plot2/minsky_pageable_cpu1-gpus.pdf \
../data/plot2/minsky_pageable_gpus-cpu0.pdf \
../data/plot2/minsky_pageable_gpus-cpu1.pdf \
../data/plot2/minsky_pageable_gpu02-cpu01.pdf \
../data/plot2/s822lc_cpu0-cpu1-src.pdf \
../data/plot2/s822lc_cpu0-cpu1-dst.pdf

PLOT2_CSVS = $(wildcard ../data/plot2/*.csv)


all: $(TARGETS) plot2

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


../data/plot2/%.pdf: ../data/plot2/plots.yml $(PLOT2_CSVS)
	../data/plot2/plot.py $@ $<

.PHONY: plot2
plot2: $(PLOT2_TARGETS)
		cp ../data/plot2/*.pdf generated/.

clean:
	rm -f $(TARGETS) $(GEN_DIR)/*.pdf ../data/plot2/*.pdf