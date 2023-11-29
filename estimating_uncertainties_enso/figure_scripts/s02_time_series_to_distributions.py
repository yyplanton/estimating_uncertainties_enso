# -*- coding:UTF-8 -*-
# ---------------------------------------------------------------------------------------------------------------------#
# Figure S2 of the paper about estimating_uncertainties_in_simulated_ENSO submitted to JAMES
# Plot: time series and time series of distributions
# ---------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------#
# Import packages
# ---------------------------------------------------#
# estimating_uncertainties_enso package
from . params import default_parameters
from estimating_uncertainties_enso.compute_lib.data_lib import data_organize_json, data_organize_netcdf
from estimating_uncertainties_enso.compute_lib.tool_lib import tool_put_in_dict
from estimating_uncertainties_enso.figure_templates.fig_template import fig_time_series_and_distributions
# ---------------------------------------------------#


# ---------------------------------------------------------------------------------------------------------------------#
# Default arguments
# ---------------------------------------------------------------------------------------------------------------------#
default = {
    #
    # -- Data
    #
    # list of diagnostics
    "data_diagnostics": ["ave_ts_val_n30e"],
    # list of epoch lengths
    "data_epoch_lengths": ["030_year_epoch", "060_year_epoch"],
    # list of projects
    "data_projects": ["cmip6"],
    # list of experiments
    "data_experiments": default_parameters["data_experiments"],
    #
    # -- Figure
    #
    # SMILE to plot
    "fig_selected_model": default_parameters["fig_smile_selected"],
    # figure format: eps, pdf, png, svg
    "fig_format": default_parameters["fig_format"],
    # figure name includes input parameters (may create a very long figure name)
    "fig_detailed_name": False,
    # size of each panel
    "fig_panel_size": {"x_frac": 0.04, "y_delt": 3, "y_frac": 0.1, "y_size": 16},
    # color per dataset
    "fig_colors": {
        "piControl": "royalblue",
        "030_year_epoch": ["lime", "gold"],
        "060_year_epoch": ["pink"],
    },
    # line color, style, width (for time series)
    "fig_linecolor": "k",
    "fig_linestyle": "-",
    "fig_linewidth": 0.5,
    # ticks
    "fig_ticks": {
        "y_axis": {
            "ave_ts_val_n30e": [23.7, 25.1],
            "tim_ts_val_n30e": [20.0, 29.5],
        },
    },
    # plot titles
    "fig_titles": {
        "x_axis": {"historical": {"ave_ts_val_n30e": "Time"}, "piControl": {"ave_ts_val_n30e": "Year"}},
        **default_parameters["fig_titles"],  # add diagnostics, experiments and absolute / relative uncertainty
    },
    # panel parameters (to modify default values in fig_panel.py)
    "panel_param": {"x_nbr_minor": 0, "title_col_y": 8},
}
# ---------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------------------------------------------------------------------------#
# Main
# ---------------------------------------------------------------------------------------------------------------------#
def s02_creating_distributions(data_diagnostics: list = default["data_diagnostics"],
                               data_epoch_lengths: list = default["data_epoch_lengths"],
                               data_experiments: list = default["data_experiments"],
                               data_projects: list = default["data_projects"],
                               fig_colors: dict = default["fig_colors"],
                               fig_detailed_name: bool = default["fig_detailed_name"],
                               fig_format: str = default["fig_format"],
                               fig_linecolor: str = default["fig_linecolor"],
                               fig_linestyle: str = default["fig_linestyle"],
                               fig_linewidth: float = default["fig_linewidth"],
                               fig_panel_size: dict = default["fig_panel_size"],
                               fig_selected_model: str = default["fig_selected_model"],
                               fig_ticks: dict = default["fig_ticks"],
                               fig_titles: dict = default["fig_titles"],
                               panel_param: dict = default["panel_param"], **kwargs):
    #
    # -- Read json
    #
    values, metadata = data_organize_json(data_diagnostics, data_epoch_lengths, data_projects, data_experiments)
    #
    # -- Read netCDF
    #
    list_dia = [k.replace(k[:4], "tim_") for k in data_diagnostics]
    tim_values, tim_metadata = data_organize_netcdf(list_dia, data_projects, data_experiments)
    # add time series metadata to metadata dictionary
    for k in list(tim_metadata.keys()):
        metadata[k] = tim_metadata[k]
    #
    # -- Organize data for plot
    #
    data_to_plot = {}
    for dia in list(values.keys()):
        for dur in list(values[dia].keys()):
            for pro in list(values[dia][dur].keys()):
                for exp in list(values[dia][dur][pro].keys()):
                    for dat in list(values[dia][dur][pro][exp].keys()):
                        if dat == fig_selected_model:
                            dia_tim = dia.replace(dia[:4], "tim_")
                            # list epochs
                            list_epo = sorted(list(values[dia][dur][pro][exp][dat].keys()), key=str.casefold)
                            # boxplots
                            if exp == "piControl":
                                arr_x = [0]
                            else:
                                arr_x = [(int(epo[1:]) + int(dur.split("_")[0]) / 2) * 12 for epo in list_epo]
                            arr_y = [values[dia][dur][pro][exp][dat][epo] for epo in list_epo]
                            data_to_plot = tool_put_in_dict(data_to_plot, arr_x, dia, exp, dur, "boxplot", "x")
                            data_to_plot = tool_put_in_dict(data_to_plot, arr_y, dia, exp, dur, "boxplot", "y")
                            # markers
                            if exp == "piControl":
                                arr_y = arr_y[0]
                                arr_x = [((k + 0.5) * int(dur.split("_")[0])) * 12 for k, _ in enumerate(arr_y)]
                                data_to_plot = tool_put_in_dict(data_to_plot, arr_x, dia, exp, dur, "marker", "x")
                                data_to_plot = tool_put_in_dict(data_to_plot, arr_y, dia, exp, dur, "marker", "y")
                            # time series
                            if dur == data_epoch_lengths[0]:
                                arr_y = tim_values[dia_tim][pro][exp][dat]
                                arr_x = list(range(len(arr_y[0])))
                                if exp != "piControl":
                                    arr_x = [int(list_epo[0][1:]) * 12 + k for k in arr_x]
                                arr_x = [arr_x] * len(arr_y)
                                data_to_plot = tool_put_in_dict(data_to_plot, arr_x, dia, exp, "0000", "curve", "x")
                                data_to_plot = tool_put_in_dict(data_to_plot, arr_y, dia, exp, "0000", "curve", "y")
    for dia in list(values.keys()) + list(tim_values.keys()):
        # x title
        for exp in data_experiments:
            if "x_axis" in list(fig_titles.keys()) and isinstance(fig_titles["x_axis"], dict) is True and \
                    exp in list(fig_titles["x_axis"].keys()) and isinstance(fig_titles["x_axis"][exp], dict) is True \
                    and dia in list(fig_titles["x_axis"][exp].keys()) and \
                    isinstance(fig_titles["x_axis"][exp][dia], dict) is True:
                pass
            else:
                fig_titles = tool_put_in_dict(fig_titles, "", "x_axis", exp, dia)
        # y title
        statistic = "" if fig_titles[dia]["z"] == "" else " " + str(fig_titles[dia]["z"])
        units = "" if metadata[dia]["units"] == "" else " (" + str(metadata[dia]["units"]) + ")"
        name = str(fig_titles[dia]["x"]) + str(statistic) + str(units)
        fig_titles = tool_put_in_dict(fig_titles, name, "y_axis", dia)
        # y tics
        if "y_axis" in list(fig_ticks.keys()) and isinstance(fig_ticks, dict) is True and \
                dia in list(fig_ticks["y_axis"].keys()) and isinstance(fig_ticks["y_axis"][dia], list) is True:
            pass
        else:
            fig_ticks = tool_put_in_dict(fig_ticks, None, "y_axis", dia)
    #
    # -- Figure
    #
    for dia in list(data_to_plot.keys()):
        # output figure name will be the file name (path removed and extension removed)
        fig_name = __file__.split("/")[-1].split(".")[0] + "_" + str(dia)
        if fig_detailed_name is True:
            # add details of the computation to the figure name
            fig_name += "_data_" + str(len(data_projects)) + "pro_" + str(len(data_experiments)) + "exp"
        fig_time_series_and_distributions(data_to_plot[dia], dia, data_epoch_lengths, data_experiments,
                                          fig_format, fig_name, fig_colors, fig_linecolor, fig_linestyle, fig_linewidth,
                                          fig_panel_size, fig_ticks, fig_titles, panel_param=panel_param)
# ---------------------------------------------------------------------------------------------------------------------#
