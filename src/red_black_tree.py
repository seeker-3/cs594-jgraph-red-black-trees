from collections import deque
from enum import Enum, auto
from dataclasses import dataclass
from re import T
from typing import TypeVar
from jgraph import JGraph

T = TypeVar("T")


def unwrap(node: T | None) -> T:
    assert node is not None
    return node


class Color(Enum):
    RED = auto()
    BLACK = auto()


@dataclass
class Node:
    key: int
    color: Color
    left: "Node | None" = None
    right: "Node | None" = None
    parent: "Node | None" = None


NIL = Node(
    key=-1,
    color=Color.BLACK,
)


class RedBlackTree:
    def __init__(self):
        self.root = NIL

    def left_rotate(self, x: Node):
        y = unwrap(x.right)
        z = unwrap(y.left)

        x.right = z

        if z != NIL:
            z.parent = x

        y.parent = x.parent

        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    def right_rotate(self, x: Node):
        y = unwrap(x.left)
        z = unwrap(y.right)

        x.left = z

        if z != NIL:
            z.parent = x

        y.parent = x.parent

        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y

        y.right = x
        x.parent = y

    def insert(self, key: int):
        z = Node(
            key,
            color=Color.RED,
            left=NIL,
            right=NIL,
        )

        y: Node | None = None
        x = self.root

        while x != NIL:
            y = x
            if z.key < x.key:
                x = unwrap(x.left)
            else:
                x = unwrap(x.right)

        z.parent = y
        if y is None:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z
        self.render(f"insert-{key}")
        self.insert_fixup(z)

    def insert_fixup(self, z: Node):
        while z.parent is not None and z.parent.color == Color.RED:

            assert z.parent.parent is not None

            if z.parent == z.parent.parent.left:
                y = unwrap(z.parent.parent.right)

                if y.color == Color.RED:
                    z.parent.color = Color.BLACK
                    y.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    z = z.parent.parent
                    self.render("insert-fixup-recolor")

                else:
                    if z == z.parent.right:
                        z = z.parent
                        self.left_rotate(z)

                    assert z.parent is not None
                    assert z.parent.parent is not None

                    z.parent.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    self.right_rotate(z.parent.parent)
                    self.render("insert-fixup-right-rotate")
            else:
                y = unwrap(z.parent.parent.left)

                if y.color == Color.RED:
                    z.parent.color = Color.BLACK
                    y.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    z = z.parent.parent
                    self.render("insert-fixup-recolor")
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self.right_rotate(z)

                    assert z.parent is not None
                    assert z.parent.parent is not None

                    z.parent.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    self.left_rotate(z.parent.parent)
                    self.render("insert-fixup-left-rotate")

            if z == self.root:
                break

        if self.root.color == Color.RED:
            self.root.color = Color.BLACK
            self.render("insert-fixup-recolor-root")

    def delete(self, key: int):
        z = self.search(key)

        if z == NIL:
            return

        y = z
        y_orig_color = y.color

        # case 1
        if z.left == NIL:
            x = unwrap(z.right)
            self.transplant(z, x)
        # case 2
        elif z.right == NIL:
            x = unwrap(z.left)
            self.transplant(z, x)
        # case 3
        else:
            assert z.right is not None
            y = self.minimum(z.right)
            y_orig_color = y.color
            x = unwrap(y.right)

            if y.parent == z:
                x.parent = y
            else:
                assert y.right is not None
                self.transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.transplant(z, y)
            y.left = z.left
            unwrap(y.left).parent = y
            y.color = z.color

        self.render(f"delete-{key}")
        if y_orig_color == Color.BLACK:
            self.delete_fixup(x)

    def delete_fixup(self, x: Node):
        while x != self.root and x.color == Color.BLACK:
            assert x.parent is not None
            if x == x.parent.left:
                w = unwrap(x.parent.right)

                # type 1
                if w.color == Color.RED:
                    w.color = Color.BLACK
                    x.parent.color = Color.RED
                    self.left_rotate(x.parent)
                    w = unwrap(x.parent.right)
                    self.render("delete-fixup-left-rotate")

                # type 2
                assert w.left is not None
                assert w.right is not None
                if w.left.color == Color.BLACK and w.right.color == Color.BLACK:
                    w.color = Color.RED
                    x = x.parent
                    self.render("delete-fixup-recolor")
                else:
                    # type 3
                    if w.right.color == Color.BLACK:
                        w.left.color = Color.BLACK
                        w.color = Color.RED
                        self.right_rotate(w)
                        w = unwrap(x.parent.right)
                        self.render("delete-fixup-right-rotate")
                    # type 4
                    assert w.right is not None
                    w.color = x.parent.color
                    x.parent.color = Color.BLACK
                    w.right.color = Color.BLACK
                    self.left_rotate(x.parent)
                    x = self.root
                    self.render("delete-fixup-left-rotate")
            else:
                w = unwrap(x.parent.left)

                # type 1
                if w.color == Color.RED:
                    w.color = Color.BLACK
                    x.parent.color = Color.RED
                    self.right_rotate(x.parent)
                    w = unwrap(x.parent.left)
                    self.render("delete-fixup-right-rotate")

                # type 2
                assert w.left is not None
                assert w.right is not None

                if w.right.color == Color.BLACK and w.left.color == Color.BLACK:
                    w.color = Color.RED
                    x = x.parent
                    self.render("delete-fixup-recolor")
                else:

                    # type 3
                    if w.left.color == Color.BLACK:
                        w.right.color = Color.BLACK
                        w.color = Color.RED
                        self.left_rotate(w)
                        w = unwrap(x.parent.left)
                        self.render("delete-fixup-left-rotate")

                    # type 4
                    assert w.left is not None

                    w.color = x.parent.color
                    x.parent.color = Color.BLACK
                    w.left.color = Color.BLACK
                    self.right_rotate(x.parent)
                    x = self.root
                    self.render("delete-fixup-right-rotate")

        if x.color == Color.RED:
            x.color = Color.BLACK
            self.render("delete-fixup-recolor-x")

    def transplant(self, u: Node, v: Node):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def minimum(self, x: Node):
        while x.left != NIL:
            x = unwrap(x.left)
        return x

    def search(self, key: int):
        x = self.root
        while x != NIL and key != x.key:
            if key < x.key:
                x = unwrap(x.left)
            else:
                x = unwrap(x.right)
        return x

    def render_helper(
        self,
        jgraph: JGraph,
        node: Node,
        height: int,
        x=0,
        depth=1,
        parent_x: int | None = None,
        parent_y: int | None = None,
    ):
        if node == NIL:
            return

        x_offset = 2 ** (height - depth)
        if x_offset < 0.5:
            print("Tree too large to render")
            exit(1)

        y = 1 - depth
        color = (0, 0, 0) if node.color == Color.BLACK else (1, 0, 0)
        jgraph.draw_node(node.key, x, y, color)

        if parent_x is not None and parent_y is not None:
            jgraph.draw_edge(parent_x, parent_y, x, y)

        self.render_helper(
            node=unwrap(node.left),
            height=height,
            x=x - x_offset,
            depth=depth + 1,
            parent_x=x,
            parent_y=y,
            jgraph=jgraph,
        )
        self.render_helper(
            node=unwrap(node.right),
            height=height,
            x=x + x_offset,
            depth=depth + 1,
            parent_x=x,
            parent_y=y,
            jgraph=jgraph,
        )

    def render(self, title):
        self.render_helper(
            jgraph=JGraph(title),
            node=self.root,
            height=4,
        )

    def __len__(self):
        if self.root == NIL:
            return 0

        queue = deque()
        queue.append(self.root)

        size = 0

        while queue:
            node = queue.popleft()
            size += 1

            if node.left != NIL:
                queue.append(node.left)
            if node.right != NIL:
                queue.append(node.right)

        return size
