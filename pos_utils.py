from graph_components import Node


def get_reduce_edge(rule_label: str, reduce_amount: int, node: Node, S):
    reduce_edge = None
    for edge in node.edges:
        if edge.label == rule_label and edge.next_node == S[-reduce_amount - 1] and edge.is_pop:
            reduce_edge = edge
            break
    return reduce_edge


def push(stack, trace, queue, edge, cur_stack_history=None):
    new_path = {
        'stack': stack.copy() + [edge.next_node],
        'trace': trace.copy() + [edge]
    }
    if cur_stack_history is not None:
        # update the stack history
        cur_stack_history[edge.next_node.label] = len(new_path['stack'])
        new_path['stack_history'] = cur_stack_history
    queue.append(new_path)


def pop(stack, trace, queue, edge, pop_amount, cur_stack_history=None):
    new_stack = stack.copy()
    for i in range(pop_amount):
        new_stack.pop(len(new_stack) - 1)
    new_path = {
        'stack': new_stack,
        'trace': trace.copy() + [edge]
    }
    if cur_stack_history is not None:
        # update the stack history
        cur_stack_history[edge.next_node.label] = len(new_stack)
        new_path['stack_history'] = cur_stack_history

    queue.append(new_path)


def extract_pos(T, graph):
    out = ''
    for edge in T:
        if edge.label in graph.terminal and edge.label != "$end":
            out += edge.label + ' '
    return [out]
