# -*- coding:UTF-8 -*-
# ---------------------------------------------------------------------------------------------------------------------#
# Figure R7 for the review of the paper about estimating_uncertainties_in_simulated_ENSO submitted to JAMES
# Plot: relationship between the departure from the theory of influence of the epoch length on the uncertainty of the
# ensemble mean computed for the mean state vs. the variance (e.g., x-axis is N3 PR mean and y-axis is N3 PR variance)
# ---------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------#
# Import packages
# ---------------------------------------------------#
# basic python package
from math import ceil as math__ceil
from random import randint
from typing import Literal
# estimating_uncertainties_enso package
from . params import default_parameters
from estimating_uncertainties_enso.compute_lib.data_lib import data_organize_json
from estimating_uncertainties_enso.compute_lib.nest_lib import deepcopy, nest_compute_uncertainty, \
    nest_influence_of_epoch_length
from estimating_uncertainties_enso.compute_lib.tool_lib import tool_put_in_dict
from estimating_uncertainties_enso.compute_lib.stat_lib import stat_regression
from estimating_uncertainties_enso.figure_templates.fig_template import fig_basic
from estimating_uncertainties_enso.figure_templates.fig_panel import default_plot
from estimating_uncertainties_enso.figure_templates.fig_tools import tool_figure_axis
# ---------------------------------------------------#


# ---------------------------------------------------------------------------------------------------------------------#
# Default arguments
# ---------------------------------------------------------------------------------------------------------------------#
default = {
    #
    # -- Data
    #
    # list of diagnostics
    "data_diagnostics": ["ave_pr_val_n30e", "ave_ts_val_n30e", "var_pr_ano_n30e", "var_ts_ano_n30e"],
    # list of epoch lengths
    "data_epoch_lengths": default_parameters["data_epoch_lengths"],
    # list of projects
    "data_projects": ["cmip6"],
    # list of experiments
    "data_experiments": ["historical"],
    # create the MME: True, False
    "data_mme_create": default_parameters["data_mme_create"],
    # MME made with all available SMILEs (or 1st SMILE of each model): True, False
    "data_mme_use_all_smiles": default_parameters["data_mme_use_all_smiles"],
    # MME made with ensemble means (or 1st member of each SMILE): True, False
    "data_mme_use_smile_mean": default_parameters["data_mme_use_smile_mean"],
    # minimum number of member for SMILEs: int [1, 100]
    "data_smile_minimum_size": default_parameters["data_smile_minimum_size"],
    # list of rejected SMILEs
    "data_smile_rejected": default_parameters["data_smile_rejected"],
    # require all experiments to keep SMILE: True, False
    "data_smile_require_all_experiments": default_parameters["data_smile_require_all_experiments"],
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
    # maximum of minimum value used as a reference for the plot
    "fig_uncertainty_reference": "maximum",
    # figure format: eps, pdf, png, svg
    "fig_format": default_parameters["fig_format"],
    # something added to figure name by user: str
    "fig_name_add": "",
    # figure name includes input parameters (may create a very long figure name)
    "fig_name_details": False,
    # figure orientation: column (column = variables, row = statistics), row (column = statistics, row = variables)
    "fig_orientation": default_parameters["fig_orientation"],
    # position of the legend on the plot: bottom, right
    "fig_legend_position": default_parameters["fig_legend_position"],
    # panel per line
    "fig_nbr_panel": 2,
    # size of each panel
    "fig_panel_size": {
        "frac": {"x": 0.25, "y": 0.25},
        "panel_1": {"x_delt": 7, "x_size": 16, "y_delt": 7, "y_size": 16},
    },
    # color per dataset
    "fig_colors": default_parameters["fig_colors"],
    # marker per dataset
    "fig_markers": default_parameters["fig_markers"],
    # marker size: all marker have the same size
    "fig_marker_size": 60.,
    # ticks
    "fig_ticks": {
        "maximum": {
            "030_year_epoch": {
                "ave_pr_val_n30e": [round(ii / 10, 1) for ii in list(range(-14, 15, 7))],
                "ave_ts_val_n30e": [round(ii / 10, 1) for ii in list(range(-14, 15, 7))],
                "var_pr_ano_n30e": [round(ii / 10, 1) for ii in list(range(-14, 15, 7))],
                "var_ts_ano_n30e": [round(ii / 10, 1) for ii in list(range(-14, 15, 7))],
            },
        },
    },
    # titles
    "fig_titles": {
        "x_axis": {
            "maximum": "ratio departure from theory",
        },
        "y_axis": {
            "maximum": "ratio departure from theory",
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
def r07_departure_from_theory(
        data_diagnostics: list = default["data_diagnostics"],
        data_epoch_lengths: list = default["data_epoch_lengths"],
        data_projects: list = default["data_projects"],
        data_experiments: list = default["data_experiments"],
        data_mme_create: bool = default["data_mme_create"],
        data_mme_use_all_smiles: bool = default["data_mme_use_all_smiles"],
        data_mme_use_smile_mean: bool = default["data_mme_use_smile_mean"],
        data_smile_minimum_size: int = default["data_smile_minimum_size"],
        data_smile_rejected: list = default["data_smile_rejected"],
        data_smile_require_all_experiments: bool = default["data_smile_require_all_experiments"],
        uncertainty_combinations: int = default["uncertainty_combinations"],
        uncertainty_confidence_interval: float = default["uncertainty_confidence_interval"],
        uncertainty_distribution: str = default["uncertainty_distribution"],
        uncertainty_relative: bool = default["uncertainty_relative"],
        uncertainty_resamples: int = default["uncertainty_resamples"],
        uncertainty_theory: bool = default["uncertainty_theory"],
        fig_colors: dict = default["fig_colors"],
        fig_format: Literal["eps", "pdf", "png", "svg"] = default["fig_format"],
        fig_legend_position: Literal["bottom", "right"] = default["fig_legend_position"],
        fig_markers: dict = default["fig_markers"],
        fig_marker_size: float = default["fig_marker_size"],
        fig_name_add: str = default["fig_name_add"],
        fig_name_details: bool = default["fig_name_details"],
        fig_nbr_panel: int = default["fig_nbr_panel"],
        fig_orientation: str = default["fig_orientation"],
        fig_panel_size: dict = default["fig_panel_size"],
        fig_ticks: dict = default["fig_ticks"],
        fig_titles: dict = default["fig_titles"],
        fig_uncertainty_reference: str = default["fig_uncertainty_reference"],
        panel_param: dict = default["panel_param"],
        **kwargs):
    #
    # -- Read json
    #
    values, metadata = data_organize_json(
        data_diagnostics, data_epoch_lengths, data_projects, data_experiments, data_mme_create=data_mme_create,
        data_mme_use_all_smiles=data_mme_use_all_smiles, data_mme_use_smile_mean=data_mme_use_smile_mean,
        data_smile_minimum_size=data_smile_minimum_size, data_smile_rejected=data_smile_rejected,
        data_smile_require_all_experiments=data_smile_require_all_experiments)
    #
    # -- Compute uncertainty
    #
    uncertainties, _, _ = nest_compute_uncertainty(
        values, uncertainty_confidence_interval, uncertainty_distribution, uncertainty_relative,
        uncertainty_combinations, uncertainty_resamples, uncertainty_theory)
    #
    # -- Compute the influence of the ensemble size on uncertainty
    #
    influence = nest_influence_of_epoch_length(uncertainties, fig_uncertainty_reference)
    #
    # -- Organize data to for figure
    #
    plot_data = {}
    list_ave = [k for k in data_diagnostics if k in list(influence.keys()) and k[:4] == "ave_"]
    list_var = [k for k in data_diagnostics if k in list(influence.keys()) and k[:4] == "var_"]
    list_dia_x, list_dia_y = list_ave + list_ave[-1:] + list_var[-1:], list_var + list_ave[:1] + list_var[:1]
    # markers
    for diax, diay in zip(list_dia_x, list_dia_y):
        list_dat = sorted(list(set(list(influence[diax].keys())) & set(list(influence[diay].keys()))), key=str.casefold)
        for dat in list_dat:
            list_exp = sorted(list(set(list(influence[diax][dat].keys())) &
                                   set(list(influence[diay][dat].keys()))), key=str.casefold)
            for exp in list_exp:
                list_siz = sorted(list(set(list(influence[diax][dat][exp].keys())) &
                                       set(list(influence[diay][dat][exp].keys()))), key=str.casefold)
                for siz in list_siz:
                    list_dur = [k for k in data_epoch_lengths if k in list(uncertainties[diax].keys())]
                    if fig_uncertainty_reference == "maximum":
                        list_dur = list(reversed(list_dur))
                    # first element not used as it is the reference epoch length, therefore the departure is 0
                    for ii, dur in enumerate(list_dur[1:]):
                        # dictionaries
                        d1, d2 = influence[diax][dat][exp][siz], influence[diay][dat][exp][siz]
                        # theoretical value
                        theory = (max(d1["x"]) / d1["x"][ii + 1])**0.5
                        # departure
                        x_val = d1["y"][ii + 1] - theory
                        y_val = d2["y"][ii + 1] - theory
                        # save values to plot
                        tmp = str(diax) + "--" + str(diay)
                        plot_type = "mar"
                        panel = "panel_1"
                        val = fig_colors[dat]
                        plot_data = tool_put_in_dict(plot_data, [val], dur, tmp, panel, str(plot_type) + "_cf")
                        val = fig_markers[dat]
                        plot_data = tool_put_in_dict(plot_data, [val], dur, tmp, panel, str(plot_type) + "_m")
                        val = deepcopy(fig_marker_size)
                        plot_data = tool_put_in_dict(plot_data, [val], dur, tmp, panel, str(plot_type) + "_s")
                        plot_data = tool_put_in_dict(plot_data, [x_val], dur, tmp, panel, str(plot_type) + "_x")
                        plot_data = tool_put_in_dict(plot_data, [y_val], dur, tmp, panel, str(plot_type) + "_y")
                        val = randint(1, 8)
                        plot_data = tool_put_in_dict(plot_data, [val], dur, tmp, panel, str(plot_type) + "_z")
    # axes
    method = "relative" if uncertainty_relative is True else "absolute"
    figure_axes = {}
    for dur in list(plot_data.keys()):
        for ii, dia in enumerate(list(plot_data[dur].keys())):
            for jj, pan in enumerate(list(plot_data[dur][dia].keys())):
                for k1, k2 in zip(["x", "y"], dia.split("--")):
                    t1 = str(k1) + "_axis"
                    # axis name
                    name = ""
                    if t1 in list(fig_titles.keys()) and fig_uncertainty_reference in list(fig_titles[t1].keys()):
                        name = str(fig_titles[k2]["x"]) + " " + str(fig_titles[k2]["z"]) + "\n" + \
                               str(fig_titles[method]) + " " + str(fig_titles[t1][fig_uncertainty_reference])
                    figure_axes = tool_put_in_dict(figure_axes, name, dur, dia, pan, str(k1) + "_nam")
                    # axis ticks
                    list_ticks, list_values = None, []
                    if dur in list(fig_ticks.keys()) and t1 in list(fig_ticks[dur].keys()) and \
                            isinstance(fig_ticks[dur][t1], dict) is True and dia in list(fig_ticks[dur][t1].keys()) \
                            and isinstance(fig_ticks[dur][t1][dia], list) is True:
                        list_ticks = fig_ticks[dur][t1][dia]
                    elif fig_uncertainty_reference in list(fig_ticks.keys()) and \
                            dur in list(fig_ticks[fig_uncertainty_reference].keys()) and \
                            k2 in list(fig_ticks[fig_uncertainty_reference][dur].keys()):
                        list_ticks = fig_ticks[fig_uncertainty_reference][dur][k2]
                    else:
                        for k3 in ["box", "cur", "mar", "sha"]:
                            if str(k3) + "_" + str(k1) in list(plot_data[dur][dia][pan].keys()):
                                list_values.append(plot_data[dur][dia][pan][str(k3) + "_" + str(k1)])
                            elif k3 == "sha":
                                for k4 in ["1", "2"]:
                                    if str(k3) + "_" + str(k1) + str(k4) in list(plot_data[dur][dia][pan].keys()):
                                        list_values.append(plot_data[dur][dia][pan][str(k3) + "_" + str(k1) + str(k4)])
                    list_labels, list_min_max, list_ticks = tool_figure_axis(list_ticks, arr_i=list_values)
                    figure_axes = tool_put_in_dict(figure_axes, list_labels, dur, dia, pan, str(k1) + "_lab")
                    figure_axes = tool_put_in_dict(figure_axes, list_min_max, dur, dia, pan, str(k1) + "_lim")
                    figure_axes = tool_put_in_dict(figure_axes, list_ticks, dur, dia, pan, str(k1) + "_tic")
                # title column
                if ii == 0 and jj + 1 == len(list(plot_data[dur][dia].keys())):
                    val = str(fig_titles[method]) + " " + str(fig_titles["x_axis"][fig_uncertainty_reference])
                    figure_axes = tool_put_in_dict(figure_axes, val, dur, dia, pan, "title_col")
                    val = 100 + fig_panel_size[pan]["x_delt"] * 50 / fig_panel_size[pan]["x_size"]
                    figure_axes = tool_put_in_dict(figure_axes, val, dur, dia, pan, "title_col_x")
                # title row
                if ii % fig_nbr_panel == 0:
                    val = "variance vs. mean" if ii == 0 else "PR vs. SST"
                    figure_axes = tool_put_in_dict(figure_axes, val, dur, dia, pan, "title_row")
                    figure_axes = tool_put_in_dict(figure_axes, 40, dur, dia, pan, "title_row_x")
    # linear regression
    for dur in list(plot_data.keys()):
        for dia in list(plot_data[dur].keys()):
            for pan in list(plot_data[dur][dia].keys()):
                x1, x2, y1, y2 = figure_axes[dur][dia][pan]["x_lim"] + figure_axes[dur][dia][pan]["y_lim"]
                dx = (x2 - x1) * default_plot["size_x"] / (
                        fig_panel_size[pan]["x_size"] * fig_panel_size["frac"]["x"] * 100)
                dy = (y2 - y1) * default_plot["size_y"] / (
                        fig_panel_size[pan]["y_size"] * fig_panel_size["frac"]["y"] * 100)
                if "mar_x" in list(plot_data[dur][dia][pan].keys()) and \
                        "mar_y" in list(plot_data[dur][dia][pan].keys()):
                    # values
                    x_val, y_val = plot_data[dur][dia][pan]["mar_x"], plot_data[dur][dia][pan]["mar_y"]
                    # regression
                    slope, intercept, correlation, p_value = stat_regression(x_val, y_val)
                    # regression line
                    plot_type = "cur"
                    plot_data = tool_put_in_dict(plot_data, [2], dur, dia, pan, str(plot_type) + "_lw")
                    val = [x1, x2]
                    plot_data = tool_put_in_dict(plot_data, [val], dur, dia, pan, str(plot_type) + "_x")
                    val = [k * slope + intercept for k in val]
                    plot_data = tool_put_in_dict(plot_data, [val], dur, dia, pan, str(plot_type) + "_y")
                    plot_data = tool_put_in_dict(plot_data, [9], dur, dia, pan, str(plot_type) + "_z")
                    # text (r, s, p)
                    plot_type = "text"
                    l1, l2 = ["r=", "s=", "p="], [correlation, slope, p_value]
                    for kk, (tt, vv) in enumerate(zip(l1, l2)):
                        val = str(tt) + "{0:.3f}".format(round(vv, 3))
                        plot_data = tool_put_in_dict(plot_data, [val], dur, dia, pan, plot_type)
                        plot_data = tool_put_in_dict(plot_data, ["right"], dur, dia, pan, str(plot_type) + "_ha")
                        plot_data = tool_put_in_dict(plot_data, [x2 - 2 * dx], dur, dia, pan, str(plot_type) + "_x")
                        val = y1 + 7 * dy * (len(l1) - 0.3 - kk)
                        plot_data = tool_put_in_dict(plot_data, [val], dur, dia, pan, str(plot_type) + "_y")
    # legend
    for dur in list(plot_data.keys()):
        for ii, dia in enumerate(list(plot_data[dur].keys())):
            for jj, pan in enumerate(list(plot_data[dur][dia].keys())):
                nn, mm = len(list(plot_data[dur].keys())), len(list(plot_data[dur][dia].keys()))
                if (fig_legend_position == "bottom" and jj == 0 and ii % fig_nbr_panel == 0 and
                        ii >= nn - fig_nbr_panel) or (
                        fig_legend_position == "right" and jj == mm - 1 and ii == min(nn, fig_nbr_panel) - 1):
                    # list dataset
                    list_datasets = []
                    for pro in list(values[dia.split("--")[0]][dur].keys()):
                        for exp in list(values[dia.split("--")[0]][dur][pro].keys()):
                            list_datasets += list(values[dia.split("--")[0]][dur][pro][exp].keys())
                    list_datasets = sorted(list(set(list_datasets)), key=str.casefold)
                    # positions
                    if fig_legend_position == "bottom":
                        # legend added under the bottom left panel
                        n_per_col = math__ceil(len(list_datasets) / (fig_nbr_panel * 2))
                        x0, x1, y0, y1 = -30, 75, -35, 8
                    else:
                        # legend added to the right the top right panel
                        n_per_col = len(list_datasets)
                        x0, x1, y0, y1 = 105, 0, 94, 8
                    x1 *= default_plot["size_x"] / (fig_panel_size[pan]["x_size"] * fig_panel_size["frac"]["x"])
                    y1 *= default_plot["size_y"] / (fig_panel_size[pan]["y_size"] * fig_panel_size["frac"]["y"])
                    leg_d = {}
                    for k1, k2 in enumerate(list_datasets):
                        leg_d[k2] = {"text": {"color": fig_colors[k2], "fontsize": 12}}
                        leg_d[k2]["marker"] = {"facecolor": fig_colors[k2], "marker": fig_markers[k2], "s": 80}
                        leg_d[k2]["position"] = {"x": x0 + x1 * (k1 // n_per_col), "y": y0 - y1 * (k1 % n_per_col)}
                    for k1 in list(leg_d.keys()):
                        for k2 in list(leg_d[k1].keys()):
                            for k3 in list(leg_d[k1][k2].keys()):
                                plot_data = tool_put_in_dict(plot_data, leg_d[k1][k2][k3], dur, dia, pan,
                                                             "legend_param", k1, k2, k3)
                    plot_data = tool_put_in_dict(plot_data, list_datasets, dur, dia, pan, "legend_txt")
    #
    # -- Figure
    #
    for dur in sorted(list(plot_data.keys()), key=str.casefold)[:1]:
        # output figure name will be the file name (path removed and extension removed)
        fig_name = __file__.split("/")[-1].split(".")[0] + "_" + str(dur) + str(fig_name_add)
        if fig_name_details is True:
            # add details of the computation to the figure name
            fig_name += "_data_" + str(len(data_projects)) + "pro_" + str(len(data_experiments)) + "exp_" + \
                        str(data_smile_minimum_size) + "mem_" + str(len(data_diagnostics)) + "dia"
            if data_mme_create is True:
                fig_name += "_mme"
                fig_name += "_of_em" if data_mme_use_smile_mean is True else "_of_1m"
                fig_name += "_all_smile" if data_mme_use_all_smiles is True else "_1st_smile"
            fig_name += "_relative_uncertainty" if uncertainty_relative is True else "_absolute_uncertainty"
            fig_name += "_theory" if uncertainty_theory is True else "_random"
            fig_name += "_" + str(uncertainty_confidence_interval) + "ci_" + str(fig_uncertainty_reference)
            if uncertainty_theory is True:
                fig_name += "_" + str(uncertainty_distribution) + "_distribution"
            fig_name += "_" + str(fig_orientation)
        fig_basic(plot_data[dur], list(plot_data[dur].keys()), fig_nbr_panel, figure_axes[dur], fig_format, fig_name,
                  fig_panel_size, panel_position="bottom", panel_param=panel_param)
# ---------------------------------------------------------------------------------------------------------------------#
