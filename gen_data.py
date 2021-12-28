import os, sys


def call_pytomata(coverage, seed, grammar, out):
    command = "python main.py -f %s -c %s -o %s --seed %d --classic" % (grammar, coverage, out, seed)
    os.system(command)


if __name__ == "__main__":
    grammar = sys.argv[1]
    coverage = "positive"
    for i in range(1, 101):
        out = "lr_%d.test" % (i)
        call_pytomata(coverage, i, grammar, out)
    os.system("mkdir -p data")
    for i in range(1, 101):
        out_file = open("out/lr_%d.test" % (i), 'r')
        contents = out_file.readlines()
        os.system('mkdir -p data/lr-%d' % (i))
        for j, line in enumerate(contents):
            new_line = line.replace('STRING', '\"\"')
            new_file = open('data/lr-%d/lr_%d_%d.test' % (i, i, j), 'w')
            new_file.writelines([new_line])
            new_file.close()
        out_file.close()
