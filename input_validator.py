import argparse
import os


def check_type(type):
    if type != "LALR1" and type != "LR0" and type != "LR1":
        print("Invalid automaton automaton_type selected. Only valid arguments are LR0, LR1 and LALR1")
        exit(1)


def check_file(filename):
    if filename is None:
        print("No grammar specified")
        exit(1)

    f = open(filename, 'r')
    try:
        f = open(filename, 'r')
    except:
        print(os.getcwd())
        print("File not found")
        exit(1)


def check_coverage_criteria(coverage_type):
    valid_types = ['positive', 'neg-sub', 'neg-cut', 'neg-del', 'neg-add']
    if coverage_type is None:
        print('No coverage type specified.')
        exit(1)
    if coverage_type not in valid_types:
        valid_str = ""
        for i in range(len(valid_types)):
            if i == len(valid_types) - 1:
                valid_str += valid_types[i] + '.'
            elif i != len(valid_types) - 2:
                valid_str += valid_types[i] + ', '
            elif i == len(valid_types) - 2:
                valid_str += valid_types[i] + ' and '
        print("Invalid coverage criteria.Valid types are " + valid_str)
        exit(1)


def parse_args():
    # initialise the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--lr', help='LR automaton type. Defaults to LR0', default='LR0')
    parser.add_argument('-f', '--input-file', help='Path to input grammar file, relative to this folder.')
    parser.add_argument('-g', '--graph', action='store_true',
                        help='Flag for whether graph should be produced in ./out/')
    parser.add_argument('-c', '--coverage',
                        help='Coverage type. Can be positive, neg-sub, neg-cut, neg-del and neg-add.')
    parser.add_argument('-o', '--output-file', help='Name of output file. Stored in ./out/')
    parser.add_argument('-s', '--classic', action='store_true', help='Use algorithms for SLE2020')
    parser.add_argument('--classicimproved', action='store_true', help='Use improved BFS algorithm from 2020')
    parser.add_argument('--seed', type=int, help='Seed for random choices', default=1)
    parser.add_argument('--stack', help='Should produce negative test suites using stack mutations', action='store_true')
    args = vars(parser.parse_args())

    return args
