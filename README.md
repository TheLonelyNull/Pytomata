# PyTomata
PyTomata is a program that generates test cases for context free grammars
using the LR-automaton corresponding to the grammar. It can produce both
positive and negative test suites.
## Notes for SLE2020 reviewer
In order to produce the same test suite as seen in the LR column of the table please run the program with
the `--classic` flag as we have since improved our algorithm. We have improved on LR* so the test suites 
currently generated without the `--classic` flag are considerably smaller than those presented in the column
for LR*. However, please take note that this improved implementation is still a work in progress and may not
be fully stable yet.

All grammar files used for our data may be found in the `grammars/SLE2020-grammars` directory.

All of the data generated may also be found in the `sle_results` directory.
## Dependencies
1. Python 3.7
2. Python libraries(install using requirements.txt)
3. GraphViz (only required if a graph for the automaton is to be produced)
4. Hyacc (bundled with Pytomata)

## Installation
1. Extract this archive to a suitable location
2. Enter the folder into which you extracted it
3. Enter the `hyacc` directory with `cd hyacc`
4. Ensure that build tools(`gcc` and `make`) are installed and up to date. Running
`gcc -version` should return version `10.2.0` or greater
5. Extract the hyacc by running `tar xvf hyacc_unix_src_04-08-09.tar.gz`
6. Still within the `hyacc` directory run `make release`. This should result in the message
`release version is successfully built`
7. Go back to the parent directory by running `cd ..s` 
8. Ensure `python3.7+` is installed on your system by running `python --version`. If python3 is not
the default on your system but it is installed you may use `python3` instead of `python` to run the commands
in the examples below
4. Install python dependencies from requirements.txt using pip. Run `pip3 install -r requirements.txt`. 
5. Install GraphViz for your system if you want to produce graphs(found [here](https://graphviz.org/))

## Usage
PyTomata assumes the grammar file in BNF form as used by Bison/Yacc.
### Main
To generate a test suite run
```
python main.py <command-line options>
```
#### Options for main
```
-l      The automaton type to use.
        Only supports LR(0) at this time.
        Defaults to LR0
-f      Path to grammar file in yacc format. Relative to the folder containing main.py
-g      Boolean flag for whether to produce graph.
        Defaults to False
-c      Test suite type. Valid types are positive,
        neg-sub, neg-cut, neg-del and neg-add.
-o      output file name. Prints to terminal if not
        specified
-s,     Use version of algorithms for SLE2020
```
### Testing Coverage
To test coverage run
```
python coverage_tester.py  <command-line options>
```
#### Options for coverage coverage_tester
```
-l      The automaton type to use.
        Only supports LR(0) at this time.
        Defaults to LR0
-f      Path to grammar file in yacc format. Relative to main.py
-g      Boolean flag for whether to produce graph.
        Defaults to False
-i      Path to input file containing test suite. Expects tokens
        separated by spaces.
```
### Comparing Test suites
To test overlap between test suites run
```
python overlap_tester.py  <command-line options>
```
#### Options for coverage overlap_tester
```
-f1     Path to input file containing test suite 1. Expects tokens
        separated by spaces.
-f2     Path to input file containing test suite 2s. Expects tokens
        separated by spaces.
```

### Example
To generate positive test cases for the Expr1 grammar using the LR 
algorithm as found in the paper for SLE2020 run
```
python main.py -f grammars/SLE2020-grammars/expr1.y -g -c positive -o expr1.test --classic
```
This will produce two output files in the `./out/` directory. `visual.pdf` is a graphical representation
of the LR-graph and `expr1.test` contains the test suite that has been generated.

To confirm the coverage achieved by this test suite run
```
python coverage_tester.py -f grammars/SLE2020-grammars/expr1.y -i out/expr1.test
``` 