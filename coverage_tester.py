import os
import file_utils
from graph_constructor import construct_graph
from graph_components import Edge, Node, Graph
from tqdm import tqdm
import argparse

def parse_args():
    # initialise the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-l')
    parser.add_argument('-f')
    parser.add_argument('-g')
    parser.add_argument('-i')
    args = parser.parse_args()

    # checks that the automaton automaton_type is a valid option
    automaton_type = args.l
    if automaton_type is None:
        automaton_type = 'LALR1'

    #  checks the input file
    filename = args.f

    # check the graph output types
    graph_type = args.g

    # get output filename
    tests_filename = args.i
    return [automaton_type, filename, graph_type, tests_filename]


def get_test_cases(filename):
    file = open(filename, 'r')
    test_cases = []
    for line in file.readlines():
        if len(line) == 0:
            test_cases.append(line)
        if len(line) > 0 and line[0] != '#':
            test_cases.append(line)
    return test_cases


def tokenize(test_cases):
    tokenized_test_cases = []
    for case in test_cases:
        # split on space and ignore newline at end
        case = case.rstrip()
        tokens = case.split(" ")
        new_tokens = []
        for token in tokens:
            if len(token)>0:
                new_tokens.append(token)
        tokenized_test_cases.append(new_tokens)
    return tokenized_test_cases


def parse(graph, tokens):
    E = []
    queue = list()
    queue.append({
        'stack': [graph.nodes[0]],
        'trace': [],
        'tokens': tokens
    })
    while len(queue) > 0:
        path = queue.pop(0)
        cur_stack = path['stack']
        cur_trace = path['trace']
        cur_node = cur_stack[-1]
        token_stream = path['tokens']

        if cur_node.label == 'acc' and len(token_stream) == 0:
            return True, path
        # check if there is a reduce rule that may exist for this state
        reduce_edges = []
        if cur_node.reduce_rule is not None:
            for rule in cur_node.reduce_rule:
                reduce_edges.append(get_reduce_edge(rule[0], rule[1], cur_node, cur_stack))

        # Shift
        if len(token_stream) > 0:
            next_token = token_stream[0]
            for edge in cur_node.edges:
                if edge.label in graph.terminal and not edge.is_return and edge.label == next_token:
                    cur_token_stream = token_stream.copy()
                    cur_token_stream.pop(0)
                    new_path = {
                        'stack': cur_stack.copy() + [edge.next_node],
                        'trace': cur_trace.copy() + [edge],
                        'tokens': cur_token_stream
                    }
                    queue.append(new_path)
        for edge in cur_node.edges:
            if edge.label == '$end':
                new_path = {
                    'stack': cur_stack.copy() + [edge.next_node],
                    'trace': cur_trace.copy() + [edge],
                    'tokens': token_stream.copy()
                }
                queue.append(new_path)
        # Reduce
        for rule_index in range(len(reduce_edges)):
            edge = reduce_edges[rule_index]
            new_stack = cur_stack.copy()
            for i in range(cur_node.reduce_rule[rule_index][1]):
                new_stack.pop(len(new_stack) - 1)
            new_trace = cur_trace.copy() + [edge]
            shift_edge: Edge
            for e in edge.next_node.edges:
                if e.label == new_trace[-1].label and not e.is_return:
                    shift_edge = e
                    break
            new_path = {
                'stack': new_stack.copy() + [shift_edge.next_node],
                'trace': new_trace.copy() + [shift_edge],
                'tokens': token_stream.copy()
            }
            queue.append(new_path)

    return False, None


def get_reduce_edge(rule_label: str, reduce_amount: int, node: Node, S):
    reduce_edge = None
    for edge in node.edges:
        if edge.label == rule_label and edge.next_node == S[-reduce_amount - 1] and edge.is_return:
            reduce_edge = edge
            break
    return reduce_edge


if __name__ == '__main__':
    file_utils.clean_directory()

    args = parse_args()
    command_automaton_map = {
        "LALR1": "-R",
        "LR0": "-S",
        "LR1": ""
    }

    # generate graph file and automaton text file
    command = "./hyacc/hyacc -v -g -O0 " + command_automaton_map[args[0]] + " " + args[1]
    os.system(command)

    graph = construct_graph(automaton_type=args[0], graphics_type="", should_produce_graph=False)
    file_utils.remove_intermediary_files()

    filename = args[3]
    cases = get_test_cases(filename)
    tokenized = tokenize(cases)
    seen_edges = set()
    for i in tqdm(range(len(tokenized))):
        token_stream = tokenized[i]
        result = parse(graph, token_stream)
        if result[0]:
            for edge in result[1]['trace']:
                seen_edges.add(edge)
        else:
            print(token_stream)
    print("Edges Covered:")
    print(len(seen_edges))
    print("Edges in Graph")
    print(len(graph.edges))
    print("Coverage: "+str(len(seen_edges)*100/len(graph.edges))+"%")
    for e in graph.edges-seen_edges:
        pass
        #print(e)