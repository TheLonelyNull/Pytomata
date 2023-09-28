from pathlib import Path
from typing import TextIO

from config import Config
from graph_components import Node, Graph, Edge


def get_bison_file(file: Path | str) -> TextIO:
    return open(file, 'r')


def get_graph_nodes(io: TextIO) -> list[Node]:
    accept_state = None
    rules: dict[int, tuple[str, list]] = {}
    node_reduce_lines_map: dict[int, list[str]] = {}
    node_map: dict[int, Node] = {}
    # Skip over grammar headers to the states
    current_non_terminal = None
    while "Grammar" not in (line := io.readline()):
        continue
    while "State" not in (line := io.readline()):
        if (line := line.strip()) and line[0].isnumeric():
            rule_num, rule = line.split(maxsplit=1)
            rule_num = int(rule_num)
            rule: str
            rule.strip()
            if not rule.startswith('|'):
                current_non_terminal, terminals = rule.split(":", maxsplit=1)
            else:
                terminals = rule[1:]
            terminals = terminals.strip()
            terminals = terminals.replace("ε", "")
            terminals = terminals.split()
            stripped_terminals = []
            for terminal in terminals:
                terminal = terminal.strip("'")
                terminal = terminal.strip('"')
                stripped_terminals.append(terminal)
            rules[rule_num] = (current_non_terminal, stripped_terminals)

    current_state = int(line.strip("State "))
    while line := io.readline():
        if line.startswith("State "):
            current_state = int(line.strip("State "))
            continue

        if "go to state" in line:
            line = line.replace("shift, and go to state ", "")
            line = line.replace(" go to state ", "")
            split_line = line.split()
            symbol, target_state = split_line[0], int(split_line[-1])
            symbol = symbol.strip("'")
            symbol = symbol.strip('"')
            # This seems impossible but found in Bison, remove?
            if current_state == target_state:
                continue
            current_node = node_map.get(current_state, Node(current_state, [], False, []))
            target_node = node_map.get(target_state, Node(target_state, [], False, []))
            edge = Edge(symbol, target_node, False)
            edge.source = current_node
            current_node.edges.append(edge)
            target_node.pre_edges.append(edge)
            node_map[current_state] = current_node
            node_map[target_state] = target_node
        if line.strip().endswith("accept"):
            accept_state = current_state

        # Compute pop edges afterward
        if "reduce using rule" in line and "[reduce" not in line:
            lines = node_reduce_lines_map.get(current_state, [])
            lines.append(line.strip())
            node_reduce_lines_map[current_state] = lines

    # Fill in Pop edges
    for state_num, lines in node_reduce_lines_map.items():
        for line in lines:
            split = line.split("reduce using rule")
            rule_num = int(split[1].split()[0])
            non_terminal, stack = rules[rule_num]
            current_node = node_map[state_num]
            if stack:
                # Traverse stack backwards to find source
                trace: dict[Node, list[Node]] = {current_node: [current_node]}
                nodes_in_layer = [current_node]
                for symbol in stack[::-1]:
                    next_layer = []
                    for node in nodes_in_layer:
                        for edge in node.pre_edges:
                            if edge.label == symbol:
                                trace[edge.source] = [edge.source] + trace[node]
                                next_layer.append(edge.source)
                    nodes_in_layer = next_layer
                for target_node in nodes_in_layer:
                    edge = Edge(non_terminal, target_node, True)
                    edge.source = current_node
                    edge.local_stack = trace[target_node]
                    edge.pop_count = len(stack)
                    current_node.edges.append(edge)
                    target_node.pre_edges.append(edge)
                    current_node.reduce_rule.append((non_terminal, len(stack)))

            else:
                # It is a self reduction
                edge = Edge(non_terminal, current_node, True)
                edge.source = current_node
                edge.local_stack = [current_node]
                current_node.edges.append(edge)
                current_node.pre_edges.append(edge)
                current_node.reduce_rule.append((non_terminal, len(stack)))
    node_map[accept_state].is_accept = True
    return sorted(list(node_map.values()), key=lambda x: x.label)


def construct_graph(file: TextIO) -> Graph:
    config = Config.get_instance()
    should_produce_graph = config.should_produce_graph()

    nodes = get_graph_nodes(file)
    graph = Graph(nodes[0], nodes)
    return graph


if __name__ == "__main__":
    file = get_bison_file("bison_grammars/ampl.output")
    graph = construct_graph(file)
    print()
