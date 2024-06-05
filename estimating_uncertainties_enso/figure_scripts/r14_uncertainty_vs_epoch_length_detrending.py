# -*- coding:UTF-8 -*-
# ---------------------------------------------------------------------------------------------------------------------#
# Figure R11 for the review of the paper about estimating_uncertainties_in_simulated_ENSO submitted to JAMES
# Plot: influence of the epoch length on the uncertainty of the ensemble mean
# This time a single very large SMILE is used (fig_smile_selected) and the values are plotted for different detrending
# methods
# ---------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------#
# Import packages
# ---------------------------------------------------#
# basic python package
from copy import deepcopy
# estimating_uncertainties_enso package
from . params import default_parameters
from estimating_uncertainties_enso.compute_lib.data_lib import data_organize_json
from estimating_uncertainties_enso.compute_lib.nest_lib import nest_compute_uncertainty, nest_influence_of_epoch_length
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
    # file name
    "data_filename": "estimating_uncertainties_in_simulated_enso_for_review.json",
    # list of diagnostics
    "data_diagnostics": ["ave_pr_val_n30e_d0", "ave_pr_val_n30e_d1", "ave_pr_val_n30e_d2", "ave_pr_val_n30e_de",
                         "ave_ts_val_n30e_d0", "ave_ts_val_n30e_d1", "ave_ts_val_n30e_d2", "ave_ts_val_n30e_de",
                         "var_pr_ano_n30e_d0", "var_pr_ano_n30e_d1", "var_pr_ano_n30e_d2", "var_pr_ano_n30e_de",
                         "var_ts_ano_n30e_d0", "var_ts_ano_n30e_d1", "var_ts_ano_n30e_d2", "var_ts_ano_n30e_de",
                         "ske_pr_ano_n30e_d0", "ske_pr_ano_n30e_d1", "ske_pr_ano_n30e_d2", "ske_pr_ano_n30e_de",
                         "ske_ts_ano_n30e_d0", "ske_ts_ano_n30e_d1", "ske_ts_ano_n30e_d2", "ske_ts_ano_n30e_de"],
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
    #
    # -- Figure
    #
    # SMILE to plot (largest SMILEs: ACCESS-ESM1-5 = 40, CanESM5_p2 = 40, CanESM5-1 = 47, HadGEM3-GC31-LL = 55,
    # IPSL-CM6A-LR = 33, MIROC-ES2L = 30, MIROC6 = 50, MPI-ESM1-2-LR = 50, NorCPM1 = 30)
    "fig_smile_selected": "IPSL-CM6A-LR",
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
    "fig_colors": {"none": "dodgerblue", "linear": "limegreen", "quadratic": "goldenrod", "cubic": "darkorchid",
                   "ensemble mean": "r"},
    # linestyle per experiment
    "fig_linestyles": default_parameters["fig_linestyles"],
    # linewidth: all lines have the same width
    "fig_linewidth": 3.,
    # linezorder: all lines have the same zorder; e.g., zorder = 2 is plotted over zorder = 1
    "fig_linezorder": 1,
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
                    "ave_pr_val_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "ave_ts_val_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "ske_pr_ano_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "ske_ts_ano_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "var_pr_ano_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "var_ts_ano_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                },
                "CanESM5_p2": {
                    "ave_pr_val_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "ave_ts_val_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "ske_pr_ano_n30e": [round(k / 10, 1) for k in list(range(5, 26, 5))],
                    "ske_ts_ano_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "var_pr_ano_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "var_ts_ano_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                },
                "CanESM5-1": {
                    "ave_pr_val_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "ave_ts_val_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "ske_pr_ano_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "ske_ts_ano_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "var_pr_ano_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "var_ts_ano_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                },
                "HadGEM3-GC31-LL": {
                    "ave_pr_val_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "ave_ts_val_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "ske_pr_ano_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "ske_ts_ano_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "var_pr_ano_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "var_ts_ano_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                },
                "IPSL-CM6A-LR": {
                    "ave_pr_val_n30e": [round(k / 10, 1) for k in list(range(10, 27, 4))],
                    "ave_ts_val_n30e": [round(k / 10, 1) for k in list(range(10, 27, 4))],
                    "ske_pr_ano_n30e": [round(k / 10, 1) for k in list(range(10, 27, 4))],
                    "ske_ts_ano_n30e": [round(k / 10, 1) for k in list(range(10, 27, 4))],
                    "var_pr_ano_n30e": [round(k / 10, 1) for k in list(range(10, 27, 4))],
                    "var_ts_ano_n30e": [round(k / 10, 1) for k in list(range(10, 27, 4))],
                },
                "MIROC-ES2L": {
                    "ave_pr_val_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "ave_ts_val_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "ske_pr_ano_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "ske_ts_ano_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "var_pr_ano_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "var_ts_ano_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                },
                "MIROC6": {
                    "ave_pr_val_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "ave_ts_val_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "ske_pr_ano_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "ske_ts_ano_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "var_pr_ano_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "var_ts_ano_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                },
                "MPI-ESM1-2-LR": {
                    "ave_pr_val_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "ave_ts_val_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "ske_pr_ano_n30e": [round(k / 10, 1) for k in list(range(0, 21, 5))],
                    "ske_ts_ano_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "var_pr_ano_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "var_ts_ano_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                },
                "NorCPM1": {
                    "ave_pr_val_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "ave_ts_val_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "ske_pr_ano_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "ske_ts_ano_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "var_pr_ano_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "var_ts_ano_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
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
def r14_epoch_length_detrending(
        data_diagnostics: list = default["data_diagnostics"],
        data_epoch_lengths: list = default["data_epoch_lengths"],
        data_filename: str = default["data_filename"],
        data_projects: list = default["data_projects"],
        data_experiments: list = default["data_experiments"],
        uncertainty_combinations: int = default["uncertainty_combinations"],
        uncertainty_confidence_interval: float = default["uncertainty_confidence_interval"],
        uncertainty_distribution: str = default["uncertainty_distribution"],
        uncertainty_relative: bool = default["uncertainty_relative"],
        uncertainty_resamples: int = default["uncertainty_resamples"],
        uncertainty_theory: bool = default["uncertainty_theory"],
        fig_colors: dict = default["fig_colors"],
        fig_detailed_name: bool = default["fig_detailed_name"],
        fig_format: str = default["fig_format"],
        fig_legend_position: str = default["fig_legend_position"],
        fig_linestyles: dict = default["fig_linestyles"],
        fig_linewidth: float = default["fig_linewidth"],
        fig_linezorder: int = default["fig_linezorder"],
        fig_marker: str = default["fig_marker"],
        fig_marker_size: float = default["fig_marker_size"],
        fig_orientation: str = default["fig_orientation"],
        fig_panel_size: dict = default["fig_panel_size"],
        fig_smile_selected: str = default["fig_smile_selected"],
        fig_ticks: dict = default["fig_ticks"],
        fig_titles: dict = default["fig_titles"],
        fig_uncertainty_reference: str = default["fig_uncertainty_reference"],
        panel_param: dict = default["panel_param"],
        **kwargs):
    #
    # -- Read json
    #
    values, metadata = data_organize_json(data_diagnostics, data_epoch_lengths, data_projects, data_experiments,
                                          data_filename=data_filename)
    #
    # -- Reorder dictionary and keep only the selected dataset
    #
    values_new = {}
    for dia in list(values.keys()):
        for dur in list(values[dia].keys()):
            for pro in list(values[dia][dur].keys()):
                for exp in list(values[dia][dur][pro].keys()):
                    dat = deepcopy(fig_smile_selected)
                    if exp != "historical" or dat not in list(values[dia][dur][pro][exp].keys()):
                        # do not continue the computation but continue the loop if the selected dataset is not available
                        continue
                    for epo in list(values[dia][dur][pro][exp][dat].keys()):
                        values_new = tool_put_in_dict(values_new, values[dia][dur][pro][exp][dat][epo], dia, dur, pro,
                                                      exp, dat, epo)
    #
    # -- Compute uncertainty
    #
    uncertainties, _, _ = nest_compute_uncertainty(
        values_new, uncertainty_confidence_interval, uncertainty_distribution, uncertainty_relative,
        uncertainty_combinations, uncertainty_resamples, uncertainty_theory)
    #
    # -- Compute the influence of the ensemble size on uncertainty
    #
    influence = nest_influence_of_epoch_length(uncertainties, fig_uncertainty_reference)
    #
    # -- Organize data to for figure
    #
    # data to plot
    data_to_plot = {}
    dict_detrend = {0: "none", 1: "linear", 2: "quadratic", 3: "cubic", "e": "ensemble mean"}
    for dia in list(influence.keys()):
        for dat in list(influence[dia].keys()):
            for exp in list(influence[dia][dat].keys()):
                for siz in list(influence[dia][dat][exp].keys()):
                    for axi in list(influence[dia][dat][exp][siz].keys()):
                        # get array
                        arr = influence[dia][dat][exp][siz][axi]
                        # output keys
                        dia_o = deepcopy(dia)
                        det_o = deepcopy(dict_detrend[1])
                        for k in list(range(4)) + ["e"]:
                            if "_d" + str(k) in dia_o:
                                dia_o = dia.replace("_d" + str(k), "")
                                det_o = deepcopy(dict_detrend[k])
                                break
                        # save value
                        data_to_plot = tool_put_in_dict(data_to_plot, arr, dia_o, det_o, exp, siz, axi)
    list_dia = list(data_to_plot.keys())
    list_dia = [k for k in list_dia if k[:4] == "ave_"] + [k for k in list_dia if k[:4] == "var_"] + \
               [k for k in list_dia if k[:4] == "ske_"]
    # panels, axes, titles
    method = "relative" if uncertainty_relative is True else "absolute"
    for dia in list_dia:
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
    fig_markers = dict((k, fig_marker) for k in list(fig_colors.keys()))
    #
    # -- Figure
    #
    # output figure name will be the file name (path removed and extension removed)
    fig_name = __file__.split("/")[-1].split(".")[0] + "_" + str(fig_smile_selected)
    if fig_detailed_name is True:
        # add details of the computation to the figure name
        fig_name += "_data_" + str(len(data_projects)) + "pro_" + str(len(data_experiments)) + "exp_" + \
                    str(len(list_dia)) + "dia_" + str(fig_smile_selected)
        fig_name += "_relative_uncertainty" if uncertainty_relative is True else "_absolute_uncertainty"
        fig_name += "_theory" if uncertainty_theory is True else "_random"
        fig_name += "_" + str(uncertainty_confidence_interval) + "ci_" + str(fig_uncertainty_reference)
        if uncertainty_theory is True:
            fig_name += "_" + str(uncertainty_distribution) + "_distribution"
        fig_name += "_" + str(fig_orientation)
    fig_influence_of(data_to_plot, list_dia, data_experiments, fig_format, fig_name, fig_colors,
                     fig_legend_position, fig_linestyles, fig_linewidth, fig_linezorder, fig_markers, fig_marker_size,
                     fig_orientation, fig_panel_size, fig_ticks, fig_titles, 10, "epoch_length",
                     fig_uncertainty_reference, panel_param=panel_param)
# ---------------------------------------------------------------------------------------------------------------------#
