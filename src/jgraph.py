from io import TextIOWrapper
from pathlib import Path
from shell import bash
from shutil import rmtree

RED = (1, 0, 0)
BLACK = (0, 0, 0)

JGR_DIR = Path("jgr")
JPG_DIR = Path("jpg")
PDF_DIR = Path("pdf")
PS_DIR = Path("ps")
NODES_JGR_FILE = JGR_DIR / "nodes.jgr"
VALUES_JGR_FILE = JGR_DIR / "values.jgr"
EDGES_JGR_FILE = JGR_DIR / "edges.jgr"
RB_TREE_JGR_FILE = JGR_DIR / "rb-tree.jgr"
RB_TREE_PS_FILE = JGR_DIR / "rb-tree.ps"
RB_TREE_PDF_FILE = JGR_DIR / "rb-tree.pdf"


class JGraph:
    number_images = 0

    def __init__(self, title: str):
        if JGraph.number_images == 0:
            rmtree(JGR_DIR, ignore_errors=True)
            rmtree(PS_DIR, ignore_errors=True)
            rmtree(PDF_DIR, ignore_errors=True)
            rmtree(JPG_DIR, ignore_errors=True)

            JGR_DIR.mkdir(exist_ok=True)
            PS_DIR.mkdir(exist_ok=True)
            PDF_DIR.mkdir(exist_ok=True)
            JPG_DIR.mkdir(exist_ok=True)

        self.title = title

        self.nodes_file: TextIOWrapper = open(NODES_JGR_FILE, "w")
        self.values_file: TextIOWrapper = open(VALUES_JGR_FILE, "w")
        self.edges_file: TextIOWrapper = open(EDGES_JGR_FILE, "w")
        self.rb_tree_file: TextIOWrapper = open(RB_TREE_JGR_FILE, "w")

        self.rb_tree_file.write("newgraph\n")
        self.rb_tree_file.write(
            f"newstring x 0 y 1 hjc vjc font ``Monaco'' fontsize 12 : {title}\n"
        )
        self.rb_tree_file.write(f"xaxis size 8 min -16 max 16 nodraw\n")
        self.rb_tree_file.write(f"yaxis size 6 min -4.5 max 1 nodraw\n")

        self.rb_tree_file.write(f"include {EDGES_JGR_FILE}\n")
        self.rb_tree_file.write(f"include {NODES_JGR_FILE}\n")
        self.rb_tree_file.write(f"include {VALUES_JGR_FILE}\n")

    def __del__(self):
        self.nodes_file.close()
        self.values_file.close()
        self.edges_file.close()
        self.rb_tree_file.close()

        output_name = f"rb-tree-{JGraph.number_images:04}-{self.title}"
        print(output_name)

        output_ps = PS_DIR / f"{output_name}.ps"
        output_pdf = PDF_DIR / f"{output_name}.pdf"
        output_jpg = JPG_DIR / f"{output_name}.jpg"

        bash(f"jgraph -L -P {RB_TREE_JGR_FILE} > {output_ps}")
        bash(f"ps2pdf {output_ps} {output_pdf}")

        bash(f"convert -density 300 -quality 90 {output_pdf} {output_jpg}")
        JGraph.number_images += 1

    def draw_node(
        self,
        key: int,
        x: int,
        y: int,
        color: tuple[float, float, float],
    ):
        node = f"newcurve marktype circle pts {x} {y} marksize 1 color {color[0]} {color[1]} {color[2]}\n"
        value = f"newstring lcolor 1 1 1 x {x} y {y} hjc vjc font ``Monaco'' fontsize 12 : {key}\n"
        self.nodes_file.write(node)
        self.values_file.write(value)

    def draw_edge(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
    ):
        line = f"newcurve pts {x1} {y1} {x2} {y2} marktype none linethickness 1 linetype solid\n"
        self.edges_file.write(line)
