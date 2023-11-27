# -*- coding:UTF-8 -*-
# ---------------------------------------------------------------------------------------------------------------------#
# Functions to compute statistics for the paper about estimating_uncertainties_in_simulated_ENSO submitted to JAMES
# ---------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------#
# Import packages
# ---------------------------------------------------#
# basic python package
from copy import deepcopy
from inspect import stack as inspect__stack
from itertools import combinations as itertools__combinations
from math import ceil as math__ceil
from math import factorial as math__factorial
from random import sample as random__sample
# numpy
from numpy import array as numpy__array
from numpy import ndarray as numpy__ndarray
from numpy.random import randint as numpy__random__randint
# scipy
from scipy.stats import linregress as scipy__stats__linregress
from scipy.stats import norm as scipy__stats__norm
from scipy.stats import scoreatpercentile as scipy__stats__scoreatpercentile
from scipy.stats import t as scipy__stats__t
# estimating_uncertainties_enso package
from . check_lib import check_integer_even_or_odd, check_interval, check_list, check_type, print_fail
# ---------------------------------------------------#


# ---------------------------------------------------------------------------------------------------------------------#
# Functions
# ---------------------------------------------------------------------------------------------------------------------#
def stat_mean(arr_i, axis=None):
    """
    Compute the mean along the given axis using numpy

    Inputs:
    -------
    :param arr_i: array_like
    :param axis: None or int, optional
        Axis along which the mean is computed
        Default is None (compute mean of the flattened array)

    Output:
    -------
    :return: ndarray
        array containing the mean values
    """
    return numpy__array(arr_i).mean(axis=axis)


def stat_standard_deviation(arr_i, axis=None):
    """
    Compute the standard deviation along the given axis using numpy

    Inputs:
    -------
    :param arr_i: array_like
    :param axis: None or int, optional
        Axis along which the standard deviation is computed
        Default is None (compute standard deviation of the flattened array)

    Output:
    -------
    :return: ndarray
        Array containing the standard deviation values
    """
    return numpy__array(arr_i).std(axis=axis)


def stat_variance(arr_i, axis=None):
    """
    Compute the variance along the given axis using numpy

    Inputs:
    -------
    :param arr_i: array_like
    :param axis: None or int, optional
        Axis along which the variance is computed
        Default is None (compute variance of the flattened array)

    Output:
    -------
    :return: ndarray
        Array containing the variance values
    """
    return numpy__array(arr_i).var(axis=axis)


def stat_variance_to_mean2(arr_i, axis=None):
    """
    Compute the ratio variance / mean**2 along the given axis using numpy

    Inputs:
    -------
    :param arr_i: array_like
    :param axis: None or int, optional
        Axis along which mean and variance are computed
        Default is None (compute mean and variance of the flattened array)

    Output:
    -------
    :return: ndarray
        Array containing the variance / mean**2 values
    """
    return numpy__array(arr_i).var(axis=axis) / numpy__array(arr_i).mean(axis=axis)**2


dic_stat = {"mea": stat_mean, "std": stat_standard_deviation, "var": stat_variance,
            "var_to_mea2": stat_variance_to_mean2}


def stat_bootstrap(arr_i, statistic: str, nbr_resamples: int, sample_size: int):
    """
    Compute the given statistic on a resampled array

    Inputs:
    -------
    :param arr_i: array_like
    :param statistic: str
        Name of a statistic; e.g., statistic = 'mea'
        Four statistics are defined: 'mea', 'std', 'var', 'var_to_mea2'
    :param nbr_resamples: int
        Number of samples to generate; e.g., nbr_resamples = 1000
    :param sample_size: int
        Number of values in each sample; e.g., sample_size = 10

    Output:
    -------
    :return: ndarray
        Array containing the statistic values computed 'nbr_samples' times
    """
    # check input
    error = list()
    check_type(arr_i, "arr_i", (list, numpy__ndarray), error)
    check_list(statistic, "statistic", list(dic_stat.keys()), error)
    check_interval(nbr_resamples, "nbr_resamples", int, [10, 1e10], error)
    if isinstance(arr_i, (list, numpy__ndarray)) is True:
        check_interval(sample_size, "sample_size", int, [1, len(arr_i)], error)
    print_fail(inspect__stack(), "\n".join(k for k in error))
    # create random indices
    idx = numpy__random__randint(0, len(arr_i), (nbr_resamples, sample_size))
    # randomly select members
    sample = numpy__array(arr_i)[idx]
    # compute the statistic
    return dic_stat[statistic](sample, axis=1)


def stat_combination_indices(population_size: int, nbr_combinations: int, sample_size: int):
    """
    Compute the given statistic on a resampled array

    Inputs:
    -------
    :param population_size: int
        Number of values in the population; e.g., population_size = 100
    :param nbr_combinations: int
        Maximum number of combinations to use; e.g., nbr_combinations = 1000
    :param sample_size: int
        Number of values in each sample; e.g., sample_size = 10

    Output:
    -------
    :return: ndarray
        Indices to select from the population
    """
    # check input
    error = list()
    check_type(population_size, "population_size", int, error)
    check_interval(nbr_combinations, "nbr_combinations", int, [10, int(1e10)], error)
    check_interval(sample_size, "sample_size", int, [1, population_size - 1], error)
    print_fail(inspect__stack(), "\n".join(k for k in error))
    # define size of array and indices of the array
    indices = list(range(population_size))
    # compute the number of combinations
    maximum_combinations = int(math__factorial(population_size) / (
            math__factorial(sample_size) * math__factorial(population_size - sample_size)))
    # compute and select combinations
    if maximum_combinations < nbr_combinations * 10:
        # compute all possible combinations
        idx = list(itertools__combinations(indices, sample_size))
        # select 'nbr_samples' of them
        if maximum_combinations > nbr_combinations:
            selected = sorted(random__sample(range(maximum_combinations), nbr_combinations))
            idx = [tuple(idx)[k] for k in selected]
    else:
        idx = list()
        while len(idx) < nbr_combinations:
            # randomly generate a combination
            sample = sorted(random__sample(indices, sample_size))
            # keep it if it is not already
            if sample not in idx:
                idx.append(sample)
    return numpy__array(idx)


def stat_combination_random(arr_i, statistic: str, nbr_combinations: int, sample_size: int):
    """
    Compute the given statistic on a resampled array

    Inputs:
    -------
    :param arr_i: array_like
    :param statistic: str
        Name of a statistic; e.g., statistic = 'mea'
        Four statistics are defined: 'mea', 'std', 'var', 'var_to_mea2'
    :param nbr_combinations: int
        Maximum number of combinations to use; e.g., nbr_combinations = 1000
    :param sample_size: int
        Number of values in each sample; e.g., sample_size = 10

    Output:
    -------
    :return: ndarray
        Array containing the statistic values computed 'nbr_samples' times
    """
    # check input
    error = list()
    check_type(arr_i, "arr_i", (list, numpy__ndarray), error)
    check_list(statistic, "statistic", list(dic_stat.keys()), error)
    print_fail(inspect__stack(), "\n".join(k for k in error))
    # select necessary indices
    idx = stat_combination_indices(len(arr_i), nbr_combinations, sample_size)
    # randomly select members
    sample = numpy__array(arr_i)[idx]
    # compute the statistic
    return dic_stat[statistic](sample, axis=1)


def stat_compute_statistic(arr_i, statistic: str):
    """
    Compute the given statistic of the flattened array

    Inputs:
    -------
    :param arr_i: array_like
    :param statistic: str
        Name of a statistic; e.g., statistic = 'mea'
        Four statistics are defined: 'mea', 'std', 'var', 'var_to_mea2'

    Output:
    -------
    :return arr_o: ndarray
        Array containing the statistic values
    """
    # check input
    error = list()
    check_type(arr_i, "arr_i", (float, int, list, numpy__ndarray), error)
    check_list(statistic, "statistic", list(dic_stat.keys()), error)
    print_fail(inspect__stack(), "\n".join(k for k in error))
    # compute statistic
    if statistic == "mea" and isinstance(arr_i, (float, int)) is True:
        arr_o = deepcopy(arr_i)
    elif statistic == "mea" and isinstance(arr_i, list) is True and len(arr_i) == 1:
        arr_o = arr_i[0]
    elif isinstance(arr_i, (list, numpy__ndarray)) is True and len(arr_i) > 1:
        arr_o = float(dic_stat[statistic](arr_i))
    else:
        arr_o = None
    return arr_o


def stat_regression(arr_i1, arr_i2):
    """
    Compute the linear least-squares regression between the two given arrays
    
    Inputs:
    -------
    :param arr_i1: array_like
    :param arr_i2: array_like
    
    Outputs:
    --------
    :return slope: float
        Slope of the regression line
    :return intercept: float
        Intercept of the regression line
    :return correlation: float
        The Pearson correlation coefficient
    :return p_value: float
        The p-value for a hypothesis test whose null hypothesis is that the slope is zero, using Wald Test with
        t-distribution of the test statistic.
    """
    # check input
    error = list()
    check_type(arr_i1, "arr_i1", (list, numpy__ndarray), error)
    check_type(arr_i2, "arr_i2", (list, numpy__ndarray), error)
    if len(arr_i1) != len(arr_i2):
        error.append("arrays don't have the same length")
        error.append(str().ljust(5) + "len(arr_i1) = %s and len(arr_i2) = %s" % (repr(len(arr_i1)), type(len(arr_i2))))
    print_fail(inspect__stack(), "\n".join(k for k in error))
    # compute linear regression
    slope, intercept, correlation, p_value, _ = scipy__stats__linregress(arr_i1, arr_i2)
    return slope, intercept, correlation, p_value


def stat_res_based_on_obs(arr_model, arr_obs: float, maximum_res: int, uncertainty_confidence_interval: float,
                          uncertainty_distribution: str, uncertainty_combinations: int, uncertainty_resamples: int,
                          uncertainty_theory: bool):
    """
    Compute the required ensemble size to know the sign of the bias (using combinations of model members)
    
    Inputs:
    -------
    :param arr_model: array_like
    :param arr_obs: float
        Observed value (or reverence value); e.g., arr_obs = 3.4
    :param maximum_res: int
        Maximum value for the required ensemble size; e.g., maximum_res = 100
    :param uncertainty_confidence_interval: float
        Confidence interval used to compute the uncertainty; e.g., uncertainty_confidence_interval = 95
    :param uncertainty_distribution: str
        Name of a distribution; e.g., distribution = 'normal'
        Two distributions are defined: 'normal', 'student'
        Used only if uncertainty_theoretical is True
    :param uncertainty_combinations: int
        Maximum number of combinations to used to compute the uncertainty if sample_size < len(arr_i);
        e.g., nbr_combinations = 1000
    :param uncertainty_resamples: int
        Number of resamples to compute (boostrap uncertainty); e.g., uncertainty_resamples = 1000
    :param uncertainty_theory: bool
        True to compute the theoretical uncertainty (using the standard error; e.g., Chapter 5 p. 92 of von Storch and
        Zwiers (1999; https://doi.org/10.1017/CBO9780511612336), else compute the uncertainty using a boostrap;
        e.g., uncertainty_theoretical = True
        
    Output:
    -------
    :return res: int
        Required ensemble size to know the sign of the bias
    """
    # check input
    error = list()
    check_type(arr_model, "arr_model", (list, numpy__ndarray), error)
    check_type(arr_obs, "arr_obs", (float, int), error)
    check_type(maximum_res, "maximum_res", int, error)
    print_fail(inspect__stack(), "\n".join(k for k in error))
    # compute the sign of the bias using the largest accepted ensemble size
    low, res = 0, min(len(arr_model), maximum_res)
    is_true = stat_uncertainties_smaller_than_difference(
        arr_model, arr_obs, uncertainty_confidence_interval, uncertainty_distribution, uncertainty_combinations,
        uncertainty_resamples, uncertainty_theory, res)
    if is_true:
        # the uncertainty computed using the largest accepted ensemble size is smaller than the desired uncertainty,
        # find the smallest ensemble required.
        while low + 1 != res:
            # divide the interval by two
            size = min(res - 1, math__ceil(res / 2 + low / 2))
            # compute the sample uncertainty and the threshold using sample size = size
            is_true = stat_uncertainties_smaller_than_difference(
                arr_model, arr_obs, uncertainty_confidence_interval, uncertainty_distribution, uncertainty_combinations,
                uncertainty_resamples, uncertainty_theory, size)
            if is_true:
                # uncertainty computed with size samples is smaller than desired uncertainty (ensemble too large)
                res = deepcopy(size)
            else:
                # uncertainty computed with size samples is larger than desired uncertainty (ensemble too small)
                low = deepcopy(size)
    else:
        # res cannot be computed
        res = deepcopy(maximum_res)
    return res


def stat_res_bootstrap(arr_i, res_maximum: int, uncertainty_confidence_interval: float, uncertainty_resamples: int,
                       uncertainty_threshold: float):
    """
    Compute the required ensemble size to obtain the given uncertainty of the ensemble mean (using bootstrap)

    Inputs:
    -------
    :param arr_i: array_like
    :param res_maximum: int
        Maximum value for the required ensemble size; e.g., maximum_res = 100
    :param uncertainty_confidence_interval: float
        Confidence interval used to compute the uncertainty; e.g., uncertainty_confidence_interval = 95
    :param uncertainty_resamples: int
        Number of samples to generate; e.g., uncertainty_resamples = 1000
    :param uncertainty_threshold: float
        Desired uncertainty; e.g., uncertainty = 1

    Output:
    -------
    :return res: int
        Required ensemble size to obtain the given uncertainty
    """
    # check input
    error = list()
    check_type(arr_i, "arr_i", (list, numpy__ndarray), error)
    check_type(res_maximum, "maximum_res", int, error)
    check_interval(uncertainty_threshold, "uncertainty_threshold", (float, int), [0, 1e20], error)
    print_fail(inspect__stack(), "\n".join(k for k in error))
    # compute uncertainty using the largest accepted ensemble size
    low, res = 0, min(len(arr_i), res_maximum)
    sample_uncertainty = stat_uncertainty_bootstrap(arr_i, uncertainty_confidence_interval, False,
                                                    uncertainty_resamples, res)
    if sample_uncertainty < uncertainty_threshold:
        # the uncertainty computed using the largest accepted ensemble size is smaller than the desired uncertainty,
        # find the smallest ensemble required.
        while low + 1 != res:
            # divide the interval by two
            size = min(res - 1, math__ceil(res / 2 + low / 2))
            sample_uncertainty = stat_uncertainty_bootstrap(arr_i, uncertainty_confidence_interval, False,
                                                            uncertainty_resamples, size)
            if sample_uncertainty < uncertainty_threshold:
                # uncertainty computed with size samples is lower than desired uncertainty (ensemble too large)
                res = deepcopy(size)
            else:
                # uncertainty computed with size samples is higher than desired uncertainty (ensemble too small)
                low = deepcopy(size)
    else:
        # res cannot be computed
        res = deepcopy(res_maximum)
    return res


def stat_res_theory(arr_i, maximum_res: int, uncertainty_confidence_interval: float, uncertainty_threshold: float):
    """
    Compute the required ensemble size to obtain the given uncertainty of the ensemble mean (using the standard error of
    the mean).
    YYP: Distributions are assumed to be normal. The student distribution should be used for the uncertainty of the
    ensemble mean, but it depends on n (sample size) and that's what we are looking for

    Inputs:
    -------
    :param arr_i: array_like
    :param maximum_res: int
        Maximum value for the required ensemble size; e.g., maximum_res = 100
    :param uncertainty_confidence_interval: float
        Confidence level used to compute the z-score; e.g., uncertainty_confidence_interval = 95
    :param uncertainty_threshold: float
        Desired uncertainty; e.g., uncertainty_threshold = 1

    Output:
    -------
    :return res: int
        Required ensemble size to obtain the given uncertainty
    """
    # check input
    error = list()
    check_type(arr_i, "arr_i", (list, numpy__ndarray), error)
    check_type(maximum_res, "maximum_res", int, error)
    check_interval(uncertainty_threshold, "uncertainty", (float, int), [0, 1e20], error)
    print_fail(inspect__stack(), "\n".join(k for k in error))
    # number of standard deviations needed to obtain given significance_level (the sample size is set to 1 as it is not
    # used for a normal distribution)
    zscore = stat_zscore(1, uncertainty_confidence_interval, "normal")
    # compute ensemble variance using combination of sample_size values from arr_i
    variance = stat_compute_statistic(arr_i, "var")
    # required ensemble size
    res = math__ceil(zscore**2 * variance / uncertainty_threshold**2)
    if res > maximum_res:
        res = deepcopy(maximum_res)
    return res


def stat_smooth_triangle(arr_i, window: int):
    """
    Smooth given array using a triangle-weighted running average
    
    :param arr_i: array_like
    :param window: int
        Number of points used to compute the running average
    
    :return arr_o: array_like
        Smoothed array
    """
    # check input
    error = list()
    check_type(arr_i, "arr_i1", (list, numpy__ndarray), error)
    check_integer_even_or_odd(window, "window", "odd", error)
    print_fail(inspect__stack(), "\n".join(k for k in error))
    # degree
    degree = window // 2
    #
    # -- Smooth the first degree points of the array
    #
    arr_o = [arr_i[0]]
    for k in range(1, degree):
        # create the weight array (triangle)
        weight = [float(1 + k - abs(k - i)) for i in range(0, (2 * k) + 1)]
        # total weight
        weight_sum = sum(weight)
        # smooth
        arr_o.append(sum([i * j for i, j in zip(arr_i[: len(weight)], weight)]) / weight_sum)
    #
    # -- Smooth the core of the array
    #
    # create the weight array (triangle)
    weight = [float(1 + degree - abs(degree - k)) for k in range(0, (2 * degree) + 1)]
    # total weight
    weight_sum = sum(weight)
    # smooth
    for k in range(degree, len(arr_i) - degree):
        arr_o.append(sum([i * j for i, j in zip(arr_i[k - degree: k + degree + 1], weight)]) / weight_sum)
    #
    # -- Smooth the last degree points of the array
    #
    for k in range(degree - 1, 0, -1):
        # create the weight array (triangle)
        weight = [float(1 + k - abs(k - i)) for i in range(0, (2 * k) + 1)]
        # total weight
        weight_sum = sum(weight)
        # smooth
        arr_o.append(sum([i * j for i, j in zip(arr_i[-len(weight):], weight)]) / weight_sum)
    arr_o += [arr_i[-1]]
    # convert to ndarray if the input was ndarray
    if isinstance(arr_i, numpy__ndarray):
        arr_o = numpy__array(arr_o)
    return arr_o


def stat_uncertainties_smaller_than_difference(arr_model, arr_obs, uncertainty_confidence_interval: float,
                                               uncertainty_distribution: str, uncertainty_combinations: int,
                                               uncertainty_resamples: int, uncertainty_theory: bool,
                                               uncertainty_sample_size: int):
    """
    Compute the uncertainty of the ensemble mean using given sample size, as well as the threshold for this uncertainty
    This is the case where the uncertainty of the ensemble mean need to be smaller than the difference model-obs
    
    Inputs:
    -------
    :param arr_model: array_like
    :param arr_obs: float
        Observed value (or reverence value); e.g., arr_obs = 3.4
    :param uncertainty_confidence_interval: float
        Confidence interval used to compute the uncertainty; e.g., uncertainty_confidence_interval = 95
    :param uncertainty_distribution: str
        Name of a distribution; e.g., distribution = 'normal'
        Two distributions are defined: 'normal', 'student'
        Used only if uncertainty_theoretical is True
    :param uncertainty_combinations: int
        Maximum number of combinations to used to compute the uncertainty if sample_size < len(arr_i);
        e.g., nbr_combinations = 1000
    :param uncertainty_resamples: int
        Number of resamples to compute (boostrap uncertainty); e.g., uncertainty_resamples = 1000
    :param uncertainty_theory: bool
        True to compute the theoretical uncertainty (using the standard error; e.g., Chapter 5 p. 92 of von Storch and
        Zwiers (1999; https://doi.org/10.1017/CBO9780511612336), else compute the uncertainty using a boostrap;
        e.g., uncertainty_theoretical = True
    :param uncertainty_sample_size: int
        Number of values in each sample; e.g., uncertainty_sample_size = 10
    
    Output:
    -------
    :return: bool
        True if the uncertainty of the ensemble mean is smaller than the difference model-obs
    """
    # check input
    error = list()
    check_type(arr_model, "arr_model", (list, numpy__ndarray), error)
    check_type(arr_obs, "arr_obs", (float, int), error)
    check_type(uncertainty_theory, "uncertainty_theory", bool, error)
    print_fail(inspect__stack(), "\n".join(k for k in error))
    # compute uncertainty and threshold of said uncertainty (desired maximum value)
    if uncertainty_theory is True:
        if uncertainty_sample_size < len(arr_model):
            # compute ensemble mean using sample_size
            sample_mean = stat_combination_random(arr_model, "mea", uncertainty_combinations, uncertainty_sample_size)
            # uncertainty threshold
            threshold = float(scipy__stats__scoreatpercentile(abs(sample_mean - arr_obs),
                                                              100 - uncertainty_confidence_interval))
        else:
            # if sample_size is the size of the ensemble, the sample mean becomes the ensemble mean (i.e., 1 value) by
            # definition uncertainty threshold becomes the difference between the two values
            threshold = abs(stat_compute_statistic(arr_model, "mea") - arr_obs)
        uncertainty = stat_uncertainty_theory(
            arr_model, uncertainty_confidence_interval, False, uncertainty_combinations, uncertainty_sample_size,
            uncertainty_distribution)
    else:
        # compute ensemble mean using 'res' sample size
        sample_mean = stat_bootstrap(arr_model, "mea", uncertainty_resamples, uncertainty_sample_size)
        # uncertainty threshold
        threshold = float(scipy__stats__scoreatpercentile(abs(sample_mean - arr_obs),
                                                          100 - uncertainty_confidence_interval))
        # half confidence interval on the statistic
        uncertainty = scipy__stats__scoreatpercentile(abs(sample_mean - float(stat_mean(sample_mean))),
                                                      uncertainty_confidence_interval)
    # is the uncertainty smaller?
    return uncertainty < threshold


def stat_uncertainty_bootstrap(arr_i, uncertainty_confidence_interval: float, uncertainty_relative: bool,
                               uncertainty_resamples: int, uncertainty_sample_size: int):
    """
    Compute the uncertainty of the sample mean (using a boostrap)

    Inputs:
    -------
    :param arr_i: array_like
    :param uncertainty_confidence_interval: float
        Confidence interval used to compute the uncertainty; e.g., uncertainty_confidence_interval = 95
    :param uncertainty_relative: bool
        True to compute the uncertainty relative to the sample mean, else the absolute uncertainty is computed;
        e.g., uncertainty_relative = True
    :param uncertainty_resamples: int
        Number of resamples to compute (boostrap uncertainty); e.g., uncertainty_resamples = 1000
    :param uncertainty_sample_size: int
        Number of values in each sample; e.g., uncertainty_sample_size = 10

    Output:
    -------
    :return: float
        Uncertainty of the sample mean computed using a boostrap
    """
    # check input
    error = list()
    check_type(arr_i, "arr_i", (list, numpy__ndarray), error)
    check_interval(uncertainty_confidence_interval, "uncertainty_confidence_interval", (float, int), [0, 100], error)
    check_type(uncertainty_relative, "uncertainty_relative", bool, error)
    print_fail(inspect__stack(), "\n".join(k for k in error))
    # compute uncertainty using bootstrap
    bootstrap = stat_bootstrap(arr_i, "mea", uncertainty_resamples, uncertainty_sample_size)
    # mean
    mean = float(stat_mean(bootstrap))
    # half confidence interval on the statistic
    uncertainty = scipy__stats__scoreatpercentile(abs(bootstrap - mean), uncertainty_confidence_interval)
    if uncertainty_relative is True:
        uncertainty *= 100 / abs(mean)
    return uncertainty


def stat_uncertainty_select_and_compute(arr_i, uncertainty_confidence_interval: float, uncertainty_distribution: str,
                                        uncertainty_relative: bool, uncertainty_combinations: int,
                                        uncertainty_resamples: int, uncertainty_theory: bool,
                                        uncertainty_sample_size: int):
    """
    Compute the uncertainty of the sample mean, either using the theory or a bootstrap

    Inputs:
    -------
    :param arr_i: array_like
    :param uncertainty_confidence_interval: float
        Confidence interval used to compute the uncertainty; e.g., uncertainty_confidence_interval = 95
    :param uncertainty_distribution: str
        Name of a distribution; e.g., distribution = 'normal'
        Two distributions are defined: 'normal', 'student'
        Used only if uncertainty_theory is True
    :param uncertainty_relative: bool
        True to compute the uncertainty relative to the sample mean, else the absolute uncertainty is computed;
        e.g., uncertainty_relative = True
    :param uncertainty_combinations: int
        Maximum number of combinations to used to compute the uncertainty if uncertainty_sample_size < len(arr_i);
        e.g., uncertainty_combinations = 1000
    :param uncertainty_resamples: int
        Number of resamples to compute (boostrap uncertainty); e.g., uncertainty_resamples = 1000
    :param uncertainty_theory: bool
        True to compute the theoretical uncertainty (using the standard error; e.g., Chapter 5 p. 92 of von Storch and
        Zwiers (1999; https://doi.org/10.1017/CBO9780511612336), else compute the uncertainty using a boostrap;
        e.g., uncertainty_theory = True
    :param uncertainty_sample_size: int
        Number of values in each sample; e.g., uncertainty_sample_size = 10

    Output:
    -------
    :return uncertainty: float
        Uncertainty of the sample mean
    """
    # check input
    error = list()
    check_type(uncertainty_relative, "uncertainty_relative", bool, error)
    print_fail(inspect__stack(), "\n".join(k for k in error))
    # compute uncertainty
    if uncertainty_theory is True:
        # compute the uncertainty based on the theory (using standard error)
        uncertainty = stat_uncertainty_theory(arr_i, uncertainty_confidence_interval, uncertainty_relative,
                                              uncertainty_combinations, uncertainty_sample_size,
                                              uncertainty_distribution)
    else:
        # compute uncertainty using bootstrap
        uncertainty = stat_uncertainty_bootstrap(arr_i, uncertainty_confidence_interval, uncertainty_relative,
                                                 uncertainty_resamples, uncertainty_sample_size)
    return uncertainty


def stat_uncertainty_theory(arr_i, uncertainty_confidence_interval: float, uncertainty_relative: bool,
                            uncertainty_combinations: int, uncertainty_sample_size: int, uncertainty_distribution: str):
    """
    Compute the uncertainty of the sample mean (using the theory, i.e., the standard error).
    E.g., Chapter 5 p. 92 of von Storch and Zwiers (1999; https://doi.org/10.1017/CBO9780511612336)

    Inputs:
    -------
    :param arr_i: array_like
    :param uncertainty_confidence_interval: float
        Confidence interval used to compute the uncertainty; e.g., uncertainty_confidence_interval = 95
    :param uncertainty_relative: bool
        True to compute the uncertainty relative to the sample mean, else the absolute uncertainty is computed;
        e.g., uncertainty_relative = True
    :param uncertainty_combinations: int
        Maximum number of combinations to used to compute the uncertainty if uncertainty_sample_size < len(arr_i);
        e.g., uncertainty_combinations = 1000
    :param uncertainty_sample_size: int
        Number of values in each sample; e.g., uncertainty_sample_size = 10
    :param uncertainty_distribution: str
        Name of a distribution; e.g., distribution = 'normal'
        Two distributions are defined: 'normal', 'student'

    Output:
    -------
    :return: float or ndarray
        Uncertainty of the sample mean computed using the theory
    """
    # check input
    error = list()
    check_type(arr_i, "arr_i", (list, numpy__ndarray), error)
    check_type(uncertainty_relative, "uncertainty_relative", bool, error)
    print_fail(inspect__stack(), "\n".join(k for k in error))
    # statistic for the uncertainty of the ensemble mean
    statistic = "var_to_mea2" if uncertainty_relative is True else "var"
    # compute ensemble variance using combination of sample_size values from arr_i
    if uncertainty_sample_size == len(arr_i):
        variance = stat_compute_statistic(arr_i, statistic)
    else:
        variance = stat_combination_random(arr_i, statistic, uncertainty_combinations, uncertainty_sample_size)
    # number of standard deviations needed to obtain given significance_level
    zscore = stat_zscore(uncertainty_sample_size, uncertainty_confidence_interval, uncertainty_distribution)
    # standard error
    se = variance**0.5 / uncertainty_sample_size**0.5
    # theoretical uncertainty of the sample mean
    uncertainty = zscore * se
    if uncertainty_relative is True:
        uncertainty *= 100
    # average uncertainty across combinations
    if uncertainty_sample_size != len(arr_i):
        uncertainty = float(stat_mean(uncertainty))
    return uncertainty


def stat_zscore(sample_size, confidence_interval: float, distribution: str):
    """
    Compute the distribution's zscore for the given significance_level

    Input:
    ------
    :param sample_size: float or list
        Number of values in each sample; e.g., sample_size = 10
    :param confidence_interval: float
        Confidence interval used to compute the z-score; e.g., confidence_interval = 95
    :param distribution: str
        Name of a distribution, Variance of the population; e.g., distribution = 'normal'
        Two distributions are defined: 'normal', 'student'
    

    Output:
    -------
    :return zscore: float
        Normal distribution's zscore for the given significance_level
    """
    # check input
    error = list()
    known_distributions = ["normal", "student"]
    check_type(sample_size, "sample_size", (float, int), error)
    check_interval(confidence_interval, "confidence_interval", (float, int), [0, 100], error)
    check_list(distribution, "distribution", known_distributions, error)
    print_fail(inspect__stack(), "\n".join(k for k in error))
    # confidence level for 2-sided confidence interval
    alpha = 0.5 + confidence_interval / 200
    # number of standard deviations needed to obtain given significance_level
    if distribution == "normal":
        zscore = scipy__stats__norm.ppf(alpha)
    else:
        zscore = scipy__stats__t.ppf(alpha, sample_size - 1)
    return zscore
# ---------------------------------------------------------------------------------------------------------------------#
