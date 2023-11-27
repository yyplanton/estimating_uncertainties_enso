# -*- coding:UTF-8 -*-
# ---------------------------------------------------------------------------------------------------------------------#
# Functions to check input values for the paper about estimating_uncertainties_in_simulated_ENSO submitted to JAMES
# ---------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------------------------------------------------------------------------#
# Classes
# ---------------------------------------------------------------------------------------------------------------------#
class BackgroundColors:
    blue = '\033[94m'
    green = '\033[92m'
    orange = '\033[93m'
    red = '\033[91m'
    normal = '\033[0m'
# ---------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------------------------------------------------------------------------#
# Functions
# ---------------------------------------------------------------------------------------------------------------------#
def _types_to_string(type_or_types):
    if isinstance(type_or_types, tuple):
        type_to_print = ", ".join(repr(k.__name__) for k in sorted(type_or_types, key=repr))
    else:
        type_to_print = type_or_types.__name__
    return type_to_print


def check_interval(input_value, input_name: str, type_or_types, interval: list, error_list: list):
    check_type(input_value, input_name, type_or_types, error_list)
    if len(error_list) == 0 and (input_value < min(interval) or input_value > max(interval)):
        error_list.append("%s value error" % repr(input_name))
        error_list.append(str().ljust(5) + "%s %s should be within interval [%s, %s]" % (
            repr(input_name), repr(input_value), repr(min(interval)), repr(max(interval))))


def check_integer_even_or_odd(input_value, input_name: str, even_or_odd: str, error_list: list):
    check_type(input_value, input_name, int, error_list)
    check_list(even_or_odd, "even_or_odd", ["even", "odd"], error_list)
    if len(error_list) == 0 and ((even_or_odd == "even" and input_value % 2 == 1) or
                                 (even_or_odd == "odd" and input_value % 2 == 0)):
        error_list.append("%s value error" % repr(input_name))
        error_list.append(str().ljust(5) + "%s %s should be an %s number" % (
            repr(input_name), repr(input_value), repr(min(even_or_odd))))


def check_list(input_value, input_name: str, list_of_defined_values, error_list: list):
    if input_value not in list_of_defined_values:
        error_list.append("unknown %s: %s" % (repr(input_name), repr(input_value)))
        error_list.append(str().ljust(5) + "known %s%s: %s" % (
            repr(input_name), plural_s(list_of_defined_values),
            ", ".join(repr(k) for k in sorted(list_of_defined_values, key=repr))))
        
        
def check_type(input_value, input_name: str, type_or_types, error_list: list):
    if isinstance(input_value, type_or_types) is False:
        # input is not the right type
        error_list.append("%s type error" % repr(input_name))
        error_list.append(str().ljust(5) + "%s is instance of %s, should be instance of (%s)" % (
            repr(input_name), type(input_value), _types_to_string(type_or_types)))


def plural_s(list_i: list) -> str:
    return "s" if len(list_i) > 1 else ""


def print_fail(stack_i: list, error_i: str):
    if isinstance(error_i, str) and error_i != "":
        tmp = "ERROR: file " + str(stack_i[0][1]) + " ; fct " + str(stack_i[0][3]) + " ; line " + str(stack_i[0][2])
        raise ValueError(BackgroundColors.red + str(tmp) + "\n" + str(error_i) + BackgroundColors.normal)
# ---------------------------------------------------------------------------------------------------------------------#
