import os
from config import Config
import file_utils
from graph_constructor import construct_graph
import test_generator

if __name__ == '__main__':
    file_utils.clean_directory()

    config = Config.get_instance()

    command_automaton_map = {
        "LALR1": "-R",
        "LR0": "-S",
        "LR1": ""
    }

    # generate graph file and automaton text file
    print(command_automaton_map[
              config.get_automaton_type()])
    command = "./hyacc/hyacc -v -g -O0 " + command_automaton_map[
        config.get_automaton_type()] + " " + config.get_grammar_filename()
    print(command)
    os.system(command)

    graph = construct_graph()
    #file_utils.remove_intermediary_files()
    test_generator.gen_test(graph)
