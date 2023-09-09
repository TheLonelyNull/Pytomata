class Node:
    def __init__(self, label: int, edges: list, is_accept: bool, reduce_rule: list):
        self.label = label
        self.edges = edges
        self.pre_edges = list()
        self.is_accept = is_accept
        self.reduce_rule = reduce_rule
        self.predecessors = list() # Only used in old hyacc construction

    def __str__(self):
        return '(' + str(self.label) + ',' + str(self.edges) + ',' + str(self.is_accept) + ',' + str(
            self.reduce_rule) + ')'


class Edge:
    def __init__(self, label, next_node, is_pop):
        self.label = label
        self.source = None
        self.next_node = next_node
        self.is_pop = is_pop
        self.delete = False
        self.add = None
        self.swap = None
        self.pop_count = 0
        self.local_stack = None

    def __eq__(self, other):
        if other is None:
            return False
        if self.label != other.label:
            return False
        if self.source.label != other.source.label:
            return False
        if self.next_node.label != other.next_node.label:
            return False
        if self.is_pop != other.is_pop:
            return False
        if self.pop_count != other.pop_count:
            return False
        return True

    def __ne__(self, other):
        if other is None:
            return True
        if self.label != other.label:
            return True
        if self.source.label != other.source.label:
            return True
        if self.next_node.label != other.next_node.label:
            return True
        if self.is_pop != other.is_pop:
            return True
        if self.pop_count != other.pop_count:
            return True
        return False

    def __hash__(self):
        return hash(self.label) + hash(self.source.label) + hash(self.next_node.label) + hash(self.is_pop) + hash(
            self.pop_count)

    def __str__(self):
        pop_str = ""
        if self.is_pop:
            pop_str = "/" + str(self.pop_count)
        return '{ ' + str(self.source.label) + " " + str(self.label) + pop_str + ' -> ' + str(
            self.next_node.label) + '}'


class Graph:
    def __init__(self, root: Node, nodes: list):
        self.root = root
        self.nodes = nodes
        self.edges = set()
        self.set_edges()
        self.terminal = set()
        self.nonterminal = set()
        self.set_terminal_and_nonterminal()
        self.empty_table_entries = dict()

    def set_terminal_and_nonterminal(self):
        for node in self.nodes:
            for edge in node.edges:
                self.terminal.add(edge.label)
            if node.reduce_rule is not None:
                for rule in node.reduce_rule:
                    symbol = rule[0]
                    self.nonterminal.add(symbol)
        self.terminal = self.terminal - self.nonterminal

    def set_edges(self):
        for node in self.nodes:
            for edge in node.edges:
                self.edges.add(edge)

    def get_terminal(self):
        return self.terminal.copy()

    def get_nonterminal(self):
        return self.nonterminal.copy()

    def get_edges(self):
        return self.edges.copy()

    def get_root(self):
        return self.root
