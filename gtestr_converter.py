import sys
import re
from typing import IO


def parse_terms(f: IO):
    terms = []
    started = False
    while True:
        line = f.readline()
        if not line.startswith("terminal") and started:
            break

        if line.startswith("terminal") and not started:
            started = True

        if started:
            arr = re.split("\(|\)", line)
            term = arr[1]
            terms.append(term)
    return terms


def parse_nonterms(file):
    nonterms = []
    started = False
    while True:
        line = f.readline()
        if not line.startswith("nonterm") and started:
            break

        if line.startswith("nonterm") and not started:
            started = True

        if started:
            arr = re.split("\(|\)", line)
            term = arr[1]
            nonterms.append(term)
    return nonterms


def parse_rules(file, terms, nonterms):
    rules = {}
    started = False
    i = None
    while True:
        line = f.readline()
        if not line.startswith("rule") and started:
            break

        if line.startswith("rule") and not started:
            started = True

        if started:
            arr = re.split("\((?=\d*:\d*)|\)\.\n|\)\.\Z", line)
            contents = re.split("(?=.*\[),", arr[1])
            rule_nr = int(re.split(":", contents[0])[0])
            nonterm = contents[1].strip()
            if rule_nr != i:
                i = rule_nr
                rules[nonterm] = list()
            rhs = contents[2].strip()
            rhs = rhs[1:-1]
            rhs = re.split(', ', rhs)
            for j in range(len(rhs)):
                rhs[j] = rhs[j].strip()
            rules[nonterm].append(rhs)
    return rules


if __name__ == "__main__":
    filename = sys.argv[1]
    f = open(filename, 'r')

    nt = parse_nonterms(f)
    t = parse_terms(f)
    rules = parse_rules(f, t, nt)
    name = re.split('.')[0]
    out = open(name+".y", 'w')
    for rule in rules:
        line = ""
        line += rule
        for sub in rules[rule]:
            