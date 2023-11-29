# -*- coding:UTF-8 -*-
# ---------------------------------------------------------------------------------------------------------------------#
# Figure S3 of the paper about estimating_uncertainties_in_simulated_ENSO submitted to JAMES
# Plot: uncertainty of the ensemble mean computed using the theory (standard error) vs bootstrap
# ---------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------#
# Import packages
# ---------------------------------------------------#
# estimating_uncertainties_enso package
from . params import default_parameters
from estimating_uncertainties_enso.compute_lib.data_lib import data_organize_json
from estimating_uncertainties_enso.compute_lib.nest_lib import nest_compute_uncertainty
from estimating_uncertainties_enso.compute_lib.tool_lib import tool_put_in_dict
from estimating_uncertainties_enso.figure_templates.fig_template import fig_scatter_and_regression
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
    "data_experiments": default_parameters["data_experiments"],
    # create the MME: True, False
    "data_mme_create": True,
    # MME made with all available SMILEs (or 1st SMILE of each model): True, False
    "data_mme_use_all_smiles": default_parameters["data_mme_use_all_smiles"],
    # MME made with ensemble means (or 1st member of each SMILE): True, False
    "data_mme_use_smile_mean": default_parameters["data_mme_use_smile_mean"],
    # minimum number of member for SMILEs: int [1, 100]
    "data_smile_minimum_size": default_parameters["data_smile_minimum_size"],
    # list of rejected SMILEs
    "data_smile_rejected": default_parameters["data_smile_rejected"],
    # require all experiments to keep SMILE: True, False
    "data_smile_require_all_experiments": False,
    #
    # -- Uncertainty
    #
    # compute relative uncertainty (or absolute): True, False
    "uncertainty_relative": default_parameters["uncertainty_relative"],
    # confidence interval of the uncertainty: float [0, 100]
    "uncertainty_confidence_interval": default_parameters["uncertainty_confidence_interval"],
    # distribution used to compute the confidence interval if uncertainty_theory is True: 'normal', 'student'
    "uncertainty_distribution": default_parameters["uncertainty_distribution"],
    # maximum number of combinations used if uncertainty_theory is True and smile_size > sample_size: int [10, 1e10]
    "uncertainty_combinations": int(1e3),  # default_parameters["uncertainty_combinations"],
    # number of resamples used for the bootstrap if uncertainty_theory is False: int [10, 1e10]
    "uncertainty_resamples": int(1e4),  # default_parameters["uncertainty_resamples"],
    #
    # -- Figure
    #
    # figure format: eps, pdf, png, svg
    "fig_format": default_parameters["fig_format"],
    # figure name includes input parameters (may create a very long figure name)
    "fig_detailed_name": False,
    # figure orientation: column (column = variables, row = statistics), row (column = statistics, row = variables)
    "fig_orientation": default_parameters["fig_orientation"],
    # size of each panel
    "fig_panel_size": {"x_delt": 6, "x_frac": 0.25, "x_size": 16, "y_delt": 5, "y_frac": 0.25, "y_size": 16},
    # marker shape, color and size: all markers are the same
    "fig_marker": "o",
    "fig_marker_color": "grey",
    "fig_marker_size": 50.,
    # ticks
    "fig_ticks": {
        "absolute": {
            "ave_pr_val_n30e": [round(k / 100, 2) for k in list(range(0, 21, 5))],
            "ave_ts_val_n30e": [round(k / 100, 2) for k in list(range(0, 21, 5))],
            "ske_pr_ano_n30e": [round(k / 100, 2) for k in list(range(0, 141, 35))],
            "ske_ts_ano_n30e": [round(k / 100, 2) for k in list(range(0, 41, 10))],
            "var_pr_ano_n30e": [round(k / 100, 2) for k in list(range(0, 141, 35))],
            "var_ts_ano_n30e": [round(k / 100, 2) for k in list(range(0, 37, 9))],
        },
    },
    # titles
    "fig_titles": default_parameters["fig_titles"],
    # panel parameters (to modify default values of fig_panel.py)
    "panel_param": {},
}
# ---------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------------------------------------------------------------------------#
# Main
# ---------------------------------------------------------------------------------------------------------------------#
def s03_theory_vs_bootstrap(data_diagnostics: list = default["data_diagnostics"],
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
                            fig_detailed_name: bool = default["fig_detailed_name"],
                            fig_format: str = default["fig_format"],
                            fig_marker: str = default["fig_marker"],
                            fig_marker_color: str = default["fig_marker_color"],
                            fig_marker_size: float = default["fig_marker_size"],
                            fig_orientation: str = default["fig_orientation"],
                            fig_panel_size: dict = default["fig_panel_size"],
                            fig_ticks: dict = default["fig_ticks"],
                            fig_titles: dict = default["fig_titles"],
                            panel_param: dict = default["panel_param"], **kwargs):
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
    bootstrap, _, _ = nest_compute_uncertainty(
        values, uncertainty_confidence_interval, uncertainty_distribution, uncertainty_relative,
        uncertainty_combinations, uncertainty_resamples, False)
    theory, _, _ = nest_compute_uncertainty(
        values, uncertainty_confidence_interval, uncertainty_distribution, uncertainty_relative,
        uncertainty_combinations, uncertainty_resamples, True)
    #
    # -- Organize data for the figure
    #
    data_to_plot = {}
    for dia in sorted(list(theory.keys()), key=str.casefold):
        for dur in sorted(list(theory[dia].keys()), key=str.casefold):
            for pro in sorted(list(theory[dia][dur].keys()), key=str.casefold):
                for exp in sorted(list(theory[dia][dur][pro].keys()), key=str.casefold):
                    for dat in sorted(list(theory[dia][dur][pro][exp].keys()), key=str.casefold):
                        for epo in sorted(list(theory[dia][dur][pro][exp][dat].keys()), key=str.casefold):
                            for siz in sorted(list(theory[dia][dur][pro][exp][dat][epo].keys()), key=str.casefold):
                                # uncertainty of the sample mean computed using the bootstrap as x values
                                data_to_plot = tool_put_in_dict(
                                    data_to_plot, [bootstrap[dia][dur][pro][exp][dat][epo][siz]], dia, dat, "x")
                                # uncertainty of the sample mean computed using the theory as y values
                                data_to_plot = tool_put_in_dict(
                                    data_to_plot, [theory[dia][dur][pro][exp][dat][epo][siz]], dia, dat, "y")
    fig_colors = dict((dat, fig_marker_color) for dat in list(data_to_plot[data_diagnostics[0]].keys()))
    fig_markers = dict((dat, fig_marker) for dat in list(data_to_plot[data_diagnostics[0]].keys()))
    method = "relative" if uncertainty_relative is True else "absolute"
    for dia in list(data_to_plot.keys()):
        units = ""
        if method == "absolute" and metadata[dia]["units"] != "":
            units = " (" + str(metadata[dia]["units"]) + ")"
        elif method == "relative":
            units = " (%)"
        # x-axis
        name = str(fig_titles[method]) + " from random sampling" + str(units)
        fig_titles = tool_put_in_dict(fig_titles, name, "x_axis", dia)
        # y-axis
        name = str(fig_titles[method]) + " from theory" + str(units)
        fig_titles = tool_put_in_dict(fig_titles, name, "y_axis", dia)
        # x-y tics
        if dia in list(fig_ticks.keys()) and isinstance(fig_ticks[dia], list) is True:
            pass
        else:
            list_ticks = None
            if method in list(fig_ticks.keys()) and isinstance(fig_ticks[method], dict) is True and \
                    dia in list(fig_ticks[method].keys()) and isinstance(fig_ticks[method][dia], list) is True:
                list_ticks = fig_ticks[method][dia]
            fig_ticks = tool_put_in_dict(fig_ticks, list_ticks, dia)
    #
    # -- Figure
    #
    # output figure name will be the file name (path removed and extension removed)
    fig_name = __file__.split("/")[-1].split(".")[0]
    if fig_detailed_name is True:
        # add details of the computation to the figure name
        fig_name += "_data_" + str(len(data_projects)) + "pro_" + str(len(data_experiments)) + "exp_" + \
                    str(data_smile_minimum_size) + "mem_" + str(len(data_diagnostics)) + "dia"
        if data_mme_create is True:
            fig_name += "_mme"
            fig_name += "_of_em" if data_mme_use_smile_mean is True else "_of_1m"
            fig_name += "_all_smile" if data_mme_use_all_smiles is True else "_1st_smile"
        fig_name += "_relative_uncertainty" if uncertainty_relative is True else "_absolute_uncertainty"
        fig_name += "_" + str(uncertainty_confidence_interval) + "ci"
        fig_name += "_" + str(uncertainty_distribution) + "_distribution"
        fig_name += "_" + str(fig_orientation)
    fig_scatter_and_regression(data_to_plot, data_diagnostics, fig_format, fig_name, fig_colors, fig_markers,
                               fig_marker_size, fig_orientation, fig_panel_size, fig_ticks, fig_titles,
                               fig_legend_bool=False, panel_param=panel_param)
# ---------------------------------------------------------------------------------------------------------------------#
