import os
from pathlib import Path


def call_pytomata(coverage, seed, grammar, out):
    command = "python main.py -f %s -c %s -o %s --seed %d" % (grammar, coverage, out, seed)
    os.system(command)


if __name__ == "__main__":
    grammar = "grammars/ampl17.y"
    coverage = "positive"
    os.system("mkdir lr_data")
    for i in range(1, 101):
        continue
        out = "lr_%d.test" % (i)
        call_pytomata(coverage, i, grammar, out)
    os.system("mkdir data")
    for i in range(1, 101):
        os.system("mkdir data/lr_%d" % (i))
        out = "lr_%d.test" % (i)
        test_file = open('out/%s' % (out), 'r')
        lines = test_file.readlines()
        count = 1
        for line in lines:
            if line.startswith('#'):
                continue

            line = line.strip()
            line = line.replace("string", "\"\"")
            line += "\n"
            new_file = open('data/lr_%d/lr_%d.test' % (i, count), 'w')
            new_file.writelines(line)
            new_file.close()
            count += 1

        test_file.close()
