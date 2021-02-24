import argparse
import os
import re


def parse_args():
    # initialise the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-f1')
    parser.add_argument('-f2')
    args = parser.parse_args()

    file1 = args.f1
    file2 = args.f2

    return [file1, file2]


def get_test_cases(filename):
    file = open(filename, 'r')
    test_cases = set()
    for line in file.readlines():
        line = line.rstrip()
        line = line.lstrip()
        if len(line) == 0:
            test_cases.add(line)
        if len(line) > 0 and line[0] != '#':
            line = line.rstrip()
            line = line.lstrip()
            line = re.sub(r"\s+", "", line)
            test_cases.add(line)
    return test_cases


if __name__ == '__main__':
    args = parse_args()
    test_suite1 = get_test_cases(args[0])
    test_suite2 = get_test_cases(args[1])
    print("Test cases in test suite 1 and not in suite 2:")
    diff1 = test_suite1 - test_suite2
    print("Test cases in test suite 2 and not in suite 1:")
    diff2 = test_suite2 - test_suite1
    print("Test suite 1 - Test suite 2: " + str(len(diff1)))
    print("Overlap of 1 with 2: " + str((len(test_suite1) - len(diff1)) / len(test_suite1)))
    print("Test suite 2 - Test suite 1: " + str(len(diff2)))
    print("Overlap of 2 with 1: " + str((len(test_suite2) - len(diff2)) / len(test_suite2)))
    print("Number in common: " + str(len(test_suite2.intersection(test_suite1))))
    print("Number in common: " + str(len(test_suite1.intersection(test_suite2))))

    size = os.get_terminal_size()
    l1 = list(diff1)
    l2 = list(diff2)
    l1.sort(key=len)
    l2.sort(key=len)
    max_c = max(len(l1), len(l2))
    for i in range(max_c):
        case1 = ""
        case2 = ""
        if i < len(l1):
            case1 += l1[i]
        if i < len(l2):
            case2 += l2[i]

        term_width = os.get_terminal_size().columns
        col_width = (term_width - 1) // 2

        if len(case1) < col_width:
            spaces_needed = col_width - len(case1)
            case1 = case1 + " " * spaces_needed

        if len(case2) < col_width:
            spaces_needed = col_width - len(case2)
            case2 = case2 + " " * spaces_needed

        print(case1 + "|" + case2)
