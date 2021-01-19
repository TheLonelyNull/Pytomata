from graph_components import Graph, Edge, Node
from copy import deepcopy
import multiprocessing
from functools import partial
from tqdm import tqdm


def bfs_full_edge(graph: Graph):
    E = graph.edges.copy()
    test_cases = set()
    # bfs till graph covered
    print("Starting graph flooding")
    queue = bfs_cover([graph.nodes[0]], E, [], graph)

    print("Graph covering complete. Test cases to complete " + str(len(queue)))
    # complete found paths
    pool = multiprocessing.Pool(multiprocessing.cpu_count() - 1)
    func = partial(parallel_complete_path, test_cases, graph, False)
    results = []
    for result in tqdm(pool.imap(func=func, iterable=queue), total=len(queue)):
        results.append(result)
    pool.close()
    pool.join()
    for case in results:
        if case is not None:
            test_cases.update(case)
    return test_cases


def parallel_complete_path(test_cases, graph, modified, path):
    if 'modified' not in path:
        complete_path = bfs_path(path['stack'], path['trace'], 'acc', graph, modified=modified)
    else:
        complete_path = bfs_path(path['stack'], path['trace'], 'acc', graph, modified=path['modified'])
    if complete_path is not None:
        return extract_test_case(complete_path['trace'], graph)


def negative_cut(graph: Graph):
    E = graph.edges.copy()
    # bfs till graph covered
    test_cases = bfs_cut_cover([graph.nodes[0]], E, [], graph)
    return test_cases


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


def get_can_complete_without_terminal(state: int, graph):
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


def trace_to_str(T, graph):
    trace = "0"
    for edge in T:
        colour = "\033[1;32;40m"
        if edge.is_pop:
            colour = "\033[94m"
        elif edge.label in graph.nonterminal:
            colour = "\033[1;33;40m"
        trace += colour + " -" + str(edge.label) + "-> \033[0m" + str(edge.next_node.label)
    return trace


def get_reduce_edge(rule_label: str, reduce_amount: int, node: Node, S):
    reduce_edge = None
    for edge in node.edges:
        if edge.label == rule_label and edge.next_node == S[-reduce_amount - 1] and edge.is_pop:
            reduce_edge = edge
            break
    return reduce_edge


def extract_test_case(T, graph):
    cases = [""]
    for edge in T:
        if edge.swap is not None:
            # only one swap per traversal
            case = cases[0]
            cases.clear()
            for label in edge.swap:
                cases.append(case + str(label) + " ")
        elif edge.delete:
            # don't add edge to traversal
            continue
        elif edge.add is not None:
            # only one swap per traversal
            case = cases[0]
            cases.clear()
            for label in edge.add:
                if edge.label in graph.terminal and edge.label != "$end":
                    cases.append(case + str(edge.label)+ " " + str(label)+ " ")
                else:
                    cases.append(case + str(label) + " ")
        elif edge.label in graph.terminal and edge.label != "$end":
            for i in range(len(cases)):
                cases[i] += edge.label + " "
    return cases


def bfs_cut_cover(S, E, T, graph):
    test_cases = set()
    queue = list()
    queue.append({
        'stack': S.copy(),
        'trace': T.copy()
    })
    seen_edges = set()
    while True:
        path = queue.pop(0)
        cur_stack = path['stack']
        cur_trace = path['trace']
        cur_node = cur_stack[-1]

        # check for bad test case
        if len(cur_trace) > 2 * len(graph.edges):
            continue

        # append cut to test cases if its not an accepting state and can't get there without terminal
        if not cur_node.label == 'acc':
            # check if previous wasn't reduction edge that doesn't need a shift
            if (len(cur_trace) == 0 and not get_can_complete_without_terminal(cur_node.label, graph)) or (
                    len(cur_trace) > 0 and
                    not cur_trace[-1].is_pop and not get_can_complete_without_terminal(cur_node.label, graph)):
                test_cases.update(extract_test_case(cur_trace, graph))

        print_cond = False
        # check if all edges covered
        if len(E - seen_edges) == 0:
            queue.append(path)
            return test_cases

        if cur_node.label == 'acc':
            queue.append(path.copy())
            continue
        # check if there is a reduce rule that may exist for this state
        reduce_edges = []
        if cur_node.reduce_rule is not None:
            for rule in cur_node.reduce_rule:
                reduce_edges.append(get_reduce_edge(rule[0], rule[1], cur_node, cur_stack))

        # check if the previous move was reduce so we should shift a non-terminal
        if len(cur_trace) > 0 and cur_trace[-1].is_pop:
            shift_edge: Edge
            for edge in cur_node.edges:
                if edge.label == cur_trace[-1].label and not edge.is_pop:
                    shift_edge = edge
                    break
            seen_edges.add(shift_edge)
            new_path = {
                'stack': cur_stack.copy() + [shift_edge.next_node],
                'trace': cur_trace.copy() + [shift_edge]
            }

            if print_cond:
                print(extract_test_case(cur_trace, graph))
                print("Shifting non-terminal")
                print("Before: " + trace_to_str(cur_trace, graph))
                print('After: ' + trace_to_str(new_path['trace'], graph))
            queue.append(new_path)
        else:
            # if the previous step wasn't a reduce then we should shift on terminals and check
            # for valid reductions on all edges
            for edge in cur_node.edges:
                # avoid shifting on an self-loop
                if edge.label in graph.terminal and (edge.next_node != cur_node or edge not in seen_edges):
                    seen_edges.add(edge)
                    new_path = {
                        'stack': cur_stack.copy() + [edge.next_node],
                        'trace': cur_trace.copy() + [edge]
                    }
                    if print_cond:
                        print(extract_test_case(cur_trace, graph))
                        print("Shifting terminal")
                        print("Before: " + trace_to_str(cur_trace, graph))
                        print('After: ' + trace_to_str(new_path['trace'], graph))
                    queue.append(new_path)
                # check that reduction edge is correct edge
                elif edge.label in graph.nonterminal and edge in reduce_edges:
                    # pop nodes of stack
                    for rule_index in range(len(reduce_edges)):
                        if edge == reduce_edges[rule_index]:
                            new_stack = cur_stack.copy()
                            for i in range(cur_node.reduce_rule[rule_index][1]):
                                new_stack.pop(len(new_stack) - 1)

                            seen_edges.add(edge)
                            new_path = {
                                'stack': new_stack,
                                'trace': cur_trace.copy() + [edge],
                            }
                            if print_cond:
                                print(extract_test_case(cur_trace, graph))
                                print("Reducing")
                                print("Before: " + trace_to_str(cur_trace, graph))
                                print('After: ' + trace_to_str(new_path['trace'], graph))
                                print([edge])
                            queue.append(new_path)


def negative_replacement(graph):
    E = graph.edges.copy()
    test_cases = set()
    # bfs till graph covered
    print("Starting graph flooding")
    print(len(graph.edges))
    # bfs till graph covered
    queue = bfs_switch_cover([graph.nodes[0]], E, [], graph)

    # complete found paths
    new_queue = []
    for path in queue:
        if path['modified']:
            new_queue.append(path)
    queue = new_queue
    print("Graph covering complete. Test cases to complete " + str(len(queue)))
    # complete found paths
    pool = multiprocessing.Pool(multiprocessing.cpu_count() - 1)
    func = partial(parallel_complete_path, test_cases, graph, True)
    results = []
    for result in tqdm(pool.imap(func=func, iterable=queue), total=len(queue)):
        results.append(result)
    pool.close()
    pool.join()
    for case in results:
        if case is not None:
            test_cases.update(case)
    return test_cases


def bfs_switch_cover(S, E, T, graph: Graph):
    queue = list()
    queue.append({
        'stack': S.copy(),
        'trace': T.copy(),
        'modified': False  # field to check whether we should try and modify this current traversal or just complete it
    })
    seen_edges = set()
    while True:
        path = queue.pop(0)
        cur_stack = path['stack']
        cur_trace = path['trace']
        cur_node = cur_stack[-1]

        # check for bad test case
        if len(cur_trace) > 2 * len(graph.edges):
            continue

        # check if the traversal has not been modified and previous edge is a shift on a terminal
        if not path['modified'] and len(cur_trace) > 0 and (
                not cur_trace[-1].is_pop and cur_trace[-1].label in graph.terminal):
            # check if there are any terminal symbols in this grammar that doesnt intersect with the followset
            # of the previous state. This means that the previous shift edge can be replaced
            prev_state = 0
            if len(cur_trace) > 1:
                prev_state = cur_trace[-2].next_node.label
            follow_set = get_follow_set(prev_state, graph)
            set_diff = graph.terminal - follow_set - {'$end'}
            if len(set_diff) > 0:
                # duplicate the edge so that the original copy is not modified
                edge_copy = deepcopy(cur_trace[-1])
                edge_copy.swap = set_diff
                # duplicate the traversal so that one is modified and one is not
                path_copy = deepcopy(path)
                # replace last edge in copy with the modified edge
                path_copy['trace'][-1] = edge_copy
                path_copy['modified'] = True
                # add this extra path to the back of the queue and go on
                queue.append(path_copy)

        print_cond = False
        # check if all edges covered
        if len(E - seen_edges) == 0:
            queue.append(path)
            return queue

        # just continue if we already modified an edge in this traversal
        if path['modified']:
            queue.append(path.copy())
            continue

        if cur_node.label == 'acc':
            queue.append(path.copy())
            continue
        # check if there is a reduce rule that may exist for this state
        reduce_edges = []
        if cur_node.reduce_rule is not None:
            for rule in cur_node.reduce_rule:
                reduce_edges.append(get_reduce_edge(rule[0], rule[1], cur_node, cur_stack))

        # check if the previous move was reduce so we should shift a non-terminal
        if len(cur_trace) > 0 and cur_trace[-1].is_pop:
            shift_edge: Edge
            for edge in cur_node.edges:
                if edge.label == cur_trace[-1].label and not edge.is_pop:
                    shift_edge = edge
                    break
            seen_edges.add(shift_edge)
            new_path = {
                'stack': cur_stack.copy() + [shift_edge.next_node],
                'trace': cur_trace.copy() + [shift_edge],
                'modified': path['modified']
            }

            if print_cond:
                print(extract_test_case(cur_trace, graph))
                print("Shifting non-terminal")
                print("Before: " + trace_to_str(cur_trace, graph))
                print('After: ' + trace_to_str(new_path['trace'], graph))
            queue.append(new_path)
        else:
            # if the previous step wasn't a reduce then we should shift on terminals and check
            # for valid reductions on all edges
            for edge in cur_node.edges:
                # avoid shifting on an self-loop
                if edge.label in graph.terminal and (edge.next_node != cur_node or edge not in seen_edges):
                    seen_edges.add(edge)
                    new_path = {
                        'stack': cur_stack.copy() + [edge.next_node],
                        'trace': cur_trace.copy() + [edge],
                        'modified': path['modified']
                    }
                    if print_cond:
                        print(extract_test_case(cur_trace, graph))
                        print("Shifting terminal")
                        print("Before: " + trace_to_str(cur_trace, graph))
                        print('After: ' + trace_to_str(new_path['trace'], graph))
                    queue.append(new_path)
                # check that reduction edge is correct edge
                elif edge.label in graph.nonterminal and edge in reduce_edges:
                    # pop nodes of stack
                    for rule_index in range(len(reduce_edges)):
                        if edge == reduce_edges[rule_index]:
                            new_stack = cur_stack.copy()
                            for i in range(cur_node.reduce_rule[rule_index][1]):
                                new_stack.pop(len(new_stack) - 1)

                            seen_edges.add(edge)
                            new_path = {
                                'stack': new_stack,
                                'trace': cur_trace.copy() + [edge],
                                'modified': path['modified']
                            }
                            if print_cond:
                                print(extract_test_case(cur_trace, graph))
                                print("Reducing")
                                print("Before: " + trace_to_str(cur_trace, graph))
                                print('After: ' + trace_to_str(new_path['trace'], graph))
                                print([edge])
                            queue.append(new_path)


def negative_deletion(graph: Graph):
    E = graph.edges.copy()
    test_cases = set()
    # bfs till graph covered
    queue = bfs_delete_cover([graph.nodes[0]], E, [], graph)

    # complete found paths
    new_queue = []
    for path in queue:
        if path['modified']:
            new_queue.append(path)
    queue = new_queue
    print("Graph covering complete. Test cases to complete " + str(len(queue)))
    # complete found paths
    pool = multiprocessing.Pool(multiprocessing.cpu_count() - 1)
    func = partial(parallel_complete_path, test_cases, graph, True)
    results = []
    for result in tqdm(pool.imap(func=func, iterable=queue), total=len(queue)):
        results.append(result)
    pool.close()
    pool.join()
    for case in results:
        if case is not None:
            test_cases.update(case)
    return test_cases


def bfs_delete_cover(S, E, T, graph):
    queue = list()
    queue.append({
        'stack': S.copy(),
        'trace': T.copy(),
        'modified': False  # field to check whether we should try and modify this current traversal or just complete it
    })
    seen_edges = set()
    while True:
        path = queue.pop(0)
        cur_stack = path['stack']
        cur_trace = path['trace']
        cur_node = cur_stack[-1]

        # check for bad test case
        if len(cur_trace) > 2 * len(graph.edges):
            continue

        # check if the traversal has not been modified and previous edge is a shift on a terminal
        if not path['modified'] and len(cur_trace) > 1 and (
                not cur_trace[-1].is_pop and cur_trace[-1].label in graph.terminal) and cur_trace[
            -1].label != '$end':
            # check that there is no intersection in the followset of the two states around the last edge
            prev_state = 0
            if len(cur_trace) > 1:
                prev_state = cur_trace[-2].next_node.label
            prev_follow_set = get_follow_set(prev_state, graph)
            cur_follow_set = get_follow_set(cur_trace[-1].next_node.label, graph)
            # if there is no overlap in followset and we can't complete traversal from prev state
            # with no terminal shifts then we can safely delete this edge
            if prev_follow_set.isdisjoint(cur_follow_set) and not get_can_complete_without_terminal(prev_state, graph):
                # duplicate the edge so that the original copy is not modified
                edge_copy: Edge
                edge_copy = deepcopy(cur_trace[-1])
                edge_copy.delete = True
                # duplicate the traversal so that one is modified and one is not
                path_copy = deepcopy(path)
                # replace last edge in copy with the modified edge
                path_copy['trace'][-1] = edge_copy
                path_copy['modified'] = True
                # add this extra path to the back of the queue and go on
                queue.append(path_copy)

        print_cond = False
        # check if all edges covered
        if len(E - seen_edges) == 0:
            queue.append(path)
            return queue

        # just continue if we already modified an edge in this traversal
        if path['modified']:
            queue.append(path.copy())
            continue

        if cur_node.label == 'acc':
            queue.append(path.copy())
            continue
        # check if there is a reduce rule that may exist for this state
        reduce_edges = []
        if cur_node.reduce_rule is not None:
            for rule in cur_node.reduce_rule:
                reduce_edges.append(get_reduce_edge(rule[0], rule[1], cur_node, cur_stack))

        # check if the previous move was reduce so we should shift a non-terminal
        if len(cur_trace) > 0 and cur_trace[-1].is_pop:
            shift_edge: Edge
            for edge in cur_node.edges:
                if edge.label == cur_trace[-1].label and not edge.is_pop:
                    shift_edge = edge
                    break
            seen_edges.add(shift_edge)
            new_path = {
                'stack': cur_stack.copy() + [shift_edge.next_node],
                'trace': cur_trace.copy() + [shift_edge],
                'modified': path['modified']
            }

            if print_cond:
                print(extract_test_case(cur_trace, graph))
                print("Shifting non-terminal")
                print("Before: " + trace_to_str(cur_trace, graph))
                print('After: ' + trace_to_str(new_path['trace'], graph))
            queue.append(new_path)
        else:
            # if the previous step wasn't a reduce then we should shift on terminals and check
            # for valid reductions on all edges
            for edge in cur_node.edges:
                # avoid shifting on an self-loop
                if edge.label in graph.terminal and (edge.next_node != cur_node or edge not in seen_edges):
                    seen_edges.add(edge)
                    new_path = {
                        'stack': cur_stack.copy() + [edge.next_node],
                        'trace': cur_trace.copy() + [edge],
                        'modified': path['modified']
                    }
                    if print_cond:
                        print(extract_test_case(cur_trace, graph))
                        print("Shifting terminal")
                        print("Before: " + trace_to_str(cur_trace, graph))
                        print('After: ' + trace_to_str(new_path['trace'], graph))
                    queue.append(new_path)
                # check that reduction edge is correct edge
                elif edge.label in graph.nonterminal and edge in reduce_edges:
                    # pop nodes of stack
                    for rule_index in range(len(reduce_edges)):
                        if edge == reduce_edges[rule_index]:
                            new_stack = cur_stack.copy()
                            for i in range(cur_node.reduce_rule[rule_index][1]):
                                new_stack.pop(len(new_stack) - 1)

                            seen_edges.add(edge)
                            new_path = {
                                'stack': new_stack,
                                'trace': cur_trace.copy() + [edge],
                                'modified': path['modified']
                            }
                            if print_cond:
                                print(extract_test_case(cur_trace, graph))
                                print("Reducing")
                                print("Before: " + trace_to_str(cur_trace, graph))
                                print('After: ' + trace_to_str(new_path['trace'], graph))
                                print([edge])
                            queue.append(new_path)


def bfs_cover(S, E, T, graph):
    queue = list()
    queue.append({
        'stack': S.copy(),
        'trace': T.copy()
    })
    seen_edges = set()
    while True:
        path = queue.pop(0)
        cur_stack = path['stack']
        cur_trace = path['trace']
        cur_node = cur_stack[-1]
        print_cond = False

        # check for bad test case
        if len(cur_trace) > 2 * len(graph.edges):
            continue

        # check if all edges covered
        if len(E - seen_edges) == 0:
            queue.append(path)
            return queue

        if cur_node.label == 'acc':
            queue.append(path.copy())
            continue
        # check if there is a reduce rule that may exist for this state
        reduce_edges = []
        if cur_node.reduce_rule is not None:
            for rule in cur_node.reduce_rule:
                reduce_edges.append(get_reduce_edge(rule[0], rule[1], cur_node, cur_stack))

        # check if the previous move was reduce so we should shift a non-terminal
        if len(cur_trace) > 0 and cur_trace[-1].is_pop:
            shift_edge: Edge
            for edge in cur_node.edges:
                if edge.label == cur_trace[-1].label and not edge.is_pop:
                    shift_edge = edge
                    break
            seen_edges.add(shift_edge)
            new_path = {
                'stack': cur_stack.copy() + [shift_edge.next_node],
                'trace': cur_trace.copy() + [shift_edge]
            }

            if print_cond:
                print(extract_test_case(cur_trace, graph))
                print("Shifting non-terminal")
                print("Before: " + trace_to_str(cur_trace, graph))
                print('After: ' + trace_to_str(new_path['trace'], graph))
            queue.append(new_path)
        else:
            # if the previous step wasn't a reduce then we should shift on terminals and check
            # for valid reductions on all edges
            for edge in cur_node.edges:
                # avoid shifting on an self-loop
                if edge.label in graph.terminal and (edge.next_node != cur_node or edge not in seen_edges):
                    seen_edges.add(edge)
                    new_path = {
                        'stack': cur_stack.copy() + [edge.next_node],
                        'trace': cur_trace.copy() + [edge]
                    }
                    if print_cond:
                        print(extract_test_case(cur_trace, graph))
                        print("Shifting terminal")
                        print("Before: " + trace_to_str(cur_trace, graph))
                        print('After: ' + trace_to_str(new_path['trace'], graph))
                    queue.append(new_path)
                # check that reduction edge is correct edge
                elif edge.label in graph.nonterminal and edge in reduce_edges:
                    # pop nodes of stack
                    for rule_index in range(len(reduce_edges)):
                        if edge == reduce_edges[rule_index]:
                            new_stack = cur_stack.copy()
                            if print_cond:
                                print(cur_node.reduce_rule)
                            for i in range(cur_node.reduce_rule[rule_index][1]):
                                new_stack.pop(len(new_stack) - 1)

                            seen_edges.add(edge)
                            new_path = {
                                'stack': new_stack,
                                'trace': cur_trace.copy() + [edge]
                            }
                            if print_cond:
                                print(extract_test_case(cur_trace, graph))
                                print("Reducing")
                                print("Before: " + trace_to_str(cur_trace, graph))
                                print('After: ' + trace_to_str(new_path['trace'], graph))
                                print([edge])
                                string = "stack: [ "
                                for node in cur_stack:
                                    string += str(node.label)+" "
                                print(string)
                            queue.append(new_path)


def negative_addition(graph: Graph):
    E = graph.edges.copy()
    test_cases = set()
    # bfs till graph covered
    queue = bfs_add_cover([graph.nodes[0]], E, [], graph)

    # complete found paths
    new_queue = []
    for path in queue:
        if path['modified']:
            new_queue.append(path)
    queue = new_queue
    print("Graph covering complete. Test cases to complete " + str(len(queue)))
    # complete found paths
    pool = multiprocessing.Pool(multiprocessing.cpu_count() - 1)
    func = partial(parallel_complete_path, test_cases, graph, True)
    results = []
    for result in tqdm(pool.imap(func=func, iterable=queue), total=len(queue)):
        results.append(result)
    pool.close()
    pool.join()
    for case in results:
        if case is not None:
            test_cases.update(case)
    return test_cases

    return test_cases


def bfs_add_cover(S, E, T, graph):
    queue = list()
    queue.append({
        'stack': S.copy(),
        'trace': T.copy(),
        'modified': False  # field to check whether we should try and modify this current traversal or just complete it
    })
    seen_edges = set()
    while True:
        path = queue.pop(0)
        cur_stack = path['stack']
        cur_trace = path['trace']
        cur_node = cur_stack[-1]

        # check for bad test case
        if len(cur_trace) > 2 * len(graph.edges):
            continue

        # check if the traversal has not been modified and we aren't already in the accept state
        if not path['modified'] and not cur_node.is_accept:
            # check if there are any terminal symbols in this grammar that doesnt intersect with the followset
            # of the previous state. This means that the previous shift edge can be replaced
            cur_state = 0
            if len(cur_trace) > 0:
                cur_state = cur_trace[-1].next_node.label

            follow_set = get_follow_set(cur_state, graph)
            set_diff = graph.terminal - follow_set - {'$end'}
            if len(set_diff) > 0:
                if len(cur_trace) > 0:
                    # duplicate the edge so that the original copy is not modified
                    edge_copy = deepcopy(cur_trace[-1])
                    edge_copy.add = set_diff
                    # duplicate the traversal so that one is modified and one is not
                    path_copy = deepcopy(path)
                    # replace last edge in copy with the modified edge
                    path_copy['trace'][-1] = edge_copy
                    path_copy['modified'] = True
                    # add this extra path to the back of the queue and go on
                    queue.append(path_copy)
                else:
                    # duplicate the edge so that the original copy is not modified
                    edge_copy = Edge("", None, False)
                    edge_copy.add = set_diff
                    # duplicate the traversal so that one is modified and one is not
                    path_copy = deepcopy(path)
                    # replace last edge in copy with the modified edge
                    path_copy['trace'].append(edge_copy)
                    path_copy['modified'] = True
                    # add this extra path to the back of the queue and go on
                    queue.append(path_copy)

        print_cond = False
        # check if all edges covered
        if len(E - seen_edges) == 0:
            queue.append(path)
            return queue

        # just continue if we already modified an edge in this traversal
        if path['modified']:
            queue.append(path.copy())
            continue

        if cur_node.label == 'acc':
            queue.append(path.copy())
            continue
        # check if there is a reduce rule that may exist for this state
        reduce_edges = []
        if cur_node.reduce_rule is not None:
            for rule in cur_node.reduce_rule:
                reduce_edges.append(get_reduce_edge(rule[0], rule[1], cur_node, cur_stack))

        # check if the previous move was reduce so we should shift a non-terminal
        if len(cur_trace) > 0 and cur_trace[-1].is_pop:
            shift_edge: Edge
            for edge in cur_node.edges:
                if edge.label == cur_trace[-1].label and not edge.is_pop:
                    shift_edge = edge
                    break
            seen_edges.add(shift_edge)
            new_path = {
                'stack': cur_stack.copy() + [shift_edge.next_node],
                'trace': cur_trace.copy() + [shift_edge],
                'modified': path['modified']
            }

            if print_cond:
                print(extract_test_case(cur_trace, graph))
                print("Shifting non-terminal")
                print("Before: " + trace_to_str(cur_trace, graph))
                print('After: ' + trace_to_str(new_path['trace'], graph))
            queue.append(new_path)
        else:
            # if the previous step wasn't a reduce then we should shift on terminals and check
            # for valid reductions on all edges
            for edge in cur_node.edges:
                # avoid shifting on an self-loop
                if edge.label in graph.terminal and (edge.next_node != cur_node or edge not in seen_edges):
                    seen_edges.add(edge)
                    new_path = {
                        'stack': cur_stack.copy() + [edge.next_node],
                        'trace': cur_trace.copy() + [edge],
                        'modified': path['modified']
                    }
                    if print_cond:
                        print(extract_test_case(cur_trace, graph))
                        print("Shifting terminal")
                        print("Before: " + trace_to_str(cur_trace, graph))
                        print('After: ' + trace_to_str(new_path['trace'], graph))
                    queue.append(new_path)
                # check that reduction edge is correct edge
                elif edge.label in graph.nonterminal and edge in reduce_edges:
                    # pop nodes of stack
                    for rule_index in range(len(reduce_edges)):
                        if edge == reduce_edges[rule_index]:
                            new_stack = cur_stack.copy()
                            for i in range(cur_node.reduce_rule[rule_index][1]):
                                new_stack.pop(len(new_stack) - 1)

                            seen_edges.add(edge)
                            new_path = {
                                'stack': new_stack,
                                'trace': cur_trace.copy() + [edge],
                                'modified': path['modified']
                            }
                            if print_cond:
                                print(extract_test_case(cur_trace, graph))
                                print("Reducing")
                                print("Before: " + trace_to_str(cur_trace, graph))
                                print('After: ' + trace_to_str(new_path['trace'], graph))
                                print([edge])
                            queue.append(new_path)


def bfs_path(S, T, goal_label, graph, modified=False):
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

        print_cond = False
        # check if the destination has been reached
        if str(cur_node.label) == goal_label:
            path['modified'] = modified
            return path

        # check for bad test case
        if len(cur_trace) > 2 * len(graph.edges):
            continue

        # check if there is a reduce rule that may exist for this state
        reduce_edges = []
        if cur_node.reduce_rule is not None:
            for rule in cur_node.reduce_rule:
                reduce_edges.append(get_reduce_edge(rule[0], rule[1], cur_node, cur_stack))

        # check if the previous move was reduce so we should shift a non-terminal
        if len(cur_trace) > 0 and cur_trace[-1].is_pop:
            shift_edge: Edge
            for edge in cur_node.edges:
                if edge.label == cur_trace[-1].label and not edge.is_pop:
                    shift_edge = edge
                    break

            new_path = {
                'stack': cur_stack.copy() + [shift_edge.next_node],
                'trace': cur_trace.copy() + [shift_edge]
            }

            if print_cond:
                print(extract_test_case(cur_trace, graph))
                print("Shifting non-terminal")
                print("Before: " + trace_to_str(cur_trace, graph))
                print('After: ' + trace_to_str(new_path['trace'], graph))
            queue.append(new_path)
        else:
            # if the previous step wasn't a reduce then we should shift on terminals and check
            # for valid reductions on all edges
            for edge in cur_node.edges:
                if edge.label in graph.terminal and edge.next_node != cur_node:
                    new_path = {
                        'stack': cur_stack.copy() + [edge.next_node],
                        'trace': cur_trace.copy() + [edge]
                    }
                    if print_cond:
                        print(extract_test_case(cur_trace, graph))
                        print("Shifting terminal")
                        print("Before: " + trace_to_str(cur_trace, graph))
                        print('After: ' + trace_to_str(new_path['trace'], graph))
                    queue.append(new_path)
                # check that reduction edge is correct edge
                elif edge.label in graph.nonterminal and edge in reduce_edges:
                    # pop nodes of stack
                    for rule_index in range(len(reduce_edges)):
                        if edge == reduce_edges[rule_index]:
                            new_stack = cur_stack.copy()
                            for i in range(cur_node.reduce_rule[rule_index][1]):
                                new_stack.pop(len(new_stack) - 1)

                            new_path = {
                                'stack': new_stack,
                                'trace': cur_trace.copy() + [edge]
                            }
                            if print_cond:
                                print(extract_test_case(cur_trace, graph))
                                print("Reducing by " + str(cur_node.reduce_rule[rule_index][1]))
                                print(cur_node.reduce_rule)
                                print("Before: " + trace_to_str(cur_trace, graph))
                                stack = "[ "
                                for node in cur_stack:
                                    stack += str(node.label) + " "
                                print(stack)
                                print('After: ' + trace_to_str(new_path['trace'], graph))
                                stack = "[ "
                                for node in new_stack:
                                    stack += str(node.label) + " "
                                print(stack)
                            queue.append(new_path)
