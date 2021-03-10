from graph_components import Node
from config import Config
from neg_utils import extract_add, extract_del, extract_cut, extract_sub, extract_stack_del
from pos_utils import extract_pos


def extract_test_case(T, graph, test_suite_type=None, stack= None, sub_table=None, shortest_table=None):
    if test_suite_type is None:
        test_suite_type = Config.get_instance().get_test_suite_type()
    if stack is None:
        stack = Config.get_instance().get('stack')
    if stack:
        if test_suite_type == 'neg-sub':
            return extract_sub(T, graph)
        elif test_suite_type == 'neg-del':
            return extract_stack_del(T, graph)
        elif test_suite_type == 'neg-add':
            return extract_add(T, graph)
        else:
            print("No negative mutation specified with stack. Quiting...")
            exit(0)
    else:
        if test_suite_type == 'neg-sub':
            return extract_sub(T, graph)
        elif test_suite_type == 'neg-del':
            return extract_del(T, graph)
        elif test_suite_type == 'neg-add':
            return extract_add(T, graph)
        elif test_suite_type == 'neg-cut':
            return extract_cut(T, graph)
        elif test_suite_type == 'positive':
            return extract_pos(T, graph)
