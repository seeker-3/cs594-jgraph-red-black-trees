# JGraph Red Black Tree GIF Creator

![Red Black Tree](example.gif)

## Usage

Input file in the form of `i|d number`, where `i` and `d` are the operations insert and delete, followed by a number, separated by any amount of whitespace.

For example:

```txt
i 20
i 10
i 30
i 5
i 15
d 20
d 30
```

Some input files are in the `data` directory. The data is limited to about 16 nodes for the best visualization.

## Usage

```bash
python3.11 main.py data/data1.txt
```

or use the makefile

```bash
make
```

This will create a gif called `rb-tree.gif` in the root directory.

To clean run

```bash
make clean
```

## Sources

I started with the following red-black tree implementation:

- [Red-Black Tree](https://github.com/msambol/dsa/blob/master/trees/red_black_tree.py)
