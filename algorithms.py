import random
import sys
import zlib

import tqdm

import debug_utils
from config import Config
from debug_utils import trace_to_str
from general_utils import extract_test_case
from graph_components import Graph, Edge
from pos_utils import get_reduce_edge, push, pop

shortest_deriv_map = dict()


def dynamic_traversal(graph: Graph):
    # we only look at push edges during traversal to solve for pop edges. Pop edges should be solved before
    # the corresponding non-terminal push edges is considered valid. We initialize valid edges with all terminal
    # push edges and non-terminal push edges originating from epsilon reductions.
    valid_edges = set()
    rem_pop = set()
    sub_table = dict()
    waiting = set()
    for e in graph.edges:
        if e.is_pop:
            rem_pop.add(e)
    # start solving for pop edges
    print("Started Solving for Pop Edges. Total " + str(len(rem_pop)))
    previous_remainder = -1
    while 0 < len(rem_pop) + len(waiting) != previous_remainder:
        print(f"Remaining pop edges: {len(rem_pop) + len(waiting)}             \r")
        previous_remainder = len(rem_pop) + len(waiting)
        rem_pop.update(waiting)
        waiting = set()
        for edge in rem_pop.copy():
            solved, solution = solve_for_pop(edge, graph)
            if solved:
                # find non term push edge in sub table add to table
                for e in edge.next_node.edges:
                    if not e.is_pop and e.label in graph.nonterminal:
                        if e not in sub_table:
                            sub_table[e] = list()
                        if solution['trace'][-1].label == e.label:
                            solution['stack'] = [e.next_node]
                            solution['trace'].append(e)
                            sub_table[e].append(solution)
            else:
                print("Waiting")
                waiting.add(edge)
            rem_pop.remove(edge)
    print("Finished Solving for Pop Edges.")
    if len(rem_pop) + len(waiting) > 0:
        print(f"Skipped {len(rem_pop) + len(waiting)} pop edges")
    # splice solutions together
    complete = cover_all_pop(sub_table, graph)
    print("Finished Splicing Solutions.")
    tests = set()
    for path in tqdm.tqdm(complete):
        # if extract_test_case(path['trace'], graph, sub_table=sub_table,
        #                      shortest_table=shortest_deriv_map,
        #                      test_suite_type="positive")[0] != "PROGRAM ID : MAIN : IF ID : CHILLAX END ":
        #     continue
        # extracted_cases = extract_test_case(path['trace'], graph, sub_table=sub_table,
        #                                         shortest_table=shortest_deriv_map)
        # for case in extracted_cases:
        #     if case.replace(" ", "") == "PROGRAMID:MAIN:IFNOTID:CHILLAXEND":
        #         print("Old path: __________________________________")
        #         print(debug_utils.trace_to_str(path['trace'], graph))
        #         print("Unmutated case:_________________________________")
        #         print(extract_test_case(path['trace'], graph, sub_table=sub_table, shortest_table=shortest_deriv_map,
        #                                 test_suite_type="positive")[0])
        #         print("Mutated case:_____________________________________")
        #         print(case)
        tests.update(extract_test_case(path['trace'], graph, sub_table=sub_table,
                                       shortest_table=shortest_deriv_map))
    return tests


def solve_for_pop(candidate: Edge, graph):
    assert candidate.is_pop
    # make a path out of only push edges which can then be subbed out in later pass
    src = candidate.next_node
    target = candidate.source
    assert candidate.local_stack[0] == src
    assert candidate.local_stack[-1] == target
    trace = []
    debug_str = "Computing pop tmp"
    for i in range(len(candidate.local_stack) - 1):
        node = candidate.local_stack[i]
        next_node = candidate.local_stack[i + 1]
        smallest_e = None
        pop_tmp = dict()
        for e in node.pre_edges:
            if e.is_pop:
                debug_str += f"\n found pop edge {e} "
                if e.label not in pop_tmp:
                    debug_str += f"and added it to map with count : {e.pop_count}"
                    pop_tmp[e.label] = e.pop_count
                elif e.pop_count < pop_tmp[e.label]:
                    debug_str += f"and replaced existing count with {e.pop_count}"
                    pop_tmp[e.label] = e.pop_count
                else:
                    debug_str += "but did nothing"

        smallest_nt = None
        min_pop = 1000000
        for e in node.edges:
            if e.next_node == next_node and not e.is_pop and e.label in graph.nonterminal and \
                    e.label not in pop_tmp:
                continue
            if e.next_node == next_node and not e.is_pop and e.label in graph.nonterminal and \
                    pop_tmp[
                        e.label] < min_pop:
                smallest_nt = e
                min_pop = pop_tmp[e.label]
                if min_pop == 0:
                    break
            elif e.next_node == next_node and e.label in graph.terminal and not e.is_pop and smallest_e is None:
                smallest_e = e

        if smallest_e is None or min_pop == 0:
            smallest_e = smallest_nt
        if smallest_e is None:
            print(f"Ignoring {candidate}")
            return False, None
        assert smallest_e is not None
        trace.append(smallest_e)
    trace.append(candidate)
    assert len(trace) == len(candidate.local_stack)
    return True, {
        'stack': [src],
        'trace': trace
    }


def cover_all_pop(sub_table, graph):
    # find starting branches
    print('Constructing reduction graph')
    reduction_graph = construct_reduction_graph(sub_table, graph)
    print('Finished constructing reduction graph')
    # precompute shortest derivations
    print("Calculation shortest derivations")
    shortest_derivations(sub_table, shortest_deriv_map, graph)
    print("Finished calculation shortest derivations")
    # sub together shortest paths to cover all segments
    complete = []
    for i, key in enumerate(sub_table):
        for p in sub_table[key]:
            path = complete_segment(p, shortest_deriv_map, reduction_graph, graph)
            if path is not None:
                complete.append(path)
    return complete


def construct_reduction_graph(sub_table, graph):
    # find starting branches
    start_edges = find_start_edges(sub_table, graph)
    node_map = dict()
    tree_content = set()
    next_layer_contents = set()
    current_layer = list()
    next_layer = list()
    # fill in first layer from start edges
    for edge in start_edges:
        node = {
            'edge': edge,
            'traces': [],
            'parent': None,
            'index_in_parent': None,
        }
        """
        edge is this edge,
        traces or its possible reduction paths, contains children of this edge in trace
        parent is the parent node of this node
        index_in_parent is a tuple indicating trace and position in trace
        """
        paths = sub_table[edge]
        paths.sort(key=lambda x: trace_to_str(x['trace'], graph))
        for path in paths:
            node['traces'].append(path['trace'])
        current_layer.append(node)
        if edge not in node_map:
            node_map[edge] = []
        node_map[edge].append(node)
        tree_content.add(edge)
    # loop until we have a tree of shallowest embeddings
    next_layer = current_layer
    layer_count = 1
    while len(next_layer) != 0:
        current_layer = next_layer
        next_layer = list()
        next_layer_contents = set()
        print("Layer %d: %d" % (layer_count, len(current_layer)))
        layer_count += 1
        for node in current_layer:
            for i, t in enumerate(node['traces']):
                for j, e in enumerate(t):
                    # only embed new reduction paths or ones at the same depth
                    if (not e.is_pop and e.label in graph.nonterminal) and (
                            e not in tree_content or e in next_layer_contents):
                        new_node = {
                            'edge': e,
                            'traces': [],
                            'parent': node,
                            'index_in_parent': (i, j)
                        }
                        paths = sub_table[e]
                        paths.sort(key=lambda x: trace_to_str(x['trace'], graph))
                        for path in paths:
                            new_node['traces'].append(path['trace'])
                        next_layer.append(new_node)
                        if e not in node_map:
                            node_map[e] = []
                        node_map[e].append(new_node)
                        tree_content.add(e)
                        next_layer_contents.add(e)
    return node_map


def complete_segment(path, shortest_derivation_map, reduction_tree_map, graph):
    trace = path['trace']
    if trace[-1] not in reduction_tree_map:
        # TODO figure out why this happened with simpl18
        print("Ignoring " + str(trace[-1]))
        return
    cur_node_list = reduction_tree_map[trace[-1]]
    # pick a node from the same depth at random
    seed = Config.get_instance().get_seed()
    seed += zlib.adler32(str(path['trace'][-1]).encode('utf_8'))
    random.seed(seed)
    i = random.randint(0, len(cur_node_list) - 1)
    cur_node_list.sort(key=lambda x: str(x['edge']))
    cur_node = cur_node_list[i]
    # imbed till we reach the top of the reduction tree
    while cur_node['parent'] is not None:
        parent_node = cur_node['parent']
        trace_index = cur_node['index_in_parent'][0]
        parent_trace = parent_node['traces'][trace_index]
        embed_index = cur_node['index_in_parent'][1]
        trace = parent_trace[:embed_index] + trace + parent_trace[embed_index + 1:]
        cur_node = parent_node
    # sub out all remaining with shortest derivation
    subbed_trace = []
    for i, e in enumerate(trace):
        if not e.is_pop and e.label in graph.nonterminal and not (
                trace[i - 1].is_pop):
            if e not in shortest_deriv_map:
                print("Ignoring " + str(trace[-1]))
                return
            subbed_trace.extend(shortest_deriv_map[e]['trace'])
        else:
            subbed_trace.append(e)
    return {'trace': subbed_trace}


def is_unsubbed_nt(i, cur_trace, graph):
    edge = cur_trace[i]
    if not edge.is_pop and edge.label in graph.nonterminal and not cur_trace[
        i - 1].is_pop:
        return True
    return False


def reverse_sub_table(sub_table, graph):
    reverse = dict()
    for key in sub_table:
        for p in sub_table[key]:
            for i in range(len(p['trace'])):
                if is_unsubbed_nt(i, p['trace'], graph):
                    edge = p['trace'][i]
                    if not edge in reverse:
                        reverse[edge] = []
                    reverse[edge].append(p['trace'])
    return reverse


def shortest_derivations(sub_map, shortest_map, graph):
    tmp_map = {}
    previous = -1
    while 0 < len(sub_map.keys() - shortest_map.keys()) != previous:
        previous = len(sub_map.keys() - shortest_map.keys())
        next_solve = list(sub_map.keys() - shortest_map.keys())
        next_solve.sort(key=str)
        # loop over all non-terminal edges we don't have a shortest derivation for yet
        for nt_edge in tqdm.tqdm(next_solve):
            min_len = 1000000
            min_paths = []

            for path in sub_map[nt_edge]:
                deriv = []
                i = 0
                can_solve = True
                for e in path['trace']:
                    if e.label in graph.terminal or e.is_pop:
                        deriv.append(e)
                    else:
                        if is_unsubbed_nt(i, path['trace'], graph):
                            edge = path['trace'][i]
                            if edge in shortest_map:
                                deriv.extend(shortest_map[edge]['trace'])
                            else:
                                can_solve = False
                                break
                        else:
                            deriv.append(e)
                    i += 1
                if can_solve and len(deriv) < min_len:
                    min_len = len(deriv)
                    min_paths = [deriv]
                elif can_solve and len(deriv) == min_len:
                    min_paths.append(deriv)
            if len(min_paths) != 0:
                if len(min_paths) == 1:
                    string = \
                        extract_test_case(min_paths[0], graph,
                                          test_suite_type='positive',
                                          stack=False)[0]
                    tmp_map[nt_edge] = [string]
                    shortest_map[nt_edge] = {'trace': min_paths[0]}
                else:
                    strs = []
                    str_map = dict()
                    for trace in min_paths:
                        string = \
                            extract_test_case(trace, graph, test_suite_type='positive',
                                              stack=False)[0]
                        strs.append(string)
                        str_map[string] = trace
                    strs.sort()
                    tmp_map[nt_edge] = strs
                    seed = Config.get_instance().get_seed()
                    seed += zlib.adler32(str(nt_edge).encode('utf_8'))
                    random.seed(seed)
                    i = random.randint(0, len(strs) - 1)
                    shortest_map[nt_edge] = {'trace': str_map[strs[i]]}

    if previous > 0:
        print(f"Could not find shortest derivations for {previous}")


def splice_segments(sub_map, graph: Graph):
    # find shortest for all sub
    shortest_map = find_shortest_sub_map(sub_map)
    # find starting branches
    start_edges = find_start_edges(sub_map, graph)
    queue = []
    subbed = set()
    complete_paths = []
    for edge in start_edges:
        queue.extend(sub_map[edge])
    seen = set()
    # splice in using BFS
    while len(queue) > 0:
        sys.stdout.write("Subbed: " + str(len(subbed)) + "\r" * 30)
        cur_path = queue.pop(0)
        cur_trace = cur_path['trace']
        if trace_to_str(cur_trace, graph) in seen:
            continue
        seen.add(trace_to_str(cur_trace, graph))
        complete = True
        for i in range(len(cur_trace)):
            edge = cur_trace[i]
            # check for possible non term push edge to sub
            if not edge.is_pop and edge.label in graph.nonterminal and not cur_trace[
                i - 1].is_pop:
                # splice
                if edge not in subbed:
                    subbed.add(edge)
                    for p in sub_map[edge]:
                        new_trace = cur_trace[:i] + p['trace'] + cur_trace[i + 1:]
                        queue.append({'trace': new_trace})
                else:
                    new_trace = cur_trace[:i] + shortest_map[edge]['trace'] + cur_trace[
                                                                              i + 1:]
                    queue.append({'trace': new_trace})
                complete = False
        if complete:
            complete_paths.append(cur_path)
    return complete_paths


def find_shortest_sub_map(sub_map):
    shortest_map = dict()
    for key in sub_map:
        min_p = sub_map[key][0]
        min_l = len(min_p['trace'])
        for p in sub_map[key]:
            if len(p['trace']) < min_l:
                min_p = p
                min_l = len(min_p['trace'])
        shortest_map[key] = min_p
    return shortest_map


def find_start_edges(sub_map, graph):
    start = list()
    for key in sub_map:
        next_node = key.next_node
        can_accept = False
        for edge in next_node.edges:
            if edge.next_node.label == 'acc' or edge.next_node.is_accept:
                can_accept = True
                break
        if can_accept:
            start.append(key)
    return start


def full_traversal(graph: Graph):
    dynamic_traversal(graph)
    E = graph.edges.copy()
    test_cases = set()
    config = Config.get_instance()
    # bfs till graph covered
    print("Starting graph flooding: " + str(len(E)) + " edges to cover.")
    queue = []
    if not config.get_clasic_flag():
        queue = flooding_improved([graph.nodes[0]], E, [], graph)
    else:
        queue = flooding([graph.nodes[0]], E, [], graph)
    print("Graph covering complete. Test cases to complete " + str(len(queue)))
    # complete found paths
    count = 0
    for path in queue:
        complete = None
        print("------------------------------")
        print(debug_utils.trace_to_str(path['trace'], graph))
        if not config.get_clasic_flag():
            complete = path_completion_improved(path['stack'], path['trace'], 'acc',
                                                graph)

        else:
            complete = path_completion(path['stack'], path['trace'], 'acc', graph)
        print(debug_utils.trace_to_str(complete['trace'], graph))
        print(extract_test_case(complete['trace'], graph)[0])
        test_cases.update(extract_test_case(complete['trace'], graph))
        count += 1
    print("Path completion complete")
    return test_cases


def flooding(S, E, T, graph):
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
                reduce_edges.append(
                    get_reduce_edge(rule[0], rule[1], cur_node, cur_stack))

        # check if the previous move was reduce so we should shift a non-terminal
        if len(cur_trace) > 0 and cur_trace[-1].is_pop:
            shift_edge: Edge
            for edge in cur_node.edges:
                if edge.label == cur_trace[-1].label and not edge.is_pop:
                    shift_edge = edge
                    break
            seen_edges.add(shift_edge)
            push(cur_stack, cur_trace, queue, shift_edge)
        else:
            # if the previous step wasn't a reduce then we should shift on terminals and check
            # for valid reductions on all edges
            for edge in cur_node.edges:
                # avoid shifting on an self-loop
                if edge.label in graph.terminal and (
                        edge.next_node != cur_node or edge not in seen_edges):
                    seen_edges.add(edge)
                    push(cur_stack, cur_trace, queue, edge)
                # check that reduction edge is correct edge
                elif edge.label in graph.nonterminal and edge in reduce_edges:
                    for rule_index in range(len(reduce_edges)):
                        if edge == reduce_edges[rule_index]:
                            # pop nodes of stack
                            pop(cur_stack, cur_trace, queue, edge,
                                cur_node.reduce_rule[rule_index][1])
                            seen_edges.add(edge)


def flooding_improved(S, E, T, graph):
    fresh_queue = list()  # traversals that have just covered a previously unseen edge
    stale_queue = list()  # traversal that has covered a previously unseen edge but now has no more unseen edges to cover
    brute_force_queue = list()  # traversal that covers an already seen edge as its last edge. Used when no fresh_queue
    fresh_queue.append({
        'stack': S.copy(),
        'trace': T.copy()
    })
    seen_edges = set()
    while True:
        new_edge_seen = False
        path_from_brute = False
        path = None
        if len(fresh_queue) > 0:
            path = fresh_queue.pop(0)
        else:
            unblock(S, E, T, graph, seen_edges, fresh_queue, stale_queue)
            continue
        cur_stack = path['stack']
        cur_trace = path['trace']
        cur_node = cur_stack[-1]

        # check for bad test case
        if len(cur_trace) > 2 * len(graph.edges):
            continue

        # check if all edges covered
        if len(E - seen_edges) == 0:
            stale_queue.append(path)
            return stale_queue + fresh_queue

        if cur_node.label == 'acc':
            stale_queue.append(path.copy())
            continue
        # check if there is a reduce rule that may exist for this state
        reduce_edges = []
        if cur_node.reduce_rule is not None:
            for rule in cur_node.reduce_rule:
                reduce_edges.append(
                    get_reduce_edge(rule[0], rule[1], cur_node, cur_stack))

        # check if the previous move was reduce so we should shift a non-terminal
        if len(cur_trace) > 0 and cur_trace[-1].is_pop:
            shift_edge: Edge
            for edge in cur_node.edges:
                if edge.label == cur_trace[-1].label and not edge.is_pop:
                    shift_edge = edge
                    break
            if shift_edge not in seen_edges:
                push(cur_stack, cur_trace, fresh_queue, shift_edge)
                new_edge_seen = True
            else:
                push(cur_stack, cur_trace, brute_force_queue, shift_edge)
            seen_edges.add(shift_edge)

        else:
            # if the previous step wasn't a reduce then we should shift on terminals and check
            # for valid reductions on all edges
            for edge in cur_node.edges:
                # avoid shifting on an self-loop
                if edge.label in graph.terminal:
                    if edge not in seen_edges:
                        new_edge_seen = True
                        push(cur_stack, cur_trace, fresh_queue, edge)
                    else:
                        push(cur_stack, cur_trace, brute_force_queue, edge)
                    seen_edges.add(edge)
                # check that reduction edge is correct edge
                elif edge.label in graph.nonterminal and edge in reduce_edges:
                    for rule_index in range(len(reduce_edges)):
                        if edge == reduce_edges[rule_index]:
                            # pop nodes of stack
                            if edge not in seen_edges:
                                new_edge_seen = True
                                pop(cur_stack, cur_trace, fresh_queue, edge,
                                    cur_node.reduce_rule[rule_index][1])
                            else:
                                pop(cur_stack, cur_trace, brute_force_queue, edge,
                                    cur_node.reduce_rule[rule_index][1])
                            seen_edges.add(edge)
        if not new_edge_seen and not path_from_brute:
            stale_queue.append(path)


def path_completion(S, T, goal_label, graph):
    queue = list()
    queue.append({
        'stack': S.copy(),
        'trace': T.copy()
    })
    total_paths = 1
    while len(queue) > 0:
        path = queue.pop(0)
        cur_stack = path['stack']
        cur_trace = path['trace']
        cur_node = cur_stack[-1]

        print("Total Paths: " + str(total_paths))
        # check if the destination has been reached
        if str(cur_node.label) == goal_label:
            return path

        # check for bad test case
        if len(cur_trace) > 2 * len(graph.edges):
            continue
        else:
            total_paths -= 1

        # check if there is a reduce rule that may exist for this state
        reduce_edges = []
        if cur_node.reduce_rule is not None:
            for rule in cur_node.reduce_rule:
                reduce_edges.append(
                    get_reduce_edge(rule[0], rule[1], cur_node, cur_stack))

        # check if the previous move was pop so we should shift a non-terminal
        if len(cur_trace) > 0 and cur_trace[-1].is_pop:
            shift_edge: Edge
            for edge in cur_node.edges:
                if edge.label == cur_trace[-1].label and not edge.is_pop:
                    shift_edge = edge
                    break
            push(cur_stack, cur_trace, queue, shift_edge)
            total_paths += 1
        else:
            # if the previous step wasn't a pop then we should shift on terminals and check
            # for valid reductions on all edges
            for edge in cur_node.edges:
                if edge.label in graph.terminal and edge.next_node != cur_node:
                    push(cur_stack, cur_trace, queue, edge)
                    total_paths += 1
                # check that reduction edge is correct edge
                elif edge.label in graph.nonterminal and edge in reduce_edges:
                    # pop nodes of stack
                    for rule_index in range(len(reduce_edges)):
                        if edge == reduce_edges[rule_index]:
                            # pop nodes of stack
                            pop(cur_stack, cur_trace, queue, edge,
                                cur_node.reduce_rule[rule_index][1])
                            total_paths += 1


def path_completion_improved(S, T, goal_label, graph):
    """Complete a path that was generated during the flooding phase"""
    high_priority_queue = list()
    low_priority_queue = list()
    stack_depth_dict = precalc_node_stack_depth(T)
    high_priority_queue.append({
        'stack': S.copy(),
        'trace': T.copy(),
        'stack_history': stack_depth_dict
    })

    while len(high_priority_queue) + len(low_priority_queue) > 0:
        path = None
        if len(high_priority_queue) > 0:
            path = high_priority_queue.pop(0)
        else:
            path = low_priority_queue.pop(0)

        cur_stack = path['stack']
        cur_trace = path['trace']
        cur_node = cur_stack[-1]
        cur_stack_history = path['stack_history']

        # check if the destination has been reached
        if str(cur_node.label) == goal_label:
            return path

        # check for bad test case
        if len(cur_trace) > 2 * len(graph.edges):
            continue

        # check if there is a reduce rule that may exist for this state
        reduce_edges = []
        if cur_node.reduce_rule is not None:
            for rule in cur_node.reduce_rule:
                reduce_edges.append(
                    get_reduce_edge(rule[0], rule[1], cur_node, cur_stack))

        # check if the previous move was pop so we should shift a non-terminal
        if len(cur_trace) > 0 and cur_trace[-1].is_pop:
            shift_edge: Edge
            for edge in cur_node.edges:
                if edge.label == cur_trace[-1].label and not edge.is_pop:
                    shift_edge = edge
                    break
            # always push even if this is a loop
            push(cur_stack, cur_trace, high_priority_queue, shift_edge,
                 cur_stack_history=cur_stack_history)
        else:
            # if the previous step wasn't a pop then we should shift on terminals and check
            # for valid reductions on all edges
            stuck_flag = True
            for edge in cur_node.edges:
                if edge.label in graph.terminal:
                    # if this is a loop we only take it if the stack does not increase in size
                    if edge.next_node.label not in cur_stack_history or (
                            edge.next_node.label in cur_stack_history and
                            cur_stack_history[
                                edge.next_node.label] >= len(
                        cur_stack) + 1):
                        push(cur_stack, cur_trace, high_priority_queue, edge,
                             cur_stack_history=cur_stack_history)
                    else:
                        push(cur_stack, cur_trace, low_priority_queue, edge,
                             cur_stack_history=cur_stack_history)
                # check that reduction edge is correct edge
                elif edge.label in graph.nonterminal and edge in reduce_edges:
                    # pop nodes of stack
                    for rule_index in range(len(reduce_edges)):
                        if edge == reduce_edges[rule_index]:
                            # if this is a loop we only take it if the stack does not increase in size
                            if edge.next_node.label not in cur_stack_history or (
                                    edge.next_node.label in cur_stack_history and
                                    cur_stack_history[
                                        edge.next_node.label] >= len(
                                cur_stack) - edge.pop_count):
                                # pop nodes of stack
                                pop(cur_stack, cur_trace, high_priority_queue, edge,
                                    cur_node.reduce_rule[rule_index][1],
                                    cur_stack_history=cur_stack_history)
                            else:
                                pop(cur_stack, cur_trace, low_priority_queue, edge,
                                    cur_node.reduce_rule[rule_index][1],
                                    cur_stack_history=cur_stack_history)


def precalc_node_stack_depth(trace):
    """Calculate the stack depth the last time this node was visited"""
    depth_map = dict()
    depth_map[0] = 1
    cur_depth = 1
    for edge in trace:
        if edge.is_pop:
            cur_depth -= edge.pop_count
            depth_map[edge.next_node.label] = cur_depth
        else:
            cur_depth += 1
            depth_map[edge.next_node.label] = cur_depth
    return depth_map


def unblock(S, E, T, graph, seen_edges, fresh_queue, stale_queue):
    """Solve for stuck pop edges and splice them in"""
    candidate_edges = []
    visited_states = set()
    for e in seen_edges:
        if not e.is_pop:
            visited_states.add(e.next_node)
    for e in E - seen_edges:
        if e.is_pop and e.next_node in visited_states:
            candidate_edges.append(e)

    for e in candidate_edges:
        solution = lookback_for_pop(e, graph, E - seen_edges)
        splice(solution, fresh_queue, stale_queue, graph)


def lookback_for_pop(candidate, graph, unseen_edges):
    target_stack_depth = candidate.pop_count
    src = candidate.next_node
    target = candidate.source
    possible_solutions = []
    max_len = len(graph.edges)
    queue = list()
    queue.append({
        'stack': [src],
        'trace': []
    })
    while len(queue) > 0:
        path = queue.pop(0)
        cur_stack = path['stack']
        cur_trace = path['trace']
        cur_node = cur_stack[-1]

        # check for bad test case
        if len(cur_trace) > max_len:
            continue

        if cur_node == target and len(cur_stack) - 1 == target_stack_depth:
            possible_solutions.append(path.copy())
            max_len = len(cur_trace)
            continue
        # check if there is a reduce rule that may exist for this state
        reduce_edges = []
        if cur_node.reduce_rule is not None:
            for rule in cur_node.reduce_rule:
                pop_amount = rule[1]
                # don't take excessively large pops
                if len(cur_stack) >= pop_amount + 1:
                    reduce_edges.append(
                        get_reduce_edge(rule[0], rule[1], cur_node, cur_stack))

        # check if the previous move was reduce so we should shift a non-terminal
        if len(cur_trace) > 0 and cur_trace[-1].is_pop:
            shift_edge: Edge
            for edge in cur_node.edges:
                if edge.label == cur_trace[-1].label and not edge.is_pop:
                    shift_edge = edge
                    break
            push(cur_stack, cur_trace, queue, shift_edge)
        else:
            # if the previous step wasn't a reduce then we should shift on terminals and check
            # for valid reductions on all edges
            for edge in cur_node.edges:
                if edge.label in graph.terminal:
                    push(cur_stack, cur_trace, queue, edge)
                # check that reduction edge is correct edge
                elif edge.label in graph.nonterminal and edge in reduce_edges:
                    for rule_index in range(len(reduce_edges)):
                        if edge == reduce_edges[rule_index]:
                            # pop nodes of stack
                            pop(cur_stack, cur_trace, queue, edge, pop_amount)
    # find the possible solution that covers as many new edges as possible
    best_path = possible_solutions[0]
    new_count = 0
    for e in best_path:
        if e in unseen_edges:
            new_count += 1
    for path in possible_solutions[1:]:
        count = 0
        for e in path:
            if e in unseen_edges:
                count += 1
        if count > new_count:
            new_count = count
            best_path = path
    return best_path


def splice(partial, fresh_queue, stale_queue, graph):
    src_node = partial['trace'][0].source
    done = False
    for path in fresh_queue + stale_queue:
        for i in range(len(path['trace'])):
            e = path['trace'][i]
            # find possible node to splice into
            if e.next_node == src_node and not e.is_pop:
                new_trace = path['trace'][:i + 1] + partial['trace']
                # recompute new stace
                new_stack = [new_trace[0].source]
                for e in new_trace:
                    if not e.is_pop:
                        new_stack.append(e.next_node)
                    else:
                        for i in range(e.pop_count):
                            new_stack.pop(len(new_stack) - 1)
                fresh_queue.append({'stack': new_stack, 'trace': new_trace})
                # remove path if solution just appended to path in stale queue
                if i == len(path['trace']) - 1 and path in stale_queue:
                    stale_queue.remove(path)
                done = True
                break
        if done:
            break
    assert done
