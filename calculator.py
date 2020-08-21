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


def extract_characters(x, char_list):
    if len(x) == 0:
        return char_list
    c = x[0]
    out_s = x[1:]
    size = len(char_list)
    if c == '+':
        if size > 0:
            if char_list[-1] == '-':
                char_list[-1] = '-'
            elif char_list[-1] == '+':
                char_list[-1] = '+'
            else:
                char_list.append(c)
    elif c == '-':
        if size > 0:
            if char_list[-1] == "-":
                char_list[-1] = "+"
            elif char_list[-1] == "+":
                char_list[-1] = "-"
            else:
                char_list.append("-")
        else:
            char_list.append(c)
    elif c.isdigit():
        if size > 0:
            if char_list[-1] == '-':
                if size == 1:
                    char_list[-1] = char_list[-1] + c
                else:
                    char_list.append(c)
            elif char_list[-1] in "+*/(^":
                char_list.append(c)
            elif char_list[-1][-1].isdigit():
                char_list[-1] = char_list[-1] + c
            else:
                raise InvalidIdentifier
        else:
            char_list.append(c)
    elif c.isalpha():
        if size > 0:
            if char_list[-1] in '+-*/()':
                char_list.append(c)
            elif char_list[-1].isalpha():
                char_list[-1] = char_list[-1] + c
            else:
                raise InvalidIdentifier
        else:
            char_list.append(c)

    elif c in "^*/":
        if size > 0:
            if char_list[-1] not in '*/(':
                char_list.append(c)
            else:
                raise InvalidExpression
        else:
            char_list.append(c)

    elif c == '(':
        if size > 0:
            if char_list[-1].isalpha():
                raise InvalidExpression
            else:
                char_list.append(c)
        else:
            char_list.append(c)
    elif c == ')':
        if size > 0:
            if char_list[-1] in '+-*/':
                raise InvalidExpression
            elif char_list[-1] == '(':
                del char_list[-1]
            else:
                char_list.append(c)
        else:
            raise InvalidExpression

    return extract_characters(out_s, char_list)


def eval_character(x, v_dict):
    try:
        number = int(x)
        return number
    except ValueError:
        if x in v_dict:
            return v_dict[x]
        elif x.isalpha():
            raise UnknownVariable
        elif x in '+-*/()^':
            return x
        else:
            raise InvalidIdentifier


def perform_operation(x_list):
    if x_list[1] == "+":
        return x_list[0] + x_list[2]
    elif x_list[1] == "-":
        return x_list[0] - x_list[2]
    elif x_list[1] == "*":
        return x_list[0] * x_list[2]
    elif x_list[1] == "/":
        return x_list[0] // x_list[2]
    elif x_list[1] == "^":
        return x_list[0] ** x_list[2]


def prepare_variables(x_list):
    if len(x_list) == 3:
        if x_list[1] in "+-*/^":
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
        index = 1
        if ')' in x_list:
            r_index = x_list.index(')')
            l_index = max(i for i in range(len(x_list[0:r_index]))
                          if x_list[i] == '(')
            p_list = x_list[l_index + 1: r_index]
            p_val = calculate_list(p_list)
            new_list = x_list[:l_index] + [p_val] + x_list[r_index + 1:]
            return calculate_list(new_list)

        if "^" in x_list:
            index = x_list.index("^")
        elif "*" in x_list:
            index = x_list.index('*')
        elif "/" in x_list:
            index = x_list.index('/')
        p_val = prepare_variables(x_list[index - 1:index + 2])
        new_list = x_list[:index - 1] + [p_val] + x_list[index + 2:]
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
    elems = input().replace(" ", "")
    try:
        if '=' in elems:
            assign_value(elems, values)
        elif elems.startswith('/'):
            check_command(elems)
        elif elems in values:
            print(values[elems])
        elif elems != '':
            e_chars = extract_characters(elems, [])
            chars = [eval_character(x, values) for x in e_chars]
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
