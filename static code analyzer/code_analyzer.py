# write your code here
import os
import sys
import ast


def check_path(path_):
    if path_.endswith(".py"):
        main(path_)
    else:
        for file in os.listdir(path_):
            if file.endswith(".py"):
                file_path = path_ + "\\" + file
                main(file_path)


def check_length(path_, string, num):
    if len(string) > 79:
        print(f"{path_}: Line {num + 1}: S001 Too long")


def check_indentation(path_, string, num):
    count = 0
    for c in string:
        if c == " ":
            count += 1
        else:
            break
    if count % 4 != 0:
        print(f"{path_}: Line {num + 1}: S002 Indentation is not a multiple of four")


def check_semicolon(path_, string, num):
    string_split = string.split(";")[0]
    if "#" not in string_split:
        if (string_split.count("\"") or string_split.count("'")) % 2 == 0:
            print(f"{path_}: Line {num + 1}: S003 Unnecessary semicolon after a statement")


def check_spaces(path_, string, num):
    string_split = string.split("#")[0][-2:]
    if string_split != "  ":
        print(f"{path_}: Line {num + 1}: S004 At least two spaces before inline comments required")


def check_todo(path_, string, num):
    string = string.lower()
    if "todo" in string:
        string_split = string.split("todo")[0]
        if "#" in string_split:
            print(f"{path_}: Line {num + 1}: S005 TODO found")


def check_class_names(path_, string, num):
    count_spaces(path_, string, num, "class")

    if string.isupper() or string.islower():
        name = string.split()[1]
        print(f"{path_}: Line {num + 1}: S008 Class name '{name}' should "
              f"use CamelCase")


def check_def_names(path_, string, num):
    count_spaces(path_, string, num, "function")

    check_snake_case(path_, string, num, "S009", "Function")

    root = ast.parse(string)
    function = root.body[0]
    arg_names = [a.arg for a in function.args.args]
    def_vals = [b.id for b in function.args.defaults]
    for arg_name in arg_names:
        check_snake_case(path_, arg_name, num, "S010", "Argument")

    if def_vals:
        for def_val in def_vals:
            if def_val in ("[]", "{}", "set()"):
                print(f"{path_}: Line {num + 1}: S012 Default argument value is mutable")


def check_snake_case(path_, string, num, code, entity):
    if not string.isupper() and not string.islower() and "_" not in string:
        if string.startswith("class") or string.stsrtswith("def"):
            string = string.split()[1]
        if entity == "Varible":
            print(f"{path_}: Line {num + 1}: {code} {entity} '{string}' "
                  f"in functions should use snake_case")
        else:
            print(f"{path_}: Line {num + 1}: {code} {entity} name '{string}' "
                  f"should use snake_case")


def count_spaces(path_, string, num, entity):
    if string.count(" ") > 1:
        print(f"{path_}: Line {num + 1}: S007 Too many spaces after "
              f"'{entity}'")


def check_variable_names(path_, string, num):
    root = ast.parse(string)
    func_call = [node for node in ast.walk(root) if isinstance(node, ast.Call)]
    args = [ast.literal_eval(a) for a in func_call[0].args]
    for arg in args:
        check_snake_case(path_, arg, num, "S011", "Variable")


def main(path_):
    with open(path_) as input_script:
        blank_line = 0
        for i, line in enumerate(input_script):
            if line.strip() == "":
                blank_line += 1
            check_length(path_, line, i)
            check_indentation(path_, line, i)
            if ";" in line:
                check_semicolon(path_, line, i)
            if not line.startswith("#") and "#" in line:
                check_spaces(path_, line, i)
            check_todo(path_, line, i)
            if line.strip() != "" and blank_line > 2:
                print(f"{path_}: Line {i + 1}: S006 More than two blank lines used before this line")
                blank_line = 0
            if line.startswith("class"):
                check_class_names(path_, line, i)
            check_variable_names(path_, line, i)
            if line.startswith("def"):
                check_def_names(path_, line, i)


path = sys.argv[1]
check_path(path)
