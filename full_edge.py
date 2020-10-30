from graph_components import Graph, Edge, Node


def full_edge(graph: Graph):
    E = graph.edges.copy()
    test_cases = []
    while len(E) > 0 and len(test_cases) < 10:
        S = list()
        S.append(graph.root)
        cur = S[-1]
        trace = list()

        while not cur.is_accept:
            print(trace_to_str(trace, graph))
            if len(trace) > 0 and trace[-1].label in graph.nonterminal and trace[-1].is_return:
                non_terminal_edge = get_non_terminal_edge(cur, trace[-1].label)
                shift(non_terminal_edge, S, trace)
            elif can_reduce(S, E, trace, graph, cur):
                reduce_edge = get_reduce_edge(cur.reduce_rule[0][0], cur.reduce_rule[0][1], cur, S)
                reduce(reduce_edge, S, trace, cur.reduce_rule[0][1])
            else:
                terminal_edge = get_terminal_edge(S, E, trace, cur, graph)
                shift(terminal_edge, S, trace)
            cur = S[-1]

        print(trace_to_str(trace, graph))
        print(extract_test_cast(trace, graph))
        test_cases.append(extract_test_cast(trace, graph))
        remove_edges(trace, E, graph)
    return test_cases


def trace_to_str(T, graph):
    trace = "0"
    for edge in T:
        colour = "\033[1;32;40m"
        if edge.is_return:
            colour = "\033[94m"
        elif edge.label in graph.nonterminal:
            colour = "\033[1;33;40m"
        trace += colour + " -" + str(edge.label) + "-> \033[0m" + str(edge.next_node.label)
    return trace


def shift(edge: Edge, S, T: list()):
    T.append(edge)
    S.append(edge.next_node)
    return edge.next_node


def reduce(edge, S, T, reduce_amount):
    # get stack to the right place
    for i in range(reduce_amount):
        S.pop(len(S) - 1)
    T.append(edge)


def can_reduce(S, E, T, graph, cur):
    # check for reduction rules
    if cur.reduce_rule is None:
        return False

    reduce_edge = get_reduce_edge(cur.reduce_rule[0][0], cur.reduce_rule[0][1], cur, S)

    # checks for self reduction cycles
    if cur == reduce_edge.next_node:
        # check if this is the only valid choice. i.e. no terminal edges
        if reduce_edge not in E:
            terminal_count = 0
            for edge in cur.edges:
                if edge.label in graph.terminal and edge not in T:
                    terminal_count += 1
            if terminal_count > 0:
                return False
            return True

    # avoid cycles
    # if reduce_edge in T:
    #    return False

    return True


def get_non_terminal_edge(cur: Node, non_terminal: str):
    for edge in cur.edges:
        if edge.label == non_terminal:
            return edge


def get_terminal_edge(S, E, T, cur, graph):
    terminal_edge = None
    # try to pick the first non visited edge
    for edge in cur.edges:
        if edge.label in graph.terminal and edge in E and edge not in T:
            terminal_edge = edge
            break

    # pick edge with shortest path to accept state if all have been visited
    if terminal_edge is None:
        count = 0
        for edge in cur.edges:
            if edge.label in graph.terminal:
                count += 1
                terminal_edge = edge
        if count > 1:
            print("Trying Shortest path")
            shortest = bfs(S.copy(), T.copy(), 'acc', graph)
            # check that there actually is a path
            print(trace_to_str(shortest['trace'], graph))
            print(extract_test_cast(shortest['trace'], graph))
            terminal_edge = shortest['trace'][len(T)]
    return terminal_edge


def get_reduce_edge(rule_label: str, reduce_amount: int, node: Node, S):
    reduce_edge = None
    for edge in node.edges:
        if edge.label == rule_label and edge.next_node == S[-reduce_amount - 1]:
            reduce_edge = edge
            break
    return reduce_edge


def remove_edges(T, E, graph):
    prev_rem = len(E) + 1
    while prev_rem != len(E):
        prev_rem = len(E)
        for edge in T[::-1]:
            if can_remove_edge(edge, E, T, graph):
                print("Removed: " + str(edge))
                E.remove(edge)


def can_remove_edge(edge, E, T, graph):
    if edge not in E:
        return False
    if edge.label in graph.nonterminal:
        # allow removal of all terminal edges since other rules apply when looking at non-terminal edges
        return True
    else:
        # make sure that all later terminal edges are visited before removal of this edge
        for edge2 in edge.next_node.edges:
            if edge2.label in graph.terminal and (edge2 in E and edge2 not in T and edge != edge2):
                return False
    return True


def extract_test_cast(T, graph):
    case = ""
    for edge in T:
        if edge.label in graph.terminal and edge.label != "$end":
            case += edge.label
    return case


def bfs(S, T, goal_label, graph):
    queue = list()
    queue.append({
        'stack': S.copy(),
        'trace': T.copy()
    })
    while len(queue) > 0:
        path = queue.pop(0)
        cur_stack = path['stack']
        cur_trace = path['trace']
        cur_node = cur_stack[-1]

        # check if the destination has been reached
        if str(cur_node.label) == goal_label:
            return path

        # check if there is a reduce rule that may exist for this state
        reduce_edge = None
        if cur_node.reduce_rule is not None:
            reduce_edge = get_reduce_edge(cur_node.reduce_rule[0][0], cur_node.reduce_rule[0][1], cur_node, cur_stack)

        # check if the previous move was reduce so we should shift a non-terminal
        if len(cur_trace) > 0 and cur_trace[-1].is_return:
            shift_edge: Edge
            for edge in cur_node.edges:
                if edge.label == cur_trace[-1].label and not edge.is_return:
                    shift_edge = edge
                    break

            new_path = {
                'stack': cur_stack.copy() + [shift_edge.next_node],
                'trace': cur_trace.copy() + [shift_edge]
            }

            if False:
                print(extract_test_cast(cur_trace, graph))
                print("Shifting non-terminal")
                print("Before: " + trace_to_str(cur_trace, graph))
                print('After: ' + trace_to_str(new_path['trace'], graph))
            queue.append(new_path)
        else:
            # if the previous step wasn't a reduce then we should shift on terminals and check
            # for valid reductions on all edges
            for edge in cur_node.edges:
                # avoid shifting on an self-loop
                if edge.label in graph.terminal and edge.next_node != cur_node:
                    new_path = {
                        'stack': cur_stack.copy() + [edge.next_node],
                        'trace': cur_trace.copy() + [edge]
                    }
                    if False:
                        print(extract_test_cast(cur_trace, graph))
                        print("Shifting terminal")
                        print("Before: " + trace_to_str(cur_trace, graph))
                        print('After: ' + trace_to_str(new_path['trace'], graph))
                    queue.append(new_path)
                # check that reduction edge is correct edge
                elif edge.label in graph.nonterminal and edge == reduce_edge:
                    # pop nodes of stack
                    for i in range(cur_node.reduce_rule[0][1]):
                        cur_stack.pop(len(cur_stack) - 1)
                    new_path = {
                        'stack': cur_stack.copy(),
                        'trace': cur_trace.copy() + [edge]
                    }
                    if False:
                        print(extract_test_cast(cur_trace, graph))
                        print("Reducing")
                        print("Before: " + trace_to_str(cur_trace, graph))
                        print('After: ' + trace_to_str(new_path['trace'], graph))
                    queue.append(new_path)
