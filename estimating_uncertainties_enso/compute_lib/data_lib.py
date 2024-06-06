# -*- coding:UTF-8 -*-
# ---------------------------------------------------------------------------------------------------------------------#
# Functions to read and organize input data for the paper about estimating_uncertainties_in_simulated_ENSO submitted to
# JAMES
# ---------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------#
# Import packages
# ---------------------------------------------------#
# basic python package
from copy import deepcopy
from glob import iglob as glob__iglob
from inspect import stack as inspect__stack
import os
# estimating_uncertainties_enso package
from . check_lib import check_interval, check_type, print_fail
from . stat_lib import stat_compute_statistic
from . tool_lib import tool_put_in_dict, tool_read_json, tool_read_netcdf, tool_sort_members
# ---------------------------------------------------#


# ---------------------------------------------------------------------------------------------------------------------#
# Functions
# ---------------------------------------------------------------------------------------------------------------------#
def data_create_mme(dict_i: dict, project: str, data_mme_use_all_smiles: bool, data_mme_use_smile_mean: bool) -> dict:
    """
    Create multimodel ensemble

    Inputs:
    -------
    :param dict_i: dict
        Dictionary with three nested levels [experiment, dataset, epoch], filled with a list of floats;
        or four nested levels [experiment, dataset, epoch, member], filled with a float
    :param project: str
        Project name; e.g., project = 'cmip6'
    :param data_mme_use_all_smiles: bool
        True to use all smiles for the multimodel ensemble, not only the first smile of each model;
        e.g., mme_use_all_smiles = True
    :param data_mme_use_smile_mean: bool
        True to use smile means for the multimodel ensemble, not the first member of each smile;
        e.g., mme_use_smile_mean = False

    Output:
    -------
    :return dict_o: dict
        Dictionary with three nested levels [experiment, dataset, epoch], filled with a list of floats;
        or four nested levels [experiment, dataset, epoch, member], filled with a float
        with the multimodel ensemble in the dataset level
    """
    # check input
    error = list()
    check_type(dict_i, "dict_i", dict, error)
    check_type(project, "project", str, error)
    check_type(data_mme_use_all_smiles, "data_mme_use_all_smiles", bool, error)
    check_type(data_mme_use_smile_mean, "data_mme_use_smile_mean", bool, error)
    print_fail(inspect__stack(), "\n".join(k for k in error))
    # create mme
    dict_o = deepcopy(dict_i)
    for exp in list(dict_i.keys()):  # loop on experiments
        # list datasets
        list_datasets = sorted(list(dict_i[exp].keys()), key=str.casefold)
        if data_mme_use_all_smiles is False:
            list_datasets = data_one_smile_per_model(list_datasets)
        for dat in list_datasets:  # loop on datasets
            for epo in list(dict_i[exp][dat].keys()):  # loop on epochs
                # get value for each member
                list_of_values = dict_i[exp][dat][epo]
                if isinstance(list_of_values, dict) is True:
                    # list members
                    list_members = tool_sort_members(dat, list(list_of_values.keys()))
                    # put all members in a list
                    list_of_values = [list_of_values[mem] for mem in list_members]
                # compute ensemble mean or select the first member
                if exp == "piControl" or data_mme_use_smile_mean is True:
                    value = stat_compute_statistic(list_of_values, "mea")
                else:
                    value = list_of_values[0]
                # save value
                if isinstance(list_of_values, dict) is True:
                    dict_o = tool_put_in_dict(dict_o, [value], exp, "MME--" + str(project).upper(), epo, dat)
                else:
                    dict_o = tool_put_in_dict(dict_o, [value], exp, "MME--" + str(project).upper(), epo)
    return dict_o


def data_one_smile_per_model(list_datasets) -> list:
    """
    Keep only one smile per model

    Input:
    ------
    :param list_datasets: list
        Dataset names; e.g., list_datasets = ['CanESM5_p1', 'CanESM5_p2']

    Output:
    -------
    :return list_o: list
        Dataset names with only one smile per model; e.g., list_o = ['CanESM5_p1']
    """
    # check input
    error = list()
    check_type(list_datasets, "list_datasets", list, error)
    print_fail(inspect__stack(), "\n".join(k for k in error))
    # delete extra smiles in the list
    list_o = deepcopy(list_datasets)
    # list models that have multiple smiles
    # if multiple ensemble are available, '_' is between the model name and the ensemble name, e.g., 'CanESM5_p1'
    dataset_with_multiple_smile = list(set([k.split("_")[0] for k in list_datasets if "_" in k]))
    for k1 in dataset_with_multiple_smile:  # loop on models with multiple smiles
        # list smiles of given model
        smiles = sorted([k2 for k2 in list_datasets if str(k1) + "_" in k2], key=str.casefold)
        # remove all but the first smiles
        for k2 in smiles[1:]:
            while k2 in list_o:
                list_o.remove(k2)
    return list_o


def data_organize_json(data_diagnostics: list, data_epoch_lengths: list, data_projects: list, data_experiments: list,
                       data_mme_create: bool = False, data_mme_use_all_smiles: bool = True,
                       data_mme_use_smile_mean: bool = False, data_filename: str = None,
                       data_observations_desired: dict = None, data_smile_minimum_size: int = 1,
                       data_smile_rejected: list = None, data_smile_require_all_experiments: bool = False,
                       members_as_list: bool = True) -> (dict, dict):
    """
    Read json dictionary and select values

    Inputs:
    -------
    :param data_diagnostics: list
        Diagnostic names; e.g., data_diagnostics = ['var_pr_ano_nin3', 'var_ts_ano_nin3']
    :param data_epoch_lengths: list
        Epoch length names; e.g., data_epoch_lengths = ['030_year_epoch', '150_year_epoch']
    :param data_filename: str
        json file name to read
    :param data_projects: list
        Project names; e.g., data_projects = ['cmip6', 'observations']
    :param data_experiments: list
        Experiment names; e.g., data_experiments = ['historical', 'piControl']
    :param data_mme_create: bool, optional
        True to create the multimodel ensemble; e.g., data_mme_create = False
        Default is False (multimodel ensemble not created)
    :param data_mme_use_all_smiles: bool, optional
        True to use all smiles for the multimodel ensemble, not only the first smile of each model;
        e.g., data_mme_use_all_smiles = True
        Default is True (all smiles for the multimodel ensemble are used)
    :param data_mme_use_smile_mean: bool, optional
        True to use smile means for the multimodel ensemble, not the first member of each smile;
        e.g., data_mme_use_smile_mean = False
        Default is False (the first member of each smile is used)
    :param data_observations_desired: dict, optional
        Read only desired observational datasets for each diagnostic;
        e.g., data_observations_desired = {'var_pr_ano_nin3': ['CMAP'], 'var_ts_ano_nin3': ['OISSTv2']}
        Default is None (all observational datasets kept)
    :param data_smile_minimum_size: int, optional
        Minimum number of members (epochs for piControl) required to keep a SMILE; e.g., data_smile_minimum_size = 10
        Default is 1 (all SMILEs are kept)
    :param data_smile_rejected: list, optional
        Reject given SMILEs; e.g., data_smile_rejected = ['KACE-1-0-G']
        Default is None (all SMILEs are kept)
    :param data_smile_require_all_experiments: bool, optional
        True to keep SMILEs for which all experiments are available (smile_minimum_size threshold must be met for all
        experiments); e.g., data_smile_require_all_experiments = True
        Default is False (all SMILEs are kept)
    :param members_as_list: bool, optional
        True to put members (epochs for piControl) in a list instead of a dictionary for a given epoch;
        e.g., members_as_list = True

    Outputs:
    --------
    :return dict_diagnostics: dict
        If members_as_list is True, dictionary with six nested levels
        [diagnostic, epoch_length, project, experiment, dataset, epoch], filled with a list of floats
        If members_as_list is False, dictionary with seven nested levels
        [diagnostic, epoch_length, project, experiment, dataset, epoch, member], filled with a float
    :return dict_metadata: dict
        Dictionary with two nested levels [diagnostic, metadata], filled with a string, metadata keys are: 'method',
        'name_long', 'name_short' and 'units'
    """
    # check input
    error = list()
    if data_observations_desired is None:
        data_observations_desired = {}
    if data_smile_rejected is None:
        data_smile_rejected = []
    check_type(data_diagnostics, "data_diagnostics", list, error)
    check_type(data_epoch_lengths, "data_epoch_lengths", list, error)
    check_type(data_experiments, "data_experiments", list, error)
    check_type(data_mme_create, "data_mme_create", bool, error)
    check_type(data_observations_desired, "data_observations_desired", dict, error)
    check_interval(data_smile_minimum_size, "data_smile_minimum_size", int, [0, 100], error)
    check_type(data_smile_rejected, "data_smile_rejected", list, error)
    check_type(data_smile_require_all_experiments, "data_smile_require_all_experiments", bool, error)
    check_type(members_as_list, "members_as_list", bool, error)
    print_fail(inspect__stack(), "\n".join(k for k in error))
    # read input json file
    dict_i = tool_read_json(filename=data_filename)
    # output metadata and value dictionaries
    dict_diagnostics, dict_metadata = {}, {}
    # list desired diagnostics that are available
    list_dia = [k for k in data_diagnostics if k in list(dict_i.keys())]
    for dia in list_dia:  # loop on diagnostics
        # list projects
        list_pro = [k for k in list(dict_i[dia]["diagnostic"]["value"].keys()) if k in data_projects]
        for pro in list_pro:  # loop on projects
            # list datasets
            list_dat = list(dict_i[dia]["diagnostic"]["value"][pro].keys())
            # select datasets
            if pro != "observations" and len(data_smile_rejected) > 0:
                list_dat = list(set(list_dat) - set(data_smile_rejected))
            elif pro == "observations" and dia in list(data_observations_desired.keys()):
                # list desired observational datasets that are available
                list_dat = [k for k in list_dat if k in data_observations_desired[dia]]
            for dat in list_dat:  # loop on datasets
                # temporary dictionary
                dict_t = dict_i[dia]["diagnostic"]["value"][pro][dat]
                # list desired experiments that are available
                list_exp = [k for k in list(dict_t.keys()) if k in data_experiments]
                for exp in list_exp:  # loop on experiments
                    # list members
                    list_mem = tool_sort_members(dat, list(dict_t[exp].keys()))
                    for mem in list_mem:  # loop on members
                        # list desired epoch lengths that are available
                        list_dur = [k for k in list(dict_t[exp][mem].keys()) if k in data_epoch_lengths]
                        for dur in list_dur:  # loop on epoch lengths
                            # list epochs
                            list_epo = sorted(list(dict_t[exp][mem][dur].keys()), key=str.casefold)
                            if exp == "piControl" and dat == "HadGEM3-GC31-LL":
                                list_epo = [k for k in list_epo if int(k[1:]) > int(list_epo[0][1:]) + 649]
                            for epo in list_epo:  # loop on epochs
                                k1, k2 = deepcopy(epo), deepcopy(mem)
                                if exp == "piControl":
                                    k1, k2 = "y0001", deepcopy(epo)
                                    if members_as_list is False and mem != list_mem[0] and \
                                            dia in list(dict_diagnostics.keys()) and \
                                            dur in list(dict_diagnostics[dia].keys()) and \
                                            pro in list(dict_diagnostics[dia][dur].keys()) and \
                                            exp in list(dict_diagnostics[dia][dur][pro].keys()) and \
                                            dat in list(dict_diagnostics[dia][dur][pro][exp].keys()) and \
                                            k1 in list(dict_diagnostics[dia][dur][pro][exp][dat].keys()):
                                        # last epoch saved
                                        last = sorted(list(dict_diagnostics[dia][dur][pro][exp][dat][k1].keys()),
                                                      key=str.casefold)[-1]
                                        # add 1000 years to last millennia saved separate new member
                                        k2 = "y" + str(1000 + int(last[1:]) // 1000 + int(k2[1:])).zfill(4)
                                # save value
                                if members_as_list is True:
                                    dict_diagnostics = tool_put_in_dict(
                                        dict_diagnostics, [dict_t[exp][mem][dur][epo]], dia, dur, pro, exp, dat, k1)
                                else:
                                    dict_diagnostics = tool_put_in_dict(
                                        dict_diagnostics, dict_t[exp][mem][dur][epo], dia, dur, pro, exp, dat, k1, k2)
            # create MME if desired
            if pro != "observations" and dia in list(dict_diagnostics.keys()):
                # list epoch lengths
                list_dur = [
                    k for k in list(dict_diagnostics[dia].keys()) if pro in list(dict_diagnostics[dia][k].keys())]
                for dur in list_dur:
                    if data_mme_create is True:
                        # create MME if desired
                        dict_diagnostics[dia][dur][pro] = data_create_mme(
                            dict_diagnostics[dia][dur][pro], pro, data_mme_use_all_smiles, data_mme_use_smile_mean)
                    if data_smile_minimum_size > 1:
                        # delete smiles with few members
                        for exp in list(dict_diagnostics[dia][dur][pro].keys()):
                            for dat in list(dict_diagnostics[dia][dur][pro][exp].keys()):
                                # temporary dictionary
                                dict_t = dict_diagnostics[dia][dur][pro][exp][dat]
                                # first epoch
                                k = sorted(list(dict_t.keys()), key=str.casefold)[0]
                                if (members_as_list is True and len(dict_t[k]) < data_smile_minimum_size) or (
                                        members_as_list is False and
                                        len(list(dict_t[k].keys())) < data_smile_minimum_size):
                                    # number of members too small: delete dataset
                                    del dict_diagnostics[dia][dur][pro][exp][dat]
                if data_smile_require_all_experiments is True:
                    # keep SMILE only if all experiments are available
                    # list available SMILEs
                    list_dat = list(set([dat for dur in list_dur for exp in list(dict_diagnostics[dia][dur][pro].keys())
                                         for dat in list(dict_diagnostics[dia][dur][pro][exp].keys())]))
                    for dat in list_dat:
                        # list experiments for given dataset
                        list_exp = list(set([exp for dur in list_dur
                                             for exp in list(dict_diagnostics[dia][dur][pro].keys())
                                             if dat in list(dict_diagnostics[dia][dur][pro][exp].keys())]))
                        # check the number of experiments
                        if len(list(set(data_experiments) - set(list_exp))) > 0:
                            for dur in list_dur:
                                for exp in list(dict_diagnostics[dia][dur][pro].keys()):
                                    if dat in list(dict_diagnostics[dia][dur][pro][exp].keys()):
                                        del dict_diagnostics[dia][dur][pro][exp][dat]
                # check if all data has been deleted
                for dur in list_dur:
                    for exp in list(dict_diagnostics[dia][dur][pro].keys()):
                        if len(list(dict_diagnostics[dia][dur][pro][exp].keys())) == 0:
                            del dict_diagnostics[dia][dur][pro][exp]
                    if len(list(dict_diagnostics[dia][dur][pro].keys())) == 0:
                        del dict_diagnostics[dia][dur][pro]
        # read metadata
        method = dict_i[dia]["metadata"]["method"]
        name_long = dict_i[dia]["metadata"]["diagnostic_long_name"]
        name_short = dict_i[dia]["metadata"]["diagnostic_short_name"].replace("AVE", r"$\bar{x}$")
        name_short = name_short.replace("SKE", "g$_1$").replace("STD", r"$\sigma$").replace("VAR", r"$\sigma^2$")
        name_short = name_short.replace("n*", "n$^{*}$")
        unit = dict_i[dia]["metadata"]["units"].replace("degC", "$^\circ$C").replace("1e", "10")
        for ii in range(-10, 11):
            unit = unit.replace("**" + str(ii), "$^{" + str(ii) + "}$")
        dict_metadata[dia] = {"method": method, "name_long": name_long, "name_short": name_short, "units": unit}
    # check if empty dictionary level is empty
    for dia in list(dict_diagnostics.keys()):
        for dur in list(dict_diagnostics[dia].keys()):
            for pro in list(dict_diagnostics[dia][dur].keys()):
                for exp in list(dict_diagnostics[dia][dur][pro].keys()):
                    for dat in list(dict_diagnostics[dia][dur][pro][exp].keys()):
                        if len(list(dict_diagnostics[dia][dur][pro][exp][dat].keys())) == 0:
                            del dict_diagnostics[dia][dur][pro][exp][dat]
                    if len(list(dict_diagnostics[dia][dur][pro][exp].keys())) == 0:
                        del dict_diagnostics[dia][dur][pro][exp]
                if len(list(dict_diagnostics[dia][dur][pro].keys())) == 0:
                    del dict_diagnostics[dia][dur][pro]
            if len(list(dict_diagnostics[dia][dur].keys())) == 0:
                del dict_diagnostics[dia][dur]
        if len(list(dict_diagnostics[dia].keys())) == 0:
            del dict_diagnostics[dia]
            del dict_metadata[dia]
    return dict_diagnostics, dict_metadata


def data_organize_netcdf(data_diagnostics: list, data_projects: list, data_experiments: list,
                         data_observations_desired: dict = None, members_as_list: bool = True) -> (dict, dict):
    """
    Read json dictionary and select values

    Inputs:
    -------
    :param data_diagnostics: list
        Diagnostic names; e.g., data_diagnostics = ['var_pr_ano_nin3', 'var_ts_ano_nin3']
    :param data_projects: list
        Project names; e.g., data_projects = ['cmip6', 'observations']
    :param data_experiments: list
        Experiment names; e.g., data_experiments = ['historical', 'piControl']
    :param data_observations_desired: dict, optional
        Read only desired observational datasets for each diagnostic;
        e.g., data_observations_desired = {'var_pr_ano_nin3': ['CMAP'], 'var_ts_ano_nin3': ['OISSTv2']}
        Default is None (read all observational datasets)
    :param members_as_list: bool, optional
        True to put members (epochs for piControl) in a list instead of a dictionary for a given epoch;
        e.g., members_as_list = True

    Outputs:
    --------
    :return dict_diagnostics: dict
        If members_as_list is True, dictionary with four nested levels [diagnostic, project, experiment, dataset],
        filled with a list of DataArray
        If members_as_list is False, dictionary with five nested levels
        [diagnostic, project, experiment, dataset, member], filled with a DataArray
    :return dict_metadata: dict
        Dictionary with two nested levels [diagnostic, metadata], filled with a string, metadata keys are: 'method',
        'name_long', 'name_short' and 'units'
    """
    # check input
    error = list()
    if data_observations_desired is None:
        data_observations_desired = {}
    check_type(data_diagnostics, "data_diagnostics", list, error)
    check_type(data_experiments, "data_experiments", list, error)
    check_type(data_observations_desired, "data_observations_desired", dict, error)
    check_type(members_as_list, "members_as_list", bool, error)
    print_fail(inspect__stack(), "\n".join(k for k in error))
    # plot directory (relative to current file directory)
    data_directory = "/".join(os.path.dirname(__file__).split("/")[:-2]) + "/data"
    # output metadata and value dictionaries
    dict_diagnostics, dict_metadata = {}, {}
    for dia in data_diagnostics:  # loop on diagnostics
        for pro in data_projects:  # loop on projects
            # list datasets
            list_dat = ["*"]
            # select datasets
            if pro == "observations" and dia in list(data_observations_desired.keys()):
                # list desired observational datasets that are available
                list_dat = data_observations_desired[dia]
            for dat in list_dat:  # loop on datasets
                for exp in data_experiments:  # loop on experiments
                    # path and file name pattern
                    list_files = list(glob__iglob(os.path.join(
                        data_directory, str(dia) + "_" + str(pro) + "_" + str(dat) + "_" + str(exp) + "_*.nc")))
                    for fil in list_files:  # loop on files
                        # read given netCDF file
                        array, metadata, dataset, member = tool_read_netcdf(fil, dia)
                        # save value
                        if members_as_list is True:
                            dict_diagnostics = tool_put_in_dict(dict_diagnostics, [array], dia, pro, exp, dataset)
                        else:
                            dict_diagnostics = tool_put_in_dict(dict_diagnostics, array, dia, pro, exp, dataset, member)
                        if dia not in list(dict_metadata.keys()):
                            dict_metadata[dia] = metadata
    return dict_diagnostics, dict_metadata
# ---------------------------------------------------------------------------------------------------------------------#
