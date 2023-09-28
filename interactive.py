import os
from config import Config
import file_utils
from graph_constructor import construct_graph
from debug_utils import trace_to_str
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
        config.get_automaton_type()] + " " + config.get_input_file_name()
    os.system(command)

    graph = construct_graph()
    file_utils.remove_intermediary_files()

    while True:
        statestr = input("Enter state:")
        state = None
        try:
            state = int(statestr)
            if state < 0 or state > len(graph.nodes):
                continue
        except:
            if state.label != 'acc':
                continue
            else:
                state = -1

        print("arriving")
        for edge in graph.nodes[state].pre_edges:
            print(trace_to_str([edge], graph))
        print("leaving")
        for edge in graph.nodes[state].edges:
            print(trace_to_str([edge], graph))