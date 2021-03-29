import os
import re
from pathlib import Path


def call_pytomata(coverage, seed, grammar, out):
    command = "python main.py -f %s -c %s -o %s --seed %d" % (grammar, coverage, out, seed)
    os.system(command)


def sub_json_keys(input_str):
    """For json contact since yacc cant take strings directly"""
    keys = re.findall("[a-z\-]+:", input_str)
    keys = list(set(keys))
    output = input_str
    for key in keys:
        output = output.replace(key, '\"' + key[:-1] + '\"' + " :")
    return output


def sub_strings(input):
    tokens = {
        'email_str': '\"a@b.com\"',
        'date_string': '\"01/01/2021\"',
        'phone_string': '\"0123456789\"',
        'string': '\"a\"'}
    output = input
    for key in tokens:
        output = output.replace(key, tokens[key])
    return output


if __name__ == "__main__":
    grammar = "grammars/json_contact.y"
    coverage = "positive"
    for i in range(1, 101):
        out = "lr_%d.test" % (i)
        call_pytomata(coverage, i, grammar, out)
    os.system("mkdir -p data")
    for i in range(1, 101):
        os.system("mkdir -p data/lr_%d" % (i))
        out = "lr_%d.test" % (i)
        test_file = open('out/%s' % (out), 'r')
        lines = test_file.readlines()
        count = 1
        for line in lines:
            if line.startswith('#'):
                continue

            line = line.strip()
            line = sub_json_keys(line)
            #line = sub_strings(line)
            line += "\n"
            new_file = open('data/lr_%d/lr_%d.test' % (i, count), 'w')
            new_file.writelines(line)
            new_file.close()
            count += 1

        test_file.close()
