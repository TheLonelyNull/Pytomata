import os


def clean_directory():
    os.system('rm -f y.* visual.*')


def remove_intermediary_files():
    os.system('rm -f y.* visual.gviz')


def output_test_cases(test_cases, filename):
    out_str = ""
    case_nr = 1
    test_cases = list(test_cases)
    test_cases.sort()
    for case in test_cases:
        case_nr_str = "###### Test Case " + str(case_nr) + " ######"
        out_str += "#" * len(case_nr_str) + "\n"
        out_str += case_nr_str + "\n"
        out_str += "#" * len(case_nr_str) + "\n"
        # space it out
        for char in case:
            out_str += char + ""
        out_str.rstrip()
        out_str += "\n"
        out_str += "#" * len(case_nr_str) + "\n"
        case_nr += 1

    if filename is None:
        print(out_str)
    else:
        file = open("./out/"+filename, 'w')
        print("Wrote results to ./out/"+filename)
        file.write(out_str)
        file.close()
