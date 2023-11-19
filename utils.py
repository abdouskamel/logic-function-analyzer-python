# Return True if a = /b
def are_opposite(a, b):
    return (a[0] == "/" and a[1] == b) or (b[0] == "/" and b[1] == a)

# Get in a list all variables defined in a and b
def get_all_variables(a, b):
    variables = a.split(".") + b.split(".")
    result = list()

    for el in variables:
        if result.count(el) == 0:
            result.append(el)

    return result

def xor(a, b):
    if a == b:
        return 0

    else:
        return 1

def no(a):
    if a:
        return 0

    else:
        return 1
