import os
import re
from pathlib import Path
from sub_sql import sub


def call_pytomata(coverage, seed, grammar, out):
    command = "python main.py -f %s -c %s -o %s --seed %d" % (grammar, coverage, out, seed)
    os.system(command)


if __name__ == "__main__":
    grammar = "grammars/sqlite.y"
    coverage = "positive"
    for i in range(1, 101):
        out = "lr_%d.test" % (i)
        call_pytomata(coverage, i, grammar, out)
    os.system("mkdir -p data")
    for i in range(1, 101):
        out = "lr_%d.test" % (i)
        test_file = open('out/%s' % (out), 'r')
        lines = test_file.readlines()
        test_file.close()
        lines = sub(lines)
        new_file = open('data/%s' % (out), 'w')
        new_file.writelines(lines)
        new_file.close()
