import os


def gen_graphic(nodes):

    f = open("visual.gviz", 'w')
    # add boilerplate
    f.write("digraph abstract {\n\n")
    f.write("  node [shape = doublecircle]; 0 acc;\n")
    f.write("  node [shape = circle];\n")
    for node in nodes:
        edges = set()
        for edge in node.edges:
            if edge.is_return:
                from_label = str(node.label)
                to_label = str(edge.next_node.label)
                if ("  " + from_label + " -> " + to_label + " [ label=\"" + str(
                        edge.label) + "/" + str(edge.red_pop_count) + "" + "\" style=\"dashed\" ];\n") not in edges:
                    f.write("  " + from_label + " -> " + to_label + " [ label=\"" + str(
                        edge.label) + "/" + str(edge.red_pop_count) + "" + "\" style=\"dashed\" ];\n")
                    edges.add("  " + from_label + " -> " + to_label + " [ label=\"" + str(
                        edge.label) + "/" + str(edge.red_pop_count) + ""+ "\" style=\"dashed\" ];\n")
            elif not edge.is_return:
                from_label = str(node.label)
                to_label = str(edge.next_node.label)
                if ("  " + from_label + " -> " + to_label + " [ label=\"" + str(
                        edge.label) + "\" ];\n") not in edges:
                    f.write("  " + from_label + " -> " + to_label + " [ label=\"" + str(
                        edge.label) + "\" ];\n")
                    edges.add("  " + from_label + " -> " + to_label + " [ label=\"" + str(
                        edge.label) + "\" ];\n")
    f.write("\n}\n")
    f.close()
    command = "dot -Tpdf visual.gviz > out/visual.pdf"
    print("Generated graph in ./out/visual.pdf")
    os.system(command)
