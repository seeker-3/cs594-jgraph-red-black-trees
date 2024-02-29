from sys import argv

from red_black_tree import RedBlackTree
from re import split
from typing import Literal
from shell import bash


def get_operations():
    input_filename = argv[1]

    with open(input_filename, "r") as file:
        tokens = split(r"\s+", file.read())
        operations = list[tuple[Literal["i", "d"], int]]([])

        for operation, value in zip(tokens[::2], tokens[1::2]):
            if operation == "i" or operation == "d":
                operations.append((operation, int(value)))

        return operations


def main():
    if len(argv) != 2:
        print("Usage: python3 main.py <input_file>")
        exit(1)

    operations = get_operations()
    tree = RedBlackTree()

    for operation, value in operations:
        match operation:
            case "i":
                tree.insert(value)
            case "d":
                tree.delete(value)
            case _:
                print("Invalid operation")
                exit(1)

    print("Creating gif...")
    bash("convert -delay 150 -loop 0 jpg/* rb-tree.gif")


if __name__ == "__main__":
    main()
