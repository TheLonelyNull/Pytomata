from general_utils import extract_test_case


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


def print_state(cur_trace, new_trace, graph):
    print(extract_test_case(cur_trace, graph))
    print("Shifting non-terminal")
    print("Before: " + trace_to_str(cur_trace, graph))
    print('After: ' + trace_to_str(new_trace, graph))
