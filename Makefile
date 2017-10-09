LATEX = pdflatex
BIBTEX = bibtex

all:
	echo ===== LATEX 1 =====
	${LATEX} ecethesis
	echo ===== BIBTEX =====
	${BIBTEX} ecethesis
	echo ===== LATEX 2 =====
	${LATEX} ecethesis
	echo ===== LATEX 3 =====
	${LATEX} ecethesis

clean:
	rm -f *.toc *.log *.lof *.lot *.aux *.bbl *.blg ecethesis.pdf sections/*.aux