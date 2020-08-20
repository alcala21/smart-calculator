class BreakCommand(Exception):
    pass


class HelpCommand(Exception):
    pass


class UnknownCommand(Exception):
    pass


class InvalidExpression(Exception):
    pass


class UnknownVariable(Exception):
    pass


class InvalidIdentifier(Exception):
    pass


class InvalidAssignment(Exception):
    pass


def get_sign(signs):
    if len(signs) == 1:
        return signs
    sign = "+" if signs[0] == signs[1] else "-"
    if len(signs) == 2:
        return sign
    new_signs = sign + signs[2:]
    return get_sign(new_signs)


def extract_character(x, v_dict):
    try:
        number = int(x)
        return number
    except ValueError:
        if x in v_dict:
            return v_dict[x]
        elif x.isalpha():
            raise UnknownVariable
        elif not any([y not in '+-' for y in x]):
            return get_sign(x)
        else:
            raise InvalidIdentifier


def perform_operation(x_list):
    if x_list[1] == "+":
        return x_list[0] + x_list[2]
    return x_list[0] - x_list[2]


def prepare_variables(x_list):
    if len(x_list) == 3:
        if x_list[1] in "+-":
            return perform_operation(x_list)
        else:
            raise InvalidExpression
    else:
        raise InvalidExpression


def calculate_list(x_list):
    try:
        if len(x_list) == 3:
            return prepare_variables(x_list)
        elif len(x_list) == 1:
            return int(x_list[0])
        p_val = prepare_variables(x_list[:3])
        new_list = [p_val] + x_list[3:]
        return calculate_list(new_list)
    except Exception:
        raise InvalidExpression


def assign_value(x, v_dict):
    x = x.replace(" ", "")
    if x.count("=") > 1:
        raise InvalidAssignment
    x_list = x.split("=")
    try:
        if x_list[0].isalpha():
            v_dict[x_list[0]] = int(x_list[-1])
        else:
            raise InvalidIdentifier
    except ValueError:
        if x_list[-1] in v_dict:
            v_dict[x_list[0]] = v_dict[x_list[-1]]
        elif not x_list[-1].isalpha():
            raise InvalidAssignment
        else:
            raise UnknownVariable


def check_command(x):
    if x == '/exit':
        raise BreakCommand
    elif x == '/help':
        raise HelpCommand
    else:
        raise UnknownCommand


values = dict()

while True:
    elems = input().strip()
    try:
        if '=' in elems:
            assign_value(elems, values)
        elif elems.startswith('/'):
            check_command(elems)
        elif elems in values:
            print(values[elems])
        elif elems != '':
            elems = elems.split(" ")
            chars = [extract_character(x, values) for x in elems]
            print(calculate_list(chars))
    except BreakCommand:
        print("Bye!")
        break
    except HelpCommand:
        print("This program performs addition and subtraction of integer variables.")
    except UnknownCommand:
        print('Unknown command')
    except InvalidExpression:
        print('Invalid expression')
    except UnknownVariable:
        print('Unknown variable')
    except InvalidIdentifier:
        print('Invalid identifier')
    except InvalidAssignment:
        print('Invalid assignment')
