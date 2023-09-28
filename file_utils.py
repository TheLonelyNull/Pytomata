import os

import tqdm


def clean_directory():
    os.system('rm -f y.* visual.*')


def remove_intermediary_files():
    os.system('rm -f y.* visual.gviz')


def output_test_cases(test_cases, filename):
    print(f"Writing to {filename}")
    out_lines = []
    case_nr = 1
    test_cases = list(test_cases)
    test_cases.sort()
    for case in tqdm.tqdm(test_cases):
        # case = case.replace('FULLSTOP', '.')
        # case = case.replace('RIGHTARROW', '->')
        case = case.replace('STRING', '""')
        case.rstrip()
        case += "\n"
        out_lines.append(case)
        # space it out
        # for char in case:
        #     out_str += char + ""
        case_nr += 1

    if filename is None:
        print("".join(out_lines))
    else:
        file = open("./out/" + filename, 'w')
        file.writelines(out_lines)
        print("Wrote results to ./out/" + filename)
        file.close()
