from graph_components import Graph, Edge, Node
from config import Config
from file_utils import output_test_cases
from algorithms import full_traversal, dynamic_traversal


def gen_test(graph):
    config = Config.get_instance()
    test_cases = set()
    if config.get_clasic_flag() or config.get_classic_improved_flag():
        test_cases = full_traversal(graph)
    else:
        test_cases = dynamic_traversal(graph)

    output_filename = config.get_output_filename()
    output_test_cases(test_cases, output_filename)
