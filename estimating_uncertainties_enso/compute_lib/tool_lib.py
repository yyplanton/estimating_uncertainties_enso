# -*- coding:UTF-8 -*-
# ---------------------------------------------------------------------------------------------------------------------#
# Functions to do basic processing for the paper about estimating_uncertainties_in_simulated_ENSO submitted to JAMES
# ---------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------#
# Import packages
# ---------------------------------------------------#
# basic python package
from copy import deepcopy
from inspect import stack as inspect__stack
from json import load as json__load
import os
# numpy
from numpy import ndarray as numpy__ndarray
# xarray
from xarray import open_dataset
# estimating_uncertainties_enso package
from . check_lib import check_type, print_fail
# ---------------------------------------------------#


# ---------------------------------------------------------------------------------------------------------------------#
# Functions
# ---------------------------------------------------------------------------------------------------------------------#
def tool_put_in_dict(dict_i: dict, value, *args) -> dict:
    """
    Put value in the dictionary

    Inputs:
    -------
    :param dict_i: dict
        Dictionary in which the value must be added
    :param value: int or float or list
        Value to add in the dictionary
        If it is a list, it will be appended to the list already inside the dictionary
    :param args: str
        Non keyword arguments used as keys in the dictionary

    Output:
    -------
    :return dict_i: dict
        Dictionary in which the value was added at the nested level given by the list of keys
    """
    # check input
    error = list()
    check_type(dict_i, "dict_i", dict, error)
    check_type(value, "value", (float, int, list, numpy__ndarray, str, type(None)), error)
    check_type(args, "args", tuple, error)
    print_fail(inspect__stack(), "\n".join(k for k in error))
    # put value in the dictionary
    _dict = dict_i
    for k in args:
        if k == args[-1] and k in list(_dict.keys()) and isinstance(value, list) is True:
            _dict[k] += value
        elif k == args[-1] and k not in list(_dict.keys()):
            _dict[k] = value
        else:
            if k not in list(_dict.keys()):
                _dict[k] = dict()
            _dict = _dict[k]
    return dict_i


def tool_read_json(filename: str = None) -> dict:
    """
    Read the json file

    Input:
    ------
    :param filename: str
        json file name to read
        
    Output:
    -------
    :return dict_o: dict
        Dictionary with nine nested levels [metric, diagnostic or metadata, value or metadata_name, project, dataset,
        experiment, member, epoch_length, epoch], filled with a value
    """
    if isinstance(filename, str) is False:
        filename = "estimating_uncertainties_in_simulated_enso.json"
    # data directory (relative to current file directory)
    data_directory = "/".join(os.path.dirname(__file__).split("/")[:-2])
    # path to input data file
    json_file_path = os.path.join(data_directory, "data/" + str(filename))
    # load data
    with open(json_file_path) as ff:
        dict_o = json__load(ff)
    ff.close()
    return dict_o["RESULTS"]


def tool_read_netcdf(file_i, variable_i):
    """
    Read neCDF file
    
    Inputs:
    -------
    :param file_i: str
        Name of the file to open
    :param variable_i: str
        Name of the variable to read in the file
    
    Outputs:
    --------
    :return array: array_like
    :return metadata: dict
        Dictionary with one level [metadata], filled with a string, metadata keys are: 'method', 'name_long',
        'name_short' and 'units'
    :return dataset: str
        Name of the dataset, as specified in the file
    :return member: str
        Name of the member, as specified in the file
    """
    # open files
    array = open_dataset(file_i, decode_times=False)[variable_i]
    # read metadata
    metadata = dict()
    for k in ["diagnostic_long_name", "diagnostic_short_name", "method", "units"]:
        att = array.attrs[k]
        if k == "diagnostic_short_name":
            att = att.replace("AVE", r"$\bar{x}$").replace("SKE", "g$_1$").replace("STD", r"$\sigma$")
            att = att.replace("VAR", r"$\sigma^2$").replace("n*", "n$^{*}$")
        else:
            att = att.replace("degC", "$^\circ$C").replace("C2", "C$^2$")
            att = att.replace("mm/day", "mm.day$^{-1}$").replace("mm2/day2", "mm$^{2}$.day$^{-2}$")
            att = att.replace("1e-3", "10$^{-3}$").replace("1e-6", "10$^{-6}$")
            att = att.replace("N/m2", "Pa").replace("N2/m4", "Pa$^{2}$")
            att = att.replace("W/m2", "W.m$^{-2}$").replace("W2/m4", "W$^{2}$.m$^{-4}$")
            for ii in range(-10, 11):
                att = att.replace("**" + str(ii), "$^{" + str(ii) + "}$")
        # output attribute name
        name_o = "name_long" if k == "diagnostic_long_name" else ("name_short" if k == "diagnostic_short_name" else k)
        metadata[name_o] = deepcopy(att)
    # read details about the data
    _, dataset, _, member = array.attrs["dataset"].split(" ")[:4]
    # read variable
    return array, metadata, dataset, member


def tool_sort_members(dataset: str, list_members: list) -> list:
    """
    Sort members

    Inputs:
    -------
    :param dataset: str
        Dataset name; e.g., dataset = 'ACCESS-CM2'
    :param list_members: list
        List of members; e.g., list_members = ['r10i1p1f1', 'r1i1p1f1', 'r20i1p1f1', 'r2i1p1f1']

    Output:
    -------
    :return list_o: list
        Sorted list of members; e.g., list_o = ['r1i1p1f1', 'r2i1p1f1', 'r10i1p1f1', 'r20i1p1f1']
    """
    # check input
    error = list()
    check_type(dataset, "dataset", str, error)
    check_type(list_members, "list_members", list, error)
    print_fail(inspect__stack(), "\n".join(k for k in error))
    # sort members
    list_o = deepcopy(list_members)
    if dataset == "MPI-ESM" and len(list_members) > 1:
        list_o = sorted(list_members, key=str.casefold)
    elif len(list_members) > 1:
        # pad every variant-ID with 6 zeros
        list_t = list()
        for k in list_members:
            # realisation (i.e. ensemble member)
            rr = str(k.split("i")[0].replace("r", "")).zfill(6)
            # initialisation method
            ii = str(k.split("i")[1].split("p")[0]).zfill(6)
            # physics
            pp = str(k.split("p")[1].split("f")[0]).zfill(6)
            # forcing
            if "f" in k:
                ff = "f" + str(k.split("f")[1]).zfill(6)
            else:
                ff = ""
            # save new member name
            list_t.append("r" + str(rr) + "i" + str(ii) + "p" + str(pp) + str(ff))
        # sort padded member names
        list_t = sorted(list_t, key=str.casefold)
        # remove pads
        list_o = list()
        for k in list_t:
            tmp = deepcopy(k)
            while "r0" in tmp:
                tmp = tmp.replace("r0", "r")
            while "i0" in tmp:
                tmp = tmp.replace("i0", "i")
            while "p0" in tmp:
                tmp = tmp.replace("p0", "p")
            while "f0" in tmp:
                tmp = tmp.replace("f0", "f")
            list_o.append(tmp)
    return list_o


def tool_tuple_for_dict(tuple_of_keys: tuple, tuple_of_last_key: tuple) -> (tuple, tuple):
    """
    Remove keys that reached the end of the list

    Inputs:
    -------
    :param tuple_of_keys: tuple
        Keys for nested dictionary
    :param tuple_of_last_key: tuple
        Keys of the last key of each nested level
    
    Outputs:
    --------
    :return tuple_of_keys: tuple
        Keys for nested dictionary, with last key(s) removed
    :param tuple_of_last_key: tuple
        Keys of the last key of each nested level, with last key(s) removed
    """
    # reverse the order of the tuple_of_last_key
    list_r = list(reversed(tuple_of_last_key))
    # check if the last key of a level has been reached, if yes, remove this level from the tuples
    for k in list_r:
        if tuple_of_keys[-1] == k:
            tuple_of_keys = tuple_of_keys[:-1]
            tuple_of_last_key = tuple_of_last_key[:-1]
    # remove last item in both tuples as it has been saved in the output dictionary
    tuple_of_keys = tuple_of_keys[:-1]
    tuple_of_last_key = tuple_of_last_key[:-1]
    return tuple_of_keys, tuple_of_last_key
# ---------------------------------------------------------------------------------------------------------------------#
