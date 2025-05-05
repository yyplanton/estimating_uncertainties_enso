# -*- coding:UTF-8 -*-
# ---------------------------------------------------------------------------------------------------------------------#
# Figure templates for the paper about estimating_uncertainties_in_simulated_ENSO submitted to JAMES
# ---------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------#
# Import packages
# ---------------------------------------------------#
# basic python package
from copy import deepcopy
from math import ceil as math__ceil
import os
from random import randint as random__randint
import string
from typing import Literal
# cartopy
import cartopy.crs as ccrs
# matplotlib
from matplotlib.gridspec import GridSpec
import matplotlib.pyplot as plt
# numpy
from numpy import linspace as numpy__linspace
# estimating_uncertainties_enso package
from . fig_panel import default_map, default_plot, plot_main, plot_map
from . fig_tools import tool_axis_label, tool_figure_axis, tool_figure_initialization, tool_legend_datasets, tool_title
from estimating_uncertainties_enso.compute_lib.check_lib import plural_s
from estimating_uncertainties_enso.compute_lib.stat_lib import stat_regression
# ---------------------------------------------------#


# ---------------------------------------------------------------------------------------------------------------------#
# Figure templates
# ---------------------------------------------------------------------------------------------------------------------#
def fig_basic(
        dict_i: dict[str, dict[str, dict[str, list[float | int] | list[list[float | int]] | str]]],
        list_panel_group: list[str],
        n_panel_per_line: int,
        fig_axes: dict[str, dict[str, dict[str, float | int | list[float | int] | str | None]]],
        fig_format: Literal["eps", "pdf", "png", "svg"],
        fig_name: str,
        fig_panel_size: dict[str, dict[str, float | int]],
        fig_title_bool: bool = True,
        panel_position: Literal["bottom", "right"] = "right",
        panel_param: dict = None):
    # set None input to it's default value
    if panel_param is None:
        panel_param = {}
    # plot initialization
    x_frac, y_frac = fig_panel_size["frac"]["x"], fig_panel_size["frac"]["y"]
    panel_names = sorted([k for k in list(fig_panel_size.keys()) if k != "frac"], key=str.casefold)
    nbr_c, nbr_l = 0, 0
    for ii, grp in enumerate(list_panel_group):
        tmp_c, tmp_l = 0, 0
        for jj, pan in enumerate(list(dict_i[grp].keys())):
            if panel_position == "bottom":
                # panels are place in columns (i.e., panel 2 under panel 1)
                # number of columns (width) is the maximum panel width (x_size)
                tmp_c = max(tmp_c, fig_panel_size[pan]["x_size"])
                if jj + 1 == len(list(dict_i[grp].keys())) and (ii + 1) % n_panel_per_line != 0:
                    tmp_c += fig_panel_size[pan]["x_delt"]
                # number of lines (length) is the sum of panel length and space between (y_size + y_delt)
                tmp_l += fig_panel_size[pan]["y_delt"] + fig_panel_size[pan]["y_size"]
            else:
                # panels are place in lines (i.e., panel 2 on the right of panel 1)
                # number of columns (width) is the sum of panel width and space between (x_size + x_delt)
                tmp_c += fig_panel_size[pan]["x_delt"] + fig_panel_size[pan]["x_size"]
                # number of lines (length) is the maximum panel length (y_size)
                tmp_l = max(tmp_l, fig_panel_size[pan]["y_size"])
                if jj + 1 == len(list(dict_i[grp].keys())):
                    tmp_l += fig_panel_size[pan]["y_delt"]
        if ii + 1 > n_panel_per_line:
            # the maximum number of panel groups in a line has been reached, now only the number of lines is increased
            nbr_c = max(nbr_c, tmp_c)
            nbr_l += tmp_l
        else:
            nbr_c += tmp_c
            nbr_l += max(nbr_l, tmp_l)
    plt.figure(0, figsize=(nbr_c * x_frac, nbr_l * y_frac))
    gs = GridSpec(nbr_l, nbr_c)
    numbering = string.ascii_lowercase
    x_position, y_position = 0, 0
    counter = 0
    for ii, grp in enumerate(list_panel_group):
        list_panels = [k for k in panel_names if k in list(dict_i[grp].keys())]
        for jj, pan in enumerate(list_panels):
            x_delt, y_delt = fig_panel_size[pan]["x_delt"], fig_panel_size[pan]["y_delt"]
            x_size, y_size = fig_panel_size[pan]["x_size"], fig_panel_size[pan]["y_size"]
            kwarg = {**panel_param, **{"x_size": x_size * x_frac, "y_size": y_size * y_frac}}
            if grp in list(dict_i.keys()) and pan in list(dict_i[grp].keys()):
                # data to plot
                kwarg.update(dict_i[grp][pan])
                # panel number
                if fig_title_bool is True:
                    kwarg["title"] = numbering[counter]
                # panel axes
                kwarg.update(fig_axes[grp][pan])
                # check x/y axes
                for k1 in ["x", "y"]:
                    if str(k1) + "_lab" not in list(kwarg.keys()) or str(k1) + "_tic" not in list(kwarg.keys()) or (
                            str(k1) + "_lab" in list(kwarg.keys()) and kwarg[str(k1) + "_lab"] is None) or (
                            str(k1) + "_tic" in list(kwarg.keys()) and kwarg[str(k1) + "_tic"] is None):
                        tic = None if str(k1) + "_tic" not in list(kwarg.keys()) else kwarg[str(k1) + "_tic"]
                        val = []
                        for k2 in ["box", "cur", "mar", "sha"]:
                            if str(k2) + "_" + str(k1) in list(kwarg.keys()):
                                val.append(kwarg[str(k2) + "_" + str(k1)])
                            elif k2 == "sha":
                                for k3 in ["1", "2"]:
                                    if str(k2) + "_" + str(k1) + str(k3) in list(kwarg.keys()):
                                        val.append(kwarg[str(k2) + "_" + str(k1) + str(k3)])
                        kwarg[str(k1) + "_lab"], kwarg[str(k1) + "_lim"], kwarg[str(k1) + "_tic"] = \
                            tool_figure_axis(tic, arr_i=val)
                # plot
                ax = plt.subplot(gs[y_position: y_position + y_size, x_position: x_position + x_size])
                plot_main(ax, **kwarg)
            if len(list_panels) > 1 and panel_position == "bottom":
                y_position += y_size + y_delt
            else:
                x_position += x_size + x_delt
            if (ii + 1) % n_panel_per_line == 0 and (jj + 1) == len(list_panels):
                x_position = 0
                y_position += y_size + y_delt
            counter += 1
    # plot directory (relative to current file directory)
    plot_directory = "/".join(os.path.dirname(__file__).split("/")[:-2])
    # path to output figure
    figure_file_path = os.path.join(plot_directory, "plot/" + str(fig_name)) + "." + str(fig_format)
    # save
    plt.savefig(figure_file_path, bbox_inches="tight", format=fig_format)
    plt.close()
    return


def fig_distribution_and_ensemble_size(
        dict_distributions: dict,
        dict_influence: dict,
        data_diagnostics: list,
        data_experiments: list,
        fig_format: str,
        fig_name: str,
        fig_box_linestyle: str,
        fig_box_linewidth: float,
        fig_box_mean_size: float,
        fig_box_outlier_size: float,
        fig_colors: dict,
        fig_linewidth: float,
        fig_linezorder: int,
        fig_markers: dict,
        fig_panel_size: dict,
        fig_smile_selected: str,
        fig_threshold: float,
        fig_ticks: dict,
        fig_titles: dict,
        uncertainty_reference: str,
        panel_param_distributions: dict = None,
        panel_param_influence: dict = None):
    """
    Template for S11:
         - Normalized distributions of diagnostics of all datasets
         - Influence of ensemble size on the uncertainty of the ensemble mean for given cases
    
    Inputs:
    -------
    :param dict_distributions: dict
        Dictionary with four nested levels [diagnostic, experiment, boxplot-or-marker, x-or-y], filled with the data to
        plot as boxplots or markers
    :param dict_influence: dict
        Dictionary with four nested levels [diagnostic, dataset, experiment, key], filled with the data to plot
    :param data_diagnostics: list
        Names of diagnostic (to keep them in the right order);
        e.g., data_diagnostics = ['ave_pr_val_n30e', 'ave_ts_val_n30e']
    :param data_experiments: list
        Names of experiment (to keep them in the right order); e.g., data_experiments = ['piControl', 'historical']
    :param fig_format: str
        Format of the figure; e.g., fig_format = 'pdf'
        Four figure formats are accepted: 'eps', 'pdf', 'png', 'svg'
    :param fig_name: str
        Name of the output file; e.g., fig_name = 'name_of_the_figure'
    :param fig_box_linestyle: str
        Style of the lines for boxplots; e.g., fig_box_linestyle = '-'
    :param fig_box_linewidth: float
        Width of the lines for boxplots; e.g., fig_box_linewidth = 1.
    :param fig_box_mean_size: float
        Size of the mean markers for boxplots; e.g., fig_box_mean_size = 10.
    :param fig_box_outlier_size: float
        Size of the outlier markers for boxplots; e.g., fig_box_outlier_size = 2.
    :param fig_colors: dict
        Dictionary with one level [dataset], filled with the color to plot each dataset;
        e.g., fig_colors = {'ACCESS-CM2': 'orange', 'ACCESS-ESM1-5': 'forestgreen'}
    :param fig_linewidth: float
        Width of the lines; e.g., fig_linewidth = 1.
    :param fig_linezorder: int
        zorder of the lines; e.g., fig_linezorder = 1
    :param fig_markers: dict
        Dictionary with one level [dataset], filled with the marker to plot each dataset;
        e.g., fig_markers = {'ACCESS-CM2': '>', 'ACCESS-ESM1-5': '<'}
    :param fig_panel_size: dict
        Dictionary defining the size of each panel;
        e.g., fig_panel_size = {'x_delt': 2, 'x_frac': 0.5, 'x_size': 5, 'y_delt': 3, 'y_frac': 0.5, 'y_size': 8}
        'x' and 'y' correspond respectively to the x-axis (horizontal) and y-axis (vertical)
        'delt' is the distance between panels (in inches)
        'size' is the size of each panel (in inches)
        'frac' is a fraction to multiply 'delt' and 'size' (to shrink or expend figure proportionally)
    :param fig_smile_selected: str
        Name of a smile selected to be highlighted in the figure; e.g., fig_smile_selected = 'MPI-ESM1-2-LR'
    :param fig_threshold: float
        Threshold to indicate in the figure; e.g., fig_threshold = 4.
    :param fig_ticks: dict
        Dictionary with two nested levels [x-or-y_axis, diagnostic], filled with a list of tics;
        e.g., fig_ticks = {
            'distribution': {
                'x_axis': {'ave_pr_val_n30e': [0, 1]},
                'y_axis': None,
            },
            'influence': {
                'x_axis': [0, 0.5, 1.0],
                'y_axis': {'ave_pr_val_n30e': [0, 1, 2, 3, 4]},
            },
        }
    :param fig_titles: dict
        Dictionary defining the titles of panels and axes;
        e.g., fig_titles = {
            'ave_pr_val_n30e': {'x': 'N3 PR', 'y': 'mean', 'z': 'xbar'},
            'x_axis': {'ave_pr_val_n30e': ''},
            'y_axis': {'ave_pr_val_n30e': 'N3 PR xbar (mm/day)'},
        }
    :param uncertainty_reference: str
        Reference plotted (used to select plot legend); e.g., uncertainty_reference = 'maximum'
        One reference is recognized: 'maximum'
        Other values will have no effect
    :param panel_param_distributions: dict, optional
        Dictionary to modify default values of panel parameters for boxplots (see fig_panel.py);
        e.g., panel_param_distributions = {'x_nbr_minor': 0}
        Default is None (no modification of the default values)
    :param panel_param_influence: dict, optional
        Dictionary to modify default values of panel parameters for curves (see fig_panel.py);
        e.g., panel_param_influence = {'x_nbr_minor': 0}
        Default is None (no modification of the default values)
    """
    if panel_param_distributions is None:
        panel_param_distributions = {}
    if panel_param_influence is None:
        panel_param_influence = {}
    # plot initialization
    x_delt, x_frac, x_size = fig_panel_size["x_delt_box"], fig_panel_size["x_frac_box"], fig_panel_size["x_size_box"]
    y_delt, y_frac, y_size = fig_panel_size["y_delt_box"], fig_panel_size["y_frac_box"], fig_panel_size["y_size_box"]
    x_size_cur, y_size_cur = fig_panel_size["x_size_cur"], fig_panel_size["y_size_cur"]
    nbr_c = x_size + x_delt + x_size_cur
    nbr_l = len(data_diagnostics) * (max(y_size, y_size_cur) + y_delt) - y_delt
    plt.figure(0, figsize=(nbr_c * x_frac, nbr_l * y_frac))
    gs = GridSpec(nbr_l, nbr_c)
    numbering = string.ascii_lowercase
    x_position, y_position = 0, 0
    counter = 0
    for jj, dia in enumerate(data_diagnostics):
        #
        # -- Boxplot
        #
        kwarg = {**panel_param_distributions, **{"x_size": x_size * x_frac, "y_size": y_size * y_frac}}
        # list data types
        list_typ = list(dict_distributions[dia].keys())
        # boxplot
        arr_c, arr_x, arr_y = [], [], []
        for typ in list_typ:
            d1 = dict_distributions[dia][typ]
            arr_c += [fig_colors[typ]] * len(d1["x"])
            arr_x += d1["x"] if isinstance(d1["x"], list) is True else [d1["x"]]
            arr_y += d1["y"] if isinstance(d1["y"], list) is True else [d1["y"]]
        kwarg.update({"box_c": arr_c, "box_fs": [fig_box_outlier_size] * len(arr_x),
                      "box_ls": [fig_box_linestyle] * len(arr_x), "box_lw": [fig_box_linewidth] * len(arr_x),
                      "box_ms": [fig_box_mean_size] * len(arr_x), "box_vert": [False] * len(arr_x), "box_x": arr_x,
                      "box_y": arr_y})
        # title
        kwarg["title"] = numbering[counter]
        # x-axis
        kwarg["x_lab"], kwarg["x_lim"], kwarg["x_tic"] = tool_figure_axis(
            fig_ticks["distribution"]["x_axis"][dia], arr_i=arr_y)
        kwarg["x_nam"] = fig_titles["distribution"]["x_axis"] + \
            fig_titles[dia]["x"] + " " + fig_titles[dia]["z"]
        # y-axis
        list_datasets = dict_distributions[dia][list_typ[0]]["x_tick_labels"]
        kwarg["y_tic"] = list(range(len(list_datasets)))
        kwarg["y_lab"] = [""] * len(list_datasets)
        kwarg["y_lim"] = [min(kwarg["y_tic"]) - 0.5, max(kwarg["y_tic"]) + 0.5]
        # text
        x1, x2, y1, y2 = kwarg["x_lim"] + kwarg["y_lim"]
        dx = (x2 - x1) * default_plot["size_x"] / (x_size * x_frac * 100)
        arr_c, arr_x, arr_y = [], [], []
        for ii, dat in enumerate(list_datasets):
            cc = "k"
            if dat in list(fig_colors.keys()):
                cc = fig_colors[dat]
            elif dat == fig_smile_selected and "DATASET" in list(fig_colors.keys()):
                cc = fig_colors["DATASET"]
            elif "other LEs" in list(fig_colors.keys()):
                cc = fig_colors["other LEs"]
            arr_c.append(cc)
            arr_x.append(x1 - 4 * dx)
            arr_y.append(ii)
        for typ in list_typ:
            for k1, k2 in zip(dict_distributions[dia][typ]["x"], dict_distributions[dia][typ]["z"]):
                list_datasets.append("{0:.1f}".format(round(k2, 1)))
                arr_c.append(fig_colors[typ])
                arr_x.append(x1 + 70 * dx)
                arr_y.append(k1)
        kwarg.update({"text": list_datasets, "text_c": arr_c, "text_fs": [12] * len(arr_x),
                      "text_ha": ["right"] * len(arr_x), "text_va": ["center"] * len(arr_x), "text_x": arr_x,
                      "text_y": arr_y})
        # curves (line between datasets)
        arr_y = [[ii + 0.5, ii + 0.5] for ii, _ in enumerate(list_datasets[: -1])]
        arr_c, arr_lw, arr_x = ["k"] * len(arr_y), [1] * len(arr_y), [[x1, x2]] * len(arr_y)
        # threshold (curve)
        arr_c += [fig_colors["DAT w/o outliers"] if "DAT w/o outliers" in list(fig_colors.keys()) else "k"]
        arr_lw += [2]
        arr_x += [[fig_threshold, fig_threshold]]
        arr_y += [kwarg["y_lim"]]
        kwarg.update({"cur_c": arr_c, "cur_lw": arr_lw, "cur_x": arr_x, "cur_y": arr_y, "cur_z": [1] * len(arr_y)})
        # plot
        ax = plt.subplot(gs[y_position: y_position + y_size, x_position: x_position + x_size])
        plot_main(ax, **kwarg)
        counter += 1
        x_position += x_size + x_delt
        #
        # -- Influence
        #
        kwarg = {**panel_param_influence, **{"x_size": x_size_cur * x_frac, "y_size": y_size_cur * y_frac}}
        # dictionary
        d1 = dict_influence[dia]
        # curves
        cur_c, cur_ls, cur_lw, cur_x, cur_y, cur_z = [], [], [], [], [], []
        for dat in list(d1.keys()):
            for exp in list(d1[dat].keys()):
                for k1 in list(d1[dat][exp].keys()):
                    d2 = d1[dat][exp][k1]
                    col = fig_colors[dat]
                    if isinstance(d2["x"], list) is True and isinstance(d2["x"][0], list) is True:
                        xx, yy = d2["x"], d2["y"]
                    else:
                        xx, yy = [d2["x"]], [d2["y"]]
                    # curves
                    for k2, k3 in zip(xx, yy):
                        cur_c.append(col)
                        cur_ls.append("-")
                        cur_lw.append(fig_linewidth - 1 if col == "grey" else fig_linewidth)
                        cur_x.append(k2)
                        cur_y.append(k3)
                        cur_z.append(fig_linezorder if col == "grey" else fig_linezorder + 1)
        # title
        kwarg["title"] = numbering[counter]
        # x-axis
        kwarg["x_lab"], kwarg["x_lim"], kwarg["x_tic"] = tool_figure_axis(
            fig_ticks["influence"]["x_axis"][uncertainty_reference], arr_i=cur_x)
        if uncertainty_reference == "maximum" and fig_ticks["influence"]["x_axis"][uncertainty_reference] is not None:
            kwarg["x_lim"][0] -= 0.1
        kwarg["x_nam"] = fig_titles["influence"]["x_axis"][uncertainty_reference]
        # y-axis
        kwarg["y_lab"], kwarg["y_lim"], kwarg["y_tic"] = tool_figure_axis(
            fig_ticks["influence"]["y_axis"][uncertainty_reference][dia], arr_i=cur_y)
        kwarg["y_nam"] = fig_titles["influence"]["y_axis"][uncertainty_reference]
        # legend
        leg_t = [r"y = $\sqrt{\frac{1}{x}}$"] if uncertainty_reference == "maximum" else [r"y = $\sqrt{\frac{x_0}{x}}$"]
        list_experiments = sorted(list(set([k2 for k1 in list(d1.keys()) for k2 in list(d1[k1].keys())])),
                                  key=str.casefold)
        list_experiments = [fig_titles[k] for k in data_experiments if k in list_experiments]
        leg_t += ["experiment%s: %s" % (plural_s(list_experiments), " & ".join(list_experiments))]
        list_durations = sorted(list(set([int(k3.split("_")[0]) for k1 in list(d1.keys())
                                          for k2 in list(d1[k1].keys()) for k3 in list(d1[k1][k2].keys())])))
        tmp = "epoch length%s: " % plural_s(list_durations)
        if len(list_durations) == 1:
            tmp += str(list_durations[0])
        elif len(list_durations) == 2:
            tmp += " & ".join(str(k) for k in list_durations)
        else:
            tmp += str(list_durations[0]) + " to " + str(list_durations[-1])
        leg_t += [tmp]
        if uncertainty_reference == "maximum":
            leg_t = list(reversed(leg_t))
        leg_d = {}
        for k1, k2 in enumerate(leg_t):
            leg_d[k2] = {"text": {"color": "k", "fontsize": 12}}
            if "sqrt" in k2 and "frac" in k2:
                leg_d[k2]["line"] = {"color": "k", "linestyle": "--"}
            if uncertainty_reference == "maximum":
                leg_d[k2]["text"]["horizontalalignment"] = "right"
                if "sqrt" in k2 and "frac" in k2:
                    leg_d[k2]["text"]["horizontalalignment"] = "left"
                x0, x1, y0, y1 = 98, -31, 95, -9
            else:
                x0, x1, y0, y1 = 2, 0, 5, -9
                y0 -= (len(leg_t) - 1) * y1
            x1 *= default_plot["size_x"] / (x_size_cur * x_frac)
            y1 *= default_plot["size_y"] / (y_size_cur * y_frac)
            leg_d[k2]["position"] = {"x": x0 + max(0, k1 - 1) * x1, "y": y0 + k1 * y1}
        # add markers and dataset names at the bottom or top right of the figure
        list_d1 = [k for k in list(fig_markers.keys()) if k in list(d1.keys())]
        list_d2 = [k.replace("DATASET", fig_smile_selected).replace("DAT", fig_smile_selected[:3])
                   for k in list(fig_markers.keys()) if k in list(d1.keys())]
        x0, y0, y1 = 0, -25, -8
        x1 *= default_plot["size_x"] / (x_size_cur * x_frac)
        y1 *= default_plot["size_y"] / (y_size_cur * y_frac)
        for k1, (k2, k3) in enumerate(zip(list_d1, list_d2)):
            leg_d[k3] = {"text": {"color": fig_colors[k2], "fontsize": 12}}
            leg_d[k3]["marker"] = {"facecolor": fig_colors[k2], "marker": fig_markers[k2], "s": 80}
            leg_d[k3]["position"] = {"x": x0, "y": y0 + y1 * k1}
            leg_t.append(k3)
        kwarg.update({"legend_param": leg_d, "legend_txt": leg_t})
        # theoretical relationship
        lx = list(numpy__linspace(min(kwarg["x_lim"]), max(kwarg["x_lim"]), 50))
        cur_c.append("k")
        cur_ls.append("--")
        cur_lw.append(4)
        cur_x.append(lx)
        if uncertainty_reference == "maximum":
            cur_y.append([(lx[-1] / k)**0.5 for k in lx])
        else:
            cur_y.append([(lx[0] / k)**0.5 for k in lx])
        cur_z.append(10)
        kwarg.update({"cur_c": cur_c, "cur_ls": cur_ls, "cur_lw": cur_lw, "cur_x": cur_x, "cur_y": cur_y,
                      "cur_z": cur_z})
        # plot
        ax = plt.subplot(gs[y_position: y_position + y_size_cur, x_position: x_position + x_size_cur])
        plot_main(ax, **kwarg)
        counter += 1
        x_position = 0
        y_position += max(y_size, y_size_cur) + y_delt
    # plot directory (relative to current file directory)
    plot_directory = "/".join(os.path.dirname(__file__).split("/")[:-2])
    # path to output figure
    figure_file_path = os.path.join(plot_directory, "plot/" + str(fig_name)) + "." + str(fig_format)
    # save
    plt.savefig(figure_file_path, bbox_inches="tight", format=fig_format)
    plt.close()
    return


def fig_examples_of_res(dict_i: dict, data_diagnostics: list, fig_format: str, fig_name: str, fig_colors: dict,
                        fig_markers: dict, fig_marker_size: float, fig_orientation: str, fig_panel_size: dict,
                        fig_selected_model: str, fig_ticks: dict, fig_titles: dict, fig_title_bool: bool = True,
                        panel_param: dict = None):
    """
    Template for F5: required ensemble size (RES) to limit the uncertainty to a desired value (uncertainty defined
    using 3 different methods)
    
    Inputs:
    -------
    :param dict_i: dict
        Dictionary with three nested levels [diagnostic, method, boxplot-or-marker], filled with the data to plot
    :param data_diagnostics: list
        Names of diagnostic (to keep them in the right order);
        e.g., data_diagnostics = ['ave_pr_val_n30e', 'ave_ts_val_n30e']
    :param fig_format: str
        Format of the figure; e.g., fig_format = 'pdf'
        Four figure formats are accepted: 'eps', 'pdf', 'png', 'svg'
    :param fig_name: str
        Name of the output file; e.g., fig_name = 'name_of_the_figure'
    :param fig_colors: dict
        Dictionary with one level [key], filled with the color to plot each key;
        e.g., fig_colors = {'unc': 'b', 'obs': 'k', 'mme': 'r', fig_selected_model: 'g'}
    :param fig_markers: dict
        Dictionary with on level [key], filled with the marker to plot each key;
        e.g., fig_markers = {fig_selected_model: '>'}
    :param fig_marker_size: float
        Size of the markers; e.g., fig_marker_size = 60.
    :param fig_orientation: str
        Orientation of the figure; e.g., fig_orientation = 'column'
        Two figure orientations are accepted:
            'column' (column = variables,  row = statistics)
            'row'    (column = statistics, row = variables)
    :param fig_panel_size: dict
        Dictionary defining the size of each panel;
        e.g., fig_panel_size = {'x_delt': 2, 'x_frac': 0.5, 'x_size': 5, 'y_delt': 3, 'y_frac': 0.5, 'y_size': 8}
        'x' and 'y' correspond respectively to the x-axis (horizontal) and y-axis (vertical)
        'delt' is the distance between panels (in inches)
        'size' is the size of each panel (in inches)
        'frac' is a fraction to multiply 'delt' and 'size' (to shrink or expend figure proportionally)
    :param fig_selected_model: str
        Name of the model selected to be plotted as a marker; e.g., fig_selected_model = 'IPSL-CM6A-LR'
    :param fig_ticks: dict
        Dictionary defining the range and tics of axes; e.g., fig_ticks = {'x_axis': [0, 1], 'y_axis': [0, 1, 2, 3, 4]}
    :param fig_titles: dict
        Dictionary defining the titles of panels and axes;
        e.g., fig_titles = {
            'ave_pr_val_n30e': {'x': 'N3 PR', 'y': 'mean', 'z': 'xbar'},
            'x_axis': {'ave_pr_val_n30e': ''},
            'y_axis': {'ave_pr_val_n30e': 'ensemble size'},
        }
    :param fig_title_bool: bool, optional
        True to plot titles of columns and rows; e.g., fig_title_bool = True
        Default is True
    :param panel_param: dict, optional
        Dictionary to modify default values of panel parameters (see fig_panel.py);
        e.g., panel_param = {'x_nbr_minor': 0}
        Default is None (no modification of the default values)
    """
    if panel_param is None:
        panel_param = {}
    # plot initialization
    x_delt, x_frac, x_size = fig_panel_size["x_delt"], fig_panel_size["x_frac"], fig_panel_size["x_size"]
    y_delt, y_frac, y_size = fig_panel_size["y_delt"], fig_panel_size["y_frac"], fig_panel_size["y_size"]
    list_dia, n_panel_per_line, nbr_c, nbr_l = tool_figure_initialization(
        data_diagnostics, fig_orientation, x_delt, x_size, y_delt, y_size)
    plt.figure(0, figsize=(nbr_c * x_frac, nbr_l * y_frac))
    gs = GridSpec(nbr_l, nbr_c)
    numbering = string.ascii_lowercase
    x_position, y_position = 0, 0
    for jj, dia in enumerate(list_dia):
        kwarg = {**panel_param, **{"x_size": x_size * x_frac, "y_size": y_size * y_frac}}
        # dictionary
        d1 = dict_i[dia]
        # data to plot
        box_c, box_x, box_y, mar_c, mar_m, mar_s, mar_x, mar_y = [], [], [], [], [], [], [], []
        for ii, method in enumerate(list(fig_titles["x_axis"][dia].keys())):
            for typ in list(d1[method].keys()):
                if typ == "boxplot":
                    box_c.append(fig_colors[method])
                    box_x.append(ii)
                    box_y.append(d1[method][typ])
                else:
                    mar_c.append(fig_colors[fig_selected_model])
                    mar_m.append(fig_markers[fig_selected_model])
                    mar_s.append(fig_marker_size)
                    mar_x.append(ii + 0.2)
                    mar_y.append(d1[method][typ])
        kwarg.update({"box_c": box_c, "box_x": box_x, "box_y": box_y, "mar_cf": mar_c, "mar_m": mar_m, "mar_s": mar_s,
                      "mar_x": mar_x, "mar_y": mar_y})
        # title
        if fig_title_bool is True:
            kwarg["title"] = numbering[jj]
            kwarg["title_col"], kwarg["title_row"] = tool_title(fig_titles[dia], jj, n_panel_per_line, fig_orientation)
        # x-axis
        kwarg["x_lab"], kwarg["x_lim"], kwarg["x_tic"] = tool_figure_axis(fig_ticks["x_axis"], arr_i=box_x)
        kwarg["x_lab"] = [""] * len(kwarg["x_lab"])
        kwarg["x_lim"][0] -= 0.5
        kwarg["x_lim"][1] += 0.5
        # y-axis
        kwarg["y_lab"], kwarg["y_lim"], kwarg["y_tic"] = tool_figure_axis(fig_ticks["y_axis"], arr_i=box_y)
        kwarg["y_nam"] = fig_titles["y_axis"] if jj % n_panel_per_line == 0 else ""
        x1, x2, y1, y2 = kwarg["x_lim"] + kwarg["y_lim"]
        dx, dy = (x2 - x1) / 100, (y2 - y1) / 100
        # x-axis labels in color
        txt, txt_c, txt_x, txt_y = [], [], [], []
        for ii, method in enumerate(list(fig_titles["x_axis"][dia].keys())):
            txt.append(fig_titles["x_axis"][dia][method])
            txt_c.append(fig_colors[method])
            txt_x.append(ii + 1 * dx * default_plot["size_x"] / (x_size * x_frac))
            txt_y.append(kwarg["y_lim"][0] - 1 * dy * default_plot["size_y"] / (y_size * y_frac))
        kwarg.update({"text": txt, "text_c": txt_c, "text_ha": ["right"] * len(txt), "text_r": [20] * len(txt),
                      "text_va": ["top"] * len(txt), "text_x": txt_x, "text_y": txt_y})
        # plot
        ax = plt.subplot(gs[y_position: y_position + y_size, x_position: x_position + x_size])
        plot_main(ax, **kwarg)
        x_position += x_size + x_delt
        if (jj + 1) % n_panel_per_line == 0:
            x_position = 0
            y_position += y_size + y_delt
    # plot directory (relative to current file directory)
    plot_directory = "/".join(os.path.dirname(__file__).split("/")[:-2])
    # path to output figure
    figure_file_path = os.path.join(plot_directory, "plot/" + str(fig_name)) + "." + str(fig_format)
    # save
    plt.savefig(figure_file_path, bbox_inches="tight", format=fig_format)
    plt.close()
    return


def fig_influence_of(dict_i: dict, data_diagnostics: list, data_experiments: list, fig_format: str, fig_name: str,
                     fig_colors: dict, fig_legend_position: str, fig_linestyles: dict, fig_linewidth: float,
                     fig_linezorder: int, fig_markers: dict, fig_marker_size: float, fig_orientation: str,
                     fig_panel_size: dict, fig_ticks: dict, fig_titles: dict, smile_minimum_size: int,
                     uncertainty_influence: str, uncertainty_reference: str, fig_legend_bool: bool = True,
                     fig_title_bool: bool = True, panel_param: dict = None):
    """
    Template for F2, F3 and S4: influence of ensemble size or epoch length on the uncertainty of the ensemble mean
    
    Inputs:
    -------
    :param dict_i: dict
        Dictionary with four nested levels [diagnostic, dataset, experiment, key], filled with the data to plot
    :param data_diagnostics: list
        Names of diagnostic (to keep them in the right order);
        e.g., data_diagnostics = ['ave_pr_val_n30e', 'ave_ts_val_n30e']
    :param data_experiments: list
        Names of experiment (to keep them in the right order); e.g., data_experiments = ['piControl', 'historical']
    :param fig_format: str
        Format of the figure; e.g., fig_format = 'pdf'
        Four figure formats are accepted: 'eps', 'pdf', 'png', 'svg'
    :param fig_name: str
        Name of the output file; e.g., fig_name = 'name_of_the_figure'
    :param fig_colors: dict
        Dictionary with one level [dataset], filled with the color to plot each dataset;
        e.g., fig_colors = {'ACCESS-CM2': 'orange', 'ACCESS-ESM1-5': 'forestgreen'}
    :param fig_legend_position: str
        Position of the legend; e.g., fig_legend_position = 'bottom'
        Two legend positions are accepted: 'bottom', 'right'
    :param fig_linestyles: dict
        Dictionary with one level [experiment], filled with the color to plot each experiment;
        e.g., fig_linestyles = {'historical": '-', 'piControl': ':'}
    :param fig_linewidth: float
        Width of the lines; e.g., fig_linewidth = 1.
    :param fig_linezorder: int
        zorder of the lines; e.g., fig_linezorder = 1
    :param fig_markers: dict
        Dictionary with one level [dataset], filled with the marker to plot each dataset;
        e.g., fig_markers = {'ACCESS-CM2': '>', 'ACCESS-ESM1-5': '<'}
    :param fig_marker_size: float
        Size of the markers; e.g., fig_marker_size = 60.
    :param fig_orientation: str
        Orientation of the figure; e.g., fig_orientation = 'column'
        Two figure orientations are accepted:
            'column' (column = variables,  row = statistics)
            'row'    (column = statistics, row = variables)
    :param fig_panel_size: dict
        Dictionary defining the size of each panel;
        e.g., fig_panel_size = {'x_delt': 2, 'x_frac': 0.5, 'x_size': 5, 'y_delt': 3, 'y_frac': 0.5, 'y_size': 8}
        'x' and 'y' correspond respectively to the x-axis (horizontal) and y-axis (vertical)
        'delt' is the distance between panels (in inches)
        'size' is the size of each panel (in inches)
        'frac' is a fraction to multiply 'delt' and 'size' (to shrink or expend figure proportionally)
    :param fig_ticks: dict
        Dictionary with two nested levels [x-or-y_axis, diagnostic], filled with a list of tics;
        e.g., fig_ticks = {'x_axis': {'ave_pr_val_n30e': [0, 1]}, 'y_axis': {'ave_pr_val_n30e': [0, 1, 2, 3, 4]}}
    :param fig_titles: dict
        Dictionary defining the titles of panels and axes;
        e.g., fig_titles = {
            'ave_pr_val_n30e': {'x': 'N3 PR', 'y': 'mean', 'z': 'xbar'},
            'x_axis': {'ave_pr_val_n30e': ''},
            'y_axis': {'ave_pr_val_n30e': ''},
        }
    :param smile_minimum_size: int
        Minimum number of member for SMILEs (used for the legend); e.g., smile_minimum_size = 10
    :param uncertainty_influence: str
        Influence plotted (used to select plot legend); e.g., uncertainty_reference = 'ensemble_size'
        Two influences are recognized: 'ensemble_size', 'epoch_length'
        Other values will have no effect
    :param uncertainty_reference: str
        Reference plotted (used to select plot legend); e.g., uncertainty_reference = 'maximum'
        One reference is recognized: 'maximum'
        Other values will have no effect
    :param fig_legend_bool: bool, optional
        True to plot the datasets legend; e.g., fig_legend_bool = True
        Default is True
    :param fig_title_bool: bool, optional
        True to plot titles of columns and rows; e.g., fig_title_bool = True
        Default is True
    :param panel_param: dict, optional
        Dictionary to modify default values of panel parameters (see fig_panel.py);
        e.g., panel_param = {'x_nbr_minor': 0}
        Default is None (no modification of the default values)
    """
    if panel_param is None:
        panel_param = {}
    # plot initialization
    x_delt, x_frac, x_size = fig_panel_size["x_delt"], fig_panel_size["x_frac"], fig_panel_size["x_size"]
    y_delt, y_frac, y_size = fig_panel_size["y_delt"], fig_panel_size["y_frac"], fig_panel_size["y_size"]
    list_dia, n_panel_per_line, nbr_c, nbr_l = tool_figure_initialization(
        data_diagnostics, fig_orientation, x_delt, x_size, y_delt, y_size)
    plt.figure(0, figsize=(nbr_c * x_frac, nbr_l * y_frac))
    gs = GridSpec(nbr_l, nbr_c)
    numbering = string.ascii_lowercase
    x_position, y_position = 0, 0
    for jj, dia in enumerate(list_dia):
        kwarg = {**panel_param, **{"x_size": x_size * x_frac, "y_size": y_size * y_frac}}
        # dictionary
        d1 = dict_i[dia]
        # data to plot
        cur_c, cur_ls, cur_lw, cur_x, cur_y, cur_z = [], [], [], [], [], []
        mar_c, mar_m, mar_s, mar_x, mar_y, mar_z = [], [], [], [], [], []
        sha_c, sha_x, sha_y1, sha_y2 = [], [], [], []
        for dat in list(d1.keys()):
            for exp in list(d1[dat].keys()):
                for k in list(d1[dat][exp].keys()):
                    col = fig_colors[dat]
                    if len({"x", "y1", "y2"} - set(list(d1[dat][exp][k].keys()))) == 0 and \
                            len(set(list(d1[dat][exp][k].keys())) - {"x", "y1", "y2"}) == 0:
                        sha_c.append(col)
                        sha_x.append(d1[dat][exp][k]["x"])
                        sha_y1.append(d1[dat][exp][k]["y1"])
                        sha_y2.append(d1[dat][exp][k]["y2"])
                    else:
                        lis = fig_linestyles[exp]
                        mar = fig_markers[dat]
                        # curves
                        cur_c.append(col)
                        cur_ls.append(lis)
                        cur_lw.append(fig_linewidth)
                        cur_x.append(d1[dat][exp][k]["x"])
                        cur_y.append(d1[dat][exp][k]["y"])
                        cur_z.append(fig_linezorder)
                        # markers
                        mar_c += [col] * len(d1[dat][exp][k]["x"])
                        mar_m += [mar] * len(d1[dat][exp][k]["x"])
                        mar_s += [fig_marker_size] * len(d1[dat][exp][k]["x"])
                        mar_x += deepcopy(d1[dat][exp][k]["x"])
                        mar_y += deepcopy(d1[dat][exp][k]["y"])
                        mar_z += [9 if "MME" in dat else random__randint(2, 8)] * len(d1[dat][exp][k]["x"])
        # title
        if fig_title_bool is True:
            kwarg["title"] = numbering[jj]
            kwarg["title_col"], kwarg["title_row"] = tool_title(fig_titles[dia], jj, n_panel_per_line, fig_orientation)
        # x-axis
        kwarg["x_lab"], kwarg["x_lim"], kwarg["x_tic"] = tool_figure_axis(
            fig_ticks["x_axis"][dia], arr_i=cur_x + mar_x)
        if uncertainty_reference == "maximum" and fig_ticks["x_axis"][dia] is not None:
            kwarg["x_lim"][0] -= 0.1
        if jj > len(list_dia) - n_panel_per_line - 1:
            kwarg["x_nam"] = fig_titles["x_axis"][dia]
        # y-axis
        kwarg["y_lab"], kwarg["y_lim"], kwarg["y_tic"] = tool_figure_axis(
            fig_ticks["y_axis"][dia], arr_i=cur_y + mar_y + sha_y1 + sha_y2)
        if jj % n_panel_per_line == 0:
            kwarg["y_nam"] = fig_titles["y_axis"][dia]
        # legend
        leg_t = [r"y = $\sqrt{\frac{1}{x}}$"] if uncertainty_reference == "maximum" else [r"y = $\sqrt{\frac{x_0}{x}}$"]
        list_experiments = sorted(list(set([k2 for k1 in list(d1.keys()) for k2 in list(d1[k1].keys())])),
                                  key=str.casefold)
        list_experiments = [fig_titles[k] for k in data_experiments if k in list_experiments]
        leg_t += ["experiment%s: %s" % (plural_s(list_experiments), " & ".join(list_experiments))]
        if uncertainty_influence == "ensemble_size":
            list_durations = sorted(list(set([int(k3.split("_")[0]) for k1 in list(d1.keys())
                                              for k2 in list(d1[k1].keys()) for k3 in list(d1[k1][k2].keys())])))
            leg_t += ["epoch lengths = " + str(list_durations[0]) + " to " + str(list_durations[-1])]
        elif uncertainty_influence in ["epoch_length", "epoch_length_pi"]:
            if uncertainty_influence in "epoch_length":
                leg_t += ["ensemble size = max (>=" + str(smile_minimum_size) + ")"]
            else:
                leg_t += ["ensemble size = min (>=" + str(smile_minimum_size) + ")"]
        if uncertainty_reference == "maximum":
            leg_t = list(reversed(leg_t))
        leg_d = {}
        for k1, k2 in enumerate(leg_t):
            leg_d[k2] = {"text": {"color": "k", "fontsize": 12}}
            if "sqrt" in k2 and "frac" in k2:
                leg_d[k2]["line"] = {"color": "k", "linestyle": "--"}
            if uncertainty_reference == "maximum":
                leg_d[k2]["text"]["horizontalalignment"] = "right"
                if "sqrt" in k2 and "frac" in k2:
                    leg_d[k2]["text"]["horizontalalignment"] = "left"
                x0, x1, y0, y1 = 98, -31, 95, -9
            else:
                x0, x1, y0, y1 = 2, 0, 5, -9
                y0 -= (len(leg_t) - 1) * y1
            x1 *= default_plot["size_x"] / (x_size * x_frac)
            y1 *= default_plot["size_y"] / (y_size * y_frac)
            leg_d[k2]["position"] = {"x": x0 + max(0, k1 - 1) * x1, "y": y0 + k1 * y1}
        # add markers and dataset names at the bottom or top right of the figure
        if fig_legend_bool is True:
            list_datasets = list(set([k2 for k1 in list(dict_i.keys()) for k2 in list(dict_i[k1].keys())]))
            tool_legend_datasets(list_datasets, fig_colors, fig_markers, leg_d, leg_t, list_dia, jj, n_panel_per_line,
                                 fig_legend_position, x_frac, x_size, y_frac, y_size)
        kwarg.update({"legend_param": leg_d, "legend_txt": leg_t})
        # theoretical relationship
        lx = list(numpy__linspace(min(kwarg["x_lim"]), max(kwarg["x_lim"]), 50))
        cur_c.append("k")
        cur_ls.append("--")
        cur_lw.append(4)
        cur_x.append(lx)
        if uncertainty_reference == "maximum":
            cur_y.append([(lx[-1] / k)**0.5 for k in lx])
        else:
            cur_y.append([(lx[0] / k)**0.5 for k in lx])
        cur_z.append(10)
        kwarg.update({"cur_c": cur_c, "cur_ls": cur_ls, "cur_lw": cur_lw, "cur_x": cur_x, "cur_y": cur_y,
                      "cur_z": cur_z, "mar_cf": mar_c, "mar_m": mar_m, "mar_s": mar_s, "mar_x": mar_x, "mar_y": mar_y,
                      "mar_z": mar_z, "sha_c": sha_c, "sha_x": sha_x, "sha_y1": sha_y1, "sha_y2": sha_y2})
        # plot
        ax = plt.subplot(gs[y_position: y_position + y_size, x_position: x_position + x_size])
        plot_main(ax, **kwarg)
        x_position += x_size + x_delt
        if (jj + 1) % n_panel_per_line == 0:
            x_position = 0
            y_position += y_size + y_delt
    # plot directory (relative to current file directory)
    plot_directory = "/".join(os.path.dirname(__file__).split("/")[:-2])
    # path to output figure
    figure_file_path = os.path.join(plot_directory, "plot/" + str(fig_name)) + "." + str(fig_format)
    # save
    plt.savefig(figure_file_path, bbox_inches="tight", format=fig_format)
    plt.close()
    return


def fig_presentation_uncertainties(dict_i: dict, data_diagnostics: list, fig_format: str, fig_name: str,
                                   fig_colors: dict, fig_legend_position: str, fig_linestyle: str, fig_linewidth: float,
                                   fig_orientation: str, fig_panel_size: dict, fig_ticks: dict, fig_titles: dict,
                                   panel_param_box: dict = None, panel_param_map: dict = None):
    """
    Template for F1: Maps of observed statistical moments and distributions of observed and modeled statistical moments
    
    Inputs:
    -------
    :param dict_i: dict
        Dictionary with three nested levels [diagnostic, boxplot-or-curve-or-map, dataset], filled with the data to plot
    :param data_diagnostics: list
        Names of diagnostic (to keep them in the right order);
        e.g., data_diagnostics = ['ave_pr_val_n30e', 'ave_ts_val_n30e']
    :param fig_format: str
        Format of the figure; e.g., fig_format = 'pdf'
        Four figure formats are accepted: 'eps', 'pdf', 'png', 'svg'
    :param fig_name: str
        Name of the output file; e.g., fig_name = 'name_of_the_figure'
    :param fig_colors: dict
        Dictionary with one level [dataset], filled with the color to plot each dataset;
        e.g., fig_colors = {'ACCESS-CM2': 'orange', 'ACCESS-ESM1-5': 'forestgreen'}
    :param fig_legend_position: str
        Position of the legend; e.g., fig_legend_position = 'bottom'
        Two legend positions are accepted: 'bottom', 'right'
    :param fig_linestyle: str
        Style of the lines; e.g., fig_linestyle = '-'
    :param fig_linewidth: float
        Width of the lines; e.g., fig_linewidth = 1.
    :param fig_orientation: str
        Orientation of the figure; e.g., fig_orientation = 'column'
        Two figure orientations are accepted:
            'column' (column = variables,  row = statistics)
            'row'    (column = statistics, row = variables)
    :param fig_panel_size: dict
        Dictionary defining the size of each panel;
        e.g., fig_panel_size = {
            'x_delt_box': 4, 'x_frac_box': 0.25, 'x_size_box': 6, 'y_delt_box': 2, 'y_frac_box': 0.25, 'y_size_box': 12,
            'x_delt_map': 3, 'x_size_map': 32, 'y_size_map': 8,
        }
        'box' and 'map' correspond respectively to boxplot and map panels
        'x' and 'y' correspond respectively to the x-axis (horizontal) and y-axis (vertical)
        'delt' is the distance between panels (in inches)
        'size' is the size of each panel (in inches)
        'frac' is a fraction to multiply 'delt' and 'size' (to shrink or expend figure proportionally)
    :param fig_ticks: dict
        Dictionary with two nested levels [x-or-y-or-z_axis, diagnostic], filled with a list of tics;
        e.g., fig_ticks = {
            'x_axis': {'ave_pr_val_n30e': [0, 1]},
            'y_axis': {'ave_pr_val_n30e': [0, 1, 2, 3, 4]},
            'z_axis': {'ave_pr_val': [0, 2, 4, 6, 8]},
        }
    :param fig_titles: dict
        Dictionary defining the titles of panels and axes;
        e.g., fig_titles = {
            'ave_pr_val_n30e': {'x': 'N3 PR', 'y': 'mean', 'z': 'xbar'},
            'x_axis': {'ave_pr_val_n30e': ''},
            'y_axis': {'ave_pr_val_n30e': ''},
            'z_axis': {'ave_pr_val': 'N3 PR xbar (mm/day)'},
        }
    :param panel_param_box: dict, optional
        Dictionary to modify default values of panel parameters for boxplots (see fig_panel.py);
        e.g., panel_param_box = {'x_nbr_minor': 0}
        Default is None (no modification of the default values)
    :param panel_param_map: dict, optional
        Dictionary to modify default values of panel parameters for maps (see fig_panel.py);
        e.g., panel_param_map = {'title_row_x': 30}
        Default is None (no modification of the default values)
    """
    if panel_param_box is None:
        panel_param_box = {}
    if panel_param_map is None:
        panel_param_map = {}
    # plot initialization
    x_delt, x_frac, x_size = fig_panel_size["x_delt_box"], fig_panel_size["x_frac_box"], fig_panel_size["x_size_box"]
    y_delt, y_frac, y_size = fig_panel_size["y_delt_box"], fig_panel_size["y_frac_box"], fig_panel_size["y_size_box"]
    x_delt_map, x_size_map = fig_panel_size["x_delt_map"], fig_panel_size["x_size_map"]
    y_size_map = fig_panel_size["y_size_map"]
    list_dia, n_panel_per_line, _, _ = tool_figure_initialization(
        data_diagnostics, fig_orientation, x_delt, x_size, y_delt, y_size)
    nbr_c = n_panel_per_line * (x_size_map + x_size + x_delt_map + x_delt) - x_delt
    nbr_l = math__ceil(len(list_dia) / n_panel_per_line) * (y_size + y_delt) - y_delt
    plt.figure(0, figsize=(nbr_c * x_frac, nbr_l * y_frac))
    gs = GridSpec(nbr_l, nbr_c)
    numbering = string.ascii_lowercase
    x_position, y_position = 0, 0
    counter = 0
    for jj, dia in enumerate(list_dia):
        # dictionary
        d1 = dict_i[dia]
        #
        # -- Map
        #
        tmp = dia[:-5]
        kwarg = deepcopy(panel_param_map)
        kwarg.update({"x_size": x_size_map * x_frac, "y_size": y_size_map * y_frac,
                      "legend_position": fig_legend_position})
        dataset = list(d1["map"].keys())[0]
        # title
        kwarg["title"] = numbering[counter]
        kwarg["title_col"], kwarg["title_row"] = tool_title(fig_titles[tmp], jj, n_panel_per_line, fig_orientation,
                                                            txt=str(dataset) + " ")
        # x-axis
        kwarg["x_lab"],  _, kwarg["x_tic"] = tool_figure_axis(default_map["lon_tic"], axis_name="longitude")
        kwarg["x_lim"] = default_map["lon_lim"]
        # y-axis
        kwarg["y_lab"],  _, kwarg["y_tic"] = tool_figure_axis(default_map["lat_tic"], axis_name="latitude")
        kwarg["y_lim"] = default_map["lat_lim"]
        # shading
        kwarg["sha_s"] = d1["map"][dataset][0]
        kwarg["sha_cs"] = fig_colors[tmp]
        kwarg["legend"] = deepcopy(fig_legend_position)
        kwarg["s_tic"] = fig_ticks["z_axis"][tmp]
        kwarg["s_lab"] = tool_axis_label(kwarg["s_tic"])
        kwarg["s_nam"] = fig_titles["z_axis"][tmp]
        # regions
        kwarg["region"] = [dia[-4:]]
        # projection
        kwarg["projection"] = ccrs.PlateCarree(central_longitude=0)
        crs180 = ccrs.PlateCarree(central_longitude=180)
        # plot
        ax = plt.subplot(gs[y_position: y_position + y_size_map, x_position: x_position + x_size_map],
                         projection=crs180)
        plot_map(ax, **kwarg)
        counter += 1
        x_position += x_size_map + x_delt_map
        #
        # -- Boxplot
        #
        kwarg = deepcopy(panel_param_box)
        kwarg.update({"x_size": x_size * x_frac, "y_size": y_size * y_frac})
        list_datasets = [k for k in list(d1["boxplot"].keys()) if k[:5] == "MME--"]
        list_datasets += sorted([k for k in list(d1["boxplot"].keys()) if k[:5] != "MME--"], key=str.casefold)
        # data to plot
        box_c, box_x, box_y = [], [], []
        for ii, dat in enumerate(list_datasets):
            box_c.append(fig_colors[dat])
            box_x.append(ii)
            box_y.append(d1["boxplot"][dat])
        cur_c, cur_ls, cur_lw, cur_x, cur_y = [], [], [], [], []
        for dat in list(d1["curve"].keys()):
            cur_c.append(fig_colors[dat])
            cur_ls.append(fig_linestyle)
            cur_lw.append(fig_linewidth)
            cur_x.append([-0.5, len(list_datasets) - 0.5])
            cur_y.append(d1["curve"][dat] * 2)
        kwarg.update({"box_c": box_c, "box_x": box_x, "box_y": box_y, "cur_c": cur_c, "cur_ls": cur_ls,
                      "cur_lw": cur_lw, "cur_x": cur_x, "cur_y": cur_y})
        # title
        kwarg["title"] = numbering[counter]
        kwarg["title_col"], _ = tool_title(fig_titles[dia], jj, n_panel_per_line, fig_orientation)
        # x-axis
        kwarg["x_lab"], kwarg["x_lim"], kwarg["x_tic"] = tool_figure_axis(fig_ticks["x_axis"], arr_i=box_x + cur_x)
        kwarg["x_lab"] = [""] * len(kwarg["x_lab"])
        kwarg["x_lim"][0] -= 0.5
        kwarg["x_lim"][1] += 0.5
        # y-axis
        kwarg["y_lab"], kwarg["y_lim"], kwarg["y_tic"] = tool_figure_axis(
            fig_ticks["y_axis"][dia], arr_i=box_y + cur_y)
        # x-axis labels in color
        if jj > len(list_dia) - n_panel_per_line - 1:
            txt, txt_c, txt_x, txt_y = [], [], [], []
            for ii, dat in enumerate(list_datasets):
                txt.append(dat)
                txt_c.append(fig_colors[dat])
                txt_x.append(ii)
                txt_y.append(kwarg["y_lim"][0] - 3 * (kwarg["y_lim"][1] - kwarg["y_lim"][0]) / 100)
            kwarg.update({"text": txt, "text_c": txt_c, "text_ha": ["right"] * len(txt), "text_r": [20] * len(txt),
                          "text_va": ["top"] * len(txt), "text_x": txt_x, "text_y": txt_y})
        # plot
        ax = plt.subplot(gs[y_position: y_position + y_size, x_position: x_position + x_size])
        plot_main(ax, **kwarg)
        counter += 1
        x_position += x_size + x_delt
        if (jj + 1) % n_panel_per_line == 0:
            x_position = 0
            y_position += y_size + y_delt
    # plot directory (relative to current file directory)
    plot_directory = "/".join(os.path.dirname(__file__).split("/")[:-2])
    # path to output figure
    figure_file_path = os.path.join(plot_directory, "plot/" + str(fig_name)) + "." + str(fig_format)
    # save
    plt.savefig(figure_file_path, bbox_inches="tight", format=fig_format)
    plt.close()
    return


def fig_quality_control(dict_distributions: dict, dict_time_series: dict, data_diagnostics: list, fig_format: str,
                        fig_name: str, fig_box_linestyle: str, fig_box_linewidth: float, fig_box_mean_size: float,
                        fig_box_outlier_size: float, fig_colors: dict, fig_cur_linecolor: str, fig_cur_linestyle: str,
                        fig_cur_linewidth: float, fig_panel_size: dict, fig_ticks: dict, fig_titles: dict,
                        fig_years_per_panel: int, panel_param_box: dict = None, panel_param_tim: dict = None):
    """
    Template for S1: Time series and boxplots of all diagnostics of all datasets
    
    Inputs:
    -------
    :param dict_distributions: dict
        Dictionary with four nested levels [diagnostic, experiment, boxplot-or-marker, x-or-y], filled with the data to
        plot as boxplots or markers
    :param dict_time_series: dict
        Dictionary with four nested levels [diagnostic, dataset, curve, x-or-y], filled with the data to plot as curves
    :param data_diagnostics: list
        Names of diagnostic (to keep them in the right order);
        e.g., data_diagnostics = ['ave_pr_val_n30e', 'ave_ts_val_n30e']
    :param fig_format: str
        Format of the figure; e.g., fig_format = 'pdf'
        Four figure formats are accepted: 'eps', 'pdf', 'png', 'svg'
    :param fig_name: str
        Name of the output file; e.g., fig_name = 'name_of_the_figure'
    :param fig_box_linestyle: str
        Style of the lines for boxplots; e.g., fig_box_linestyle = '-'
    :param fig_box_linewidth: float
        Width of the lines for boxplots; e.g., fig_box_linewidth = 1.
    :param fig_box_mean_size: float
        Size of the mean markers for boxplots; e.g., fig_box_mean_size = 10.
    :param fig_box_outlier_size: float
        Size of the outlier markers for boxplots; e.g., fig_box_outlier_size = 2.
    :param fig_colors: dict
        Dictionary with one level [dataset], filled with the color to plot each dataset;
        e.g., fig_colors = {'ACCESS-CM2': 'orange', 'ACCESS-ESM1-5': 'forestgreen'}
    :param fig_cur_linecolor: str
        Color of the lines for time series; e.g., fig_cur_linecolor = 'grey'
    :param fig_cur_linestyle: str
        Style of the lines for time series; e.g., fig_cur_linestyle = '-'
    :param fig_cur_linewidth: float
        Width of the lines for ime series; e.g., fig_cur_linewidth = 1.
    :param fig_panel_size: dict
        Dictionary defining the size of each panel;
        e.g., fig_panel_size = {'x_delt': 2, 'x_frac': 0.5, 'x_size': 5, 'y_delt': 3, 'y_frac': 0.5, 'y_size': 8}
        'x' and 'y' correspond respectively to the x-axis (horizontal) and y-axis (vertical)
        'delt' is the distance between panels (in inches)
        'size' is the size of each panel (in inches)
        'frac' is a fraction to multiply 'delt' and 'size' (to shrink or expend figure proportionally)
    :param fig_ticks: dict
        Dictionary with two nested levels [x-or-y_axis, diagnostic], filled with a list of tics;
        e.g., fig_ticks = {
            'x_axis': {'ave_pr_val_n30e': [0, 1]},
            'y_axis': {'ave_pr_val_n30e': [0, 1, 2, 3, 4]},
        }
    :param fig_titles: dict
        Dictionary defining the titles of panels and axes;
        e.g., fig_titles = {
            'ave_pr_val_n30e': {'x': 'N3 PR', 'y': 'mean', 'z': 'xbar'},
            'x_axis': {'ave_pr_val_n30e': ''},
            'y_axis': {'ave_pr_val_n30e': 'N3 PR xbar (mm/day)'},
        }
    :param fig_years_per_panel: int
        Number of years in each panel; e.g., fig_years_per_panel = 500
    :param panel_param_box: dict, optional
        Dictionary to modify default values of panel parameters for boxplots (see fig_panel.py);
        e.g., panel_param_box = {'x_nbr_minor': 0}
        Default is None (no modification of the default values)
    :param panel_param_tim: dict, optional
        Dictionary to modify default values of panel parameters for time series (see fig_panel.py);
        e.g., panel_param_tim = {'x_nbr_minor': 0}
        Default is None (no modification of the default values)
    """
    if panel_param_box is None:
        panel_param_box = {}
    if panel_param_tim is None:
        panel_param_tim = {}
    # plot initialization
    x_delt, x_frac, x_size = fig_panel_size["x_delt"], fig_panel_size["x_frac"], fig_panel_size["x_size"]
    y_delt, y_frac, y_size = fig_panel_size["y_delt"], fig_panel_size["y_frac"], fig_panel_size["y_size"]
    nbr_c = deepcopy(x_size)
    nbr_l = (len(list(dict_distributions.keys())) + 4) * (y_size + y_delt) + y_delt
    plt.figure(0, figsize=(nbr_c * x_frac, nbr_l * y_frac))
    gs = GridSpec(nbr_l, nbr_c)
    numbering = string.ascii_lowercase
    x_position, y_position = 0, 0
    counter = 0
    #
    # -- Time series
    #
    if len(list(dict_time_series.keys())) == 1:
        dia = list(dict_time_series.keys())[0]
        n_panel = 4
        for ii in range(n_panel):
            kwarg = {**panel_param_tim, **{"x_size": x_size * x_frac, "y_size": y_size * y_frac}}
            # dictionary
            d1 = dict_time_series[dia]
            # list datasets
            list_dat = sorted(list(d1.keys()), key=str.casefold)
            # curves to plot
            arr_c = [fig_colors["curve"][dat] if dat in list(fig_colors["curve"].keys()) else fig_cur_linecolor
                     for dat in list_dat]
            arr_ls = [fig_cur_linestyle] * len(list_dat)
            arr_lw = [fig_cur_linewidth] * len(list_dat)
            arr_x = [d1[dat]["curve"]["x"] for dat in list_dat]
            arr_y = [d1[dat]["curve"]["y"] for dat in list_dat]
            arr_z = [2 if dat in list(fig_colors["curve"].keys()) else 1 for dat in list_dat]
            kwarg.update({"cur_c": arr_c, "cur_ls": arr_ls, "cur_lw": arr_lw, "cur_x": arr_x, "cur_y": arr_y,
                          "cur_z": arr_z})
            # title
            if ii == 0:
                kwarg["title"] = numbering[counter]
            # x-axis
            kwarg["x_tic"] = [k + ii * fig_years_per_panel * 12 for k in range(0, fig_years_per_panel * 12, 100 * 12)]
            kwarg["x_lab"] = [str(int(k / 12)) for k in kwarg["x_tic"]]
            kwarg["x_lim"] = [ii * fig_years_per_panel * 12, (ii + 1) * fig_years_per_panel * 12 - 1]
            if ii == n_panel - 1:
                kwarg["x_nam"] = fig_titles["x_axis"][dia]
            # y-axis
            kwarg["y_lab"], kwarg["y_lim"], kwarg["y_tic"] = tool_figure_axis(fig_ticks["y_axis"][dia], arr_i=arr_y)
            # legend
            if ii == 0:
                leg_t = [dat for dat in list_dat if dat in list(fig_colors["curve"].keys())]
                leg_d = {}
                for k1, k2 in enumerate(leg_t):
                    leg_d[k2] = {"text": {"color": fig_colors["curve"][k2], "fontsize": 12}}
                    leg_d[k2]["position"] = {"x": (10 + k1 * 70) * default_plot["size_x"] / (x_size * x_frac), "y": 80}
                kwarg.update({"legend_param": leg_d, "legend_txt": leg_t})
            # text
            if (n_panel % 2 == 0 and ii == (n_panel / 2 - 1)) or (n_panel % 2 == 1 and ii == (n_panel - 1) / 2):
                x1, x2, y1, y2 = kwarg["x_lim"] + kwarg["y_lim"]
                dx = (x2 - x1) * default_plot["size_x"] / (x_size * x_frac * 100)
                dy = (y2 - y1) / 100
                arr_x = [x1 - 28 * dx]
                if n_panel % 2 == 0:
                    arr_y = [y1 - 50 * (y_delt / y_size) * dy]
                else:
                    arr_y = [y1 + 50 * dy]
                kwarg.update({"text": [fig_titles["y_axis"][dia]], "text_c": ["k"], "text_ha": ["center"],
                              "text_r": [90], "text_x": arr_x, "text_y": arr_y})
            # plot
            ax = plt.subplot(gs[y_position: y_position + y_size, x_position: x_position + x_size])
            plot_main(ax, **kwarg)
            y_position += y_size + y_delt
        counter += 1
        y_position += y_delt
    #
    # -- Boxplots
    #
    for dia in data_diagnostics:
        kwarg = {**panel_param_box, **{"x_size": x_size * x_frac, "y_size": y_size * y_frac}}
        # list experiments
        list_exp = list(dict_distributions[dia].keys())
        # boxplots
        arr_c, arr_x, arr_y = [], [], []
        for exp in list_exp:
            if "boxplot" in list(dict_distributions[dia][exp].keys()):
                d1 = dict_distributions[dia][exp]["boxplot"]
                arr_c += [fig_colors[exp]] * len(d1["x"])
                arr_x += d1["x"] if isinstance(d1["x"], list) is True else [d1["x"]]
                arr_y += d1["y"] if isinstance(d1["y"], list) is True else [d1["y"]]
        kwarg.update({"box_c": arr_c, "box_fs": [fig_box_outlier_size] * len(arr_x),
                      "box_ls": [fig_box_linestyle] * len(arr_x), "box_lw": [fig_box_linewidth] * len(arr_x),
                      "box_ms": [fig_box_mean_size] * len(arr_x), "box_x": arr_x, "box_y": arr_y})
        y_range = deepcopy(arr_y)
        # markers
        arr_c, arr_x, arr_y = [], [], []
        for exp in list_exp:
            if "marker" in list(dict_distributions[dia][exp].keys()):
                d1 = dict_distributions[dia][exp]["marker"]
                arr_c += [fig_colors[exp]] * len(d1["x"])
                arr_x += d1["x"] if isinstance(d1["x"], list) is True else [d1["x"]]
                arr_y += d1["y"] if isinstance(d1["y"], list) is True else [d1["y"]]
        kwarg.update({"mar_ce": arr_c, "mar_cf": arr_c, "mar_m": ["o"] * len(arr_x),
                      "mar_s": [fig_box_outlier_size] * len(arr_x), "mar_x": arr_x, "mar_y": arr_y})
        y_range += deepcopy(arr_y)
        # title
        kwarg["title"] = numbering[counter]
        # x-axis
        list_datasets = dict_distributions[dia][list_exp[0]]["boxplot"]["x_tick_labels"]
        kwarg["x_tic"] = list(range(len(list_datasets)))
        kwarg["x_lab"] = [""] * len(list_datasets)
        kwarg["x_lim"] = [min(kwarg["x_tic"]) - 0.5, max(kwarg["x_tic"]) + 0.5]
        if dia == data_diagnostics[-1]:
            kwarg["x_nam"] = fig_titles["x_axis"][dia]
        # y-axis
        kwarg["y_lab"], kwarg["y_lim"], kwarg["y_tic"] = tool_figure_axis(fig_ticks["y_axis"][dia], arr_i=y_range)
        kwarg["y_nam"] = fig_titles["y_axis"][dia]
        # text
        x1, x2, y1, y2 = kwarg["x_lim"] + kwarg["y_lim"]
        dy = (y2 - y1) * default_plot["size_y"] / (y_size * y_frac * 100)
        if dia == data_diagnostics[-1]:
            arr_c, arr_x, arr_y = [], [], []
            for ii, dat in enumerate(list_datasets):
                arr_c.append(fig_colors["boxplot"][dat] if dat in list(fig_colors["boxplot"].keys()) else "k")
                arr_x.append(ii)
                arr_y.append(y1 - 3 * dy)
            kwarg.update({"text": list_datasets, "text_c": arr_c, "text_fs": [12] * len(arr_x),
                          "text_ha": ["center"] * len(arr_x), "text_r": [90] * len(arr_x),
                          "text_va": ["top"] * len(arr_x), "text_x": arr_x, "text_y": arr_y})
        # curves (line between datasets)
        arr_x = [[ii + 0.5, ii + 0.5] for ii, _ in enumerate(list_datasets[: -1])]
        kwarg.update({"cur_x": arr_x, "cur_y": [[y1, y2]] * len(arr_x)})
        # plot
        ax = plt.subplot(gs[y_position: y_position + y_size, x_position: x_position + x_size])
        plot_main(ax, **kwarg)
        counter += 1
        y_position += y_size + y_delt
    # plot directory (relative to current file directory)
    plot_directory = "/".join(os.path.dirname(__file__).split("/")[:-2])
    # path to output figure
    figure_file_path = os.path.join(plot_directory, "plot/" + str(fig_name)) + "." + str(fig_format)
    # save
    plt.savefig(figure_file_path, bbox_inches="tight", format=fig_format)
    plt.close()
    return


def fig_scatter_and_regression(dict_i: dict, data_diagnostics: list, fig_format: str, fig_name: str,
                               fig_colors: dict, fig_markers: dict, fig_marker_size: float, fig_orientation: str,
                               fig_panel_size: dict, fig_ticks: dict, fig_titles: dict, fig_legend_bool: bool = True,
                               fig_legend_position: str = "bottom", fig_multiple_regression: bool = False,
                               fig_title_bool: bool = True, panel_param: dict = None):
    """
    Template for F4, S3 and S5: scatterplots
    
    Inputs:
    -------
    :param dict_i: dict
        Dictionary with three nested levels [diagnostic, dataset, x-or-y], filled with the data to plot
    :param data_diagnostics: list
        Names of diagnostic (to keep them in the right order);
        e.g., data_diagnostics = ['ave_pr_val_n30e', 'ave_ts_val_n30e']
    :param fig_format: str
        Format of the figure; e.g., fig_format = 'pdf'
        Four figure formats are accepted: 'eps', 'pdf', 'png', 'svg'
    :param fig_name: str
        Name of the output file; e.g., fig_name = 'name_of_the_figure'
    :param fig_colors: dict
        Dictionary with one level [dataset], filled with the color to plot each dataset;
        e.g., fig_colors = {'ACCESS-CM2': 'orange', 'ACCESS-ESM1-5': 'forestgreen'}
    :param fig_markers: dict
        Dictionary with one level [dataset], filled with the marker to plot each dataset;
        e.g., fig_markers = {'ACCESS-CM2': '>', 'ACCESS-ESM1-5': '<'}
    :param fig_marker_size: float
        Size of the markers; e.g., fig_marker_size = 60.
    :param fig_orientation: str
        Orientation of the figure; e.g., fig_orientation = 'column'
        Two figure orientations are accepted:
            'column' (column = variables,  row = statistics)
            'row'    (column = statistics, row = variables)
    :param fig_panel_size: dict
        Dictionary defining the size of each panel;
        e.g., fig_panel_size = {'x_delt': 2, 'x_frac': 0.5, 'x_size': 5, 'y_delt': 3, 'y_frac': 0.5, 'y_size': 8}
        'x' and 'y' correspond respectively to the x-axis (horizontal) and y-axis (vertical)
        'delt' is the distance between panels (in inches)
        'size' is the size of each panel (in inches)
        'frac' is a fraction to multiply 'delt' and 'size' (to shrink or expend figure proportionally)
    :param fig_ticks: dict
        Dictionary defining the range and tics of axes; e.g., fig_ticks = {'ave_pr_val_n30e': [0, 1, 2, 3, 4]}
    :param fig_titles: dict
        Dictionary defining the titles of panels and axes;
        e.g., fig_titles = {
            'ave_pr_val_n30e': {'x': 'N3 PR', 'y': 'mean', 'z': 'xbar'},
            'x_axis': {'ave_pr_val_n30e': 'piControl values'},
            'y_axis': {'ave_pr_val_n30e': 'historical values'},
        }
    :param fig_legend_bool: bool, optional
        True to plot the datasets legend; e.g., fig_legend_bool = True
        Default is True
    :param fig_legend_position: str, optional
        Position of the legend; e.g., fig_legend_position = 'bottom'
        Two legend positions are accepted: 'bottom', 'right'
        Default is 'bottom'
    :param fig_multiple_regression: bool
        Compute a different regression for each dataset; e.g., fig_multiple_regression = True
        Default is False
    :param fig_title_bool: bool, optional
        True to plot titles of columns and rows; e.g., fig_title_bool = True
        Default is True
    :param panel_param: dict, optional
        Dictionary to modify default values of panel parameters (see fig_panel.py);
        e.g., panel_param = {'x_nbr_minor': 0}
        Default is None (no modification of the default values)
    """
    if panel_param is None:
        panel_param = {}
    # plot initialization
    x_delt, x_frac, x_size = fig_panel_size["x_delt"], fig_panel_size["x_frac"], fig_panel_size["x_size"]
    y_delt, y_frac, y_size = fig_panel_size["y_delt"], fig_panel_size["y_frac"], fig_panel_size["y_size"]
    if len(data_diagnostics) == 1:
        list_dia, n_panel_per_line = deepcopy(data_diagnostics), 1
        nbr_c, nbr_l = deepcopy(x_size), deepcopy(y_size)
    else:
        list_dia, n_panel_per_line, nbr_c, nbr_l = tool_figure_initialization(
            data_diagnostics, fig_orientation, x_delt, x_size, y_delt, y_size)
    plt.figure(0, figsize=(nbr_c * x_frac, nbr_l * y_frac))
    gs = GridSpec(nbr_l, nbr_c)
    numbering = string.ascii_lowercase
    x_position, y_position = 0, 0
    for jj, dia in enumerate(list_dia):
        kwarg = {**panel_param, **{"x_size": x_size * x_frac, "y_size": y_size * y_frac}}
        # dictionary
        d1 = dict_i[dia]
        # markers
        arr_c, arr_m, arr_x, arr_y, arr_z = [], [], [], [], []
        for dat in list(d1.keys()):
            xx, yy = [], []
            if (dia in list(fig_ticks.keys()) and isinstance(fig_ticks[dia], list) is True) or (
                    "x_axis" in list(fig_ticks.keys()) and dia in list(fig_ticks["x_axis"].keys()) and
                    isinstance(fig_ticks["x_axis"][dia], list) is True and "y_axis" in list(fig_ticks.keys()) and
                    dia in list(fig_ticks["y_axis"].keys()) and isinstance(fig_ticks["y_axis"][dia], list) is True):
                for k1, k2 in zip(d1[dat]["x"], d1[dat]["y"]):
                    if (dia in list(fig_ticks.keys()) and min(fig_ticks[dia]) < k1 < max(fig_ticks[dia]) and
                            min(fig_ticks[dia]) < k2 < max(fig_ticks[dia])) or (
                            "x_axis" in list(fig_ticks.keys()) and "y_axis" in list(fig_ticks.keys()) and
                            min(fig_ticks["x_axis"][dia]) < k1 < max(fig_ticks["x_axis"][dia]) and
                            min(fig_ticks["y_axis"][dia]) < k2 < max(fig_ticks["y_axis"][dia])):
                        xx.append(k1)
                        yy.append(k2)
            else:
                xx, yy = d1[dat]["x"], d1[dat]["y"]
            if len(xx) > 0:
                arr_c += [fig_colors[dat]] * len(xx)
                arr_m += [fig_markers[dat]] * len(xx)
                arr_x += deepcopy(xx)
                arr_y += deepcopy(yy)
                arr_z += [random__randint(1, 8)] * len(xx)
        kwarg.update({"mar_cf": arr_c, "mar_m": arr_m, "mar_s": [fig_marker_size] * len(arr_x), "mar_x": arr_x,
                      "mar_y": arr_y, "mar_z": arr_z})
        # title
        if fig_title_bool is True:
            kwarg["title"] = numbering[jj]
            kwarg["title_col"], kwarg["title_row"] = tool_title(fig_titles[dia], jj, n_panel_per_line, fig_orientation)
        # x-y axes
        kwarg["x_nam"] = fig_titles["x_axis"][dia]
        kwarg["y_nam"] = fig_titles["y_axis"][dia]
        if isinstance(fig_ticks, dict) is True and "x_axis" in list(fig_ticks.keys()) and \
                "y_axis" in list(fig_ticks.keys()) and dia in list(fig_ticks["x_axis"].keys()) and \
                dia in list(fig_ticks["y_axis"].keys()):
            kwarg["x_lab"], kwarg["x_lim"], kwarg["x_tic"] = tool_figure_axis(fig_ticks["x_axis"][dia], arr_i=arr_x)
            kwarg["y_lab"], kwarg["y_lim"], kwarg["y_tic"] = tool_figure_axis(fig_ticks["y_axis"][dia], arr_i=arr_y)
        else:
            list_ticks = None
            if dia in list(fig_ticks.keys()) and isinstance(fig_ticks[dia], list) is True:
                list_ticks = fig_ticks[dia]
            kwarg["x_lab"], kwarg["x_lim"], kwarg["x_tic"] = tool_figure_axis(list_ticks, arr_i=arr_x + arr_y)
            kwarg["y_lab"], kwarg["y_lim"], kwarg["y_tic"] = kwarg["x_lab"], kwarg["x_lim"], kwarg["x_tic"]
        print(dia, "min = " + str("{0:.3f}".format(round(min(arr_x + arr_y), 3))).rjust(5),
              "max = " + str("{0:.3f}".format(round(max(arr_x + arr_y), 3))).rjust(5))
        x1, x2, y1, y2 = kwarg["x_lim"] + kwarg["y_lim"]
        dx = (x2 - x1) * default_plot["size_x"] / (x_size * x_frac * 100)
        dy = (y2 - y1) * default_plot["size_y"] / (y_size * y_frac * 100)
        # curve (linear regression)
        list_regressions = []
        if fig_multiple_regression is True:
            for dat in list(d1.keys()):
                cc, mm = fig_colors[dat], fig_markers[dat]
                xx = [k3 for k1, k2, k3 in zip(arr_c, arr_m, arr_x) if k1 == cc and k2 == mm]
                yy = [k3 for k1, k2, k3 in zip(arr_c, arr_m, arr_y) if k1 == cc and k2 == mm]
                slop, inte, corr, pval = stat_regression(xx, yy)
                list_regressions.append({"c": cc, "i": inte, "n": dat, "p": pval, "r": corr, "s": slop})
        else:
            slop, inte, corr, pval = stat_regression(arr_x, arr_y)
            list_regressions.append({"c": "k", "i": inte, "n": "", "p": pval, "r": corr, "s": slop})
        arr_c, arr_y = [], []
        for k in list_regressions:
            arr_c.append(k["c"])
            arr_y.append([k["s"] * x + k["i"] for x in kwarg["x_lim"]])
        kwarg.update({"cur_c": arr_c, "cur_lw": [2] * len(arr_y), "cur_x": [kwarg["x_lim"]] * len(arr_y),
                      "cur_y": arr_y, "cur_z": [9] * len(arr_y)})
        # text
        arr_c, arr_m, arr_x, arr_y, arr_z = [], [], [], [], []
        for k1, dict_t in enumerate(list_regressions):
            lv = []
            if "n" in dict_t.keys() and dict_t["n"] != "":
                lv = [dict_t["n"]]
            lv += [str(k2) + "{0:+.3f}".format(round(k3, 3))
                   for k2, k3 in zip(["r=", "s=", "p="], [dict_t["r"], dict_t["s"], dict_t["p"]])]
            for k2, v in enumerate(lv):
                arr_c.append(dict_t["c"])
                arr_m.append(v)
                if len(list_regressions) == 1 or k1 == 0:
                    arr_x.append(x2 - 2 * dx)
                    arr_y.append(y1 + 7 * dy * (len(lv) - 0.3 - k2))
                    arr_z.append("right")
                else:
                    arr_x.append(x1 + 2 * dx)
                    arr_y.append(y2 - 7 * dy * (2 + k2))
                    arr_z.append("left")
        kwarg.update({"text": arr_m, "text_c": arr_c, "text_ha": arr_z, "text_x": arr_x, "text_y": arr_y})
        # legend
        if fig_legend_bool is True:
            # add markers and dataset names at the bottom or top right of the figure
            leg_d, leg_t = {}, []
            list_datasets = list(set([k2 for k1 in list(dict_i.keys()) for k2 in list(dict_i[k1].keys())]))
            tool_legend_datasets(list_datasets, fig_colors, fig_markers, leg_d, leg_t, list_dia, jj, n_panel_per_line,
                                 fig_legend_position, x_frac, x_size, y_frac, y_size)
            kwarg.update({"legend_param": leg_d, "legend_txt": leg_t})
        # plot
        ax = plt.subplot(gs[y_position: y_position + y_size, x_position: x_position + x_size])
        plot_main(ax, **kwarg)
        x_position += x_size + x_delt
        if (jj + 1) % n_panel_per_line == 0:
            x_position = 0
            y_position += y_size + y_delt
    # plot directory (relative to current file directory)
    plot_directory = "/".join(os.path.dirname(__file__).split("/")[:-2])
    # path to output figure
    figure_file_path = os.path.join(plot_directory, "plot/" + str(fig_name)) + "." + str(fig_format)
    # save
    plt.savefig(figure_file_path, bbox_inches="tight", format=fig_format)
    plt.close()
    return


def fig_time_series_and_distributions(dict_i: dict, diagnostic: str, data_epoch_lengths: list, data_experiments: list,
                                      fig_format: str, fig_name: str, fig_colors: dict, fig_linecolor: str,
                                      fig_linestyle: str, fig_linewidth: float, fig_panel_size: dict, fig_ticks: dict,
                                      fig_titles: dict, nbr_dur: int = 2, nbr_gap: float = 0.5,
                                      panel_param: dict = None):
    """
    Template for S2: Time series and time series of boxplots
    
    Inputs:
    -------
    :param dict_i: dict
        Dictionary with four nested levels [experiment, epoch_length, boxplot-or-curve-or-marker, x-or-y], filled with
        the data to plot
    :param diagnostic: str
        Name of the diagnostic to plot; e.g., diagnostic = 'ave_pr_val_n30e'
    :param data_epoch_lengths: list
        Names of epoch length (to keep them in the right order);
        e.g., data_experiments = ['030_year_epoch', '060_year_epoch']
    :param data_experiments: list
        Names of experiment (to keep them in the right order); e.g., data_experiments = ['piControl', 'historical']
    :param fig_format: str
        Format of the figure; e.g., fig_format = 'pdf'
        Four figure formats are accepted: 'eps', 'pdf', 'png', 'svg'
    :param fig_name: str
        Name of the output file; e.g., fig_name = 'name_of_the_figure'
    :param fig_colors: dict
        Dictionary with one level [epoch_length], filled with a list of colors;
        e.g., fig_colors = {'030_year_epoch': ['orange']}
    :param fig_linecolor: str
        Color of the lines; e.g., fig_linecolor = 'k'
    :param fig_linestyle: str
        Style of the lines; e.g., fig_linestyle = '-'
    :param fig_linewidth: float
        Width of the lines; e.g., fig_linewidth = 1.
    :param fig_panel_size: dict
        Dictionary defining the size of each panel;
        e.g., fig_panel_size = {'x_delt': 2, 'x_frac': 0.5, 'x_size': 5, 'y_delt': 3, 'y_frac': 0.5, 'y_size': 8}
        'x' and 'y' correspond respectively to the x-axis (horizontal) and y-axis (vertical)
        'delt' is the distance between panels (in inches)
        'size' is the size of each panel (in inches)
        'frac' is a fraction to multiply 'delt' and 'size' (to shrink or expend figure proportionally)
    :param fig_ticks: dict
        Dictionary with two nested levels [x-or-y_axis, diagnostic], filled with a list of tics;
        e.g., fig_ticks = {
            'x_axis': {'ave_pr_val_n30e': [0, 1]},
            'y_axis': {'ave_pr_val_n30e': [0, 1, 2, 3, 4]},
        }
    :param fig_titles: dict
        Dictionary defining the titles of panels and axes;
        e.g., fig_titles = {
            'ave_pr_val_n30e': {'x': 'N3 PR', 'y': 'mean', 'z': 'xbar'},
            'x_axis': {'historical': {'ave_pr_val_n30e': ''}},
            'y_axis': {'ave_pr_val_n30e': 'N3 PR xbar (mm/day)'},
        }
    :param nbr_dur: int, optional
        Number of minimum epoch length to plot before and after the gap for the piControl run; e.g., nbr_dur = 2
        Default is 2
    :param nbr_gap: float, optional
        Number of minimum epoch length bor the size of the gap for the piControl run; e.g., nbr_gap = 1.
        Default is 0.5
    :param panel_param: dict, optional
        Dictionary to modify default values of panel parameters (see fig_panel.py);
        e.g., panel_param = {'x_nbr_minor': 0}
        Default is None (no modification of the default values)
    """
    if panel_param is None:
        panel_param = {}
    # plot initialization
    list_durations = sorted(list(dict_i[data_experiments[0]].keys()), key=str.casefold)
    dur_r = int(sorted(data_epoch_lengths, key=str.casefold)[0].split("_")[0])
    nbr_exp = len(data_experiments)
    x_frac = fig_panel_size["x_frac"]
    y_delt, y_frac, y_size = fig_panel_size["y_delt"], fig_panel_size["y_frac"], fig_panel_size["y_size"]
    nbr_c = int(dur_r * (nbr_dur * 2 + 1 + nbr_gap))
    nbr_l = nbr_exp * (len(list_durations) * (y_size + y_delt) + (4 - 1) * y_delt) - 4 * y_delt
    plt.figure(0, figsize=(nbr_c * x_frac, nbr_l * y_frac))
    gs = GridSpec(nbr_l, nbr_c)
    numbering = string.ascii_lowercase
    x_position, y_position = 0, 0
    counter = 0
    for exp in data_experiments:
        for ii, dur in enumerate(list_durations):
            # time
            d1 = dict_i[exp][list_durations[0]]["curve"]["x"][0]
            y1, y2 = int(d1[0] / 12), int(d1[-1] / 12)
            # diagnostic name
            dia = diagnostic.replace(diagnostic[:4], "tim_") if dur not in data_epoch_lengths else deepcopy(diagnostic)
            # epoch length
            dur_t = deepcopy(dur_r) if dur not in data_epoch_lengths else int(dur.split("_")[0])
            # nbr of dur_r epochs
            int_t = int(nbr_dur * dur_r / dur_t)
            # panel x-and-y sizes
            if exp == "piControl" and dur not in data_epoch_lengths:
                x_size2 = int((nbr_dur * 2 + nbr_gap + 1) * dur_r)
            elif exp == "piControl":
                x_size2 = int((nbr_dur * 2 + nbr_gap) * dur_r)
            else:
                x_size2 = y2 - y1 + 1
            y_size2 = int(y_size / 2) if dur in data_epoch_lengths else deepcopy(y_size)
            kwarg = {**panel_param, **{"x_size": x_size2 * x_frac, "y_size": y_size2 * y_frac}}
            # dictionary
            if dur not in data_epoch_lengths:
                d1 = dict_i[exp][dur]["curve"]
            elif exp == "piControl":
                d1 = dict_i[exp][dur]["marker"]
            else:
                d1 = dict_i[exp][dur]["boxplot"]
            # title
            kwarg["title"] = numbering[counter]
            if dur not in data_epoch_lengths:
                kwarg["title_col"] = deepcopy(exp)
            # x-axis
            if exp == "piControl" and dur not in data_epoch_lengths:
                kwarg["x_tic"] = list(range(0, nbr_dur * dur_r * 12 + 1, dur_r * 12)) + \
                    [k + (nbr_dur + nbr_gap) * dur_r * 12 for k in list(range(0, nbr_dur * dur_r * 12 + 1, dur_r * 12))]
                kwarg["x_lim"] = [0, (nbr_dur * 2 + nbr_gap + 1) * dur_r * 12]
            elif exp == "piControl":
                kwarg["x_tic"] = list(range(0, nbr_dur * dur_r * 12 + 1, dur_r * 12)) + \
                    [k + (nbr_dur + nbr_gap) * dur_r * 12 for k in list(range(0, nbr_dur * dur_r * 12 + 1, dur_r * 12))]
                kwarg["x_lim"] = [0, (nbr_dur * 2 + nbr_gap) * dur_r * 12]
            else:
                kwarg["x_tic"] = list(range(y1 * 12, y2 * 12 + 1, dur_r * 12))
                kwarg["x_lim"] = [y1 * 12, y2 * 12]
            kwarg["x_nam"] = fig_titles["x_axis"][exp][dia] if dur == data_epoch_lengths[-1] else ""
            if exp == "piControl" and dur == data_epoch_lengths[-1]:
                kwarg["x_lab"] = list(range(0, dur_r * nbr_dur + 1, dur_r))
                kwarg["x_lab"] += [((y2 - y1 + 1) // dur_r - nbr_dur) * dur_r + k for k in kwarg["x_lab"]]
            elif exp != "piControl" and dur == data_epoch_lengths[-1]:
                kwarg["x_lab"] = [str(int(k / 12)) for k in kwarg["x_tic"]]
            else:
                kwarg["x_lab"] = [""] * len(kwarg["x_tic"])
            # boxplot
            y_range = []
            if exp != "piControl" and dur in data_epoch_lengths:
                arr_x, arr_y = d1["x"], d1["y"]
                arr_c = fig_colors[dur] + ["k"] * (len(arr_x) - len(fig_colors[dur]))
                arr_fs = [2] * len(arr_x)
                arr_ls = ["-"] * len(arr_x)
                arr_lw = [0.5] * len(arr_x)
                arr_ms = [3] * len(arr_x)
                kwarg.update({"box_c": arr_c, "box_fs": arr_fs, "box_ls": arr_ls, "box_lw": arr_lw, "box_ms": arr_ms,
                              "box_x": arr_x, "box_y": arr_y})
                y_range += arr_y
            # marker
            if exp == "piControl" and dur in data_epoch_lengths:
                arr_y = d1["y"][: int_t] + d1["y"][-int_t:]
                arr_x = d1["x"][: int_t]
                arr_x += [(nbr_dur + nbr_gap) * dur_r * 12 + k for k in arr_x]
                arr_c = fig_colors[dur] + ["k"] * (len(arr_x) - len(fig_colors[dur]))
                arr_ls = ["o"] * len(arr_x)
                arr_lw = [30] * len(arr_x)
                kwarg.update({"mar_cf": arr_c, "mar_m": arr_ls, "mar_s": arr_lw, "mar_x": arr_x, "mar_y": arr_y})
                y_range += arr_y
            # curve
            arr_c, arr_fs, arr_ls, arr_lw, arr_ms, arr_x, arr_y, arr_w, arr_z = [], [], [], [], [], [], [], [], []
            if dur not in data_epoch_lengths:
                if exp == "piControl":
                    arr_y += [d1["y"][0][: int(nbr_dur * dur_r * 12)]]
                    arr_y += [d1["y"][0][((y2 - y1 + 1) // dur_r - nbr_dur) * dur_r * 12:]]
                    arr_x += [d1["x"][0][: int(nbr_dur * dur_r * 12)]]
                    arr_x += [[max(arr_x[0]) + nbr_gap * dur_r * 12 + k for k in range(0, len(arr_y[1]))]]
                else:
                    arr_x += d1["x"]
                    arr_y += d1["y"]
                arr_c += [fig_linecolor] * len(arr_x)
                arr_ls += [fig_linestyle] * len(arr_x)
                arr_lw += [fig_linewidth] * len(arr_x)
                arr_z += [1] * len(arr_x)
                y_range += arr_y
            # y-axis
            kwarg["y_lab"], kwarg["y_lim"], kwarg["y_tic"] = tool_figure_axis(fig_ticks["y_axis"][dia], arr_i=y_range)
            if dur not in data_epoch_lengths:
                kwarg["y_nam"] = fig_titles["y_axis"][dia]
            xx1, xx2, yy1, yy2 = kwarg["x_lim"] + kwarg["y_lim"]
            dx, dy = (xx2 - xx1) / 100, (yy2 - yy1) / 100
            if exp == "piControl":
                if dur in data_epoch_lengths:
                    list_int = [[dur_t * 12. * k] * 2 for k in range(1, int_t + 1)]
                    list_int += [[list_int[-1][0] + dur_r * 12. / 2] * 2]
                    list_int += [[list_int[-1][0] + dur_t * 12. * k] * 2 for k in range(1, int_t + 1)]
                    arr_c += ["darkgrey"] * len(list_int)
                    arr_ls += ["--"] * len(list_int)
                    arr_lw += [1] * len(list_int)
                    arr_x += list_int
                    arr_y += [kwarg["y_lim"]] * len(list_int)
                    arr_z += [2] * len(list_int)
                arr_c += ["k"]
                arr_ls += ["-"]
                arr_lw += [2]
                arr_x += [[(dur_r * nbr_dur + 1.5) * 12, (dur_r * (nbr_dur + nbr_gap) - 1.5) * 12]]
                arr_y += [[yy1 + 50 * dy] * 2]
                arr_z += [2]
            kwarg.update({"cur_c": arr_c, "cur_ls": arr_ls, "cur_lw": arr_lw, "cur_x": arr_x, "cur_y": arr_y,
                          "cur_z": arr_z})
            # text
            if dur in data_epoch_lengths:
                if exp == "piControl":
                    arr_x = [xx2 - dur_r * 12 / 2]
                    arr_y = [yy2 - 1 * dy * default_plot["size_y"] / (y_size2 * y_frac)]
                    arr_ls = ["center"]
                    arr_ms = ["top"]
                    arr_z = [str((y2 - y1 + 1) // dur_t) + " values\nusing " + str(dur_t) + "-year\nepochs"]
                else:
                    arr_x = [xx2 - 1 * dx * default_plot["size_x"] / (x_size2 * x_frac)]
                    arr_y = [yy1 + 1 * dy * default_plot["size_y"] / (y_size2 * y_frac)]
                    arr_ls = ["right"]
                    arr_ms = ["bottom"]
                    arr_z = [str(len(d1["y"][0])) + " values for each " + str(dur_t) + "-year epoch"]
                arr_c, arr_fs, arr_lw = ["k"], [9], [0]
                if ((len(data_epoch_lengths) % 2 == 0 and ii == len(data_epoch_lengths) / 2) or
                        (len(data_epoch_lengths) % 2 == 1 and ii == math__ceil(len(data_epoch_lengths) / 2))):
                    arr_x += [xx1 - 21 * dx * default_plot["size_x"] / (x_size2 * x_frac)]
                    arr_y += [yy1 - 50 * (y_delt / y_size2) * dy]
                    arr_c += ["k"]
                    arr_fs += [15]
                    arr_ls += ["right"]
                    arr_ms += ["center"]
                    arr_lw += [90]
                    arr_z += [fig_titles["y_axis"][dia]]
                kwarg.update({"text": arr_z, "text_c": arr_c, "text_fs": arr_fs, "text_ha": arr_ls, "text_r": arr_lw,
                              "text_va": arr_ms, "text_x": arr_x, "text_y": arr_y})
            # plot
            ax = plt.subplot(gs[y_position: y_position + y_size2, x_position: x_position + x_size2])
            plot_main(ax, **kwarg)
            if exp == "piControl" and dur == data_epoch_lengths[-1]:
                for k in range(3):
                    xxx = (nbr_dur * dur_r + 4 + 3.5 * k) * 12
                    yyy = yy1 + (len(data_epoch_lengths) * (1.1 + (y_delt / y_size2)) + (y_size / y_size2)) * 100 * dy
                    ax.annotate("", xy=(xxx, yy1 - 5 * dy), xytext=(xxx, yyy), xycoords="data", annotation_clip=False,
                                zorder=11, arrowprops=dict(arrowstyle="-", color="white", lw=4))
            if dur in data_epoch_lengths:
                for kk, cc in enumerate(fig_colors[dur]):
                    if exp == "piControl":
                        xx = xx1 + (dur_t / 2 + dur_t * kk) * 12
                    else:
                        xx = xx1 + (dur_t / 2 + 5 * kk) * 12
                    yy = yy1 + (125 - 12 * kk) * dy
                    ax.annotate("", xy=(xx, yy), xytext=(xx, yy - 3.5 * dy), xycoords="data", zorder=4,
                                annotation_clip=False,
                                arrowprops=dict(arrowstyle="-[,widthB=" + str(dur_t / 9) + ",lengthB=0.3", lw=2.0,
                                                color=cc))
                    ax.annotate("", xy=(xx, yy), xytext=(xx, yy1 + 40 * dy), xycoords="data", zorder=5,
                                annotation_clip=False,
                                arrowprops=dict(arrowstyle="<|-,head_length=0.5,head_width=0.3", color=cc, lw=2.0))
            counter += 1
            if exp == "piControl" and dur in data_epoch_lengths:
                #
                # -- piControl boxplot
                #
                xx, yy = xx2 + 1 * dx, yy1 + 50 * dy
                ax.annotate("", xy=(xx, yy), xytext=(xx + 15 * dx, yy), xycoords="data", zorder=2,
                            annotation_clip=False,
                            arrowprops=dict(arrowstyle="<|-,head_length=0.5,head_width=0.3", color=fig_colors[exp],
                                            lw=2.0))
                x_size2 = int(dur_r / 3.5)
                x_position = nbr_c - x_size2
                kwarg = {**panel_param, **{"x_size": x_size2 * x_frac, "y_size": y_size2 * y_frac}}
                # dictionary
                d1 = dict_i[exp][dur]["boxplot"]
                # title
                kwarg["title"] = numbering[counter]
                # x-axis
                kwarg["x_lab"], kwarg["x_lim"], kwarg["x_nam"], kwarg["x_tic"] = [""], [-0.5, 0.5], "", [-1]
                # y-axis
                kwarg["y_tic"] = fig_ticks["y_axis"][dia]
                kwarg["y_lim"] = [min(kwarg["y_tic"]), max(kwarg["y_tic"])]
                kwarg["y_lab"], kwarg["y_nam"] = [""] * len(kwarg["y_tic"]), ""
                # boxplot
                arr_x, arr_y = d1["x"], d1["y"]
                arr_c = [fig_colors[exp]] * len(arr_x)
                arr_fs = [2] * len(arr_x)
                arr_ls = ["-"] * len(arr_x)
                arr_lw = [0.5] * len(arr_x)
                arr_ms = [3] * len(arr_x)
                arr_w = [0.5] * len(arr_x)
                kwarg.update({"box_c": arr_c, "box_fs": arr_fs, "box_ls": arr_ls, "box_lw": arr_lw, "box_ms": arr_ms,
                              "box_x": arr_x, "box_y": arr_y, "box_w": arr_w})
                # plot
                ax = plt.subplot(gs[y_position: y_position + y_size2, x_position: x_position + x_size2])
                plot_main(ax, **kwarg)
                counter += 1
            x_position = 0
            y_position += y_size2 + y_delt
        y_position += y_delt * 4
    # plot directory (relative to current file directory)
    plot_directory = "/".join(os.path.dirname(__file__).split("/")[:-2])
    # path to output figure
    figure_file_path = os.path.join(plot_directory, "plot/" + str(fig_name)) + "." + str(fig_format)
    # save
    plt.savefig(figure_file_path, bbox_inches="tight", format=fig_format)
    plt.close()
    return


def fig_time_series_and_distributions_b(dict_i: dict, diagnostic: str, data_epoch_lengths: list, data_experiments: list,
                                        fig_format: str, fig_name: str, fig_colors: dict, fig_linecolor: str,
                                        fig_linestyle: str, fig_linewidth: float, fig_panel_size: dict, fig_ticks: dict,
                                        fig_titles: dict, nbr_dur: int = 2, nbr_gap: float = 0.5,
                                        panel_param: dict = None):
    if panel_param is None:
        panel_param = {}
    # plot initialization
    list_durations = sorted(list(dict_i[data_experiments[0]].keys()), key=str.casefold)
    dur_r = int(sorted(data_epoch_lengths, key=str.casefold)[0].split("_")[0])
    nbr_exp = len(data_experiments)
    x_frac = fig_panel_size["x_frac"]
    y_delt, y_frac, y_size = fig_panel_size["y_delt"], fig_panel_size["y_frac"], fig_panel_size["y_size"]
    nbr_c = int(dur_r * (nbr_dur * 2 + 1 + nbr_gap))
    nbr_l = nbr_exp * (len(list_durations) * (y_size + y_delt) + (4 - 1) * y_delt) - 4 * y_delt
    plt.figure(0, figsize=(nbr_c * x_frac, nbr_l * y_frac))
    gs = GridSpec(nbr_l, nbr_c)
    numbering = string.ascii_lowercase
    x_position, y_position = 0, 0
    counter = 0
    for exp in data_experiments:
        for ii, dur in enumerate(list_durations):
            # time
            d1 = dict_i[exp][list_durations[0]]["curve"]["x"][0]
            y1, y2 = int(d1[0] / 12), int(d1[-1] / 12)
            # diagnostic name
            dia = diagnostic.replace(diagnostic[:4], "tim_") if dur not in data_epoch_lengths else deepcopy(diagnostic)
            # epoch length
            dur_t = deepcopy(dur_r) if dur not in data_epoch_lengths else int(dur.split("_")[0])
            # nbr of dur_r epochs
            int_t = int(nbr_dur * dur_r / dur_t)
            # panel x-and-y sizes
            if exp == "piControl" and dur not in data_epoch_lengths:
                x_size2 = int((nbr_dur * 2 + nbr_gap + 1) * dur_r)
            elif exp == "piControl":
                x_size2 = int((nbr_dur * 2 + nbr_gap) * dur_r)
            else:
                x_size2 = y2 - y1 + 1
            y_size2 = int(y_size / 1.3) if dur in data_epoch_lengths else deepcopy(y_size)
            kwarg = {**panel_param, **{"x_size": x_size2 * x_frac, "y_size": y_size2 * y_frac}}
            # dictionary
            if dur not in data_epoch_lengths:
                d1 = dict_i[exp][dur]["curve"]
            elif exp == "piControl":
                d1 = dict_i[exp][dur]["marker"]
            else:
                d1 = dict_i[exp][dur]["boxplot"]
            # title
            kwarg["title"] = numbering[counter]
            if dur not in data_epoch_lengths:
                kwarg["title_col"] = deepcopy(exp)
            # x-axis
            if exp == "piControl" and dur not in data_epoch_lengths:
                kwarg["x_tic"] = list(range(0, nbr_dur * dur_r * 12 + 1, dur_r * 12)) + \
                                 [k + (nbr_dur + nbr_gap) * dur_r * 12 for k in
                                  list(range(0, nbr_dur * dur_r * 12 + 1, dur_r * 12))]
                kwarg["x_lim"] = [0, (nbr_dur * 2 + nbr_gap + 1) * dur_r * 12]
            elif exp == "piControl":
                kwarg["x_tic"] = list(range(0, nbr_dur * dur_r * 12 + 1, dur_r * 12)) + \
                                 [k + (nbr_dur + nbr_gap) * dur_r * 12 for k in
                                  list(range(0, nbr_dur * dur_r * 12 + 1, dur_r * 12))]
                kwarg["x_lim"] = [0, (nbr_dur * 2 + nbr_gap) * dur_r * 12]
            else:
                kwarg["x_tic"] = list(range(y1 * 12, y2 * 12 + 1, dur_r * 12))
                kwarg["x_lim"] = [y1 * 12, y2 * 12]
            kwarg["x_nam"] = fig_titles["x_axis"][exp][dia] if dur == data_epoch_lengths[-1] else ""
            if exp == "piControl" and dur == data_epoch_lengths[-1]:
                kwarg["x_lab"] = list(range(0, dur_r * nbr_dur + 1, dur_r))
                kwarg["x_lab"] += [((y2 - y1 + 1) // dur_r - nbr_dur) * dur_r + k for k in kwarg["x_lab"]]
            elif exp != "piControl" and dur == data_epoch_lengths[-1]:
                kwarg["x_lab"] = [str(int(k / 12)) for k in kwarg["x_tic"]]
            else:
                kwarg["x_lab"] = [""] * len(kwarg["x_tic"])
            # boxplot
            y_range = []
            if exp != "piControl" and dur in data_epoch_lengths:
                arr_x, arr_y = d1["x"], d1["y"]
                arr_c = fig_colors[dur] + ["k"] * (len(arr_x) - len(fig_colors[dur]))
                arr_fs = [2] * len(arr_x)
                arr_ls = ["-"] * len(arr_x)
                arr_lw = [0.5] * len(arr_x)
                arr_ms = [3] * len(arr_x)
                kwarg.update({"box_c": arr_c, "box_fs": arr_fs, "box_ls": arr_ls, "box_lw": arr_lw, "box_ms": arr_ms,
                              "box_x": arr_x, "box_y": arr_y})
                y_range += arr_y
            # marker
            if exp == "piControl" and dur in data_epoch_lengths:
                arr_y = d1["y"][: int_t] + d1["y"][-int_t:]
                arr_x = d1["x"][: int_t]
                arr_x += [(nbr_dur + nbr_gap) * dur_r * 12 + k for k in arr_x]
                arr_c = fig_colors[dur] + ["k"] * (len(arr_x) - len(fig_colors[dur]))
                arr_ls = ["o"] * len(arr_x)
                arr_lw = [30] * len(arr_x)
                kwarg.update({"mar_cf": arr_c, "mar_m": arr_ls, "mar_s": arr_lw, "mar_x": arr_x, "mar_y": arr_y})
                y_range += arr_y
            # curve
            arr_c, arr_fs, arr_ls, arr_lw, arr_ms, arr_x, arr_y, arr_w, arr_z = [], [], [], [], [], [], [], [], []
            if dur not in data_epoch_lengths:
                if exp == "piControl":
                    arr_y += [d1["y"][0][: int(nbr_dur * dur_r * 12)]]
                    arr_y += [d1["y"][0][((y2 - y1 + 1) // dur_r - nbr_dur) * dur_r * 12:]]
                    arr_x += [d1["x"][0][: int(nbr_dur * dur_r * 12)]]
                    arr_x += [[max(arr_x[0]) + nbr_gap * dur_r * 12 + k for k in range(0, len(arr_y[1]))]]
                else:
                    arr_x += d1["x"]
                    arr_y += d1["y"]
                arr_c += [fig_linecolor] * len(arr_x)
                arr_ls += [fig_linestyle] * len(arr_x)
                arr_lw += [fig_linewidth] * len(arr_x)
                arr_z += [1] * len(arr_x)
                y_range += arr_y
            # y-axis
            kwarg["y_lab"], kwarg["y_lim"], kwarg["y_tic"] = tool_figure_axis(fig_ticks["y_axis"][dia], arr_i=y_range)
            if dur not in data_epoch_lengths:
                kwarg["y_nam"] = fig_titles["y_axis"][dia]
            xx1, xx2, yy1, yy2 = kwarg["x_lim"] + kwarg["y_lim"]
            dx, dy = (xx2 - xx1) / 100, (yy2 - yy1) / 100
            if exp == "piControl":
                if dur in data_epoch_lengths:
                    list_int = [[dur_t * 12. * k] * 2 for k in range(1, int_t + 1)]
                    list_int += [[list_int[-1][0] + dur_r * 12. / 2] * 2]
                    list_int += [[list_int[-1][0] + dur_t * 12. * k] * 2 for k in range(1, int_t + 1)]
                    arr_c += ["darkgrey"] * len(list_int)
                    arr_ls += ["--"] * len(list_int)
                    arr_lw += [1] * len(list_int)
                    arr_x += list_int
                    arr_y += [kwarg["y_lim"]] * len(list_int)
                    arr_z += [2] * len(list_int)
                arr_c += ["k"]
                arr_ls += ["-"]
                arr_lw += [2]
                arr_x += [[(dur_r * nbr_dur + 1.5) * 12, (dur_r * (nbr_dur + nbr_gap) - 1.5) * 12]]
                arr_y += [[yy1 + 50 * dy] * 2]
                arr_z += [2]
            kwarg.update({"cur_c": arr_c, "cur_ls": arr_ls, "cur_lw": arr_lw, "cur_x": arr_x, "cur_y": arr_y,
                          "cur_z": arr_z})
            # text
            if dur in data_epoch_lengths:
                if exp == "piControl":
                    arr_x = [xx2 - dur_r * 12 / 2]
                    arr_y = [yy2 - 1 * dy * default_plot["size_y"] / (y_size2 * y_frac)]
                    arr_ls = ["center"]
                    arr_ms = ["top"]
                    arr_z = [str((y2 - y1 + 1) // dur_t) + " values\nusing " + str(dur_t) + "-year\nepochs"]
                else:
                    arr_x = [xx2 - 1 * dx * default_plot["size_x"] / (x_size2 * x_frac)]
                    arr_y = [yy1 + 1 * dy * default_plot["size_y"] / (y_size2 * y_frac)]
                    arr_ls = ["right"]
                    arr_ms = ["bottom"]
                    arr_z = [str(len(d1["y"][0])) + " values for each " + str(dur_t) + "-year epoch"]
                arr_c, arr_fs, arr_lw = ["k"], [9], [0]
                if ((len(data_epoch_lengths) % 2 == 0 and ii == len(data_epoch_lengths) / 2) or
                        (len(data_epoch_lengths) % 2 == 1 and ii == math__ceil(len(data_epoch_lengths) / 2))):
                    arr_x += [xx1 - 21 * dx * default_plot["size_x"] / (x_size2 * x_frac)]
                    arr_y += [yy1 + 50 * dy]
                    arr_c += ["k"]
                    arr_fs += [15]
                    arr_ls += ["right"]
                    arr_ms += ["center"]
                    arr_lw += [90]
                    arr_z += [fig_titles["y_axis"][dia]]
                kwarg.update({"text": arr_z, "text_c": arr_c, "text_fs": arr_fs, "text_ha": arr_ls, "text_r": arr_lw,
                              "text_va": arr_ms, "text_x": arr_x, "text_y": arr_y})
            # plot
            ax = plt.subplot(gs[y_position: y_position + y_size2, x_position: x_position + x_size2])
            plot_main(ax, **kwarg)
            if exp == "piControl" and dur == data_epoch_lengths[-1]:
                for k in range(3):
                    xxx = (nbr_dur * dur_r + 4 + 3.5 * k) * 12
                    yyy = yy1 + (len(data_epoch_lengths) * (1.1 + (y_delt / y_size2)) + (y_size / y_size2)) * 100 * dy
                    ax.annotate("", xy=(xxx, yy1 - 5 * dy), xytext=(xxx, yyy), xycoords="data", annotation_clip=False,
                                zorder=11, arrowprops=dict(arrowstyle="-", color="white", lw=4))
            if dur in data_epoch_lengths:
                for kk, cc in enumerate(fig_colors[dur]):
                    if exp == "piControl":
                        xx = xx1 + (dur_t / 2 + dur_t * kk) * 12
                    else:
                        xx = xx1 + (dur_t / 2 + 5 * kk) * 12
                    yy = yy1 + (135 - 15 * kk) * dy
                    ax.annotate("", xy=(xx, yy), xytext=(xx, yy - 3.5 * dy), xycoords="data", zorder=4,
                                annotation_clip=False,
                                arrowprops=dict(arrowstyle="-[,widthB=" + str(dur_t / 9) + ",lengthB=0.3", lw=2.0,
                                                color=cc))
                    ax.annotate("", xy=(xx, yy), xytext=(xx, yy1 + 40 * dy), xycoords="data", zorder=5,
                                annotation_clip=False,
                                arrowprops=dict(arrowstyle="<|-,head_length=0.5,head_width=0.3", color=cc, lw=2.0))
            counter += 1
            if exp == "piControl" and dur in data_epoch_lengths:
                #
                # -- piControl boxplot
                #
                xx, yy = xx2 + 1 * dx, yy1 + 50 * dy
                ax.annotate("", xy=(xx, yy), xytext=(xx + 15 * dx, yy), xycoords="data", zorder=2,
                            annotation_clip=False,
                            arrowprops=dict(arrowstyle="<|-,head_length=0.5,head_width=0.3", color=fig_colors[exp],
                                            lw=2.0))
                x_size2 = int(dur_r / 3.5)
                x_position = nbr_c - x_size2
                kwarg = {**panel_param, **{"x_size": x_size2 * x_frac, "y_size": y_size2 * y_frac}}
                # dictionary
                d1 = dict_i[exp][dur]["boxplot"]
                # title
                kwarg["title"] = numbering[counter]
                # x-axis
                kwarg["x_lab"], kwarg["x_lim"], kwarg["x_nam"], kwarg["x_tic"] = [""], [-0.5, 0.5], "", [-1]
                # y-axis
                kwarg["y_tic"] = fig_ticks["y_axis"][dia]
                kwarg["y_lim"] = [min(kwarg["y_tic"]), max(kwarg["y_tic"])]
                kwarg["y_lab"], kwarg["y_nam"] = [""] * len(kwarg["y_tic"]), ""
                # boxplot
                arr_x, arr_y = d1["x"], d1["y"]
                arr_c = [fig_colors[exp]] * len(arr_x)
                arr_fs = [2] * len(arr_x)
                arr_ls = ["-"] * len(arr_x)
                arr_lw = [0.5] * len(arr_x)
                arr_ms = [3] * len(arr_x)
                arr_w = [0.5] * len(arr_x)
                kwarg.update({"box_c": arr_c, "box_fs": arr_fs, "box_ls": arr_ls, "box_lw": arr_lw, "box_ms": arr_ms,
                              "box_x": arr_x, "box_y": arr_y, "box_w": arr_w})
                # plot
                ax = plt.subplot(gs[y_position: y_position + y_size2, x_position: x_position + x_size2])
                plot_main(ax, **kwarg)
                counter += 1
            x_position = 0
            y_position += y_size2 + y_delt
        y_position += int(y_delt * 1.5)
    # plot directory (relative to current file directory)
    plot_directory = "/".join(os.path.dirname(__file__).split("/")[:-2])
    # path to output figure
    figure_file_path = os.path.join(plot_directory, "plot/" + str(fig_name)) + "." + str(fig_format)
    # save
    plt.savefig(figure_file_path, bbox_inches="tight", format=fig_format)
    plt.close()
    return
# ---------------------------------------------------------------------------------------------------------------------#
