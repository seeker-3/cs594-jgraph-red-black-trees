from enum import Enum, auto
from dataclasses import dataclass
from typing import TypeVar
from jgraph import JGraph, RED, BLACK

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
    root = NIL

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
        new_node = Node(
            key,
            color=Color.RED,
            left=NIL,
            right=NIL,
        )

        parent: Node | None = None
        x = self.root

        while x != NIL:
            parent = x
            x = unwrap(x.left if new_node.key < x.key else x.right)

        new_node.parent = parent
        if parent is None:
            self.root = new_node
        elif new_node.key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        self.render(f"insert-{key}")
        self.insert_fixup(new_node)

    def insert_fixup(self, new_node: Node):
        while new_node.parent is not None and new_node.parent.color == Color.RED:

            assert new_node.parent.parent is not None

            if new_node.parent == new_node.parent.parent.left:
                uncle = unwrap(new_node.parent.parent.right)

                if uncle.color == Color.RED:
                    new_node.parent.color = Color.BLACK
                    uncle.color = Color.BLACK
                    new_node.parent.parent.color = Color.RED
                    new_node = new_node.parent.parent
                    self.render("insert-fixup-recolor")

                else:
                    if new_node == new_node.parent.right:
                        new_node = new_node.parent
                        self.left_rotate(new_node)

                    assert new_node.parent is not None
                    assert new_node.parent.parent is not None

                    new_node.parent.color = Color.BLACK
                    new_node.parent.parent.color = Color.RED
                    self.right_rotate(new_node.parent.parent)
                    self.render("insert-fixup-right-rotate")
            else:
                uncle = unwrap(new_node.parent.parent.left)

                if uncle.color == Color.RED:
                    new_node.parent.color = Color.BLACK
                    uncle.color = Color.BLACK
                    new_node.parent.parent.color = Color.RED
                    new_node = new_node.parent.parent
                    self.render("insert-fixup-recolor")
                else:
                    if new_node == new_node.parent.left:
                        new_node = new_node.parent
                        self.right_rotate(new_node)

                    assert new_node.parent is not None
                    assert new_node.parent.parent is not None

                    new_node.parent.color = Color.BLACK
                    new_node.parent.parent.color = Color.RED
                    self.left_rotate(new_node.parent.parent)
                    self.render("insert-fixup-left-rotate")

            if new_node == self.root:
                break

        if self.root.color == Color.RED:
            self.root.color = Color.BLACK
            self.render("insert-fixup-recolor-root")

    def delete(self, key: int):
        old_node = self.search(key)

        if old_node == NIL:
            return

        y = old_node
        y_original_color = y.color

        # case 1
        if old_node.left == NIL:
            child = unwrap(old_node.right)
            self.transplant(old_node, child)

        # case 2
        elif old_node.right == NIL:
            child = unwrap(old_node.left)
            self.transplant(old_node, child)

        # case 3
        else:
            assert old_node.right is not None
            y = self.minimum(old_node.right)
            y_original_color = y.color
            child = unwrap(y.right)

            if y.parent == old_node:
                child.parent = y
            else:
                assert y.right is not None
                self.transplant(y, y.right)
                y.right = old_node.right
                y.right.parent = y

            self.transplant(old_node, y)
            y.left = old_node.left
            unwrap(y.left).parent = y
            y.color = old_node.color

        self.render(f"delete-{key}")
        if y_original_color == Color.BLACK:
            self.delete_fixup(child)

    def delete_fixup(self, old_node: Node):
        while old_node != self.root and old_node.color == Color.BLACK:
            assert old_node.parent is not None
            if old_node == old_node.parent.left:
                sibling = unwrap(old_node.parent.right)

                # type 1
                if sibling.color == Color.RED:
                    sibling.color = Color.BLACK
                    old_node.parent.color = Color.RED
                    self.left_rotate(old_node.parent)
                    sibling = unwrap(old_node.parent.right)
                    self.render("delete-fixup-left-rotate")

                # type 2
                assert sibling.left is not None
                assert sibling.right is not None
                if (
                    sibling.left.color == Color.BLACK
                    and sibling.right.color == Color.BLACK
                ):
                    sibling.color = Color.RED
                    old_node = old_node.parent
                    self.render("delete-fixup-recolor")
                else:

                    # type 3
                    if sibling.right.color == Color.BLACK:
                        sibling.left.color = Color.BLACK
                        sibling.color = Color.RED
                        self.right_rotate(sibling)
                        sibling = unwrap(old_node.parent.right)
                        self.render("delete-fixup-right-rotate")

                    # type 4
                    assert sibling.right is not None
                    sibling.color = old_node.parent.color
                    old_node.parent.color = Color.BLACK
                    sibling.right.color = Color.BLACK
                    self.left_rotate(old_node.parent)
                    old_node = self.root
                    self.render("delete-fixup-left-rotate")
            else:
                sibling = unwrap(old_node.parent.left)

                # type 1
                if sibling.color == Color.RED:
                    sibling.color = Color.BLACK
                    old_node.parent.color = Color.RED
                    self.right_rotate(old_node.parent)
                    sibling = unwrap(old_node.parent.left)
                    self.render("delete-fixup-right-rotate")

                # type 2
                assert sibling.left is not None
                assert sibling.right is not None

                if (
                    sibling.right.color == Color.BLACK
                    and sibling.left.color == Color.BLACK
                ):
                    sibling.color = Color.RED
                    old_node = old_node.parent
                    self.render("delete-fixup-recolor")
                else:

                    # type 3
                    if sibling.left.color == Color.BLACK:
                        sibling.right.color = Color.BLACK
                        sibling.color = Color.RED
                        self.left_rotate(sibling)
                        sibling = unwrap(old_node.parent.left)
                        self.render("delete-fixup-left-rotate")

                    # type 4
                    assert sibling.left is not None

                    sibling.color = old_node.parent.color
                    old_node.parent.color = Color.BLACK
                    sibling.left.color = Color.BLACK
                    self.right_rotate(old_node.parent)
                    old_node = self.root
                    self.render("delete-fixup-right-rotate")

        if old_node.color == Color.RED:
            old_node.color = Color.BLACK
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
            x = unwrap(x.left if key < x.key else x.right)
        return x

    def render_helper(
        self,
        jgraph: JGraph,
        node: Node,
        height=4,
        depth=1,
        x=0,
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
        color = BLACK if node.color == Color.BLACK else RED
        jgraph.draw_node(node.key, x, y, color)

        if parent_x is not None and parent_y is not None:
            jgraph.draw_edge(parent_x, parent_y, x, y)

        self.render_helper(
            node=unwrap(node.left),
            height=height,
            depth=depth + 1,
            x=x - x_offset,
            parent_x=x,
            parent_y=y,
            jgraph=jgraph,
        )
        self.render_helper(
            node=unwrap(node.right),
            height=height,
            depth=depth + 1,
            x=x + x_offset,
            parent_x=x,
            parent_y=y,
            jgraph=jgraph,
        )

    def render(self, title):
        self.render_helper(
            jgraph=JGraph(title),
            node=self.root,
        )
