import os

import test_generator
from bison_graph_constructor import construct_graph as construct_graph_bison, get_bison_file
from config import Config
from graph_constructor import construct_graph

if __name__ == '__main__':
    # file_utils.clean_directory()
    #
    config = Config.get_instance()

    command_automaton_map = {
        "LALR1": "-R",
        "LR0": "-S",
        "LR1": ""
    }

    # generate graph file and automaton text file
    # graph = None
    # if config.get_automaton_type() == "LR0":
    command = "./hyacc/hyacc -v -g -O0 " + command_automaton_map[
        config.get_automaton_type()] + " " + config.get_input_file_name()
    print(command)
    os.system(command)
    graph = construct_graph()
    # else:
    #     file = get_bison_file(config.get_input_file_name())
    #     graph = construct_graph_bison(file)

    print(f"T = {len(graph.terminal)}")
    print(f"N = {len(graph.nonterminal)}")
    print(f"Nodes: {len(graph.nodes)}")
    print(f"Pop Edges: {len([edge for edge in graph.edges if edge.is_pop])}")
    print(f"Push Edges: {len([edge for edge in graph.edges if not edge.is_pop])}")

    test_generator.gen_test(graph)
