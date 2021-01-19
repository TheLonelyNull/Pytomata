def get_follow_set(state: int, graph):
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
    return follow_set


def is_almost_accepting(state: int, graph):
    """
        Check if its possible to get to the accept state without shifting a terminal.
        Basically follow reductions and their respective shift on non-terminals and see if you get to
        a dead end or the accept state
    """
    cur_node = graph.nodes[state]
    reachable_nodes = list()
    stack = list()
    stack.append(cur_node)
    while len(stack) > 0:
        cur_node = stack.pop(0)
        for edge in cur_node.edges:
            # check for $end edge since it is a shift edge and acc state won't ever be reached with only reduction
            if edge.label == "$end":
                return True
            if edge.is_pop:
                # go to node after shift on non-terminal after popping for reduction
                next_node = edge.next_node
                label = edge.label
                for edge2 in next_node.edges:
                    if not edge2.is_pop and edge2.label == label and next_node not in reachable_nodes:
                        next_node = edge2.next_node
                        if next_node != cur_node:
                            stack.append(next_node)
                        break
        reachable_nodes.append(cur_node)
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
            # sub
            for t in graph.terminal:
                if t not in source_follow_set and t != '$end':
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
            source_follow_set = get_follow_set(edge.source.label, graph)
            dest_follow_set = get_follow_set(edge.next_node.label, graph)
            # del if no overlap in follow set
            if len(source_follow_set - dest_follow_set) == len(source_follow_set):
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
            # insert
            for t in graph.terminal:
                if t not in source_follow_set and t != '$end':
                    out.append(pure_str + t + ' ')
            # calculate without insertion
            pure_str += edge.label + ' '
            # append to back of already mutated
            for i in range(len(out)):
                out[i] += edge.label + ' '
    return out
