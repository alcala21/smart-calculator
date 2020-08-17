def get_symbol(symbols):
    if len(symbols) == 1:
        return symbols[0]
    if symbols[0] == symbols[1]:
        symbol = '+'
    else:
        symbol = '-'
    if len(symbols) == 2:
        return symbol
    new_symbols = symbol + symbols[2:]
    return get_symbol(new_symbols)


def extract_character(x):
    try:
        number = int(x)
        return number
    except ValueError:
        if any([y.isalpha() for y in x]):
            raise ValueError
        elif not any([y not in '+-' for y in x]):
            return get_symbol(x)


def perform_operation(x_list):
    if len(x_list) == 3:
        if x_list[1] == "+":
            return x_list[0] + x_list[2]
        elif x_list[1] == '-':
            return x_list[0] - x_list[2]
        else:
            raise ValueError('You need operation symbols.')
    else:
        raise ValueError('List needs three elements.')


def calculate_list(x_list):
    if len(x_list) == 3:
        return perform_operation(x_list)
    elif len(x_list) == 1:
        return int(x_list[0])
    p_val = perform_operation(x_list[:3])
    new_list = [p_val] + x_list[3:]
    return calculate_list(new_list)


while True:
    elems = input().strip().split(" ")
    try:
        if elems[0] == '/exit':
            print('Bye!')
            break
        elif elems[0] == '/help':
            print("The program performs addition and subtraction of integers")
        elif elems[0] != '':
            chars = [extract_character(x) for x in elems]
            print(calculate_list(chars))
    except ValueError:
        pass
