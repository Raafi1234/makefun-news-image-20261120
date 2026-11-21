# Build the front page, then run the entry program the way the grader does.
.PHONY: run compose check clean

compose:
	python3 compose.py

run: compose
	mkdir -p out
	MAKEFUN_OUTPUT_DIR=out node main.ts

check: run
	python3 -c "from PIL import Image; im = Image.open('out/entry.png'); print(im.size, im.format)"
	ls -l out/entry.png entry.png
	cmp out/entry.png entry.png && echo "identical: OK"

clean:
	rm -rf out
