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
    if state == 20:
        print()
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

    # iterate all reachable states and get the terminal shift edges
    precede_set = set()
    for node in reachable_nodes:
        for edge in node.pre_edges:
            if edge.label in graph.terminal and not edge.is_pop and edge.label != "$end":
                precede_set.add(edge.label)
    precede_map[state] = precede_set
    return precede_set


def get_nodes_with_similar_precede_set(node: Node, graph: Graph, specific_term: str | None) -> list[Node]:
    """Nodes that have at least one symbol in common with current nodes precede set."""
    source_precede_set = get_precede_set(node.label, graph)
    nodes_with_similar_precede_set = []
    for n in graph.nodes:
        if not isinstance(n.label, int) or n == node:
            continue
        if specific_term is None and len(get_precede_set(n.label, graph)) == 0:
            nodes_with_similar_precede_set.append(n)
        elif specific_term in source_precede_set and specific_term in get_precede_set(n.label, graph):
            nodes_with_similar_precede_set.append(n)
    return nodes_with_similar_precede_set


def get_nodes_with_similar_follow_set(node: Node, graph: Graph, specific_term: str | None) -> list[Node]:
    source_follow_set = get_follow_set(node.label, graph)
    nodes_with_similar_follow_set = []
    for n in graph.nodes:
        if not isinstance(n.label, int) or n == node:
            continue
        if specific_term is None and len(get_follow_set(n.label, graph)) == 0:
            nodes_with_similar_follow_set.append(n)
        elif specific_term in source_follow_set and specific_term in get_follow_set(n.label, graph):
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
            prev_term = None
            if len(pure_str) > 2:
                prev_term = pure_str[-2]
            nodes_with_similar_precede_set = get_nodes_with_similar_precede_set(edge.source, graph, prev_term)

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
    for i, edge in enumerate(T):
        if edge.label in graph.terminal and edge.label != "$end" and edge.source != edge.next_node:
            # append to back of already deleted
            for i in range(len(out)):
                out[i] += edge.label + ' '

            prev_term = None
            if len(pure_str) > 2:
                prev_term = pure_str[-2]

            nodes_with_similar_precede_set = get_nodes_with_similar_precede_set(edge.source, graph, prev_term)

            next_term = None
            remaining_terms = [e.label for e in T[i + 1:] if e.label in graph.terminal and edge.label != "$end"]
            if remaining_terms:
                next_term = remaining_terms[0]
            nodes_with_similar_follow_set = get_nodes_with_similar_follow_set(edge.next_node, graph, next_term)

            # del if no similar state in terms of a -> (state) -> b exists
            if not set(nodes_with_similar_precede_set).intersection(set(nodes_with_similar_follow_set)) \
                    and edge.source not in nodes_with_similar_follow_set \
                    and edge.next_node not in nodes_with_similar_precede_set:
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

            prev_term = None
            if len(pure_str) > 2:
                prev_term = pure_str[-2]

            nodes_with_similar_precede_set = get_nodes_with_similar_precede_set(edge.source, graph, prev_term)
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
            # Insert after another rule application a - (next edge a ) -> a where a is
            # last node of last rule application
            # check no combo of first(path) in follow set of similar precede nodes to a
            # or no combo on last and similar follow set of a
            # # Iterate the possible insertion options and create only terminal sequences:
            for key, segments in sub_map.items():
                for segment in segments:
                    subbed_segment = sub_with_shortest(segment['trace'], short_map, graph)
                    # Can't sub with epsilon
                    if not any(True if edge.label in graph.terminal else False for edge in subbed_segment):
                        continue

                    prev_term = None
                    before_terms = [e.label for e in T[:index] if
                                    e.label in graph.terminal and edge.label != "$end"]
                    if before_terms:
                        prev_term = before_terms[-1]

                    next_term = None
                    remaining_terms = [e.label for e in T[index + 1:] if
                                       e.label in graph.terminal and edge.label != "$end"]
                    if remaining_terms:
                        next_term = remaining_terms[0]

                    # Create the current prefix if we can insert. It will be completed in following iterations
                    if can_insert(subbed_segment, edge.next_node, edge.next_node, sub_map, graph, prev_term, next_term):
                        test_case_prefix = " ".join([e.label for e in T[:index + 1] if e.label in graph.terminal])
                        test_case_prefix += " " + " ".join(
                            e.label for e in subbed_segment if e.label in graph.terminal) + " "
                        out.append(test_case_prefix)
    return out


def extract_stack_sub(T, sub_map, short_map, graph):
    out = []
    for index, edge in enumerate(T):
        if edge.label in graph.terminal and edge.label != "$end":
            # append to back of already deleted
            for i in range(len(out)):
                out[i] += edge.label + ' '
        if not edge.is_pop and edge.label in graph.nonterminal:
            # Insert over another rule application a - (next edge a ) -> b where a is
            # last node of last rule application
            # check no combo of first(path) in follow set of similar precede nodes to a
            # or no combo on last and similar follow set of b
            # # Iterate the possible insertion options and create only terminal sequences:
            for key, segments in sub_map.items():
                for segment in segments:
                    subbed_segment = sub_with_shortest(segment['trace'], short_map, graph)
                    # Can't sub with epsilon
                    if not any(True if edge.label in graph.terminal else False for edge in subbed_segment):
                        continue

                    prev_term = None
                    string_before_this_rule = deleteFromEnd(T[:index + 1], graph)

                    if len(string_before_this_rule) > 2:
                        prev_term = string_before_this_rule.strip().split(" ")[-1]

                    next_term = None
                    remaining_terms = [e.label for e in T[index + 1:] if
                                       e.label in graph.terminal and edge.label != "$end"]
                    if remaining_terms:
                        next_term = remaining_terms[0]

                    # Create the current prefix if we can sub. It will be completed in following iterations
                    if can_insert(subbed_segment, edge.source, edge.next_node, sub_map, graph, prev_term, next_term):
                        # First delete previous rule and then insert
                        test_case_prefix = deleteFromEnd(T[:index + 1], graph)
                        test_case_prefix += " " + " ".join(
                            e.label for e in subbed_segment if e.label in graph.terminal) + "  "
                        out.append(test_case_prefix)

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

        prev_term = None
        before_terms = [e.label for e in T[:index] if
                        e.label in graph.terminal and edge.label != "$end"]
        if before_terms:
            prev_term = before_terms[-1]

        next_term = None
        remaining_terms = [e.label for e in T[index + 1:] if e.label in graph.terminal and edge.label != "$end"]
        if remaining_terms:
            next_term = remaining_terms[0]

        # del if no similar state in terms of a -> (state) -> b exists
        if not edge.is_pop and edge.label in graph.nonterminal and can_delete(edge, graph, prev_term, next_term):
            out.append(deleteFromEnd(T[:index + 1], graph))
    # delete last rule application
    return out


def sub_with_shortest(segment, shortest_map, graph):
    new_segment = list()
    for i, edge in enumerate(segment):
        if not edge.is_pop and edge.label in graph.nonterminal and not segment[i - 1].is_pop:
            new_segment.extend(shortest_map[edge]['trace'])
        else:
            new_segment.append(edge)
    return new_segment


def can_insert(subbed_segment_to_insert, previous_node, next_node, sub_map, graph, previous_terminal, next_terminal):
    first_terminals_of_segment = get_first(subbed_segment_to_insert, sub_map, graph)
    last_terminals_of_segment = get_last(subbed_segment_to_insert, sub_map, graph)

    similar_precede_nodes = get_nodes_with_similar_precede_set(previous_node, graph, previous_terminal)
    union_follow_set = set()
    for node in similar_precede_nodes + [previous_node]:
        union_follow_set.update(get_follow_set(node.label, graph))

    if len(union_follow_set.intersection(first_terminals_of_segment)) == 0:
        return True

    similar_follow_nodes = get_nodes_with_similar_follow_set(next_node, graph, next_terminal)
    union_precede_set = set()

    for node in similar_follow_nodes + [next_node]:
        union_precede_set.update(get_precede_set(node.label, graph))

    if len(union_precede_set.intersection(last_terminals_of_segment)) == 0:
        return True

    return False


def get_first(trace, sub_map, graph, prev_subbed=None):
    if prev_subbed is None:
        prev_subbed = set()
    first = set()
    for i, edge in enumerate(trace):
        if edge.label in graph.terminal:
            first.add(edge.label)
            break
        elif (not edge.is_pop and edge.label in graph.nonterminal) and (
                i == 0 or not (trace[i - 1].is_pop and trace[i - 1].label == edge.label)):
            for p in sub_map[edge]:
                if edge not in prev_subbed:
                    prev_subbed.add(edge)
                    first.update(get_first(p['trace'], sub_map, graph, prev_subbed))
                    prev_subbed.remove(edge)
            break
    return first


def get_last(trace, sub_map, graph, prev_subbed=None):
    if prev_subbed is None:
        prev_subbed = set()
    last = set()
    # iterate backwards
    for i, edge in reversed(list(enumerate(trace))):
        if edge.label in graph.terminal:
            last.add(edge.label)
            break
        elif (not edge.is_pop and edge.label in graph.nonterminal) and (
                i == 0 or not (trace[i - 1].is_pop and trace[i - 1].label == edge.label)):
            for p in sub_map[edge]:
                if edge not in prev_subbed:
                    prev_subbed.add(edge)
                    last.update(get_last(p['trace'], sub_map, graph, prev_subbed))
                    prev_subbed.remove(edge)
            break
    return last


def can_delete(nt_edge, graph, previous_terminal, next_terminal):
    nodes_with_similar_precede_set = get_nodes_with_similar_precede_set(nt_edge.source, graph, previous_terminal)
    nodes_with_similar_follow_set = get_nodes_with_similar_follow_set(nt_edge.next_node, graph, next_terminal)

    return not set(nodes_with_similar_precede_set).intersection(set(nodes_with_similar_follow_set)) \
        and nt_edge.source not in nodes_with_similar_follow_set and nt_edge.next_node not in nodes_with_similar_precede_set


def deleteFromEnd(trace, graph):
    new_trace = trace.copy()[:-1]  # delete nt push edge
    target_state = new_trace[-1].next_node
    count = -new_trace[-1].pop_count
    i = len(new_trace) - 2
    cur_state = new_trace[i].next_node
    while cur_state != target_state or count != 0:
        edge = new_trace[i]
        if not edge.is_pop and edge.label in graph.terminal:
            count += 1
        elif not edge.is_pop and edge.label in graph.nonterminal:
            count += 1
            i -= 1
            # now handle the pop edge
            edge = new_trace[i]
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
