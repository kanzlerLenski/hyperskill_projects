# write your code here

def compare_regex(input_regex_, input_str_):

    if input_regex_ == ".":
        return True
    elif input_regex_ == input_str_:
        return True
    else:
        return False


def recursive_comparison(input_regex_, input_str_):

    if len(input_regex_) > 0:
        if len(input_str_) > 0:
            if compare_regex(input_regex_[0],
                             input_str_[0]):
                if not recursive_comparison(input_regex_[1:],
                                     input_str_[1:]):
                    return False
            else:
                return False
        else:
            return False

    return True


def dif_len_recursive_comparison(input_regex_,
                                 input_str_):
    saved = ""
    if input_regex_.endswith("$"):
        saved = input_regex_
        input_regex_ = input_regex_[:-1]
    new_str = input_str_
    length = len(input_str_)
    for i in range(length):
        if length > 1:
            new_str = input_str_[i:]
        result = recursive_comparison(input_regex_,
                                      new_str)
        #print(input_regex_, new_str, result)
        if result:
            if saved.endswith("$") and i == 0:
                continue
            else:
                return True
                break
        elif i == len(input_str_) - 1 and not result:
            return False


def check_empty_str(input_regex_, input_str_):

    if input_regex_ == "" and input_str_ == "":
        print("True")
    elif input_regex_ == "" and input_str_ != "":
        print("True")
    elif input_regex_ != "" and input_str_ == "":
        print("False")


def check_len(input_regex_, input_str_):
    return len(input_regex_) == len(input_str_)


def check_metachars(input_regex_, input_str_, both_=False):

    if "?" in input_regex_:
        first_case = input_regex_[:input_regex_.index("?") - 1] + input_regex_[input_regex_.index("?") + 1:]
        if recursive_comparison(first_case, input_str_):
            if both_:
                return check_len(first_case, input_str_)
            return True
        else:
            second_case = input_regex_.replace("?", "")
            if recursive_comparison(second_case, input_str_):
                if both_:
                    return check_len(second_case, input_str_)
                return True
            else:
                return False

    elif "*" in input_regex_:
        first_case = input_regex_[:input_regex_.index("*") - 1] + input_regex_[input_regex_.index("*") + 1:]
        if recursive_comparison(first_case, input_str_):
            if both_:
                return check_len(first_case, input_str_)
            return True
        else:
            second_case = input_regex_.replace("*", "")
            if recursive_comparison(second_case, input_str_):
                if both_:
                    return check_len(second_case, input_str_)
                return True
            else:
                c = input_regex_[input_regex_.index("*") - 1]
                tries = len(input_str_) - len(first_case) + 1
                temp = False
                for i in range(1, tries):
                    c2 = c * i
                    second_case = second_case.replace(c, c2)
                    if recursive_comparison(second_case, input_str_):
                        temp = True
                        break
                if temp:
                    if both_:
                        return check_len(second_case, input_str_)
                    return True
                else:
                    return False

    elif "+" in input_regex_:
        first_case = input_regex_.replace("+", "")
        if recursive_comparison(first_case, input_str_):
            if both_:
                return check_len(first_case, input_str_)
            return True
        else:
            c = input_regex_[input_regex_.index("+") - 1]
            tries = len(input_str_) - len(first_case) + 2
            temp = False
            for i in range(1, tries):
                c2 = c * i
                second_case = first_case.replace(c, c2)
                if recursive_comparison(second_case, input_str_):
                    temp = True
                    break
            if temp:
                if both_:
                    return check_len(second_case, input_str_)
                return True
            else:
                return False


def main(input_regex_, input_str_):
    if input_regex_ == "" or input_str_ == "":
        check_empty_str(input_regex_, input_str_)

    elif any(x in input_regex_ for x in \
             ("\\", "\\.", "\\+", "\\*", "\\?", "\\^", "\\$")):
        input_regex_ = input_regex_.replace("\\", "")
        if dif_len_recursive_comparison(input_regex_,
                                     input_str_):
            print("True")
        else:
            print("False")

    elif input_regex_.startswith("^") and not \
            input_regex_.endswith("$"):
        if recursive_comparison(input_regex_[1:],
                                input_str_):
            print("True")
        else:
            if check_metachars(input_regex_[1:], input_str_):
                print("True")
            else:
                print("False")

    elif input_regex_.startswith("^") and \
            input_regex_.endswith("$"):
        if input_str_ == input_regex_[1:][:-1]:
            print("True")
        else:
            if check_metachars(input_regex_[1:][:-1], input_str_, True):
                print("True")
            else:
                print("False")

    else:
        if dif_len_recursive_comparison(input_regex_,
                                        input_str_):
            print("True")
        else:
            if check_metachars(input_regex_, input_str_):
                print("True")
            else:
                print("False")


input = input().split("|")
input_regex = input[0]
input_str = input[1]
main(input_regex, input_str)