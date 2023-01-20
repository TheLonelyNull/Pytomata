from graph_components import Node, Graph

len_map = None
follow_map = {}
precede_map = {}
accepting_map = {}


def get_follow_set(state: int, graph):
    if state in follow_map:
        return follow_map[state]
    """
        Explore all reachable states without shifting a terminal. Then collect all terminals
        reachable from these states.
    """
    cur_node = graph.nodes[state]
    reachable_nodes = list()
    stack = list()
    stack.append(cur_node)
    while len(stack) > 0:
        cur_node = stack.pop(0)
        reachable_nodes.append(cur_node)
        for edge in cur_node.edges:
            if edge.is_pop:
                # go to node after shift on non-terminal after popping for reduction
                next_node = edge.next_node
                label = edge.label
                for edge2 in next_node.edges:
                    if not edge2.is_pop and edge2.label == label:
                        next_node = edge2.next_node
                        if next_node != cur_node and next_node not in reachable_nodes:
                            stack.append(next_node)
                        break
    # iterate all reachable states and get the terminal shift edges
    follow_set = set()
    for node in reachable_nodes:
        for edge in node.edges:
            if edge.label in graph.terminal and not edge.is_pop and edge.label != "$end":
                follow_set.add(edge.label)
    follow_map[state] = follow_set
    return follow_set


def get_precede_set(state: int, graph: Graph):
    if state in precede_map:
        return precede_map[state]
    """
        Explore all reverse reachable states without shifting a terminal. Then collect all terminals
        preceding these states.
    """
    cur_node = graph.nodes[state]
    reachable_nodes = list()
    stack = list()
    stack.append(cur_node)
    while len(stack) > 0:
        cur_node = stack.pop(0)
        reachable_nodes.append(cur_node)
        cur_node: Node
        for edge in cur_node.pre_edges:
            if not edge.is_pop and edge.label in graph.nonterminal:
                # go to node before pop that precedes shift on non-terminal.
                prev_node: Node = edge.source
                label = edge.label
                for edge2 in prev_node.pre_edges:
                    if edge2.is_pop and edge2.label == label:
                        prev_node = edge2.source
                        if prev_node != cur_node and prev_node not in reachable_nodes:
                            stack.append(prev_node)
                        break
    # iterate all reachable states and get the terminal shift edges
    precede_set = set()
    for node in reachable_nodes:
        for edge in node.pre_edges:
            if edge.label in graph.terminal and not edge.is_pop and edge.label != "$end":
                precede_set.add(edge.label)
    precede_map[state] = precede_set
    return precede_set


def get_nodes_with_similar_precede_set(node: Node, graph: Graph) -> list[Node]:
    """Nodes that have at least one symbol in common with current nodes precede set."""
    source_precede_set = get_precede_set(node.label, graph)
    nodes_with_similar_precede_set = []
    for n in graph.nodes:
        if not isinstance(n.label, int) or n == node:
            continue
        if source_precede_set - get_precede_set(n.label, graph) != source_precede_set:
            nodes_with_similar_precede_set.append(n)
    return nodes_with_similar_precede_set


def get_nodes_with_similar_follow_set(node: Node, graph: Graph) -> list[Node]:
    source_follow_set = get_follow_set(node.label, graph)
    nodes_with_similar_follow_set = []
    for n in graph.nodes:
        if not isinstance(n.label, int) or n == node:
            continue
        if source_follow_set - get_follow_set(n.label, graph) != source_follow_set:
            nodes_with_similar_follow_set.append(n)
    return nodes_with_similar_follow_set


def is_almost_accepting(state: int, graph):
    if state in accepting_map:
        return accepting_map[state]
    """
        Check if its possible to get to the accept state without shifting a terminal.
        Basically follow reductions and their respective shift on non-terminals and see if you get to
        a dead end or the accept state
    """
    cur_node = graph.nodes[state]
    reachable_nodes = set()
    stack = list()
    stack.append(cur_node)
    while len(stack) > 0:
        cur_node = stack.pop(0)
        for edge in cur_node.edges:
            # check for $end edge since it is a shift edge and acc state won't ever be reached with only reduction
            if edge.label == "$end":
                accepting_map[state] = True
                return True
            if edge.is_pop:
                # go to node after shift on non-terminal after popping for reduction
                next_node = edge.next_node
                label = edge.label
                for edge2 in next_node.edges:
                    if not edge2.is_pop and edge2.label == label and next_node not in reachable_nodes:
                        reachable_nodes.add(next_node)
                        next_node = edge2.next_node
                        if next_node != cur_node:
                            stack.append(next_node)
                        reachable_nodes.add(next_node)
                        break
        reachable_nodes.add(cur_node)
    accepting_map[state] = False
    return False


def extract_sub(T, graph):
    out = []
    pure_str = ''
    for edge in T:
        if edge.label in graph.terminal and edge.label != "$end":
            # append to back of already subbed
            for i in range(len(out)):
                out[i] += edge.label + ' '

            source_follow_set = get_follow_set(edge.source.label, graph)
            nodes_with_similar_precede_set = get_nodes_with_similar_precede_set(edge.source, graph)

            # sub
            for t in graph.terminal:
                in_similar_node_follow_set = any(
                    t in get_follow_set(n.label, graph) for n in nodes_with_similar_precede_set)
                if t not in source_follow_set and not in_similar_node_follow_set and t != '$end':
                    out.append(pure_str + t + ' ')
            # don't sub
            pure_str += edge.label + ' '

    return out


def extract_cut(T, graph):
    out = []
    pure_str = ''
    for edge in T:
        if edge.label in graph.terminal and edge.label != "$end":
            # cut out this edge if not almost accepting
            if not is_almost_accepting(edge.source.label, graph):
                out.append(pure_str)
            pure_str += edge.label + ' '

    return out


def extract_del(T, graph):
    out = []
    pure_str = ''
    for edge in T:
        if edge.label in graph.terminal and edge.label != "$end":
            # append to back of already deleted
            for i in range(len(out)):
                out[i] += edge.label + ' '
            nodes_with_similar_precede_set = get_nodes_with_similar_precede_set(edge.source, graph)
            nodes_with_similar_follow_set = get_nodes_with_similar_follow_set(edge.next_node, graph)

            # del if no similar state in terms of a -> (state) -> b exists
            if not set(nodes_with_similar_precede_set).intersection(set(nodes_with_similar_follow_set)):
                out.append(pure_str + ' ')
            # don't del
            pure_str += edge.label + ' '

    return out


def extract_add(T, graph):
    out = []
    pure_str = ''
    for edge in T:
        if edge.label in graph.terminal and edge.label != "$end":
            source_follow_set = get_follow_set(edge.source.label, graph)
            nodes_with_similar_precede_set = get_nodes_with_similar_precede_set(edge.source, graph)
            # insert
            for t in graph.terminal:
                in_similar_node_follow_set = any(
                    t in get_follow_set(n.label, graph) for n in nodes_with_similar_precede_set)

                if t not in source_follow_set and not in_similar_node_follow_set and t != '$end':
                    out.append(pure_str + t + ' ')
            # calculate without insertion
            pure_str += edge.label + ' '
            # append to back of already mutated
            for i in range(len(out)):
                out[i] += edge.label + ' '
    return out


def extract_stack_add(T, sub_map, short_map, graph):
    out = []
    for index, edge in enumerate(T):
        if edge.label in graph.terminal and edge.label != "$end":
            # append to back of already deleted
            for i in range(len(out)):
                out[i] += edge.label + ' '
        if not edge.is_pop and edge.label in graph.nonterminal:
            # check beginning if rule is was applied in nullable context
            follow_check_offset = 0
            pop_edge = T[index - 1]
            if pop_edge.pop_count == 0:
                follow_check_offset = 1
            # insert after last rule application
            for key in sub_map:
                for segment in sub_map[key]:
                    subbed = sub_with_shortest(segment['trace'], short_map, graph)
                    # check that this segment is not epsilon
                    epsilon = True
                    for e in subbed:
                        if not e.is_pop and e.label in graph.terminal:
                            epsilon = False
                            break
                    if epsilon:
                        continue
                    if can_insert(subbed, T, index - follow_check_offset, sub_map, graph):
                        # insert
                        out_str = ''
                        for e in T[:index + 1]:
                            if not e.is_pop and e.label not in graph.nonterminal:
                                out_str += e.label + ' '
                        for e in subbed:
                            if not e.is_pop and e.label not in graph.nonterminal:
                                out_str += e.label + ' '
                        out.append(out_str)
    return out


def extract_stack_sub(T, sub_map, short_map, graph):
    out = []
    for index, edge in enumerate(T):
        if edge.label in graph.terminal and edge.label != "$end":
            # append to back of already deleted
            for i in range(len(out)):
                out[i] += edge.label + ' '
        if not edge.is_pop and edge.label in graph.nonterminal:
            # delete last rule application
            for key in sub_map:
                for segment in sub_map[key]:
                    subbed = sub_with_shortest(segment['trace'], short_map, graph)
                    if can_insert(subbed, T, index - 1, sub_map, graph):
                        # insert
                        tmp = deleteFromEnd(T[:index + 1], graph)
                        out_str = tmp
                        for e in subbed:
                            if not e.is_pop and e.label not in graph.nonterminal:
                                out_str += e.label + ' '
                        out.append(out_str)
    return out


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


def extract_stack_del(T, graph):
    out = []
    for index, edge in enumerate(T):
        if edge.label in graph.terminal and edge.label != "$end":
            # append to back of already deleted
            for i in range(len(out)):
                out[i] += edge.label + ' '
        if not edge.is_pop and edge.label in graph.nonterminal and can_delete(edge, graph):
            # delete last rule application
            out.append(deleteFromEnd(T[:index + 1], graph))
    return out


def sub_with_shortest(segment, shortest_map, graph):
    new_segment = list()
    for i, edge in enumerate(segment):
        if not edge.is_pop and edge.label in graph.nonterminal and not segment[i - 1].is_pop:
            new_segment.extend(shortest_map[edge]['trace'])
        else:
            new_segment.append(edge)
    return new_segment


def can_insert(segment, trace, cur_index, sub_map, graph):
    cur_state = trace[cur_index].next_node
    first = get_first(segment, sub_map, graph)
    follow = get_follow_set(cur_state.label, graph)

    if len(follow - first) < len(follow) or len(first) == 0:
        return False
    return True


def get_first(trace, sub_map, graph, prev_subbed=None):
    if prev_subbed is None:
        prev_subbed = set()
    first = set()
    for i, edge in enumerate(trace):
        if edge.label in graph.terminal:
            first.add(edge.label)
            break
        elif (not edge.is_pop and edge.label in graph.nonterminal) and (i == 0 or trace[i - 1].is_pop):
            for p in sub_map[edge]:
                if edge not in prev_subbed:
                    prev_subbed.add(edge)
                    first.update(get_first(p['trace'], sub_map, graph, prev_subbed))
                    prev_subbed.remove(edge)
            break
    return first


def can_delete(nt_edge, graph):
    nt_edges = {}
    pop_edges = []
    # collect edges and check if rule application is nullable in this context
    for edge in nt_edge.source.edges:
        if not edge.is_pop and edge.label in graph.nonterminal and edge.label != nt_edge.label:
            nt_edges[edge.label] = edge
    for edge in nt_edge.source.pre_edges:
        if edge.is_pop and edge.pop_count == 0:
            # check if the current rule was nullable
            if edge.label == nt_edge.label and edge.pop_count == 0:
                return False
            pop_edges.append(edge)
    # get follow set of rule application to delete
    nt_follow = get_follow_set(nt_edge.next_node.label, graph)
    for edge in pop_edges:
        nt = nt_edges[edge.label]
        follow = get_follow_set(nt.next_node.label, graph)
        if len(nt_follow) == 0 and len(follow) == 0:
            return False
        if len(nt_follow - follow) < len(nt_follow):
            return False
    return True


def deleteFromEnd(trace, graph):
    new_trace = trace.copy()[:-1]  # delete nt push edge
    target_state = new_trace[-1].next_node
    count = -new_trace[-1].pop_count
    i = len(new_trace) - 2
    cur_state = new_trace[i].next_node
    while cur_state != target_state or count != 0:
        edge = new_trace[i]
        if not edge.is_pop:
            count += 1
        else:
            count -= edge.pop_count
        i -= 1
        cur_state = new_trace[i].next_node

    new_trace = new_trace[:i + 1]
    test_str = ""
    for e in new_trace:
        if not e.is_pop and e.label not in graph.nonterminal:
            test_str += e.label + ' '
    return test_str


def calc_sub_len(sub_map):
    # maps token length of pop edge segments
    if len_map is not None:
        return len_map
