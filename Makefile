.PHONY: run clean


run:
	python3.11 src/main.py data/data2.txt

clean:
	rm -rf jgr jpg pdf ps rb-tree.gif
