# -*- coding:UTF-8 -*-
# ---------------------------------------------------------------------------------------------------------------------#
# Functions to do basic processing for the figure templates of the paper about
# estimating_uncertainties_in_simulated_ENSO submitted to JAMES
# ---------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------#
# Import packages
# ---------------------------------------------------#
# basic python package
from copy import deepcopy
from inspect import stack as inspect__stack
from math import ceil as math__ceil
from math import floor as math__floor
from math import log as math__log
# numpy
from numpy import ndarray as numpy__ndarray
# estimating_uncertainties_enso package
from . fig_panel import default_plot
from estimating_uncertainties_enso.compute_lib.check_lib import check_type, print_fail
# ---------------------------------------------------#


# ---------------------------------------------------------------------------------------------------------------------#
# Functions
# ---------------------------------------------------------------------------------------------------------------------#
def _tool_axis_label(arr_i: list, nam_i: str = ""):
    """
    Format list of ints or floats into a list of str with the same number of decimals (up to 3 decimals)

    Inputs:
    -------
    :param arr_i: list
        List of ints or floats; e.g., arr_i = [1, 2.5]
    :param nam_i: str, optional
        Name of the axis to do special labels (nam_i = 'latitude' or 'longitude')
        Default is None (no special label)

    Output:
    -------
    :return labels: list
        List of strs; e.g., labels = ['1.0', '2.5']
    """
    # check input
    error = list()
    check_type(arr_i, "arr_i", list, error)
    check_type(nam_i, "nam_i", str, error)
    print_fail(inspect__stack(), "\n".join(k for k in error))
    # create labels
    labels = deepcopy(arr_i)
    if nam_i == "latitude":
        arr_i = [abs(k) if k < 0 else k for k in arr_i]
    elif nam_i == "longitude":
        arr_i = [360 - k if k > 180 else k for k in arr_i]
    if all([int(k) == k for k in arr_i]) is True:
        # int to str
        labels = [str(k) for k in arr_i]
    elif all([int(round(k * 10, 8)) == round(k * 10, 8) for k in arr_i]) is True:
        # format all values with 1 decimal
        labels = ["{0:.1f}".format(round(k, 1)) for k in arr_i]
    elif all([int(round(k * 100, 8)) == round(k * 100, 8) for k in arr_i]) is True:
        # format all values with 2 decimals
        labels = ["{0:.2f}".format(round(k, 2)) for k in arr_i]
    elif all([int(round(k * 1000, 8)) == round(k * 1000, 8) for k in arr_i]) is True:
        # format all values with 3 decimals
        labels = ["{0:.3f}".format(round(k, 3)) for k in arr_i]
    # latitude / longitude
    if nam_i == "latitude":
        labels = [str(k2) + "$^\circ$S" if k1 < 0 else (str(k2) + "$^\circ$N" if k1 > 0 else str(k2) + "$^\circ$")
                  for k1, k2 in zip(arr_i, labels)]
    elif nam_i == "longitude":
        labels = [str(k2) + "$^\circ$E" if k1 < 180 else (str(k2) + "$^\circ$W" if k1 > 180 else str(k2) + "$^\circ$")
                  for k1, k2 in zip(arr_i, labels)]
    return labels


def _tool_flatten_list(arr_i, list_values: list = None):
    # check input
    if list_values is None:
        list_values = []
    error = list()
    check_type(arr_i, "arr_i", (float, int, list, numpy__ndarray), error)
    print_fail(inspect__stack(), "\n".join(k for k in error))
    # if list contains list, flatten
    if isinstance(arr_i, (list, numpy__ndarray)) is True:
        for k in arr_i:
            _tool_flatten_list(k, list_values=list_values)
    else:
        list_values.append(arr_i)
    return list_values


def _tool_axis_auto_range(arr_i):
    # check input
    error = list()
    check_type(arr_i, "arr_i", list, error)
    print_fail(inspect__stack(), "\n".join(k for k in error))
    # if list contains lists, flatten lists
    list_values = _tool_flatten_list(arr_i)
    # compute auto range
    if len(list_values) == 0:
        list_tics = list(range(2))
    elif len(list_values) == 1:
        value = list_values[0]
        # order of magnitude of the value
        o_of_magnitude = math__floor(math__log(value, 10))
        # coefficient corresponding to the order of magnitude
        coefficient = 10**o_of_magnitude
        # one tick below value and one tick above value
        list_tics = [math__floor(value / coefficient) * coefficient, math__ceil(value / coefficient) * coefficient]
    else:
        # range of input values
        range_values = max(list_values) - min(list_values)
        # order of magnitude of a 4th of the range (5 tics between min and max)
        o_of_magnitude = math__floor(math__log(range_values / 4, 10))
        # coefficient corresponding to the order of magnitude - 1 (values in 10s)
        coefficient = 10**o_of_magnitude
        # lowest order of magnitude lower than the minimum value and higher than maximum value
        floor = math__floor(min(list_values) / coefficient)
        ceiling = math__ceil(max(list_values) / coefficient)
        # increment to have 5 tics between floor and max(list_values)
        increment = math__ceil((max(list_values) / coefficient - floor) / 4)
        # make sure that there is 4 increments in range
        if ceiling - floor <= 4 * increment:
            ceiling += increment
        # 5 ticks
        list_tics = [k * coefficient for k in range(floor, ceiling, increment)]
    return list_tics


def tool_figure_axis(user_ticks, arr_i=None, axis_name=""):
    if user_ticks is None:
        axis_ticks = _tool_axis_auto_range(arr_i)
    else:
        axis_ticks = deepcopy(user_ticks)
    axis_tick_labels = _tool_axis_label(axis_ticks, nam_i=axis_name)
    axis_min_max = [min(axis_ticks), max(axis_ticks)]
    return axis_tick_labels, axis_min_max, axis_ticks


def tool_figure_initialization(diagnostics, fig_orientation, x_delt, x_size, y_delt, y_size):
    # check input
    error = list()
    check_type(diagnostics, "diagnostics", list, error)
    check_type(fig_orientation, "fig_orientation", str, error)
    print_fail(inspect__stack(), "\n".join(k for k in error))
    # reorder diagnostic list and select the number of diagnostic per line
    if fig_orientation == "column":
        list_dia = deepcopy(diagnostics)
        n_panel_per_line = len([k for k in list_dia if "ave_" in k])
    else:
        list_dia = [k2 for k1 in ["_pr_", "_ts_"] for k2 in diagnostics if k1 in k2 and k2[:4] != "nst_"]
        n_panel_per_line = len([k for k in list_dia if ("_pr_" in list_dia[0] and "_pr_" in k) or
                                ("_ts_" in list_dia[0] and "_ts_" in k)])
    # number of columns and rows of the plot
    nbr_c = n_panel_per_line * (x_size + x_delt) - x_delt
    nbr_l = math__ceil(len(list_dia) / n_panel_per_line) * (y_size + y_delt) - y_delt
    return list_dia, n_panel_per_line, nbr_c, nbr_l


def tool_legend_datasets(dict_i, dict_colors, dict_markers, legend_dict, legend_list, list_diagnostics, counter,
                         nbr_panels_per_line, fig_legend_position, x_frac, x_size, y_frac, y_size,
                         uncertainty_reference: str = ""):
    if (fig_legend_position == "bottom" and counter == len(list_diagnostics) - nbr_panels_per_line) or (
            fig_legend_position == "right" and counter + 1 == nbr_panels_per_line):
        # add markers and dataset names at the bottom or top right of the figure
        list_datasets = [k for k in list(dict_markers.keys()) if k in list(dict_i.keys())]
        if fig_legend_position == "bottom":
            n_dat_per_col = math__ceil(len(list_datasets) / (nbr_panels_per_line * 2))
            x0, x1 = -35, 70
            # y0 = -32 if uncertainty_reference == "maximum" else -25
            y0 = -25
            y1 = 8
        else:
            n_dat_per_col = len(list_datasets)
            x0, x1, y0, y1 = 105, 0, 94, 8
        x1 *= default_plot["size_x"] / (x_size * x_frac)
        y1 *= default_plot["size_y"] / (y_size * y_frac)
        for k1, k2 in enumerate(list_datasets):
            legend_dict[k2] = {"text": {"color": dict_colors[k2], "fontsize": 12}}
            legend_dict[k2]["marker"] = {"facecolor": dict_colors[k2], "marker": dict_markers[k2], "s": 80}
            legend_dict[k2]["position"] = {"x": x0 + x1 * (k1 // n_dat_per_col), "y": y0 - y1 * (k1 % n_dat_per_col)}
            legend_list.append(k2)
    return


def tool_title(dict_titles, counter, nbr_panels_per_line, fig_orientation, txt=""):
    if fig_orientation == "column":
        title_column = str(txt) + str(dict_titles["x"]) if counter < nbr_panels_per_line else ""
        title_row = dict_titles["y"] if counter % nbr_panels_per_line == 0 else ""
    else:
        title_column = dict_titles["y"] if counter < nbr_panels_per_line else ""
        title_row = str(txt) + str(dict_titles["x"]) if counter % nbr_panels_per_line == 0 else ""
    return title_column, title_row
# ---------------------------------------------------------------------------------------------------------------------#
