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
def _tool_flatten_list(arr_i, list_values: list = None) -> list:
    """
    Flatten list of lists
    
    Inputs:
    -------
    :param arr_i: array_like
    :param list_values: list, optional
    
    Output:
    -------
    :return list_values: list
        Flatten list
    """
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


def _tool_axis_auto_ticks(arr_i: list) -> list:
    """
    Create automatic optimized axis ticks
    
    Input:
    ------
    :param arr_i: list
        Values to plot
    
    Output:
    -------
    :return list_ticks: list
        Ticks for the plot axis
    """
    # check input
    error = list()
    check_type(arr_i, "arr_i", list, error)
    print_fail(inspect__stack(), "\n".join(k for k in error))
    # if list contains lists, flatten lists
    list_values = _tool_flatten_list(arr_i)
    # compute auto range
    if len(list_values) == 0:
        list_ticks = list(range(2))
    elif len(list_values) == 1:
        value = list_values[0]
        # order of magnitude of the value
        o_of_magnitude = math__floor(math__log(value, 10))
        # coefficient corresponding to the order of magnitude
        coefficient = 10**o_of_magnitude
        # one tick below value and one tick above value
        list_ticks = [math__floor(value / coefficient) * coefficient, math__ceil(value / coefficient) * coefficient]
    else:
        # range of input values
        range_values = max(list_values) - min(list_values)
        # order of magnitude of a 4th of the range (5 ticks between min and max)
        o_of_magnitude = math__floor(math__log(range_values / 4, 10))
        # coefficient corresponding to the order of magnitude - 1 (values in 10s)
        coefficient = 10**o_of_magnitude
        # difference between the floor and the maximum value
        delta = max(list_values) / coefficient - math__floor(min(list_values) / coefficient)
        # increment to have 5 ticks between floor and max(list_values)
        increment = math__ceil(delta / 4)
        # adapt coefficient
        while delta / increment <= 3:
            # due to the rounding up, the increment may be too big, if it is the case the coefficient is decreased
            coefficient /= 10
            # difference between the floor and the maximum value
            delta = max(list_values) / coefficient - math__floor(min(list_values) / coefficient)
            # increment to have 5 ticks between floor and max(list_values)
            increment = math__ceil(delta / 4)
        # lowest order of magnitude lower than the minimum value and higher than maximum value
        floor = math__floor(min(list_values) / coefficient)
        ceiling = math__ceil(max(list_values) / coefficient)
        # make sure that there is 4 increments in range
        if ceiling - floor <= 4 * increment:
            ceiling += increment
        # 5 ticks
        list_ticks = [k * coefficient for k in range(floor, ceiling, increment)]
    return list_ticks


def tool_axis_label(arr_i: list, nam_i: str = "") -> list:
    """
    Format list of ints or floats into a list of str with the same number of decimals (up to 3 decimals)

    Inputs:
    -------
    :param arr_i: list
        Axis ticks; e.g., arr_i = [1, 2.5]
    :param nam_i: str, optional
        Name of the axis to do special labels (nam_i = 'latitude' or 'longitude')
        Default is '' (no special label)

    Output:
    -------
    :return labels: list
        Tick labels; e.g., labels = ['1.0', '2.5']
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


def tool_figure_axis(user_ticks, arr_i=None, axis_name: str = "") -> (list, list, list):
    """
    Create axis ticks, tick labels and limits
    
    Inputs:
    -------
    :param user_ticks: list
        User defined tics; e.g., user_ticks = [1, 2, 3, 4]
    :param arr_i: list, optional
        Values to plot; e.g., arr_i = [[1, 2], [3, 4], [[5, 6], [7, 8]]]
    :param axis_name: str, optional
        Name of the axis to do special labels; e.g., nam_i = 'latitude'
        Two names are recognized: 'latitude', 'longitude'
        Default is '' (no special label)
    
    Outputs:
    --------
    :return axis_tick_labels: list
        Axis tick labels
    :return axis_min_max: list
        Axis minimum and maximum values
    :return axis_ticks: list
        Axis ticks
    """
    if user_ticks is None:
        axis_ticks = _tool_axis_auto_ticks(arr_i)
    else:
        axis_ticks = deepcopy(user_ticks)
    axis_tick_labels = tool_axis_label(axis_ticks, nam_i=axis_name)
    axis_min_max = [min(axis_ticks), max(axis_ticks)]
    return axis_tick_labels, axis_min_max, axis_ticks


def tool_figure_initialization(data_diagnostics: list, fig_orientation: str, x_delt: int, x_size: int, y_delt: int,
                               y_size: int) -> (list, int, int, int):
    """
    Order diagnostics, choose how many diagnostics are plotted on each line, compute the number of columns and lines
    
    Inputs:
    -------
    :param data_diagnostics: list
        Names of diagnostic (to keep them in the right order);
        e.g., data_diagnostics = ['ave_pr_val_n30e', 'ave_ts_val_n30e']
    :param fig_orientation: str
        Orientation of the figure; e.g., fig_orientation = 'column'
        Two figure orientations are accepted:
            'column' (column = variables,  row = statistics)
            'row'    (column = statistics, row = variables)
    :param x_delt: int
        Horizontal distance between panels; e.g., x_delt = 1
    :param x_size: int
        Horizontal size of each panel; e.g., x_size = 4
    :param y_delt:  int
        Vertical distance between panels; e.g., y_delt = 1
    :param y_size: int
        Vertical size of each panel; e.g., y_size = 4
    
    Outputs:
    --------
    :return list_dia: list
        Ordered list of diagnostics
    :return n_panel_per_line: int
        Number of panels (diagnostics) per line
    :return nbr_c: int
        Number of columns
    :return nbr_l: int
        Number of lines
    """
    # check input
    error = list()
    check_type(data_diagnostics, "data_diagnostics", list, error)
    check_type(fig_orientation, "fig_orientation", str, error)
    print_fail(inspect__stack(), "\n".join(k for k in error))
    # reorder diagnostic list and select the number of diagnostic per line
    list_dia = []
    n_panel_per_line = 1
    if fig_orientation == "column":
        # order diagnostics to obtain first average, variance, skewness, correlation, slope
        for k1 in ["ave_", "var_", "ske_", "cor_", "fbk_"]:
            tmp = [k2 for k2 in data_diagnostics if k2[:4] == k1]
            if len(tmp) > 0:
                list_dia += tmp
                n_panel_per_line = len(tmp)
    else:
        # order diagnostics to obtain first precipitation, temperature, zonal wind stress, meridional wind stress,
        # net heat fluxes, sea level
        for k1 in ["_pr_", "_ts_", "_tx_", "_ty_", "_hf_", "_sl_"]:
            tmp = [k2 for k2 in data_diagnostics if k2[3:7] == k1 and k2[:4] not in ["cor_", "fbk_"]]
            if len(tmp) > 0:
                list_dia += tmp
                n_panel_per_line = len(tmp)
        # then wind stress feedback, heat flux feedback, thermocline feedback
        for k1 in ["_to_tx_", "_to_hf_", "_to_ts_"]:
            tmp = [k2 for k2 in data_diagnostics if k1 in k2 and k2[:4] in ["cor_", "fbk_"]]
            if len(tmp) > 0:
                list_dia += tmp
                n_panel_per_line = len(tmp)
    # number of columns and rows of the plot
    nbr_c = n_panel_per_line * (x_size + x_delt) - x_delt
    nbr_l = math__ceil(len(list_dia) / n_panel_per_line) * (y_size + y_delt) - y_delt
    return list_dia, n_panel_per_line, nbr_c, nbr_l


def tool_legend_datasets(list_legend: list, fig_colors: dict, fig_markers: dict, legend_dict: dict, legend_list: list,
                         data_diagnostics: list, counter: int, n_panel_per_line: int, fig_legend_position: str,
                         x_frac: float, x_size: int, y_frac: float, y_size: int):
    """
    Organize data for the datasets legend
    
    Inputs:
    -------
    :param list_legend: list
        Dataset names to put in the legend
    :param fig_colors: dict
        Dictionary with one level [dataset], filled with the color to plot each dataset;
        e.g., fig_colors = {'ACCESS-CM2': 'orange', 'ACCESS-ESM1-5': 'forestgreen'}
    :param fig_markers:
        Dictionary with one level [dataset], filled with the marker to plot each dataset;
        e.g., fig_markers = {'ACCESS-CM2': '>', 'ACCESS-ESM1-5': '<'}
    :param legend_dict: dict
        Dictionary with the legend parameters (see fig_panel.py) in which more keys will be added;
        e.g., legend_dict = {
            'ACCESS-CM2': {
                'position': {'x': 10, 'y': 10},
                'text': {'color': 'k'},
            },
        }
        Usually this dictionary is empty
    :param legend_list: list
        Order of the keys for the legend in which more keys will be added; e.g., legend_list = ['ACCESS-CM2']
    :param data_diagnostics:  list
        Names of diagnostic (to keep them in the right order);
        e.g., data_diagnostics = ['ave_pr_val_n30e', 'ave_ts_val_n30e']
    :param counter: int
        Panel number; e.g., counter = 0
    :param n_panel_per_line: int
        Number of panels (diagnostics) per line; e.g., n_panel_per_line = 2
    :param fig_legend_position:  str
        Position of the legend; e.g., fig_legend_position = 'bottom'
        Two legend positions are accepted: 'bottom', 'right'
    :param x_frac: float
        Fraction to multiply 'x_size' (to shrink or expend figure proportionally); e.g, x_frac = 1.
    :param x_size: int
        Horizontal size of each panel; e.g., x_size = 4
    :param y_frac: float
        Fraction to multiply 'y_size' (to shrink or expend figure proportionally); e.g., y_frac = 1.
    :param y_size: int
        Vertical size of each panel; e.g., y_size = 4
    """
    if (fig_legend_position == "bottom" and counter == len(data_diagnostics) - n_panel_per_line) or (
            fig_legend_position == "right" and counter + 1 == n_panel_per_line):
        # add markers and dataset names at the bottom or top right of the figure
        list_datasets = [k for k in list(fig_markers.keys()) if k in list_legend]
        if fig_legend_position == "bottom":
            n_dat_per_col = math__ceil(len(list_datasets) / (n_panel_per_line * 2))
            x0, x1, y0, y1 = -35, 70, -25, 8
        else:
            n_dat_per_col = len(list_datasets)
            x0, x1, y0, y1 = 105, 0, 94, 8
        x1 *= default_plot["size_x"] / (x_size * x_frac)
        y1 *= default_plot["size_y"] / (y_size * y_frac)
        for k1, k2 in enumerate(list_datasets):
            legend_dict[k2] = {"text": {"color": fig_colors[k2], "fontsize": 12}}
            legend_dict[k2]["marker"] = {"facecolor": fig_colors[k2], "marker": fig_markers[k2], "s": 80}
            legend_dict[k2]["position"] = {"x": x0 + x1 * (k1 // n_dat_per_col), "y": y0 - y1 * (k1 % n_dat_per_col)}
            legend_list.append(k2)
    return


def tool_title(fig_titles: dict, counter: int, n_panel_per_line: int, fig_orientation: str,
               txt: str = "") -> (str, str):
    """
    Choose to write column and row titles or not
    
    Inputs:
    -------
    :param fig_titles: dict
        Dictionary of 'x' and 'y' titles; e.g., fig_titles = {'x': 'N3 PR', 'y': 'mean'}
    :param counter: int
        Panel number; e.g., counter = 0
    :param n_panel_per_line: int
        Number of panels (diagnostics) per line; e.g., n_panel_per_line = 2
    :param fig_orientation: str
        Orientation of the figure; e.g., fig_orientation = 'column'
        Two figure orientations are accepted:
            'column' (column = variables,  row = statistics)
            'row'    (column = statistics, row = variables)
    :param txt: str
        Text to add to x-axis title
    
    Outputs:
    --------
    :return title_column: str
        Name of the column
    :return title_row: str
        Name of the row
    """
    if fig_orientation == "column":
        title_column = str(txt) + str(fig_titles["x"]) if counter < n_panel_per_line else ""
        title_row = fig_titles["y"] if counter % n_panel_per_line == 0 else ""
    else:
        title_column = fig_titles["y"] if counter < n_panel_per_line else ""
        title_row = str(txt) + str(fig_titles["x"]) if counter % n_panel_per_line == 0 else ""
    return title_column, title_row
# ---------------------------------------------------------------------------------------------------------------------#
