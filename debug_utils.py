def trace_to_str(T, graph):
    if len(T) == 0:
        return ""
    trace = str(T[0].source.label)
    for edge in T:
        colour = "\033[1;32;40m"
        if edge.is_pop:
            colour = "\033[94m"
        elif edge.label in graph.nonterminal:
            colour = "\033[1;33;40m"
        trace += colour + " -" + str(edge.label) + "-> \033[0m" + str(edge.next_node.label)
    return trace

