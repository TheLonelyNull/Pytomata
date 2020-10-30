from graph_components import Graph, Edge
from pos_utils import get_reduce_edge, push, pop
from general_utils import extract_test_case
from config import Config
from debug_utils import trace_to_str
import sys


def full_traversal(graph: Graph):
    E = graph.edges.copy()
    test_cases = set()
    config = Config.get_instance()
    # bfs till graph covered
    print("Starting graph flooding")
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
        if len(cur_trace) > 0 and cur_trace[-1].is_return:
            shift_edge: Edge
            for edge in cur_node.edges:
                if edge.label == cur_trace[-1].label and not edge.is_return:
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
            path = brute_force_queue.pop(0)
            path_from_brute = True
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
        if len(cur_trace) > 0 and cur_trace[-1].is_return:
            shift_edge: Edge
            for edge in cur_node.edges:
                if edge.label == cur_trace[-1].label and not edge.is_return:
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
                if edge.label in graph.terminal and (edge.next_node != cur_node or edge not in seen_edges):
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
        if len(cur_trace) > 0 and cur_trace[-1].is_return:
            shift_edge: Edge
            for edge in cur_node.edges:
                if edge.label == cur_trace[-1].label and not edge.is_return:
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
        if len(cur_trace) > 0 and cur_trace[-1].is_return:
            shift_edge: Edge
            for edge in cur_node.edges:
                if edge.label == cur_trace[-1].label and not edge.is_return:
                    shift_edge = edge
                    break
            # always push even if this is a loop
            push(cur_stack, cur_trace, high_priority_queue, shift_edge, cur_stack_history=cur_stack_history)
        else:
            # if the previous step wasn't a pop then we should shift on terminals and check
            # for valid reductions on all edges
            stuck_flag = True
            for edge in cur_node.edges:
                if edge.label in graph.terminal and edge.next_node != cur_node:
                    # if this is a loop we only take it if the stack does not increase in size
                    if edge.next_node.label in cur_stack_history and cur_stack_history[edge.next_node.label] >= len(
                            cur_stack) + 1:
                        push(cur_stack, cur_trace, high_priority_queue, edge, cur_stack_history=cur_stack_history)
                    else:
                        push(cur_stack, cur_trace, low_priority_queue, edge, cur_stack_history=cur_stack_history)
                # check that reduction edge is correct edge
                elif edge.label in graph.nonterminal and edge in reduce_edges:
                    # pop nodes of stack
                    for rule_index in range(len(reduce_edges)):
                        if edge == reduce_edges[rule_index]:
                            # if this is a loop we only take it if the stack does not increase in size
                            if edge.next_node.label in cur_stack_history and cur_stack_history[
                                edge.next_node.label] >= len(cur_stack) - edge.red_pop_count:
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
        if edge.is_return:
            cur_depth -= edge.red_pop_count
            depth_map[edge.next_node.label] = cur_depth
        else:
            cur_depth += 1
            depth_map[edge.next_node.label] = cur_depth
    return depth_map
