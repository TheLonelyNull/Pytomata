import os


def _get_node_label(node):
    if node.label == 0:
        return "init"
    return str(node.label)


def gen_graphic(nodes):
    f = open("visual.gviz", 'w')
    # add boilerplate
    f.write("digraph abstract {\n\n")
    f.write("""
    node [shape = circle, fixedsize = true, fillcolor = lightgrey, style = filled]; init;
    node [shape = doublecircle, fixedsize = true, fillcolor = white, style = filled]; acc;
    node [shape = circle, fixedsize = true, fillcolor = white];
    """)
    for node in nodes:
        edges = set()
        for edge in node.edges:
            if edge.is_pop:
                from_label = _get_node_label(node)
                to_label = _get_node_label(edge.next_node)
                if ("  " + from_label + " -> " + to_label + " [ label=\" " + str(
                        edge.label) + "/" + str(edge.pop_count) + "" + "\" style=\"dashed\" ];\n") not in edges:
                    f.write("  " + from_label + " -> " + to_label + " [ label=\" " + str(
                        edge.label) + "/" + str(edge.pop_count) + "" + "\" style=\"dashed\" ];\n")
                    edges.add("  " + from_label + " -> " + to_label + " [ label=\" " + str(
                        edge.label) + "/" + str(edge.pop_count) + "" + "\" style=\"dashed\" ];\n")
            elif not edge.is_pop:
                from_label = _get_node_label(node)
                to_label = _get_node_label(edge.next_node)
                edge_label = str(edge.label)
                if edge_label == '$end':
                    edge_label = '$'
                if ("  " + from_label + " -> " + to_label + " [ label=\" " + str(
                        edge_label) + "\" ];\n") not in edges:
                    f.write("  " + from_label + " -> " + to_label + " [ label=\" " + str(
                        edge_label) + "\" ];\n")
                    edges.add("  " + from_label + " -> " + to_label + " [ label=\" " + str(
                        edge_label) + "\" ];\n")
    f.write("\n}\n")
    f.close()
    command = "dot -Tpdf visual.gviz > out/visual.pdf"
    print("Generated graph in ./out/visual.pdf")
    os.system(command)
