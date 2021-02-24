test_file = open('out/ampl_results_force_rule.test', 'r')
lines = test_file.readlines()
count = 1
for line in lines:
    if line.startswith('#'):
        continue

    line = line.strip()
    line = line.replace("string", "\"\"")
    line += "\n"
    new_file = open('tmp/ampl_' + str(count) + ".test", 'w')
    new_file.writelines(line)
    new_file.close()
    count += 1

test_file.close()
