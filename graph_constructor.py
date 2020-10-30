import re
from graph_components import Edge, Node, Graph
import graphics_generator
from config import Config

def get_graph_lines():
    graph_file = open("y.gviz", 'r')
    graph_lines = graph_file.readlines()
    return graph_lines[4: -2]


def get_states():
    state_file = open("y.output", 'r')
    states_lines = state_file.readlines()
    state_start_indexes = []
    for i in range(len(states_lines)):
        if 'state ' in states_lines[i] and 'conflict' not in states_lines[i]:
            state_start_indexes.append(i)
    end_index = len(states_lines) - 5
    state_start_indexes.append(end_index)
    # construct list of lines relevant to states
    states = []
    for i in range(len(state_start_indexes) - 1):
        states.append([])
        cur_state = states[-1]
        for j in range(state_start_indexes[i] + 3, state_start_indexes[i + 1]):
            if bool(re.match("\s*\(\d+\).*", states_lines[j])):
                cur_state.append(states_lines[j])

    return states


def get_reduce_rule(states, node, type):
    rules = []
    # get all reduction rules that could apply for a state
    for rule in states[node]:
        r = rule.split('->')
        nonterminal = r[0].split()[-1]
        symbols = r[-1].split('(core)')[0].split()
        if type == 'LR0':
            states_to_pop = len(r[-1].split('(core)')[0].split()) - 1
        elif type == 'LR1' or type == 'LALR1':
            matches = re.split(r"{(.*\ )*(.*)}", r[-1])
            symbols = matches[0].split()
            states_to_pop = len(symbols) - 1
        else:
            states_to_pop = len(r[-1].split('{')[0].split()) - 1
        if len(symbols) > 0 and symbols[-1] == '.':
            # check that this rule is actually reduce rule
            rules.append((nonterminal, states_to_pop))
    return rules


def construct_graph(graphics_type=None, automaton_type = None, should_produce_graph = None):

    if automaton_type is None:
        config = Config.get_instance()
        automaton_type = config.get_automaton_type()

    if should_produce_graph is None:
        config = Config.get_instance()
        should_produce_graph = config.should_produce_graph()
    graph_lines = get_graph_lines()  # get all the lines relating to edges in the graph
    states = get_states()  # get all the lines relating to different states in the graph
    # init nodes
    nodes = []
    # construct base graph
    construct_base_graph(states, nodes, graph_lines, automaton_type)
    remove_duplicate_rules(nodes)
    # add return edges
    add_return_edges(nodes)
    # generate_graphic
    if should_produce_graph:
        graphics_generator.gen_graphic(nodes)
    graph = Graph(nodes[0], nodes)
    calculate_error_states(graph)
    return graph


def construct_base_graph(states, nodes, graph_lines, type):
    for i in range(len(states)):
        nodes.append(Node(i, [], False, None))
    # add another node for accept state
    nodes.append(Node("acc", [], True, None))
    # put in edges and details
    for line in graph_lines:
        line_list = line.split()
        cur = nodes[int(line_list[0])]
        cur__return_label_set = set()
        next_node = nodes[-1]
        if line_list[2] != "acc" and 'r' not in line_list[2]:
            next_node = nodes[int(line_list[2])]
        label = ""
        if line_list[5] == "style=\"dashed\"":
            label = None
            cur.reduce_rule = get_reduce_rule(states, cur.label, type)
        elif line_list[4] == "label":
            label = "$end"
        else:
            label = line_list[4].split("\"")[1]

        if label is not None:
            edge = Edge(label, next_node, False)
            edge.source = cur
            cur.edges.append(edge)
            next_node.predecessors.append(cur)
            if label == "$end":
                next_node.is_accept = True


def remove_duplicate_rules(nodes):
    for node in nodes:
        if node.reduce_rule is not None:
            rules_set = set(node.reduce_rule)
            node.reduce_rule = list(rules_set)


def add_return_edges(nodes):
    # find all nodes that need reduce edges starting from them
    leaves = []
    for node in nodes:
        if node.reduce_rule is not None:
            leaves.append(node)
    for node in leaves:
        # add all reduction edges in case of reduce/reduce conflict
        for reduce_rule in node.reduce_rule:
            nr_of_states_to_pop = reduce_rule[1]
            # go back for the number of states to pop
            count = 0
            cur_level = list()
            cur_level.append(node)
            prev_level = list()
            while count < nr_of_states_to_pop:
                # find edges linking to current level nodes
                for n in cur_level:
                    prev_level.extend(find_predecessors(n, nodes))
                count += 1
                cur_level = prev_level.copy()
                prev_level.clear()
            # add edges to graph
            for n in cur_level:
                edge = Edge(reduce_rule[0], n, True)
                edge.red_pop_count = nr_of_states_to_pop
                edge.source = node
                # avoid duplicate reduction edges. Happens when more than one reduce rule ends at same point
                # during reduce reduce conflict
                already_added = False
                for e in node.edges:
                    if e.label == edge.label and e.next_node == edge.next_node and e.is_return:
                        already_added = True
                        break
                if not already_added:
                    node.edges.append(edge)


def find_predecessors(cur, nodes_list):
    return cur.predecessors.copy()


def calculate_error_states(graph: Graph):
    state_file = open("y.output", 'r')
    states_lines = state_file.readlines()
    error_indexes = []
    empty_table_entries = dict()

    for i in range(len(states_lines)):
        if 'error' in states_lines[i]:
            error_indexes.append(i)

    for index in error_indexes:
        index -= 1
        # get error transitions
        valid_shifts = set()
        while len(states_lines[index].strip()) != 0:
            states_lines[index] = states_lines[index].strip()
            token = states_lines[index].split(" ")[0]
            valid_shifts.add(token)
            index -= 1
        error_transitions = graph.terminal - valid_shifts
        if '$end' in error_transitions:
            error_transitions.remove('$end')

        while 'state' not in states_lines[index]:
            index -= 1
        state = states_lines[index].split(" ")[-1]
        state = state.rstrip()
        if state.isnumeric():
            state = int(state)
        empty_table_entries[state] = error_transitions

    for node in graph.nodes:
        if node.label not in empty_table_entries:
            empty_table_entries[node.label] = set()
    graph.empty_table_entries = empty_table_entries
