from graph_components import Graph, Edge, Node
from config import Config
from file_utils import output_test_cases
from algorithms import full_traversal


def gen_test(graph):
    config = Config.get_instance()
    test_cases = full_traversal(graph)

    output_filename = config.get_output_filename()
    output_test_cases(test_cases, output_filename)
