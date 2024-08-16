# -*- coding:UTF-8 -*-
# ---------------------------------------------------------------------------------------------------------------------#
# Figure S1 of the paper about estimating_uncertainties_in_simulated_ENSO submitted to JAMES
# Plot: time series of global mean temperature and comparison PI vs HI
# ---------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------#
# Import packages
# ---------------------------------------------------#
# estimating_uncertainties_enso package
from . params import default_parameters
from estimating_uncertainties_enso.compute_lib.data_lib import data_organize_json
from estimating_uncertainties_enso.compute_lib.nest_lib import nest_quality_control_distributions
from estimating_uncertainties_enso.compute_lib.tool_lib import tool_put_in_dict
from estimating_uncertainties_enso.figure_templates.fig_template import fig_quality_control
# ---------------------------------------------------#


# ---------------------------------------------------------------------------------------------------------------------#
# Default arguments
# ---------------------------------------------------------------------------------------------------------------------#
default = {
    #
    # -- Data
    #
    # file name
    "data_filename": default_parameters["data_filename"],
    # list of diagnostics
    "data_diagnostics": default_parameters["data_diagnostics"],
    # list of epoch lengths
    "data_epoch_lengths": ["030_year_epoch"],
    # list of projects
    "data_projects": ["cmip6"],
    # list of experiments
    "data_experiments": default_parameters["data_experiments"],
    # minimum number of member for SMILEs: int [1, 100]
    "data_smile_minimum_size": default_parameters["data_smile_minimum_size"],
    #
    # -- Figure
    #
    # figure format: eps, pdf, png, svg
    "fig_format": default_parameters["fig_format"],
    # something added to figure name by user: str
    "fig_name_add": "",
    # figure name includes input parameters (may create a very long figure name)
    "fig_name_details": False,
    # size of each panel
    "fig_panel_size": {"x_delt": 0, "x_frac": 1, "x_size": 16, "y_delt": 3, "y_frac": 0.2, "y_size": 8},
    # color per dataset
    "fig_colors": {
        # experiments
        "historical": default_parameters["fig_colors"]["historical"],
        "piControl": default_parameters["fig_colors"]["piControl"],
        # datasets to highlight
        "boxplot": {"CAS-ESM2-0": "orange"},
    },
    # boxplots param
    "fig_box_linestyle": "-",
    "fig_box_linewidth": 1,
    "fig_box_mean_size": 4,
    "fig_box_outlier_size": 3,
    # line color, style, width (for time series)
    "fig_cur_linecolor": "grey",
    "fig_cur_linestyle": "-",
    "fig_cur_linewidth": 1,
    # ticks
    "fig_ticks": {
        "y_axis": {
            "ave_hf_val_n30e": [-5.0, 8.0],
            "ave_hf_val_n34e": [-6.0, 8.0],
            "ave_hf_val_n40e": [-10.0, 8.0],
            "ave_pr_val_n30e": [-0.8, 1.1],
            "ave_pr_val_n34e": [-1.0, 1.4],
            "ave_pr_val_n40e": [-1.3, 1.6],
            "ave_sl_val_n30e": [-7.0, 6.0],
            "ave_sl_val_n34e": [-9.0, 6.0],
            "ave_sl_val_n40e": [-10.0, 6.0],
            "ave_ts_val_n30e": [-0.7, 1.5],
            "ave_ts_val_n34e": [-0.7, 1.5],
            "ave_ts_val_n40e": [-0.7, 1.5],
            "ave_tx_val_n30e": [-4.0, 7.0],
            "ave_tx_val_n34e": [-7.0, 11.0],
            "ave_tx_val_n40e": [-7.0, 12.0],
            "ave_ty_val_n30e": [-11.0, 4.0],
            "ave_ty_val_n34e": [-11.0, 4.0],
            "ave_ty_val_n40e": [-6.0, 4.0],
            "cor_sl_n30e_to_ts_n30e": [-1.3, 0.2],
            "cor_sl_n34e_to_ts_n34e": [-1.2, 0.3],
            "cor_sl_n40e_to_ts_n40e": [-1.0, 0.5],
            "cor_ts_n30e_to_hf_n30e": [-0.3, 0.9],
            "cor_ts_n34e_to_hf_n34e": [-0.6, 0.8],
            "cor_ts_n40e_to_hf_n40e": [-0.6, 0.8],
            "cor_ts_n30e_to_tx_n34e": [-1.0, 0.3],
            "cor_ts_n30e_to_tx_n40e": [-1.1, 0.3],
            "cor_ts_n34e_to_tx_n40e": [-1.1, 0.3],
            "fbk_sl_n30e_to_ts_n30e": [-38.0, 6.0],
            "fbk_sl_n34e_to_ts_n34e": [-36.0, 10.0],
            "fbk_sl_n40e_to_ts_n40e": [-25.0, 21.0],
            "fbk_ts_n30e_to_hf_n30e": [-5.0, 16.0],
            "fbk_ts_n34e_to_hf_n34e": [-9.0, 14.0],
            "fbk_ts_n40e_to_hf_n40e": [-12.0, 14.0],
            "fbk_ts_n30e_to_tx_n34e": [-6.5, 3.5],
            "fbk_ts_n30e_to_tx_n40e": [-7.0, 4.0],
            "fbk_ts_n34e_to_tx_n40e": [-6.5, 3.0],
            "ske_hf_ano_n30e": [-3.5, 2.0],
            "ske_hf_ano_n34e": [-4.0, 2.5],
            "ske_hf_ano_n40e": [-2.5, 2.0],
            "ske_pr_ano_n30e": [-4.0, 5.0],
            "ske_pr_ano_n34e": [-3.0, 5.0],
            "ske_pr_ano_n40e": [-2.0, 2.0],
            "ske_sl_ano_n30e": [-1.5, 2.0],
            "ske_sl_ano_n34e": [-1.5, 1.5],
            "ske_sl_ano_n40e": [-2.0, 1.5],
            "ske_ts_ano_n30e": [-1.4, 1.4],
            "ske_ts_ano_n34e": [-1.4, 1.3],
            "ske_ts_ano_n40e": [-1.5, 1.2],
            "ske_tx_ano_n30e": [-0.8, 1.4],
            "ske_tx_ano_n34e": [-1.0, 1.5],
            "ske_tx_ano_n40e": [-1.0, 1.7],
            "ske_ty_ano_n30e": [-2.0, 1.5],
            "ske_ty_ano_n34e": [-4.0, 2.0],
            "ske_ty_ano_n40e": [-3.0, 2.0],
            "var_hf_ano_n30e": [-200, 550],
            "var_hf_ano_n34e": [-300, 600],
            "var_hf_ano_n40e": [-200, 400],
            "var_pr_ano_n30e": [-3.0, 7.0],
            "var_pr_ano_n34e": [-5.0, 9.0],
            "var_pr_ano_n40e": [-5.0, 9.0],
            "var_sl_ano_n30e": [-30, 50],
            "var_sl_ano_n34e": [-30, 45],
            "var_sl_ano_n40e": [-30, 45],
            "var_ts_ano_n30e": [-1.0, 2.0],
            "var_ts_ano_n34e": [-1.1, 1.9],
            "var_ts_ano_n40e": [-0.7, 1.4],
            "var_tx_ano_n30e": [-40, 75],
            "var_tx_ano_n34e": [-150, 200],
            "var_tx_ano_n40e": [-150, 300],
            "var_ty_ano_n30e": [-20.0, 30.0],
            "var_ty_ano_n34e": [-45.0, 70.0],
            "var_ty_ano_n40e": [-35.0, 55.0],
        },
    },
    # plot titles
    "fig_titles": {
        "x_axis": {"tim_ts_val_glob": "Year"},
        **default_parameters["fig_titles"],
    },
    # panel parameters (to modify default values in fig_panel.py)
    "panel_param_box": {"x_nbr_minor": 0},
    "panel_param_tim": {},
}
# ---------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------------------------------------------------------------------------#
# Main
# ---------------------------------------------------------------------------------------------------------------------#
def s01_quality_control_box(
        data_diagnostics: list = default["data_diagnostics"],
        data_epoch_lengths: list = default["data_epoch_lengths"],
        data_experiments: list = default["data_experiments"],
        data_filename: str = default["data_filename"],
        data_projects: list = default["data_projects"],
        data_smile_minimum_size: int = default["data_smile_minimum_size"],
        fig_box_linestyle: str = default["fig_box_linestyle"],
        fig_box_linewidth: float = default["fig_box_linewidth"],
        fig_box_mean_size: float = default["fig_box_mean_size"],
        fig_box_outlier_size: float = default["fig_box_outlier_size"],
        fig_colors: dict = default["fig_colors"],
        fig_cur_linecolor: str = default["fig_cur_linecolor"],
        fig_cur_linestyle: str = default["fig_cur_linestyle"],
        fig_cur_linewidth: float = default["fig_cur_linewidth"],
        fig_format: str = default["fig_format"],
        fig_name_add: str = default["fig_name_add"],
        fig_name_details: bool = default["fig_name_details"],
        fig_panel_size: dict = default["fig_panel_size"],
        fig_ticks: dict = default["fig_ticks"],
        fig_titles: dict = default["fig_titles"],
        panel_param_box: dict = default["panel_param_box"],
        panel_param_tim: dict = default["panel_param_tim"],
        **kwargs):
    #
    # -- Read json
    #
    values, metadata = data_organize_json(data_diagnostics, data_epoch_lengths, data_projects, data_experiments,
                                          data_filename=data_filename)
    #
    # -- Organize data for plot
    #
    # compute the difference between piControl mean and the other values
    distributions_to_plot = nest_quality_control_distributions(values, data_experiments)
    for dia in list(distributions_to_plot.keys()):
        # x title
        if "x_axis" in list(fig_titles.keys()) and isinstance(fig_titles["x_axis"], dict) is True and \
                dia in list(fig_titles["x_axis"].keys()) and isinstance(fig_titles["x_axis"][dia], str) is True:
            pass
        else:
            fig_titles = tool_put_in_dict(fig_titles, "", "x_axis", dia)
        # y title
        statistic = "" if fig_titles[dia]["z"] == "" else " " + str(fig_titles[dia]["z"])
        units = "\n" if metadata[dia]["units"] == "" else "\n(" + str(metadata[dia]["units"]) + ")"
        name = str(fig_titles[dia]["x"]) + str(statistic) + str(units)
        name = name.replace("feedback", "fb.")
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
    # output figure name will be the file name (path removed and extension removed)
    fig_name = __file__.split("/")[-1].split(".")[0] + str(fig_name_add)
    if fig_name_details is True:
        # add details of the computation to the figure name
        fig_name += "_data_" + str(len(data_projects)) + "pro_" + str(len(data_experiments)) + "exp_" + \
                    str(data_smile_minimum_size) + "mem_" + str(len(data_diagnostics)) + "dia_"
        if len(data_epoch_lengths) == 0:
            fig_name += str(data_epoch_lengths[0])
        else:
            fig_name += str(len(data_epoch_lengths)) + "dur"
    fig_quality_control(distributions_to_plot, {}, data_diagnostics, fig_format, fig_name,
                        fig_box_linestyle, fig_box_linewidth, fig_box_mean_size, fig_box_outlier_size, fig_colors,
                        fig_cur_linecolor, fig_cur_linestyle, fig_cur_linewidth, fig_panel_size, fig_ticks, fig_titles,
                        1, panel_param_box=panel_param_box, panel_param_tim=panel_param_tim)
# ---------------------------------------------------------------------------------------------------------------------#
