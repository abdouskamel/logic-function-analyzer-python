from my_exception import MyException

THE_OPERATORS = "/+.@"

# Return the list of tokens in function
# Raise an exception if function is erroneous
def tokenize_function(function):
    tokens = list()
    var = str()

    for i, el in enumerate(function):
        if el in THE_OPERATORS or el in "()":
            if var != "":
                tokens.append(var)
                var = ""

            tokens.append(el)

        elif not el.isspace():
            var += el

    if var != "":
        tokens.append(var)

    check_tokens(tokens)
    return tokens

# Check tokens and raise an exception if an error is found
def check_tokens(tokens):
    nb_brackets = 0

    if len(tokens) == 0:
        raise MyException(list(), -1, "Aucune expression.")

    if tokens[len(tokens) - 1] in THE_OPERATORS:
        raise MyException(tokens, len(tokens) - 1, "Opérateur à la fin de l'expression.")

    for i, el in enumerate(tokens):
        if el in THE_OPERATORS:
            if (i < len(tokens) - 1) and (tokens[i + 1] in THE_OPERATORS) and (tokens[i + 1] != "/"):
                raise MyException(tokens, i, "Deux opérateurs successifs.")

        elif el == "(":
            nb_brackets += 1

        elif el == ")":
            if nb_brackets <= 0:
                raise MyException(tokens, i, "Parenthèse fermante indépendante.")

            nb_brackets -= 1

        else:
            if not check_variable(el):
                raise MyException(tokens, i, "Vos variables ne doivent contenir que des caractères alphanumériques.")

            elif (i < len(tokens) - 1 and not (tokens[i + 1] in (THE_OPERATORS + ")"))):
                raise MyException(tokens, i + 1, "Deux variables qui se suivent sans opérateur.")

    if nb_brackets != 0:
        raise MyException(tokens, -1, "Veuillez vérifier vos parenthèses.")

# Return True if var contains only alphanumeric characters
def check_variable(var):
    if var.isdecimal() and var != "0" and var != "1":
        return False

    for el in var:
        if not var.isalnum():
            return False

    return True

# Return a list with all variables in tokens
def extract_variables_from_tokens(tokens):
    variables = list()

    for el in tokens:
        if not (el in THE_OPERATORS + "()01") and variables.count(el) == 0:
            variables.append(el)

    return variables

# Get a binary tree from tokens
def make_the_tree(bin_tree, tokens):
    if len(tokens) != 0:
        if len(tokens) == 1:
            bin_tree.append(tokens[0])
            bin_tree.append([])
            bin_tree.append([])

        else:
            brackets = 0
            the_op = 0

            remove_redundant_brackets(tokens)

            # Get the operator with the lowest priority
            for i, el in enumerate(tokens):
                if el == "(":
                    brackets += 1

                elif el == ")":
                    brackets -= 1

                elif brackets == 0:
                    if el == "/" and not (tokens[the_op] in "/@.+"):
                        the_op = i

                    elif el == "@" and not (tokens[the_op] in ".+"):
                        the_op = i

                    elif el == "." and tokens[the_op] != "+":
                        the_op = i

                    elif el == "+":
                        the_op = i

            left_tokens = tokens[:the_op]
            right_tokens = tokens[the_op + 1:]

            bin_tree.append(tokens[the_op])
            bin_tree.append([])
            bin_tree.append([])

            make_the_tree(bin_tree[1], left_tokens)
            make_the_tree(bin_tree[2], right_tokens)

# Remove redundant brackets from tokens
def remove_redundant_brackets(tokens):
    while tokens[0] == "(" and tokens[len(tokens) - 1] == ")":
        i = 1
        brackets = 0

        while i < len(tokens):
            if tokens[i] == "(":
                brackets += 1

            elif tokens[i] == ")":
                brackets -= 1
                if brackets < 0:
                    break

            i += 1

        if brackets == 0:
            tokens.pop(0)
            tokens.pop()

        else:
            break
