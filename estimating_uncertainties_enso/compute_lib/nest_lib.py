# -*- coding:UTF-8 -*-
# ---------------------------------------------------------------------------------------------------------------------#
# Functions to handle nested dictionaries for the paper about estimating_uncertainties_in_simulated_ENSO submitted to
# JAMES
# ---------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------#
# Import packages
# ---------------------------------------------------#
# basic python package
from copy import deepcopy
from inspect import stack as inspect__stack
# numpy
from numpy import array as numpy__array
from numpy import ndarray as numpy__ndarray
# scipy
from scipy.stats import scoreatpercentile as scipy__stats__scoreatpercentile
# estimating_uncertainties_enso package
from . check_lib import check_list, check_type, print_fail
from . stat_lib import stat_res_based_on_obs, stat_res_bootstrap, stat_res_theory, stat_compute_statistic,\
    stat_smooth_triangle, stat_uncertainty_select_and_compute
from . tool_lib import tool_put_in_dict, tool_tuple_for_dict
# ---------------------------------------------------#


# ---------------------------------------------------------------------------------------------------------------------#
# Functions
# ---------------------------------------------------------------------------------------------------------------------#
def nest_compute_res(dict_i, dict_threshold: dict, res_maximum: int, uncertainty_confidence_interval: float,
                     uncertainty_distribution: str, uncertainty_combinations: int, uncertainty_resamples: int,
                     uncertainty_theory: bool, dict_o: dict = None, list_k: tuple = None,
                     list_k_last: tuple = None) -> (dict, tuple, tuple):
    """
    Compute the uncertainty of the sample mean

    Inputs:
    -------
    :param dict_i: dict
        Dictionary with six nested levels [diagnostic, epoch_length, project, experiment, dataset, epoch], filled with a
        list of values
    :param dict_threshold: dict
        Dictionary with seven nested levels [diagnostic, epoch_length, project, experiment, dataset, epoch, method],
        filled with a value or a list of values
    :param res_maximum: int
        Maximum value for the required ensemble size; e.g., maximum_res = 100
    :param uncertainty_confidence_interval: float
        Confidence interval used to compute the uncertainty; e.g., uncertainty_confidence_interval = 95
    :param uncertainty_distribution: str
        Name of a distribution; e.g., distribution = 'normal'
        Two distributions are defined: 'normal', 'student'
        Used only if uncertainty_theory is True
    :param uncertainty_combinations: int
        Maximum number of combinations to compute (theoretical uncertainty); e.g., uncertainty_combinations = 1000
    :param uncertainty_resamples: int
        Number of resamples to compute (boostrap uncertainty); e.g., uncertainty_resamples = 1000
    :param uncertainty_theory: bool
        True to compute the theoretical uncertainty (using the standard error; e.g., Chapter 5 p. 92 of von Storch and
        Zwiers (1999; https://doi.org/10.1017/CBO9780511612336), else compute the uncertainty using a boostrap;
        e.g., uncertainty_theory = True
    :param dict_o: dict or None, optional
        Dictionary in which output values will be stored
    :param list_k: list or None, optional
        List of keys, in order, for the output nested dictionary
    :param list_k_last: list or None, optional
        List of the last key of each nested level, in order, to keep track of the position within the input nested
        dictionary

    Outputs:
    --------
    :return dict_o: dict
        Dictionary with seven nested levels [diagnostic, epoch_length, project, experiment, dataset, epoch, method],
        filled with the required ensemble size (or a list of required ensemble sizes)
    :return list_k: tuple
    :return list_k_last: tuple
    """
    # check input
    error = list()
    if dict_o is None:
        dict_o = {}
    if list_k is None:
        list_k = ()
    if list_k_last is None:
        list_k_last = ()
    check_type(dict_i, "dict_i", (dict, float, int, list, numpy__ndarray), error)
    check_type(dict_threshold, "dict_threshold", dict, error)
    check_type(dict_o, "dict_o", dict, error)
    check_type(list_k, "list_k", tuple, error)
    check_type(list_k_last, "list_k_last", tuple, error)
    print_fail(inspect__stack(), "\n".join(k for k in error))
    # loop through nested levels
    if isinstance(dict_i, dict) is True:
        list_keys = sorted(list(dict_i.keys()), key=str.casefold)
        for k in list_keys:
            dict_o, list_k, list_k_last = nest_compute_res(
                dict_i[k], dict_threshold[k], res_maximum, uncertainty_confidence_interval, uncertainty_distribution,
                uncertainty_combinations, uncertainty_resamples, uncertainty_theory, dict_o=dict_o,
                list_k=list_k + (k,), list_k_last=list_k_last + (list_keys[-1],))
    else:
        for criteria in list(dict_threshold.keys()):
            for threshold in list(dict_threshold[criteria].keys()):
                uncertainty_threshold = dict_threshold[criteria][threshold]
                # compute RES
                if criteria == "obs":
                    res = stat_res_based_on_obs(
                        dict_i, uncertainty_threshold, res_maximum, uncertainty_confidence_interval,
                        uncertainty_distribution, uncertainty_combinations, uncertainty_resamples, uncertainty_theory)
                else:
                    if uncertainty_theory is True:
                        res = stat_res_theory(
                            dict_i, res_maximum, uncertainty_confidence_interval, uncertainty_threshold)
                    else:
                        res = stat_res_bootstrap(dict_i, res_maximum, uncertainty_confidence_interval,
                                                 uncertainty_resamples, uncertainty_threshold)
                if res is not None:
                    # save values
                    list_f = list_k + (criteria, threshold)
                    dict_o = tool_put_in_dict(dict_o, res, *list_f)
        # remove relevant keys from the tuples of keys
        list_k, list_k_last = tool_tuple_for_dict(list_k, list_k_last)
    return dict_o, list_k, list_k_last


def nest_compute_statistic(dict_i, statistic: str, dict_o: dict = None, list_k: tuple = None,
                           list_k_last: tuple = None) -> (dict, tuple, tuple):
    """
    Compute given statistic on arrays within the nested dictionary

    Inputs:
    -------
    :param dict_i: dict
        Dictionary with six nested levels [diagnostic, epoch_length, project, experiment, dataset, epoch], filled with a
        list of values
    :param statistic: str
        Name of a statistic; e.g., statistic = 'mea'
        Four statistics are defined: 'mea', 'std', 'var', 'var_to_mea2'
    :param dict_o: dict or None, optional
        Dictionary in which output values will be stored
    :param list_k: list or None, optional
        List of keys, in order, for the output nested dictionary
    :param list_k_last: list or None, optional
        List of the last key of each nested level, in order, to keep track of the position within the input nested
        dictionary

    Outputs:
    --------
    :return dict_o: dict
        Dictionary with seven nested levels [diagnostic, epoch_length, project, experiment, dataset, epoch], filled the
        desired statistical value
    :return list_k: tuple
    :return list_k_last: tuple
    """
    # check input
    error = list()
    if dict_o is None:
        dict_o = {}
    if list_k is None:
        list_k = ()
    if list_k_last is None:
        list_k_last = ()
    check_type(dict_i, "dict_i", (dict, float, int, list, numpy__ndarray), error)
    check_type(dict_o, "dict_o", dict, error)
    check_type(list_k, "list_k", tuple, error)
    check_type(list_k_last, "list_k_last", tuple, error)
    print_fail(inspect__stack(), "\n".join(k for k in error))
    # loop through nested levels
    if isinstance(dict_i, dict) is True:
        list_keys = sorted(list(dict_i.keys()), key=str.casefold)
        for k in list_keys:
            dict_o, list_k, list_k_last = nest_compute_statistic(
                dict_i[k], statistic, dict_o=dict_o, list_k=list_k + (k,), list_k_last=list_k_last + (list_keys[-1],))
    else:
        # compute statistic
        value = stat_compute_statistic(dict_i, statistic)
        # save values
        dict_o = tool_put_in_dict(dict_o, value, *list_k)
        # remove relevant keys from the tuples of keys
        list_k, list_k_last = tool_tuple_for_dict(list_k, list_k_last)
    return dict_o, list_k, list_k_last


def nest_compute_uncertainty(dict_i, uncertainty_confidence_interval: float, uncertainty_distribution: str,
                             uncertainty_relative: bool, uncertainty_combinations: int, uncertainty_resamples: int,
                             uncertainty_theory: bool, uncertainty_sample_sizes: list = None, dict_o: dict = None,
                             list_k: tuple = None, list_k_last: tuple = None) -> (dict, tuple, tuple):
    """
    Compute the uncertainty of the sample mean

    Inputs:
    -------
    :param dict_i: dict
        Dictionary with six nested levels [diagnostic, epoch_length, project, experiment, dataset, epoch], filled with a
        list of values
    :param uncertainty_confidence_interval: float
        Confidence interval used to compute the uncertainty; e.g., uncertainty_confidence_interval = 95
    :param uncertainty_distribution: str
        Name of a distribution; e.g., distribution = 'normal'
        Two distributions are defined: 'normal', 'student'
        Used only if uncertainty_theory is True
    :param uncertainty_relative: bool
        True to compute the uncertainty relative to the sample mean, else the absolute uncertainty is computed;
        e.g., uncertainty_absolute = True
    :param uncertainty_combinations: int
        Maximum number of combinations to compute (theoretical uncertainty); e.g., uncertainty_combinations = 1000
    :param uncertainty_resamples: int
        Number of resamples to compute (boostrap uncertainty); e.g., uncertainty_resamples = 1000
    :param uncertainty_theory: bool
        True to compute the theoretical uncertainty (using the standard error; e.g., Chapter 5 p. 92 of von Storch and
        Zwiers (1999; https://doi.org/10.1017/CBO9780511612336), else compute the uncertainty using a boostrap;
        e.g., uncertainty_theory = True
    :param uncertainty_sample_sizes: list, optional
        Sample sizes used to compute the uncertainty (using resamples); e.g., uncertainty_sample_sizes = [10, 20]
        Default is None (the sample size will be the SMILE size)
    :param dict_o: dict or None, optional
        Dictionary in which output values will be stored
    :param list_k: tuple or None, optional
        List of keys, in order, for the output nested dictionary
    :param list_k_last: tuple or None, optional
        List of the last key of each nested level, in order, to keep track of the position within the input nested
        dictionary

    Outputs:
    --------
    :return dict_o: dict
        Dictionary with seven nested levels [diagnostic, epoch_length, project, experiment, dataset, epoch, sample_size]
        filled with the uncertainty of the sample mean
    :return list_k: tuple
    :return list_k_last: tuple
    """
    # check input
    error = list()
    if uncertainty_sample_sizes is None:
        uncertainty_sample_sizes = []
    if dict_o is None:
        dict_o = {}
    if list_k is None:
        list_k = ()
    if list_k_last is None:
        list_k_last = ()
    check_type(dict_i, "dict_i", (dict, float, int, list, numpy__ndarray), error)
    check_type(uncertainty_relative, "uncertainty_relative", bool, error)
    check_type(uncertainty_sample_sizes, "uncertainty_sample_sizes", list, error)
    check_type(dict_o, "dict_o", dict, error)
    check_type(list_k, "list_k", tuple, error)
    check_type(list_k_last, "list_k_last", tuple, error)
    print_fail(inspect__stack(), "\n".join(k for k in error))
    # loop through nested levels
    if isinstance(dict_i, dict) is True:
        list_keys = sorted(list(dict_i.keys()), key=str.casefold)
        for k in list_keys:
            dict_o, list_k, list_k_last = nest_compute_uncertainty(
                dict_i[k], uncertainty_confidence_interval, uncertainty_distribution, uncertainty_relative,
                uncertainty_combinations, uncertainty_resamples, uncertainty_theory,
                uncertainty_sample_sizes=uncertainty_sample_sizes, dict_o=dict_o, list_k=list_k + (k,),
                list_k_last=list_k_last + (list_keys[-1],))
    else:
        # list the sample size
        sample_siz = [k for k in uncertainty_sample_sizes if isinstance(k, int) and k < len(dict_i)] + [len(dict_i)]
        for k in sample_siz:
            uncertainty = stat_uncertainty_select_and_compute(
                dict_i, uncertainty_confidence_interval, uncertainty_distribution, uncertainty_relative,
                uncertainty_combinations, uncertainty_resamples, uncertainty_theory, k)
            # save values
            name = str(k).zfill(3) + "_members" if len(uncertainty_sample_sizes) > 0 else "max_members"
            list_f = list_k + (name,)
            dict_o = tool_put_in_dict(dict_o, uncertainty, *list_f)
        # remove relevant keys from the tuples of keys
        list_k, list_k_last = tool_tuple_for_dict(list_k, list_k_last)
    return dict_o, list_k, list_k_last


def nest_compute_uncertainty_hi_vs_pi(dict_i: dict, uncertainty_confidence_interval: float,
                                      uncertainty_distribution: str, uncertainty_relative: bool,
                                      uncertainty_combinations: int, uncertainty_resamples: int,
                                      uncertainty_theory: bool, uncertainty_historical_epoch: str,
                                      reference_experiment: str = "piControl") -> dict:
    """
    Compute the uncertainty of the sample mean

    Inputs:
    -------
    :param dict_i: dict
        Dictionary with six nested levels [diagnostic, epoch_length, project, experiment, dataset, epoch], filled with a
        list of values
    :param uncertainty_confidence_interval: float
        Confidence interval used to compute the uncertainty; e.g., uncertainty_confidence_interval = 95
    :param uncertainty_distribution: str
        Name of a distribution; e.g., distribution = 'normal'
        Two distributions are defined: 'normal', 'student'
        Used only if uncertainty_theory is True
    :param uncertainty_relative: bool
        True to compute the uncertainty relative to the sample mean, else the absolute uncertainty is computed;
        e.g., uncertainty_absolute = True
    :param uncertainty_combinations: int
        Maximum number of combinations to compute (theoretical uncertainty); e.g., uncertainty_combinations = 1000
    :param uncertainty_resamples: int
        Number of resamples to compute (boostrap uncertainty); e.g., uncertainty_resamples = 1000
    :param uncertainty_theory: bool
        True to compute the theoretical uncertainty (using the standard error; e.g., Chapter 5 p. 92 of von Storch and
        Zwiers (1999; https://doi.org/10.1017/CBO9780511612336), else compute the uncertainty using a boostrap;
        e.g., uncertainty_theory = True
    :param uncertainty_historical_epoch: str
        This epoch will be compared to reference_experiment; e.g., uncertainty_historical_epoch = 'averaged'
        Three epoch names are defined: 'averaged' or 'first' or 'last'
        Respectively, the uncertainty computed for i) all epoch and then averaged, ii) the first epoch, iii) the last
        epoch
    :param reference_experiment: str, optional
        The first epoch of this experiment will be used as a reference to which experiments will be compared;
        e.g., reference_experiment = 'piControl'
        Default in 'piControl'

    Output:
    -------
    :return dict_o: dict
        Dictionary with four nested levels [diagnostic, dataset, x-or-y], filled with the values to plot
    """
    # check input
    error = list()
    known_epochs = ["averaged", "first", "last"]
    check_type(dict_i, "dict_i", dict, error)
    check_type(uncertainty_relative, "uncertainty_relative", bool, error)
    check_list(uncertainty_historical_epoch, "uncertainty_historical_epoch", known_epochs, error)
    print_fail(inspect__stack(), "\n".join(k for k in error))
    # compute uncertainty and organize data to plot the correspondence between experiments
    dict_o = {}
    for dia in list(dict_i.keys()):
        for dur in list(dict_i[dia].keys()):
            for pro in list(dict_i[dia][dur].keys()):
                if reference_experiment in list(dict_i[dia][dur][pro].keys()):
                    for dat in list(dict_i[dia][dur][pro][reference_experiment].keys()):
                        # list experiments not reference_experiment for given dataset
                        list_exp = [exp for exp in list(dict_i[dia][dur][pro].keys())
                                    if dat in list(dict_i[dia][dur][pro][exp].keys()) and exp != reference_experiment]
                        if len(list_exp) > 1:
                            error = "there should be only one experiment available\n" + str().ljust(5)
                            error += "diagnostic: %s; epoch length: %s; project: %s; dataset: %s" % (dia, dur, pro, dat)
                            error += "\n" + str().ljust(5) + "experiments: " + str(list_exp)
                            print_fail(inspect__stack(), error)
                        # there is only one experiment (not counting reference_experiment)
                        exp = list_exp[0]
                        # dictionaries
                        dict_ref = dict_i[dia][dur][pro][reference_experiment][dat]
                        dict_exp = dict_i[dia][dur][pro][exp][dat]
                        # list epochs
                        epoch_ref = sorted(list(dict_ref.keys()), key=str.casefold)
                        epoch_exp = sorted(list(dict_exp.keys()), key=str.casefold)
                        if uncertainty_historical_epoch == "first":
                            epoch_exp = [epoch_exp[0]]
                        elif uncertainty_historical_epoch == "last":
                            epoch_exp = [epoch_exp[-1]]
                        # smallest ensemble size between reference and experiment
                        nbr = min(len(dict_ref[epoch_ref[0]]), len(dict_exp[epoch_exp[0]]))
                        # compute uncertainty of the ensemble mean for the reference
                        uncertainty_ref = stat_uncertainty_select_and_compute(
                            dict_ref[epoch_ref[0]], uncertainty_confidence_interval, uncertainty_distribution,
                            uncertainty_relative, uncertainty_combinations, uncertainty_resamples, uncertainty_theory,
                            nbr)
                        # compute uncertainty of the ensemble mean for the experiment
                        uncertainty_exp = []
                        for epo in epoch_exp:
                            # compute uncertainty of the ensemble mean for given epoch
                            tmp = stat_uncertainty_select_and_compute(
                                dict_exp[epo], uncertainty_confidence_interval, uncertainty_distribution,
                                uncertainty_relative, uncertainty_combinations, uncertainty_resamples,
                                uncertainty_theory, nbr)
                            uncertainty_exp.append(tmp)
                        # average across epoch (if experiment_epoch is 'first' or 'last', only the corresponding
                        # epoch was kept)
                        uncertainty_exp = stat_compute_statistic(uncertainty_exp, "mea")
                        # save values
                        dict_o = tool_put_in_dict(dict_o, [uncertainty_ref], dia, dat, "x")
                        dict_o = tool_put_in_dict(dict_o, [uncertainty_exp], dia, dat, "y")
    return dict_o


def nest_define_uncertainty_threshold(dict_i: dict, dict_threshold: dict,
                                      selected_model_experiment: str = None) -> (dict, dict):
    """
    Define the uncertainty thresholds for each case (diagnostic, epoch_length, project, experiment, dataset, epoch,
    method)
    
    Inputs:
    -------
    :param dict_i: dict
        Dictionary with six nested levels [diagnostic, epoch_length, project, experiment, dataset, epoch], filled with a
        list of values
    :param dict_threshold: dict
        Dictionary with three nested levels [diagnostic, method, keys], filled with a value (float | list[float] | str)
        e.g., dict_threshold = {'ave_pr_val_n30e': {'unc': {'uncertainty_relative': True, 'threshold': 5}}}
    :param selected_model_experiment: str
        Experiment selected for model data
        Default is None (all experiments are used)
    
    Outputs:
    --------
    :return dict_model: dict
        Dictionary with six nested levels [diagnostic, epoch_length, project, experiment, dataset, epoch], filled with
        the model data
    :return dict_threshold_updated: dict
        Dictionary with seven nested levels
        [diagnostic, epoch_length, project, experiment, dataset, epoch, method, threshold], filled with the uncertainty
        value to reach
    """
    # check input
    error = list()
    check_type(dict_i, "dict_i", dict, error)
    check_type(dict_threshold, "dict_threshold", dict, error)
    check_type(selected_model_experiment, "selected_model_experiment", (str, type(None)), error)
    print_fail(inspect__stack(), "\n".join(k for k in error))
    # compute uncertainty thresholds
    dict_model, dict_threshold_updated = {}, {}
    for dia in list(dict_i.keys()):
        if dia in list(dict_threshold.keys()):
            for dur in list(dict_i[dia].keys()):
                # remove 'observations' from projects
                list_projects = [k for k in list(dict_i[dia][dur].keys()) if k != "observations"]
                for pro in list_projects:
                    list_experiments = list(dict_i[dia][dur][pro].keys())
                    # keep only the selected experiment
                    if selected_model_experiment is not None:
                        list_experiments = [k for k in list_experiments if k == selected_model_experiment]
                    for exp in list_experiments:
                        # remove the MME from datasets
                        list_datasets = [k for k in list(dict_i[dia][dur][pro][exp].keys()) if k[:5] != "MME--"]
                        for dat in list_datasets:
                            for epo in list(dict_i[dia][dur][pro][exp][dat].keys()):
                                # model array
                                arr = dict_i[dia][dur][pro][exp][dat][epo]
                                # loop on methods which need an uncertainty threshold
                                for method in list(dict_threshold[dia].keys()):
                                    # check method
                                    known_methods = ["mme", "obs", "unc"]
                                    check_list(method, "threshold method", known_methods, error)
                                    print_fail(inspect__stack(), "\n".join(k for k in error))
                                    # threshold
                                    if method in ["mme", "unc"]:
                                        list_threshold = dict_threshold[dia][method]["threshold"]
                                        if isinstance(list_threshold, (float, int)) is True:
                                            list_threshold = [list_threshold]
                                    else:
                                        list_threshold = [1]
                                    # compute coefficient
                                    coefficient = 1
                                    if method == "mme" or (method == "unc" and
                                                           dict_threshold[dia][method]["uncertainty_relative"] is True):
                                        if method == "mme":
                                            # uncertainty relative to a fraction of the MME range
                                            mme = dict_i[dia][dur][pro][exp]["MME--" + str(pro).upper()][epo]
                                            # score at a given percentile
                                            score = scipy__stats__scoreatpercentile(
                                                mme, dict_threshold[dia][method]["range"])
                                            # coefficient is the score difference
                                            coefficient = score[1] - score[0]
                                        else:
                                            # the coefficient is the ensemble mean
                                            coefficient = abs(stat_compute_statistic(arr, "mea")) / 100
                                    elif method == "obs":
                                        # sign of the bias: the threshold is the observed value
                                        # find the observation for given parameters
                                        obs = dict_threshold[dia][method]["reference"]
                                        obs = dict_i[dia][dur]["observations"]["historical"][obs]
                                        # which epoch should be used?
                                        obs_epo = dict_threshold[dia][method]["epoch"]
                                        # check epoch
                                        known_epochs = ["first", "last", "same"]
                                        check_list(obs_epo, "epoch name", known_epochs, error)
                                        print_fail(inspect__stack(), "\n".join(k for k in error))
                                        # select epoch
                                        list_epoch = sorted(list(obs.keys()), key=str.casefold)
                                        if obs_epo == "first":
                                            obs_epo = list_epoch[0]
                                        elif obs_epo == "last":
                                            obs_epo = list_epoch[-1]
                                        else:
                                            obs_epo = deepcopy(epo)
                                        obs = obs[obs_epo]
                                        # the coefficient is the observed value
                                        coefficient = obs[0] if isinstance(obs, list) is True else deepcopy(obs)
                                    # save thresholds and coefficient
                                    for thr in list_threshold:
                                        dict_threshold_updated = tool_put_in_dict(
                                            dict_threshold_updated, thr * coefficient, dia, dur, pro, exp, dat, epo,
                                            method, thr)
                                # save model array
                                dict_model = tool_put_in_dict(dict_model, arr, dia, dur, pro, exp, dat, epo)
    return dict_model, dict_threshold_updated


def nest_examples_of_res_method(dict_i: dict, selected_model: str) -> dict:
    """
    Organize data to plot examples of RES values depending on the method to define it
    
    Inputs:
    -------
    :param dict_i: dict
        Dictionary with seven nested levels [diagnostic, epoch_length, project, experiment, dataset, epoch, method],
        filled with the required ensemble size
    :param selected_model: str
        Model selected to appear as a marker on the plot
    
    Output:
    -------
    :return: dict
        Dictionary with three nested levels [diagnostic, method, boxplot-or-marker], filled with the list of values to
        plot
    """
    dict_o = {}
    for dia in list(dict_i.keys()):
        # list epoch lengths
        list_epoch_lengths = list(dict_i[dia].keys())
        if len(list_epoch_lengths) > 1:
            error = "there should be only one epoch length available\n" + str().ljust(5) + "diagnostic: %s" % dia
            error += "\n" + str().ljust(5) + "epoch lengths: " + str(list_epoch_lengths)
            print_fail(inspect__stack(), error)
        dur = list_epoch_lengths[0]
        for pro in list(dict_i[dia][dur].keys()):
            # list experiments
            list_experiments = list(dict_i[dia][dur][pro].keys())
            if len(list_experiments) > 1:
                error = "there should be only one experiment available\n" + str().ljust(5)
                error += "diagnostic: %s ; epoch length: %s ; project: %s" % (dia, dur, pro)
                error += "\n" + str().ljust(5) + "experiments: " + str(list_experiments)
                print_fail(inspect__stack(), error)
            exp = list_experiments[0]
            # dictionary
            d1 = dict_i[dia][dur][pro][exp]
            # list methods
            list_methods = list(set([method for dat in list(d1.keys()) for epo in list(d1[dat].keys())
                                     for method in list(d1[dat][epo].keys())]))
            for method in list_methods:
                # list thresholds
                list_thresholds = []
                for dat in list(d1.keys()):
                    for epo in list(d1[dat].keys()):
                        if method in list(d1[dat][epo].keys()):
                            for threshold in list(d1[dat][epo][method].keys()):
                                list_thresholds.append(threshold)
                list_thresholds = list(set(list_thresholds))
                if len(list_thresholds) > 1:
                    error = "there should be only one threshold available\n" + str().ljust(5)
                    error += "diagnostic: %s ; epoch length: %s ; project: %s ; experiment: %s" % (dia, dur, pro, exp)
                    error += " ; method: %s" % method
                    error += "\n" + str().ljust(5) + "thresholds: " + str(list_thresholds)
                    print_fail(inspect__stack(), error)
                thr = list_thresholds[0]
                # get values per dataset
                dict_t = {}
                for dat in list(dict_i[dia][dur][pro][exp].keys()):
                    # res values are averaged across epochs (if the default parameters are used, exp = piControl so
                    # there is ony one epoch)
                    list_t = []
                    for epo in list(dict_i[dia][dur][pro][exp][dat].keys()):
                        if method in list(dict_i[dia][dur][pro][exp][dat][epo].keys()):
                            list_t.append(dict_i[dia][dur][pro][exp][dat][epo][method][thr])
                    if len(list_t) > 0:
                        dict_t[dat] = stat_compute_statistic(list_t, "mea")
                if len(list(dict_t.keys())) > 0:
                    # if selected_model is available, save it as marker
                    if selected_model in list(dict_t.keys()):
                        dict_o = tool_put_in_dict(dict_o, dict_t[selected_model], dia, method, "marker")
                    # save the list of values as boxplot
                    dict_o = tool_put_in_dict(dict_o, list(dict_t.values()), dia, method, "boxplot")
    return dict_o


def nest_influence_of_ensemble_size(dict_i: dict, ensemble_size_reference: str) -> dict:
    """
    Organize data to plot the influence of the ensemble size on the uncertainty of the ensemble mean
    
    Inputs:
    -------
    :param dict_i: dict
        Dictionary with seven nested levels [diagnostic, epoch_length, project, experiment, dataset, epoch, sample_size]
        filled with a list of values
    :param ensemble_size_reference: str
        Reference used to compute the influence of ensemble size
        Two references are defined: 'maximum', 'minimum'
        Defines if the 'maximum' or 'minimum' ensemble size is used as a reference to compute the influence of the
        ensemble size
    
    Output:
    -------
    :return: dict
        Dictionary with five nested levels [diagnostic, dataset, experiment, epoch_length, x-or-y], filled with the
        values to plot
    """
    # check input
    error = list()
    known_references = ["maximum", "minimum"]
    check_type(dict_i, "dict_i", dict, error)
    check_list(ensemble_size_reference, "ensemble_size_reference", known_references, error)
    print_fail(inspect__stack(), "\n".join(k for k in error))
    # organize data to plot the influence of ensemble size
    dict_o = {}
    for dia in list(dict_i.keys()):
        for dur in list(dict_i[dia].keys()):
            for pro in list(dict_i[dia][dur].keys()):
                for exp in list(dict_i[dia][dur][pro].keys()):
                    for dat in list(dict_i[dia][dur][pro][exp].keys()):
                        # dictionary
                        d1 = dict_i[dia][dur][pro][exp][dat]
                        # list sample sizes
                        list_siz = sorted(list(set([k2 for k1 in list(d1.keys()) for k2 in list(d1[k1].keys())])),
                                          key=str.casefold)
                        if len(list_siz) < 2:
                            list_siz = []
                        if ensemble_size_reference == "maximum":
                            list_siz = list(reversed(list_siz))
                        # reference ensemble size
                        ref_size = list_siz[0]
                        # compute the influence of the ensemble size
                        list_x, list_y = [], []
                        for siz in list_siz:
                            # list uncertainties by epoch
                            arr = [d1[k][siz] for k in list(d1.keys()) if siz in list(d1[k].keys())]
                            ref = [d1[k][ref_size] for k in list(d1.keys()) if ref_size in list(d1[k].keys())]
                            # compute ratio of epoch means
                            arr = float(stat_compute_statistic(arr, "mea")) / float(stat_compute_statistic(ref, "mea"))
                            # save value
                            if ensemble_size_reference == "maximum":
                                list_x.append(int(siz.split("_")[0]) / int(ref_size.split("_")[0]))
                            else:
                                list_x.append(int(siz.split("_")[0]))
                            list_y.append(arr)
                        # save value
                        dict_o = tool_put_in_dict(dict_o, list_x, dia, dat, exp, dur, "x")
                        dict_o = tool_put_in_dict(dict_o, list_y, dia, dat, exp, dur, "y")
    return dict_o


def nest_influence_of_epoch_length(dict_i: dict, epoch_length_reference: str) -> dict:
    """
    Organize data to plot the influence of the epoch length on the uncertainty of the ensemble mean
    
    Inputs:
    -------
    :param dict_i: dict
        Dictionary with seven nested levels [diagnostic, epoch_length, project, experiment, dataset, epoch, sample_size]
        filled with a list of values
    :param epoch_length_reference: str
        Reference used to compute the influence of ensemble size
        Two references are defined: 'maximum', 'minimum'
        Defines if the 'maximum' or 'minimum' ensemble size is used as a reference to compute the influence of the
        ensemble size
    
    Output:
    -------
    :return: dict
        Dictionary with five nested levels [diagnostic, dataset, experiment, ensemble_size, x-or-y], filled with the
        values to plot
    """
    # check input
    error = list()
    known_references = ["maximum", "minimum"]
    check_type(dict_i, "dict_i", dict, error)
    check_list(epoch_length_reference, "epoch_length_reference", known_references, error)
    print_fail(inspect__stack(), "\n".join(k for k in error))
    # organize data to plot the influence of ensemble size
    dict_o = {}
    for dia in list(dict_i.keys()):
        du0 = sorted(list(dict_i[dia].keys()), key=str.casefold)[0]
        for pro in list(dict_i[dia][du0].keys()):
            for exp in list(dict_i[dia][du0][pro].keys()):
                for dat in list(dict_i[dia][du0][pro][exp].keys()):
                    # dictionary
                    d1 = dict_i[dia]
                    # list epoch lengths for given data
                    list_lengths = sorted(list(set(
                        [dur for dur in list(d1.keys()) if pro in list(d1[dur].keys()) and
                         exp in list(d1[dur][pro].keys()) and dat in list(d1[dur][pro][exp].keys())])),
                        key=str.casefold)
                    if len(list_lengths) < 2:
                        list_lengths = []
                    if epoch_length_reference == "maximum":
                        list_lengths = list(reversed(list_lengths))
                    # reorganize dictionary
                    dict_t = {}
                    for dur in list_lengths:
                        for epo in list(dict_i[dia][dur][pro][exp][dat].keys()):
                            for siz in list(dict_i[dia][dur][pro][exp][dat][epo].keys()):
                                dict_t = tool_put_in_dict(
                                    dict_t, dict_i[dia][dur][pro][exp][dat][epo][siz], siz, dur, epo)
                    for siz in list(dict_t.keys()):
                        # compute the influence of the epoch length
                        list_x, list_y = [], []
                        for dur in list_lengths:
                            # reference epoch length
                            ref_length = list_lengths[0]
                            # list uncertainties by epoch
                            arr = [dict_t[siz][dur][k] for k in list(dict_t[siz][dur].keys())]
                            ref = [dict_t[siz][ref_length][k] for k in list(dict_t[siz][ref_length].keys())]
                            # compute ratio of epoch means
                            arr = float(stat_compute_statistic(arr, "mea")) / float(stat_compute_statistic(ref, "mea"))
                            # save value
                            if epoch_length_reference == "maximum":
                                list_x.append(int(dur.split("_")[0]) / int(ref_length.split("_")[0]))
                                # list_x.append(int(dur.split("_")[0]))
                            else:
                                list_x.append(int(dur.split("_")[0]))
                            list_y.append(arr)
                        # save value
                        dict_o = tool_put_in_dict(dict_o, list_x, dia, dat, exp, siz, "x")
                        dict_o = tool_put_in_dict(dict_o, list_y, dia, dat, exp, siz, "y")
    return dict_o


def nest_quality_control_distributions(dict_i: dict, data_experiments: list,
                                       reference_experiment: str = "piControl") -> dict:
    """
    Organize data to plot the quality control boxplots
    
    Inputs:
    -------
    :param dict_i: dict
        Dictionary with six nested levels [diagnostic, epoch_length, project, experiment, dataset, epoch], filled with a
        list of values
    :param data_experiments: list
        Names of experiment (to keep them in the right order); e.g., data_experiments = ['piControl', 'historical']
    :param reference_experiment: str, optional
        The mean of this experiment will be removed from all distributions of a given ensemble;
        e.g., reference_experiment = 'piControl'
        Default in 'piControl'
    
    Output:
    -------
    :return dict_o: dict
        Dictionary with four nested levels [diagnostic, experiment, boxplot, x-or-y-or-x_tick_labels], filled with the
        values to plot
    """
    # compute the difference between piControl mean and the other values
    dict_o = {}
    for dia in list(dict_i.keys()):
        list_dur = list(dict_i[dia].keys())
        if len(list_dur) > 1:
            error = "there should be only one epoch length available\n" + str().ljust(5) + "diagnostic: %s" % dia
            error += "\n" + str().ljust(5) + "epoch lengths: " + str(list_dur)
            print_fail(inspect__stack(), error)
        for dur in list_dur:
            for pro in list(dict_i[dia][dur].keys()):
                # ensemble mean of the reference
                ref = dict_i[dia][dur][pro][reference_experiment]
                list_dat = sorted(list(ref.keys()), key=str.casefold)
                epo = sorted(list(ref[list_dat[0]].keys()), key=str.casefold)[0]
                dict_ref = dict((dat, ref[dat][epo]) for dat in list_dat)
                dict_ave = dict((dat, stat_compute_statistic(dict_ref[dat], "mea")) for dat in list_dat)
                for ii, exp in enumerate(data_experiments):
                    # dictionary
                    d1 = dict_i[dia][dur][pro][exp]
                    # parameters for x values
                    n_exp = len(data_experiments)
                    dx = 1 / n_exp
                    list_x, list_y = [], []
                    for k, dat in enumerate(list_dat):
                        list_x.append(k - dx * (n_exp - 1) / 2 + ii * dx)
                        tmp = []
                        for epo in list(d1[dat].keys()):
                            tmp += d1[dat][epo] if isinstance(d1[dat][epo], list) is True else [d1[dat][epo]]
                        list_y.append([jj - dict_ave[dat] for jj in tmp])
                    dict_o = tool_put_in_dict(dict_o, list_x, dia, exp, "boxplot", "x")
                    dict_o = tool_put_in_dict(dict_o, list_y, dia, exp, "boxplot", "y")
                    dict_o = tool_put_in_dict(dict_o, list_dat, dia, exp, "boxplot", "x_tick_labels")
    return dict_o


def nest_quality_control_time_series(dict_i: dict, epoch_length: str) -> dict:
    """
    Organize data to plot the quality control time series
    
    Inputs:
    -------
    :param dict_i: dict
        Dictionary with four nested levels [diagnostic, project, experiment, dataset], filled with a list of values
    :param epoch_length: str
        Epoch length to use for the smoothing of the time series (triangular-weighted running average);
        e.g., epoch_length = '030_year_epoch'
    
    Output:
    -------
    :return dict_o: dict
        Dictionary with four nested levels [diagnostic, dataset, curve, x-or-y], filled with the values to plot
    """
    # compute the difference with the first epoch_length of the time series and smooth time series using an
    # epoch_length * 12 + 1 triangular-weighted running average
    dict_o = {}
    list_dia = list(dict_i.keys())
    if len(list_dia) > 1:
        error = "there should be only one diagnostic available\n" + str().ljust(5) + "diagnostics: " + str(list_dia)
        print_fail(inspect__stack(), error)
    for dia in list_dia:
        for pro in list(dict_i[dia].keys()):
            list_exp = list(dict_i[dia][pro].keys())
            if len(list_exp) > 1:
                error = "there should be only one experiment available\n" + str().ljust(5)
                error += "diagnostic: %s; project: %s" % (dia, pro)
                error += "\n" + str().ljust(5) + "experiments: " + str(list_exp)
                print_fail(inspect__stack(), error)
            exp = list_exp[0]
            for dat in list(dict_i[dia][pro][exp]):
                # array
                arr_y = numpy__array(dict_i[dia][pro][exp][dat][0])
                # average the first epoch_length of the time series
                dur = int(epoch_length.split("_")[0]) * 12
                ave = stat_compute_statistic(arr_y[: dur], "mea")
                # smooth time series
                arr_y = stat_smooth_triangle(arr_y, dur + 1)
                # remove epoch_length -years average
                arr_y = list(arr_y - ave)
                # x values
                arr_x = list(range(len(arr_y)))
                # remove half of epoch_length -years at both ends of the time series (poorly smoothed epoch)
                arr_x = arr_x[dur // 2: -dur // 2]
                arr_y = arr_y[dur // 2: -dur // 2]
                dict_o = tool_put_in_dict(dict_o, arr_x, dia, dat, "curve", "x")
                dict_o = tool_put_in_dict(dict_o, arr_y, dia, dat, "curve", "y")
    return dict_o
# ---------------------------------------------------------------------------------------------------------------------#
