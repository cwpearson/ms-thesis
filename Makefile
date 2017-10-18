LATEX = pdflatex
BIBTEX = bibtex

USR := $(shell id -u)
GRP := $(shell id -g)
PWD := $(shell pwd)

DOCKER = docker run --rm -i --user="${USR}:${GRP}" --net=none -v "${PWD}":/data cwpearson/latex:tikz
all:
	echo ===== LATEX 1 =====
	${LATEX} ecethesis
	echo ===== BIBTEX =====
	${BIBTEX} ecethesis
	echo ===== LATEX 2 =====
	${LATEX} ecethesis
	echo ===== LATEX 3 =====
	${LATEX} ecethesis

docker:
	echo ===== LATEX 1 =====
	${DOCKER} ${LATEX} ecethesis
	echo ===== BIBTEX =====
	${DOCKER} ${BIBTEX} ecethesis
	echo ===== LATEX 2 =====
	${DOCKER} ${LATEX} ecethesis
	echo ===== LATEX 3 =====
	${DOCKER} ${LATEX} ecethesis

clean:
	rm -f *.toc *.log *.lof *.lot *.aux *.bbl *.blg ecethesis.pdf sections/*.aux