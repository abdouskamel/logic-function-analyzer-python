import sys

from my_exception import MyException
from my_parser import tokenize_function, extract_variables_from_tokens, make_the_tree
from analyzer import create_truth_table, get_dnf, simplify_terms

if len(sys.argv) != 2 or len(sys.argv[1].strip()) == 0:
    print("Usage: python main.py \"<logic_function>\"\nExamples:")
    print("\"A + B\"")
    print("\"/A + B\"")
    print("\"A + /B.C + C\"")
    exit()

try:
    logic_func = sys.argv[1].strip()
    tokens = tokenize_function(logic_func)

    bin_tree = []
    make_the_tree(bin_tree, tokens)

    variables = extract_variables_from_tokens(tokens)
    logic_tab = create_truth_table(bin_tree, variables)

    print(variables)
    for row in logic_tab:
        print(row)

    cano_form = get_dnf(logic_tab, variables)
    print("\nDisjunctive Normal Form (DNF) : \n", " + ".join(cano_form))

    simple_form = simplify_terms(cano_form)
    print("\nSimplified form : \n", " + ".join(simple_form))

except MyException as e:
    print(e)
    exit()
