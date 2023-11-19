from copy import deepcopy
from my_parser import THE_OPERATORS
from utils import *

# Return the truth table from the given binary tree
def create_truth_table(bin_tree, variables):
    logic_tab = fill_empty_truth_table(len(variables))
    tree_copy = list()

    for i, row in enumerate(logic_tab):
        tree_copy = deepcopy(bin_tree)
        fill_tree_with_values(tree_copy, variables, row)

        compute_function_result(tree_copy)
        row.append(tree_copy[0])

    return logic_tab

# Create a blank truth table
def fill_empty_truth_table(nb_vars):
    logic_tab = list()

    i = 0
    while i < pow(2, nb_vars):
        logic_tab.append([])

        i_copy = bin_convert(i)
        j = 0

        while j < nb_vars:
            logic_tab[i].append(i_copy % 10)
            i_copy //= 10
            j += 1

        logic_tab[i].reverse()
        i += 1

    return logic_tab

# Apply the given values to the variables in the binary tree
def fill_tree_with_values(bin_tree, variables, values):
    if not (bin_tree[0] in THE_OPERATORS + "10"):
        var_index = variables.index(bin_tree[0])
        bin_tree[0] = values[var_index]

    if len(bin_tree[1]) != 0:
        fill_tree_with_values(bin_tree[1], variables, values)

    if len(bin_tree[2]) != 0:
        fill_tree_with_values(bin_tree[2], variables, values)

# Recursive function that computes the result of a function
def compute_function_result(bin_tree):
    if bin_tree[0] != "/" and (str(bin_tree[1][0]) in THE_OPERATORS):
        compute_function_result(bin_tree[1])

    if str(bin_tree[2][0]) in THE_OPERATORS:
        compute_function_result(bin_tree[2])

    result = 0

    if bin_tree[0] == "+":
        result = bin_tree[1][0] or bin_tree[2][0]

    elif bin_tree[0] == ".":
        result = bin_tree[1][0] and bin_tree[2][0]

    elif bin_tree[0] == "@":
        result = xor(bin_tree[1][0], bin_tree[2][0])

    else:  # == /
        result = no(bin_tree[2][0])

    bin_tree[0] = result
    bin_tree[1].clear()
    bin_tree[2].clear()

def bin_convert(integer):
    result = 0
    cpt = 1

    while integer > 0:
        result += (integer % 2) * cpt
        integer //= 2
        cpt *= 10

    return result

# Return the disjunctive normal form (DNF) of the function defined by the table logic_tab
def get_dnf(logic_tab, variables):
    cano_form = list()

    for i, row in enumerate(logic_tab):
        if row[len(row) - 1] == 1:
            term = str()
            j = 0

            while j < len(row) - 1:
                if row[j] == 0:
                    term += "/"

                term += variables[j]
                if j != len(row) - 2:
                    term += "."

                j += 1

            cano_form.append(term)

    return cano_form

# Simply the terms given in DNF
def simplify_terms(terms):
    result = list(terms)
    stop = False

    while not stop:
        stop = True
        cons_list = []
        result = apply_all_absorptions(result)

        i = 0
        while i < len(result) - 1:
            j = i + 1
            while j < len(result):
                cons = get_consensus(result[i], result[j])
                if cons != 0:
                    cons_list.append(cons)

                j += 1

            i += 1

        if cons_list != []:
            result += cons_list
            stop = False

    return result

# Apply all possible absorptions on the given terms
def apply_all_absorptions(terms):
    result = list(terms)
    absor = True

    while absor:
        absor = False

        i = 0
        while i < len(result) - 1:
            j = i + 1
            while j < len(result):
                facto = apply_absorption(result[i], result[j])

                if facto == 0:
                    j += 1

                else:
                    result[i] = facto
                    result.pop(j)
                    absor = True

            i += 1

    return result

# Apply the absorption law with a and b and return the result
# Return 0 if there isn't any absorption
def apply_absorption(a, b):
    result = list()
    a_vars = a.split(".")
    b_vars = b.split(".")

    a_fact = list()
    b_fact = list()

    for el in a_vars:
        if b_vars.count(el) == 0:
            a_fact.append(el)

        else:
            result.append(el)

    for el in b_vars:
        if a_vars.count(el) == 0:
            b_fact.append(el)

    if a_fact == [] or b_fact == [] or (len(a_fact) == 1 and len(b_fact) == 1 and are_opposite(a_fact[0], b_fact[0])):
        return ".".join(result)

    return 0

# Return the consensus between a and b
# Return 0 if there isn't a consensus
def get_consensus(a, b):
    variables = get_all_variables(a, b)
    result = list()
    nb_opposite = 0

    for el in variables:
        if (el[0] == "/" and variables.count(el[1:]) != 0) or (el[0] != "/" and variables.count("/" + el) != 0):
            if nb_opposite > 2:
                return 0

            nb_opposite += 1

        else:
            result.append(el)

    if result == [] or nb_opposite == 0:
        return 0

    return ".".join(result)
