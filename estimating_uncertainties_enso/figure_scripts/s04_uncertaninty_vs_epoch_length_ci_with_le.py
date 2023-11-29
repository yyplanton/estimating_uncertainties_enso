# -*- coding:UTF-8 -*-
# ---------------------------------------------------------------------------------------------------------------------#
# Figure S4 of the paper about estimating_uncertainties_in_simulated_ENSO submitted to JAMES
# Plot: influence of the epoch length on the uncertainty of the ensemble mean
# This time a single very large SMILE is used (fig_smile_selected) and the interval of values with reduced sample size
# is plotted
# ---------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------#
# Import packages
# ---------------------------------------------------#
# basic python package
from copy import deepcopy
# numpy
from numpy import array as numpy__array
# scipy
from scipy.stats import scoreatpercentile as scipy__stats__scoreatpercentile
# estimating_uncertainties_enso package
from . params import default_parameters
from estimating_uncertainties_enso.compute_lib.data_lib import data_organize_json
from estimating_uncertainties_enso.compute_lib.stat_lib import stat_combination_indices, stat_compute_statistic, \
    stat_uncertainty_select_and_compute
from estimating_uncertainties_enso.compute_lib.tool_lib import tool_put_in_dict
from estimating_uncertainties_enso.figure_templates.fig_template import fig_influence_of
# ---------------------------------------------------#


# ---------------------------------------------------------------------------------------------------------------------#
# Default arguments
# ---------------------------------------------------------------------------------------------------------------------#
default = {
    #
    # -- Data
    #
    # list of diagnostics
    "data_diagnostics": default_parameters["data_diagnostics"],
    # list of epoch lengths
    "data_epoch_lengths": default_parameters["data_epoch_lengths"],
    # list of projects
    "data_projects": ["cmip6"],
    # list of experiments
    "data_experiments": ["historical"],
    #
    # -- Uncertainty
    #
    # compute uncertainty based on theory (or bootstrap): True, False
    "uncertainty_theory": default_parameters["uncertainty_theory"],
    # compute relative uncertainty (or absolute): True, False
    "uncertainty_relative": default_parameters["uncertainty_relative"],
    # confidence interval of the uncertainty: float [0, 100]
    "uncertainty_confidence_interval": default_parameters["uncertainty_confidence_interval"],
    # distribution used to compute the confidence interval if uncertainty_theory is True: 'normal', 'student'
    "uncertainty_distribution": default_parameters["uncertainty_distribution"],
    # maximum number of combinations used if uncertainty_theory is True and smile_size > sample_size: int [10, 1e10]
    "uncertainty_combinations": default_parameters["uncertainty_combinations"],
    # number of resamples used for the bootstrap if uncertainty_theory is False: int [10, 1e10]
    "uncertainty_resamples": default_parameters["uncertainty_resamples"],
    # list of sample sizes for which the uncertainty will be computed
    "uncertainty_sample_sizes": list(range(10, 51, 10)),
    #
    # -- Figure
    #
    # SMILE to plot (largest SMILEs: ACCESS-ESM1-5 = 40, CanESM5_p2 = 40, CanESM5-1 = 47, HadGEM3-GC31-LL = 55,
    # IPSL-CM6A-LR = 33, MIROC-ES2L = 30, MIROC6 = 50, MPI-ESM1-2-LR = 50, NorCPM1 = 30)
    "fig_smile_selected": "ACCESS-ESM1-5",
    # maximum of minimum value used as a reference for the plot
    "fig_uncertainty_reference": "maximum",
    # figure format: eps, pdf, png, svg
    "fig_format": default_parameters["fig_format"],
    # figure name includes input parameters (may create a very long figure name)
    "fig_detailed_name": False,
    # figure orientation: column (column = variables, row = statistics), row (column = statistics, row = variables)
    "fig_orientation": default_parameters["fig_orientation"],
    # position of the legend on the plot: bottom, right
    "fig_legend_position": default_parameters["fig_legend_position"],
    # size of each panel
    "fig_panel_size": {"x_delt": 3, "x_frac": 0.25, "x_size": 16, "y_delt": 2, "y_frac": 0.25, "y_size": 16},
    # color per dataset
    "fig_colors": {"10 members": "dodgerblue", "20 members": "limegreen", "30 members": "goldenrod",
                   "40 members": "peru", "50 members": "darkorchid", "maximum": "r"},
    # linestyle per experiment
    "fig_linestyles": default_parameters["fig_linestyles"],
    # linewidth: all lines have the same width
    "fig_linewidth": 3.,
    # linezorder: all lines have the same zorder; e.g., zorder = 2 is plotted over zorder = 1
    "fig_linezorder": 2,
    # marker per dataset
    "fig_marker": "s",
    # marker size: all marker have the same size
    "fig_marker_size": 0.,
    # ticks
    "fig_ticks": {
        "x_axis": {
            "maximum": [round(k / 10, 1) for k in list(range(2, 11, 2))],
            "minimum": list(range(30, 151, 30)),
        },
        "y_axis": {
            "maximum": {
                "ACCESS-ESM1-5": {
                    "ave_pr_val_n30e": [round(k / 10, 1) for k in list(range(8, 37, 7))],
                    "ave_ts_val_n30e": [round(k / 10, 1) for k in list(range(8, 37, 7))],
                    "ske_pr_ano_n30e": [round(k / 10, 1) for k in list(range(8, 37, 7))],
                    "ske_ts_ano_n30e": [round(k / 10, 1) for k in list(range(8, 37, 7))],
                    "var_pr_ano_n30e": [round(k / 10, 1) for k in list(range(8, 37, 7))],
                    "var_ts_ano_n30e": [round(k / 10, 1) for k in list(range(8, 37, 7))],
                },
            },
        },
    },
    # titles
    "fig_titles": {
        "x_axis": {
            "maximum": "fraction of 150-year epoch",
            "minimum": "epoch length (yr)",
        },
        "y_axis": {
            "maximum": "ratio",
            "minimum": "ratio",
        },
        **default_parameters["fig_titles"],  # add diagnostics, experiments and absolute / relative uncertainty
    },
    # panel parameters (to modify default values in fig_panel.py)
    "panel_param": {},
}
# ---------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------------------------------------------------------------------------#
# Main
# ---------------------------------------------------------------------------------------------------------------------#
def s04_epoch_length(data_diagnostics: list = default["data_diagnostics"],
                     data_epoch_lengths: list = default["data_epoch_lengths"],
                     data_projects: list = default["data_projects"],
                     data_experiments: list = default["data_experiments"],
                     uncertainty_combinations: int = default["uncertainty_combinations"],
                     uncertainty_confidence_interval: float = default["uncertainty_confidence_interval"],
                     uncertainty_distribution: str = default["uncertainty_distribution"],
                     uncertainty_relative: bool = default["uncertainty_relative"],
                     uncertainty_resamples: int = default["uncertainty_resamples"],
                     uncertainty_sample_sizes: list = default["uncertainty_sample_sizes"],
                     uncertainty_theory: bool = default["uncertainty_theory"],
                     fig_colors: dict = default["fig_colors"],
                     fig_detailed_name: bool = default["fig_detailed_name"],
                     fig_format: str = default["fig_format"],
                     fig_legend_position: str = default["fig_legend_position"],
                     fig_linestyles: dict = default["fig_linestyles"],
                     fig_linewidth: float = default["fig_linewidth"],
                     fig_linezorder: int = default["fig_linezorder"],
                     fig_marker: dict = default["fig_marker"],
                     fig_marker_size: float = default["fig_marker_size"],
                     fig_orientation: str = default["fig_orientation"],
                     fig_panel_size: dict = default["fig_panel_size"],
                     fig_smile_selected: str = default["fig_smile_selected"],
                     fig_ticks: dict = default["fig_ticks"],
                     fig_titles: dict = default["fig_titles"],
                     fig_uncertainty_reference: str = default["fig_uncertainty_reference"],
                     panel_param: dict = default["panel_param"], **kwargs):
    #
    # -- Read json
    #
    values, metadata = data_organize_json(data_diagnostics, data_epoch_lengths, data_projects, data_experiments)
    #
    # -- Reorder dictionary and keep only the selected dataset
    #
    values_reordered = {}
    for dia in list(values.keys()):
        for dur in list(values[dia].keys()):
            for pro in list(values[dia][dur].keys()):
                for exp in list(values[dia][dur][pro].keys()):
                    dat = deepcopy(fig_smile_selected)
                    if exp != "historical" or dat not in list(values[dia][dur][pro][exp].keys()):
                        # do not continue this loop if the selected dataset is not available
                        break
                    for epo in list(values[dia][dur][pro][exp][dat].keys()):
                        values_reordered = tool_put_in_dict(values_reordered, values[dia][dur][pro][exp][dat][epo], dia,
                                                            pro, exp, dat, dur, epo)

    #
    # -- Compute uncertainty
    #
    uncertainties = {}
    for dia in list(values_reordered.keys()):
        for pro in list(values_reordered[dia].keys()):
            for exp in list(values_reordered[dia][pro].keys()):
                for dat in list(values_reordered[dia][pro][exp].keys()):
                    # dictionary
                    d1 = values_reordered[dia][pro][exp][dat]
                    # the ensemble size is the same for all epoch lengths and epochs
                    ensemble_size = len(d1[list(d1.keys())[0]][list(d1[list(d1.keys())[0]].keys())[0]])
                    # list sample sizes to use
                    sample_sizes = [k for k in uncertainty_sample_sizes if isinstance(k, int) and k < ensemble_size]
                    # compute uncertainty in maximum ensemble
                    dict_t = {}
                    for dur in list(d1.keys()):
                        for epo in list(d1[dur].keys()):
                            val = stat_uncertainty_select_and_compute(
                                d1[dur][epo], uncertainty_confidence_interval, uncertainty_distribution,
                                uncertainty_relative, uncertainty_combinations, uncertainty_resamples,
                                uncertainty_theory, ensemble_size)
                            dict_t = tool_put_in_dict(
                                dict_t, val, "maximum", dur, str(0).zfill(6), epo)
                    # compute uncertainty in reduced ensemble
                    for siz in sample_sizes:
                        # select the same indices for all epoch lengths and epochs
                        # the goal is to compute the uncertainty each time as if the ensemble size was smaller
                        idx = stat_combination_indices(ensemble_size, uncertainty_combinations, siz)
                        for dur in list(d1.keys()):
                            for epo in list(d1[dur].keys()):
                                # select members
                                sample = numpy__array(d1[dur][epo])[idx]
                                for k in list(range(uncertainty_combinations)):
                                    # compute uncertainty for each combination of reduced ensemble
                                    val = stat_uncertainty_select_and_compute(
                                        sample[k], uncertainty_confidence_interval, uncertainty_distribution,
                                        uncertainty_relative, uncertainty_combinations, uncertainty_resamples,
                                        uncertainty_theory, siz)
                                    dict_t = tool_put_in_dict(
                                        dict_t, val, str(siz) + " members", dur, str(k).zfill(6), epo)
                    # compute the influence of the epoch length for each sample size
                    for siz in list(dict_t.keys()):
                        # list epoch lengths for given data
                        list_lengths = sorted(list(dict_t[siz].keys()), key=str.casefold)
                        if len(list_lengths) < 2:
                            list_lengths = []
                        if fig_uncertainty_reference == "maximum":
                            list_lengths = list(reversed(list_lengths))
                        # reference epoch length
                        dur_ref = list_lengths[0]
                        # compute the influence of the epoch length
                        list_y_low, list_y_upp = [], []
                        for dur in list_lengths:
                            ratio_per_sample = list()
                            for nbr in list(dict_t[siz][dur].keys()):
                                # list uncertainties by epoch
                                arr = [dict_t[siz][dur][nbr][k] for k in list(dict_t[siz][dur][nbr].keys())]
                                ref = [dict_t[siz][dur_ref][nbr][k] for k in list(dict_t[siz][dur_ref][nbr].keys())]
                                # compute ratio of epoch means
                                ratio_per_sample.append(float(stat_compute_statistic(arr, "mea")) /
                                                        float(stat_compute_statistic(ref, "mea")))
                            if len(ratio_per_sample) == 1:
                                list_y_low.append(ratio_per_sample[0])
                                list_y_upp.append(ratio_per_sample[0])
                            else:
                                # lower and upper value on the interval
                                low = 50 - uncertainty_confidence_interval / 2
                                upp = 50 + uncertainty_confidence_interval / 2
                                list_y_low.append(float(scipy__stats__scoreatpercentile(ratio_per_sample, low)))
                                list_y_upp.append(float(scipy__stats__scoreatpercentile(ratio_per_sample, upp)))
                        # x-values
                        if fig_uncertainty_reference == "maximum":
                            list_x = [int(dur.split("_")[0]) / int(dur_ref.split("_")[0]) for dur in list_lengths]
                        else:
                            list_x = [int(dur.split("_")[0]) for dur in list_lengths]
                        # save value
                        if siz == "maximum":
                            uncertainties = tool_put_in_dict(uncertainties, list_x, dia, siz, exp, pro, "x")
                            uncertainties = tool_put_in_dict(uncertainties, list_y_low, dia, siz, exp, pro, "y")
                        else:
                            uncertainties = tool_put_in_dict(uncertainties, list_x, dia, siz, exp, pro, "x")
                            uncertainties = tool_put_in_dict(uncertainties, list_y_low, dia, siz, exp, pro, "y1")
                            uncertainties = tool_put_in_dict(uncertainties, list_y_upp, dia, siz, exp, pro, "y2")
    #
    # -- Organize data to for figure
    #
    method = "relative" if uncertainty_relative is True else "absolute"
    for dia in list(uncertainties.keys()):
        # x-y titles
        title = ""
        if "x_axis" in list(fig_titles.keys()) and fig_uncertainty_reference in list(fig_titles["x_axis"].keys()):
            title = fig_titles["x_axis"][fig_uncertainty_reference]
        fig_titles = tool_put_in_dict(fig_titles, title, "x_axis", dia)
        title = ""
        if "y_axis" in list(fig_titles.keys()) and fig_uncertainty_reference in list(fig_titles["y_axis"].keys()):
            title = str(fig_titles[method]) + " " + str(fig_titles["y_axis"][fig_uncertainty_reference])
        fig_titles = tool_put_in_dict(fig_titles, title, "y_axis", dia)
        # x tics
        if "x_axis" in list(fig_ticks.keys()) and isinstance(fig_ticks["x_axis"], dict) is True and \
                dia in list(fig_ticks["x_axis"].keys()) and isinstance(fig_ticks["x_axis"][dia], list) is True:
            pass
        else:
            list_ticks = None
            if "x_axis" in list(fig_ticks.keys()) and fig_uncertainty_reference in list(fig_ticks["x_axis"].keys()):
                list_ticks = fig_ticks["x_axis"][fig_uncertainty_reference]
            fig_ticks = tool_put_in_dict(fig_ticks, list_ticks, "x_axis", dia)
        # y tics
        if "y_axis" in list(fig_ticks.keys()) and isinstance(fig_ticks["y_axis"], dict) is True and \
                dia in list(fig_ticks["y_axis"].keys()) and isinstance(fig_ticks["y_axis"][dia], list) is True:
            pass
        else:
            list_ticks = None
            if "y_axis" in list(fig_ticks.keys()) and fig_uncertainty_reference in list(fig_ticks["y_axis"].keys()) \
                    and fig_smile_selected in list(fig_ticks["y_axis"][fig_uncertainty_reference].keys()) and \
                    dia in list(fig_ticks["y_axis"][fig_uncertainty_reference][fig_smile_selected].keys()):
                list_ticks = fig_ticks["y_axis"][fig_uncertainty_reference][fig_smile_selected][dia]
            fig_ticks = tool_put_in_dict(fig_ticks, list_ticks, "y_axis", dia)
    # markers
    fig_markers = dict((siz, fig_marker) for siz in list(fig_colors.keys()))
    #
    # -- Figure
    #
    # output figure name will be the file name (path removed and extension removed)
    fig_name = __file__.split("/")[-1].split(".")[0]
    if fig_detailed_name is True:
        # add details of the computation to the figure name
        fig_name += "_data_" + str(len(data_projects)) + "pro_" + str(len(data_experiments)) + "exp_" + \
                    str(len(data_diagnostics)) + "dia_" + str(fig_smile_selected)
        fig_name += "_relative_uncertainty" if uncertainty_relative is True else "_absolute_uncertainty"
        fig_name += "_theory" if uncertainty_theory is True else "_random"
        fig_name += "_" + str(uncertainty_confidence_interval) + "ci_" + str(fig_uncertainty_reference)
        if uncertainty_theory is True:
            fig_name += "_" + str(uncertainty_distribution) + "_distribution"
        fig_name += "_" + str(fig_orientation)
    fig_influence_of(uncertainties, data_diagnostics, data_experiments, fig_format, fig_name, fig_colors,
                     fig_legend_position, fig_linestyles, fig_linewidth, fig_linezorder, fig_markers, fig_marker_size,
                     fig_orientation, fig_panel_size, fig_ticks, fig_titles, 10, "epoch_length",
                     fig_uncertainty_reference, panel_param=panel_param)
# ---------------------------------------------------------------------------------------------------------------------#
