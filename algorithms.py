from graph_components import Graph, Edge
from pos_utils import get_reduce_edge, push, pop
from general_utils import extract_test_case
from config import Config
from debug_utils import trace_to_str


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
    print("Started Solving for Pop Edges")
    while len(rem_pop) + len(waiting) > 0:
        rem_pop.update(waiting)
        waiting = set()
        for edge in rem_pop.copy():
            solved, solution = solve_for_pop(edge, graph, sub_table)
            if solved:
                # find non term push edge in sub table add to table
                for e in edge.next_node.edges:
                    if not e.is_pop and e.label in graph.nonterminal:
                        if e not in sub_table:
                            sub_table[e] = list()
                        for sol in solution:
                            if sol['trace'][-1].label == e.label:
                                sol['stack'] = [e.next_node]
                                sol['trace'].append(e)
                                sub_table[e].append(sol)
            else:
                waiting.add(edge)
            rem_pop.remove(edge)
    print("Finished Solving for Pop Edges. Started Splicing.")
    # splice solutions together
    complete = splice_segments(sub_table, graph)
    print("Finished Splicing Solutions.")
    tests = set()
    for path in complete:
        tests.add(extract_test_case(path['trace'], graph)[0])
    return tests


def solve_for_pop(candidate, graph, sub_table):
    # make a path out of only push edges which can then be subbed out in later pass
    target_stack_depth = candidate.pop_count
    src = candidate.next_node
    target = candidate.source
    possible_solutions = []
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
        if len(cur_trace) > target_stack_depth:
            continue

        if cur_node == target and len(cur_stack) - 1 == target_stack_depth:
            cp = path.copy()
            cp['stack'] = []
            possible_solutions.append(cp)
            cp['trace'].append(candidate)
            continue
        else:
            # if the previous step wasn't a reduce then we should shift on terminals and check
            # for valid reductions on all edges
            for edge in cur_node.edges:
                if not edge.is_pop:
                    push(cur_stack, cur_trace, queue, edge)
    if len(possible_solutions) == 0:
        return False, None
    return True, possible_solutions


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
        cur_path = queue.pop(0)
        cur_trace = cur_path['trace']
        if trace_to_str(cur_trace, graph) in seen:
            continue
        seen.add(trace_to_str(cur_trace, graph))
        complete = True
        for i in range(len(cur_trace)):
            edge = cur_trace[i]
            # check for possible non term push edge to sub
            if not edge.is_pop and edge.label in graph.nonterminal and not cur_trace[i - 1].is_pop:
                # splice
                if edge not in subbed:
                    subbed.add(edge)
                    for p in sub_map[edge]:
                        new_trace = cur_trace[:i] + p['trace'] + cur_trace[i + 1:]
                        queue.append({'trace': new_trace})
                else:
                    new_trace = cur_trace[:i] + shortest_map[edge]['trace'] + cur_trace[i + 1:]
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
            if edge.next_node.label == 'acc':
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
        if not config.get_clasic_flag():
            complete = path_completion_improved(path['stack'], path['trace'], 'acc', graph)
        else:
            complete = path_completion(path['stack'], path['trace'], 'acc', graph)
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
                reduce_edges.append(get_reduce_edge(rule[0], rule[1], cur_node, cur_stack))

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
                if edge.label in graph.terminal and (edge.next_node != cur_node or edge not in seen_edges):
                    seen_edges.add(edge)
                    push(cur_stack, cur_trace, queue, edge)
                # check that reduction edge is correct edge
                elif edge.label in graph.nonterminal and edge in reduce_edges:
                    for rule_index in range(len(reduce_edges)):
                        if edge == reduce_edges[rule_index]:
                            # pop nodes of stack
                            pop(cur_stack, cur_trace, queue, edge, cur_node.reduce_rule[rule_index][1])
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
                reduce_edges.append(get_reduce_edge(rule[0], rule[1], cur_node, cur_stack))

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
                                pop(cur_stack, cur_trace, fresh_queue, edge, cur_node.reduce_rule[rule_index][1])
                            else:
                                pop(cur_stack, cur_trace, brute_force_queue, edge, cur_node.reduce_rule[rule_index][1])
                            seen_edges.add(edge)
        if not new_edge_seen and not path_from_brute:
            stale_queue.append(path)


def path_completion(S, T, goal_label, graph):
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

        # check for bad test case
        if len(cur_trace) > 2 * len(graph.edges):
            continue

        # check if there is a reduce rule that may exist for this state
        reduce_edges = []
        if cur_node.reduce_rule is not None:
            for rule in cur_node.reduce_rule:
                reduce_edges.append(get_reduce_edge(rule[0], rule[1], cur_node, cur_stack))

        # check if the previous move was pop so we should shift a non-terminal
        if len(cur_trace) > 0 and cur_trace[-1].is_pop:
            shift_edge: Edge
            for edge in cur_node.edges:
                if edge.label == cur_trace[-1].label and not edge.is_pop:
                    shift_edge = edge
                    break
            push(cur_stack, cur_trace, queue, shift_edge)
        else:
            # if the previous step wasn't a pop then we should shift on terminals and check
            # for valid reductions on all edges
            for edge in cur_node.edges:
                if edge.label in graph.terminal and edge.next_node != cur_node:
                    push(cur_stack, cur_trace, queue, edge)
                # check that reduction edge is correct edge
                elif edge.label in graph.nonterminal and edge in reduce_edges:
                    # pop nodes of stack
                    for rule_index in range(len(reduce_edges)):
                        if edge == reduce_edges[rule_index]:
                            # pop nodes of stack
                            pop(cur_stack, cur_trace, queue, edge, cur_node.reduce_rule[rule_index][1])


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
                reduce_edges.append(get_reduce_edge(rule[0], rule[1], cur_node, cur_stack))

        # check if the previous move was pop so we should shift a non-terminal
        if len(cur_trace) > 0 and cur_trace[-1].is_pop:
            shift_edge: Edge
            for edge in cur_node.edges:
                if edge.label == cur_trace[-1].label and not edge.is_pop:
                    shift_edge = edge
                    break
            # always push even if this is a loop
            push(cur_stack, cur_trace, high_priority_queue, shift_edge, cur_stack_history=cur_stack_history)
        else:
            # if the previous step wasn't a pop then we should shift on terminals and check
            # for valid reductions on all edges
            stuck_flag = True
            for edge in cur_node.edges:
                if edge.label in graph.terminal:
                    # if this is a loop we only take it if the stack does not increase in size
                    if edge.next_node.label not in cur_stack_history or (
                            edge.next_node.label in cur_stack_history and cur_stack_history[
                        edge.next_node.label] >= len(
                        cur_stack) + 1):
                        push(cur_stack, cur_trace, high_priority_queue, edge, cur_stack_history=cur_stack_history)
                    else:
                        push(cur_stack, cur_trace, low_priority_queue, edge, cur_stack_history=cur_stack_history)
                # check that reduction edge is correct edge
                elif edge.label in graph.nonterminal and edge in reduce_edges:
                    # pop nodes of stack
                    for rule_index in range(len(reduce_edges)):
                        if edge == reduce_edges[rule_index]:
                            # if this is a loop we only take it if the stack does not increase in size
                            if edge.next_node.label not in cur_stack_history or (
                                    edge.next_node.label in cur_stack_history and cur_stack_history[
                                edge.next_node.label] >= len(cur_stack) - edge.pop_count):
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
                    reduce_edges.append(get_reduce_edge(rule[0], rule[1], cur_node, cur_stack))

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
