# -*- coding:UTF-8 -*-
# ---------------------------------------------------------------------------------------------------------------------#
# Figure 6 of the paper about estimating_uncertainties_in_simulated_ENSO submitted to JAMES
# Plot: required ensemble sizes for several required uncertainty
# ---------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------#
# Import packages
# ---------------------------------------------------#
from copy import deepcopy
from numpy import array as numpy__array
# estimating_uncertainties_enso package
from . params import default_parameters
from estimating_uncertainties_enso.compute_lib.data_lib import data_organize_json
from estimating_uncertainties_enso.compute_lib.nest_lib import nest_compute_res, nest_define_uncertainty_threshold,\
    nest_examples_of_res_method
from estimating_uncertainties_enso.compute_lib.tool_lib import tool_put_in_dict
from estimating_uncertainties_enso.figure_templates.fig_template import fig_basic
# ---------------------------------------------------#


# ---------------------------------------------------------------------------------------------------------------------#
# Default arguments
# ---------------------------------------------------------------------------------------------------------------------#
default = {
    #
    # -- Data
    #
    # file name
    # "data_filename": default_parameters["data_filename"],
    "data_filename": "estimating_uncertainties_in_simulated_enso_sl.json",
    # list of diagnostics
    # "data_diagnostics": ["ave_sl_val_n30e", "var_sl_ano_n30e", "ske_sl_ano_n30e", "cor_sl_n30e_to_ts_n30e",
    #                      "fbk_sl_n30e_to_ts_n30e"],
    # "data_diagnostics": ["ave_sl_val_n30e", "var_sl_ano_n30e", "ske_sl_ano_n30e", "fbk_sl_n30e_to_ts_n30e"],
    "data_diagnostics": ["ave_sl_val_n30e", "var_sl_ano_n30e", "fbk_sl_n30e_to_ts_n30e"],
    # list of epoch lengths
    "data_epoch_lengths": ["030_year_epoch"],
    # list of projects
    "data_projects": default_parameters["data_projects"],
    # list of experiments
    "data_experiments": default_parameters["data_experiments"],
    # create the MME: True, False
    "data_mme_create": True,
    # MME made with all available SMILEs (or 1st SMILE of each model): True, False
    "data_mme_use_all_smiles": default_parameters["data_mme_use_all_smiles"],
    # MME made with ensemble means (or 1st member of each SMILE): True, False
    "data_mme_use_smile_mean": default_parameters["data_mme_use_smile_mean"],
    # minimum number of member for SMILEs: int [1, 100]
    "data_smile_minimum_size": 5,
    # list of rejected SMILEs
    "data_smile_rejected": default_parameters["data_smile_rejected"] + ["GISS-E2-1-G_p3f1", "GISS-E2-1-G_p5f1", "GISS-E2-2-G"],
    # require all experiments to keep SMILE: True, False
    "data_smile_require_all_experiments": False,
    #
    # -- Uncertainty
    #
    # compute uncertainty based on theory (or bootstrap): True, False
    "uncertainty_theory": default_parameters["uncertainty_theory"],
    # confidence interval of the uncertainty: float [0, 100]
    "uncertainty_confidence_interval": default_parameters["uncertainty_confidence_interval"],
    # distribution used to compute the confidence interval if uncertainty_theory is True: 'normal', 'student'
    "uncertainty_distribution": default_parameters["uncertainty_distribution"],
    # maximum number of combinations used if uncertainty_theory is True and smile_size > sample_size: int [10, 1e10]
    "uncertainty_combinations": 10000,
    # number of resamples used for the bootstrap if uncertainty_theory is False: int [10, 1e10]
    "uncertainty_resamples": 10000,
    # uncertainty computed for a given experiment
    "uncertainty_experiment": "piControl",
    # uncertainty to reach per diagnostic per method
    "uncertainty_threshold": {
        "ave_sl_val_n30e": {
            "unc": {"uncertainty_relative": False, "threshold": 1},
        },
        "ave_ts_val_n30e": {
            "unc": {"uncertainty_relative": False, "threshold": 0.1},
        },
        "ske_sl_ano_n30e": {
            "unc": {"uncertainty_relative": False, "threshold": 0.2},
        },
        "ske_ts_ano_n30e": {
            "unc": {"uncertainty_relative": False, "threshold": 0.13},
        },
        "var_sl_ano_n30e": {
            "unc": {"uncertainty_relative": True, "threshold": 20},
        },
        "var_ts_ano_n30e": {
            "unc": {"uncertainty_relative": True, "threshold": 14},
        },
        "cor_sl_n30e_to_ts_n30e": {
            "unc": {"uncertainty_relative": False, "threshold": 0.05},
        },
        "fbk_sl_n30e_to_ts_n30e": {
            "unc": {"uncertainty_relative": True, "threshold": 10},
        },
    },
    #
    # -- Required Ensemble size
    #
    # maximum ensemble size
    "res_maximum": 100,
    #
    # -- Figure
    #
    # SMILE to plot as a marker
    "fig_smile_selected": default_parameters["fig_smile_selected"],
    # figure format: eps, pdf, png, svg
    "fig_format": default_parameters["fig_format"],
    # something added to figure name by user: str
    "fig_name_add": "",
    # figure name includes input parameters (may create a very long figure name)
    "fig_name_details": False,
    # figure orientation: column (column = variables, row = statistics), row (column = statistics, row = variables)
    "fig_orientation": default_parameters["fig_orientation"],
    # size of each panel
    "fig_panel_size": {
        "frac": {"x": 0.5, "y": 0.5},
        "panel_1": {"x_delt": 2, "x_size": 16, "y_delt": 3, "y_size": 8},
    },
    # color per dataset
    "fig_colors": {
        "ave_sl_val_n30e": "k",
        "ave_ts_val_n30e": "goldenrod",
        "ske_sl_ano_n30e": "goldenrod",
        "ske_ts_ano_n30e": "r",
        "var_sl_ano_n30e": "b",
        "var_ts_ano_n30e": "b",
        "cor_sl_n30e_to_ts_n30e": "r",
        "fbk_sl_n30e_to_ts_n30e": "r",
        **default_parameters["fig_colors"],  # add colors per dataset
    },
    # marker per dataset
    "fig_markers": default_parameters["fig_markers"],
    # marker size: all marker have the same size
    "fig_marker_size": 150.,
    # ticks
    "fig_ticks": {
        "panel_1": {
            "x_lab": [""] * 3,
            "x_lim": [-0.2, 2.7],
            "x_nam": "",
            "x_tic": list(range(0, 3, 1)),
            "y_nam": "",
            # "y_lim": [0, 80],
            # "y_tic": list(range(0, 81, 40)),
            # "y_lim": [0, 1500],
            # "y_tic": list(range(0, 1501, 500)),
            "y_lim": [0, 600],
            "y_tic": list(range(0, 601, 150)),
        },
    },
    # titles
    "fig_titles": {
        "y_axis": "ensemble size",
        **default_parameters["fig_titles"],  # add diagnostics, experiments and absolute / relative uncertainty
    },
    # panel parameters (to modify default values in fig_panel.py)
    "panel_param": {"x_nbr_minor": 0},
}
# ---------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------------------------------------------------------------------------#
# Main
# ---------------------------------------------------------------------------------------------------------------------#
def z02_required_ensemble_size(
        data_diagnostics: list = default["data_diagnostics"],
        data_epoch_lengths: list = default["data_epoch_lengths"],
        data_filename: str = default["data_filename"],
        data_projects: list = default["data_projects"],
        data_experiments: list = default["data_experiments"],
        data_mme_create: bool = default["data_mme_create"],
        data_mme_use_all_smiles: bool = default["data_mme_use_all_smiles"],
        data_mme_use_smile_mean: bool = default["data_mme_use_smile_mean"],
        data_smile_minimum_size: int = default["data_smile_minimum_size"],
        data_smile_rejected: list = default["data_smile_rejected"],
        data_smile_require_all_experiments: bool = default["data_smile_require_all_experiments"],
        res_maximum: int = default["res_maximum"],
        uncertainty_combinations: int = default["uncertainty_combinations"],
        uncertainty_confidence_interval: float = default["uncertainty_confidence_interval"],
        uncertainty_distribution: str = default["uncertainty_distribution"],
        uncertainty_experiment: str = default["uncertainty_experiment"],
        uncertainty_resamples: int = default["uncertainty_resamples"],
        uncertainty_theory: bool = default["uncertainty_theory"],
        uncertainty_threshold: dict = default["uncertainty_threshold"],
        fig_colors: dict = default["fig_colors"],
        fig_format: str = default["fig_format"],
        fig_markers: dict = default["fig_markers"],
        fig_marker_size: float = default["fig_marker_size"],
        fig_name_add: str = default["fig_name_add"],
        fig_name_details: bool = default["fig_name_details"],
        fig_orientation: str = default["fig_orientation"],
        fig_panel_size: dict = default["fig_panel_size"],
        fig_smile_selected: str = default["fig_smile_selected"],
        fig_ticks: dict = default["fig_ticks"],
        fig_titles: dict = default["fig_titles"],
        panel_param: dict = default["panel_param"],
        **kwargs):
    #
    # -- Read json
    #
    values, metadata = data_organize_json(
        data_diagnostics, data_epoch_lengths, data_projects, data_experiments, data_filename=data_filename,
        data_mme_create=data_mme_create, data_mme_use_all_smiles=data_mme_use_all_smiles,
        data_mme_use_smile_mean=data_mme_use_smile_mean, data_smile_minimum_size=data_smile_minimum_size,
        data_smile_rejected=data_smile_rejected, data_smile_require_all_experiments=data_smile_require_all_experiments)
    print("values", list(values.keys()))
    #
    # -- Define thresholds for each method
    #
    values, thresholds = nest_define_uncertainty_threshold(values, uncertainty_threshold, uncertainty_experiment)
    #
    # -- Compute required ensemble size (RES) to reach an uncertainty smaller than the desired ones
    #
    res, _, _ = nest_compute_res(
        values, thresholds, res_maximum, uncertainty_confidence_interval, uncertainty_distribution,
        uncertainty_combinations, uncertainty_resamples, uncertainty_theory)
    # print("nest_compute_res", list(res.keys()))
    # k1 = "ave_sl_val_n30e"
    # print(k1, list(res[k1].keys()))
    # k2 = "030_year_epoch"
    # print(k1, k2, list(res[k1][k2].keys()))
    # k3 = "cmip6"
    # print(k1, k2, k3, list(res[k1][k2][k3].keys()))
    # k4 = "piControl"
    # print(k1, k2, k3, k4, list(res[k1][k2][k3][k4].keys()))
    # for k5 in list(res[k1][k2][k3][k4].keys()):
    #     # print(list(res[k1][k2][k3][k4][k5]["y0001"]["unc"].keys()))
    #     print(k5, res[k1][k2][k3][k4][k5]["y0001"]["unc"])
    #     # if max(res[k1][k2][k3][k4][k5]["y0001"]["unc"]) > 3:
    #     #     print(k5, res[k1][k2][k3][k4][k5]["y0001"]["unc"])
    #
    # -- Organize data for the plot
    #
    examples = nest_examples_of_res_method(res, fig_smile_selected)
    #
    # -- Organize data for plot
    #
    # x/y values for scatterplot
    figure_axes, plot_data = {}, {}
    figure_panel_size = deepcopy(fig_panel_size)
    # panel 1: boxplot
    nbr_panel = 2
    panel = "panel_1"
    for ii, dia in enumerate(data_diagnostics):  # loop on diagnostics
        if dia not in list(examples.keys()):
            continue
        pan = deepcopy(panel)
        grp = "boxplot"
        tuple_k = (grp, pan)
        # panel sizes
        # panel axes definition
        if panel in list(fig_ticks.keys()):
            for k1, k2 in fig_ticks[panel].items():
                if grp in list(figure_axes.keys()) and pan in list(figure_axes[grp].keys()) and \
                        k1 in list(figure_axes[grp][pan].keys()):
                    continue
                figure_axes = tool_put_in_dict(figure_axes, k2, *tuple_k + (k1,))
        dt = {}
        if grp in list(figure_axes.keys()) and pan in list(figure_axes[grp].keys()):
            dt = figure_axes[grp][pan]
        # dictionary
        d1 = deepcopy(examples[dia]["unc"]["boxplot"])
        d1 = [k * 30 for k in d1]
        print(dia, "{0:.1f}".format(round(float(numpy__array(d1).mean()), 1)).rjust(8),
              "{0:.1f}".format(round(min(d1), 1)).rjust(8),
              "{0:.1f}".format(round(max(d1), 1)).rjust(8))
        # -- boxplot per diagnostic (boxplot)
        plot_type = "box"
        plot_data = tool_put_in_dict(plot_data, [fig_colors[dia]], *tuple_k + (str(plot_type) + "_c",))
        plot_data = tool_put_in_dict(plot_data, [0.2], *tuple_k + (str(plot_type) + "_w",))
        plot_data = tool_put_in_dict(plot_data, [ii], *tuple_k + (str(plot_type) + "_x",))
        plot_data = tool_put_in_dict(plot_data, [d1], *tuple_k + (str(plot_type) + "_y",))
    #
    # -- Plot
    #
    # output plot directory (relative to current file directory)
    # figure name
    figure_name = __file__.split("/")[-1].split(".")[0]
    # list plot names
    list_names = list(plot_data.keys())
    # path to output figure
    # plot
    fig_basic(plot_data, list_names, 1, figure_axes, fig_format, figure_name, figure_panel_size,
              panel_param=panel_param)
# ---------------------------------------------------------------------------------------------------------------------#
