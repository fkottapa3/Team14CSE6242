import ast
from graphviz import Digraph

# Read the Python file
file_path = "Q1.py"
with open(file_path, "r") as file:
    code = file.read()

# Parse the Python code
tree = ast.parse(code)


# Extract function definitions and calls
class FunctionVisitor(ast.NodeVisitor):
    def __init__(self):
        self.functions = set()
        self.calls = []

    def visit_FunctionDef(self, node):
        self.functions.add(node.name)
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            self.calls.append(node.func.id)
        self.generic_visit(node)


visitor = FunctionVisitor()
visitor.visit(tree)

# Generate the graph
dot = Digraph()
for func in visitor.functions:
    dot.node(func, func)

for call in visitor.calls:
    dot.edge(call, call)

dot.render("output/graph", format="png")
