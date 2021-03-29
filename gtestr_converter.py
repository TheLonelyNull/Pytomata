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
        line = file.readline()
        if not line.startswith("nonterm") and started:
            break

        if line.startswith("nonterm") and not started:
            started = True

        if started:
            arr = re.split("nonterm\(|\)\.\n", line)
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
            arr = re.split("\((?=\d+:\d+)|\)\.\n|\)\.\Z", line)
            contents = re.split("(?=.*\[), ", arr[1])
            nonterm = contents[1].strip()
            assert nonterm in nonterms
            if nonterm not in rules:
                rules[nonterm] = []
            rhs = contents[2].strip()
            rhs = rhs[1:-1]
            rhs_arr = re.split(', ', rhs)
            for j in range(len(rhs_arr)):
                rhs_arr[j] = rhs_arr[j].strip()
            if len(rhs_arr) == 1 and rhs_arr[0] == "":
                rules[nonterm].insert(0, rhs_arr)
            else:
                rules[nonterm].append(rhs_arr)
    return rules


def replace_escape_char_nt(nonterms):
    nonterms_map = dict()

    for i, nt in enumerate(nonterms):
        firstchar = chr(i // 26 + 65)
        secondchar = chr(i % 26 + 65)
        nonterms_map[nt] = str(firstchar) + str(secondchar)
    return nonterms_map


def unquote_t(terms):
    terms_map = dict()
    for t in terms:
        if t[0] == "\'" and t[-1] == "\'":
            terms_map[t] = t[1:-1]
        else:
            terms_map[t] = t
    return terms_map


if __name__ == "__main__":
    filename = sys.argv[1]
    f = open(filename, 'r')

    nt = parse_nonterms(f)
    nt_map = replace_escape_char_nt(nt)
    t = parse_terms(f)
    t_map = unquote_t(t)
    rules = parse_rules(f, t, nt)
    name = re.split('.', filename)[0]
    out = open(name + ".y", 'w')
    lines = []
    for rule in rules:
        line = ""
        line += nt_map[rule] + ": "
        offset_spaces = len(line)
        # deal with epsilon
        for sub in rules[rule]:
            cur_t_str = ""
            for symbol in sub:
                if symbol in nt:
                    if len(cur_t_str) > 0:
                        line += "\'" + cur_t_str + "\' "
                        cur_t_str = ""
                    line += nt_map[symbol] + " "
                elif symbol in t:
                    cur_t_str += t_map[symbol]
            if len(cur_t_str) > 0:
                line += "\'" + cur_t_str + "\' "
            line += "|"
            lines.append(line)
            line = " " * offset_spaces
        # chop of last |
        lines[-1] = lines[-1][:-1]
        lines.append(" " * (offset_spaces - 2) + ";")
        lines.append("")

    print("%%")
    print()

    for line in lines:
        print(line)

    print()
    print("%%")
