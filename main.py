import test_generator
from bison_graph_constructor import construct_graph as construct_graph_bison, get_bison_file
from config import Config

if __name__ == '__main__':
    # file_utils.clean_directory()
    #
    config = Config.get_instance()
    #
    # command_automaton_map = {
    #     "LALR1": "-R",
    #     "LR0": "-S",
    #     "LR1": ""
    # }
    #
    # # generate graph file and automaton text file
    # print(command_automaton_map[
    #           config.get_automaton_type()])
    # command = "./hyacc/hyacc -v -g -O0 " + command_automaton_map[
    #     config.get_automaton_type()] + " " + config.get_grammar_filename()
    # print(command)
    # os.system(command)

    file = get_bison_file("bison_grammars/ampl.output")
    graph = construct_graph_bison(file)
    # file_utils.remove_intermediary_files()
    print(f"T = {len(graph.terminal)}")
    print(f"N = {len(graph.nonterminal)}")
    test_generator.gen_test(graph)
