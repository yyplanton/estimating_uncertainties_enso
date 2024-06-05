# -*- coding:UTF-8 -*-
# ---------------------------------------------------------------------------------------------------------------------#
# Figure 5 of the paper about estimating_uncertainties_in_simulated_ENSO submitted to JAMES
# Plot: uncertainty of the ensemble mean in historical vs. piControl
# ---------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------#
# Import packages
# ---------------------------------------------------#
# estimating_uncertainties_enso package
from . params import default_parameters
from estimating_uncertainties_enso.compute_lib.data_lib import data_organize_json
from estimating_uncertainties_enso.compute_lib.nest_lib import nest_compute_uncertainty_hi_vs_pi
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
    "data_epoch_lengths": ["075_year_epoch"],
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
    # first epoch, last epoch or averaged across epochs used for historical experiments
    "uncertainty_historical_epoch": "averaged",
    #
    # -- Figure
    #
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
    # size of each panel
    "fig_panel_size": {"x_delt": 2, "x_frac": 1, "x_size": 4, "y_delt": 1, "y_frac": 1, "y_size": 4},
    # color per dataset
    "fig_colors": default_parameters["fig_colors"],
    # marker per dataset
    "fig_markers": default_parameters["fig_markers"],
    # marker size: all marker have the same size
    "fig_marker_size": 60.,
    # ticks: {'x-or-y_axis': {'diagnostic': []}} or {'x-or-y_axis': {'epoch_length': {'diagnostic': []}}}
    # if only one of [x_axis, y_axis] is given, the same ticks are used for both axes
    "fig_ticks": {
        "x_axis": {
            "030_year_epoch": {
                "ave_pr_val_n30e": [round(ii / 100, 2) for ii in list(range(1, 18, 4))],
                "ave_pr_val_n34e": [round(ii / 100, 2) for ii in list(range(1, 18, 4))],
                "ave_pr_val_n40e": [round(ii / 100, 2) for ii in list(range(1, 18, 4))],
                "ave_ts_val_n30e": [round(ii / 100, 2) for ii in list(range(1, 10, 2))],
                "ave_ts_val_n34e": [round(ii / 100, 2) for ii in list(range(1, 10, 2))],
                "ave_ts_val_n40e": [round(ii / 100, 2) for ii in list(range(1, 10, 2))],
                "ave_tx_val_n30e": [round(ii / 10, 1) for ii in list(range(0, 9, 2))],
                "ave_tx_val_n34e": [round(ii / 10, 1) for ii in list(range(2, 11, 2))],
                "ave_tx_val_n40e": [round(ii / 10, 1) for ii in list(range(2, 11, 2))],
                "ave_ty_val_n30e": [round(ii / 10, 1) for ii in list(range(0, 9, 2))],
                "ave_ty_val_n34e": [round(ii / 10, 1) for ii in list(range(0, 9, 2))],
                "ave_ty_val_n40e": [round(ii / 100, 2) for ii in list(range(0, 61, 15))],
                "ske_pr_ano_n30e": [round(ii / 100, 2) for ii in list(range(0, 81, 20))],
                "ske_pr_ano_n34e": [round(ii / 100, 2) for ii in list(range(0, 101, 25))],
                "ske_pr_ano_n40e": [round(ii / 100, 2) for ii in list(range(0, 33, 8))],
                "ske_ts_ano_n30e": [round(ii / 100, 2) for ii in list(range(0, 37, 9))],
                "ske_ts_ano_n34e": [round(ii / 100, 2) for ii in list(range(0, 33, 8))],
                "ske_ts_ano_n40e": [round(ii / 100, 2) for ii in list(range(0, 25, 6))],
                "ske_tx_ano_n30e": [round(ii / 100, 2) for ii in list(range(3, 24, 5))],
                "ske_tx_ano_n34e": [round(ii / 100, 2) for ii in list(range(4, 21, 4))],
                "ske_tx_ano_n40e": [round(ii / 100, 2) for ii in list(range(5, 26, 5))],
                "ske_ty_ano_n30e": [round(ii / 100, 2) for ii in list(range(0, 25, 6))],
                "ske_ty_ano_n34e": [round(ii / 100, 2) for ii in list(range(0, 41, 10))],
                "ske_ty_ano_n40e": [round(ii / 100, 2) for ii in list(range(0, 41, 10))],
                "var_pr_ano_n30e": [round(ii / 100, 2) for ii in list(range(0, 101, 25))],
                "var_pr_ano_n34e": [round(ii / 100, 2) for ii in list(range(0, 101, 25))],
                "var_pr_ano_n40e": [round(ii / 100, 2) for ii in list(range(0, 101, 25))],
                "var_ts_ano_n30e": [round(ii / 100, 2) for ii in list(range(0, 25, 6))],
                "var_ts_ano_n34e": [round(ii / 100, 2) for ii in list(range(0, 29, 7))],
                "var_ts_ano_n40e": [round(ii / 100, 2) for ii in list(range(0, 25, 6))],
                "var_tx_ano_n30e": list(range(0, 13, 3)),
                "var_tx_ano_n34e": list(range(0, 29, 7)),
                "var_tx_ano_n40e": list(range(0, 37, 9)),
                "var_ty_ano_n30e": list(range(0, 5, 1)),
                "var_ty_ano_n34e": list(range(0, 13, 3)),
                "var_ty_ano_n40e": list(range(0, 9, 2)),
            },
            "045_year_epoch": {
                "ave_pr_val_n30e": [round(ii / 100, 2) for ii in list(range(0, 13, 3))],
                "ave_pr_val_n34e": [round(ii / 100, 2) for ii in list(range(0, 13, 3))],
                "ave_pr_val_n40e": [round(ii / 100, 2) for ii in list(range(0, 13, 3))],
                "ave_ts_val_n30e": [round(ii / 100, 2) for ii in list(range(1, 10, 2))],
                "ave_ts_val_n34e": [round(ii / 100, 2) for ii in list(range(1, 10, 2))],
                "ave_ts_val_n40e": [round(ii / 100, 2) for ii in list(range(1, 10, 2))],
                "ave_tx_val_n30e": [round(ii / 10, 1) for ii in list(range(0, 9, 2))],
                "ave_tx_val_n34e": [round(ii / 10, 1) for ii in list(range(1, 10, 2))],
                "ave_tx_val_n40e": [round(ii / 10, 1) for ii in list(range(1, 10, 2))],
                "ave_ty_val_n30e": [round(ii / 10, 1) for ii in list(range(0, 9, 2))],
                "ave_ty_val_n34e": [round(ii / 10, 1) for ii in list(range(0, 9, 2))],
                "ave_ty_val_n40e": [round(ii / 100, 2) for ii in list(range(0, 61, 15))],
                "ske_pr_ano_n30e": [round(ii / 100, 2) for ii in list(range(0, 81, 20))],
                "ske_pr_ano_n34e": [round(ii / 100, 2) for ii in list(range(0, 81, 20))],
                "ske_pr_ano_n40e": [round(ii / 100, 2) for ii in list(range(4, 29, 6))],
                "ske_ts_ano_n30e": [round(ii / 100, 2) for ii in list(range(5, 26, 5))],
                "ske_ts_ano_n34e": [round(ii / 100, 2) for ii in list(range(5, 26, 5))],
                "ske_ts_ano_n40e": [round(ii / 100, 2) for ii in list(range(5, 18, 3))],
                "ske_tx_ano_n30e": [round(ii / 100, 2) for ii in list(range(3, 20, 4))],
                "ske_tx_ano_n34e": [round(ii / 100, 2) for ii in list(range(2, 19, 4))],
                "ske_tx_ano_n40e": [round(ii / 100, 2) for ii in list(range(2, 19, 4))],
                "ske_ty_ano_n30e": [round(ii / 100, 2) for ii in list(range(0, 21, 5))],
                "ske_ty_ano_n34e": [round(ii / 100, 2) for ii in list(range(0, 41, 10))],
                "ske_ty_ano_n40e": [round(ii / 100, 2) for ii in list(range(0, 41, 10))],
                "var_pr_ano_n30e": [round(ii / 100, 2) for ii in list(range(0, 101, 25))],
                "var_pr_ano_n34e": [round(ii / 100, 2) for ii in list(range(0, 101, 25))],
                "var_pr_ano_n40e": [round(ii / 100, 2) for ii in list(range(0, 101, 25))],
                "var_ts_ano_n30e": [round(ii / 100, 2) for ii in list(range(1, 22, 5))],
                "var_ts_ano_n34e": [round(ii / 100, 2) for ii in list(range(1, 22, 5))],
                "var_ts_ano_n40e": [round(ii / 100, 2) for ii in list(range(0, 17, 4))],
                "var_tx_ano_n30e": list(range(0, 9, 2)),
                "var_tx_ano_n34e": list(range(0, 25, 6)),
                "var_tx_ano_n40e": list(range(0, 37, 9)),
                "var_ty_ano_n30e": list(range(0, 5, 1)),
                "var_ty_ano_n34e": list(range(0, 9, 2)),
                "var_ty_ano_n40e": list(range(0, 9, 2)),
            },
            "060_year_epoch": {
                "ave_pr_val_n30e": [round(ii / 100, 2) for ii in list(range(0, 13, 3))],
                "ave_pr_val_n34e": [round(ii / 100, 2) for ii in list(range(0, 13, 3))],
                "ave_pr_val_n40e": [round(ii / 100, 2) for ii in list(range(0, 13, 3))],
                "ave_ts_val_n30e": [round(ii / 100, 2) for ii in list(range(0, 9, 2))],
                "ave_ts_val_n34e": [round(ii / 100, 2) for ii in list(range(0, 9, 2))],
                "ave_ts_val_n40e": [round(ii / 100, 2) for ii in list(range(0, 9, 2))],
                "ave_tx_val_n30e": [round(ii / 10, 1) for ii in list(range(0, 5, 1))],
                "ave_tx_val_n34e": [round(ii / 10, 1) for ii in list(range(0, 9, 2))],
                "ave_tx_val_n40e": [round(ii / 10, 1) for ii in list(range(0, 9, 2))],
                "ave_ty_val_n30e": [round(ii / 100, 2) for ii in list(range(0, 61, 15))],
                "ave_ty_val_n34e": [round(ii / 100, 2) for ii in list(range(0, 61, 15))],
                "ave_ty_val_n40e": [round(ii / 100, 2) for ii in list(range(2, 31, 7))],
                "ske_pr_ano_n30e": [round(ii / 100, 2) for ii in list(range(0, 81, 20))],
                "ske_pr_ano_n34e": [round(ii / 100, 2) for ii in list(range(0, 81, 20))],
                "ske_pr_ano_n40e": [round(ii / 100, 2) for ii in list(range(0, 29, 7))],
                "ske_ts_ano_n30e": [round(ii / 100, 2) for ii in list(range(2, 23, 5))],
                "ske_ts_ano_n34e": [round(ii / 100, 2) for ii in list(range(4, 17, 3))],
                "ske_ts_ano_n40e": [round(ii / 100, 2) for ii in list(range(4, 17, 3))],
                "ske_tx_ano_n30e": [round(ii / 100, 2) for ii in list(range(2, 19, 4))],
                "ske_tx_ano_n34e": [round(ii / 100, 2) for ii in list(range(2, 19, 4))],
                "ske_tx_ano_n40e": [round(ii / 100, 2) for ii in list(range(2, 19, 4))],
                "ske_ty_ano_n30e": [round(ii / 100, 2) for ii in list(range(0, 21, 5))],
                "ske_ty_ano_n34e": [round(ii / 100, 2) for ii in list(range(0, 29, 7))],
                "ske_ty_ano_n40e": [round(ii / 100, 2) for ii in list(range(0, 29, 7))],
                "var_pr_ano_n30e": [round(ii / 100, 2) for ii in list(range(0, 81, 20))],
                "var_pr_ano_n34e": [round(ii / 100, 2) for ii in list(range(0, 101, 25))],
                "var_pr_ano_n40e": [round(ii / 100, 2) for ii in list(range(0, 101, 25))],
                "var_ts_ano_n30e": [round(ii / 100, 2) for ii in list(range(0, 21, 5))],
                "var_ts_ano_n34e": [round(ii / 100, 2) for ii in list(range(0, 21, 5))],
                "var_ts_ano_n40e": [round(ii / 100, 2) for ii in list(range(0, 13, 3))],
                "var_tx_ano_n30e": list(range(0, 9, 2)),
                "var_tx_ano_n34e": list(range(0, 21, 5)),
                "var_tx_ano_n40e": list(range(0, 41, 10)),
                "var_ty_ano_n30e": [round(ii / 10, 1) for ii in list(range(0, 29, 7))],
                "var_ty_ano_n34e": [round(ii / 10, 1) for ii in list(range(0, 61, 15))],
                "var_ty_ano_n40e": [round(ii / 10, 1) for ii in list(range(0, 61, 15))],
            },
            "075_year_epoch": {
                "ave_pr_val_n30e": [round(ii / 100, 2) for ii in list(range(0, 9, 2))],
                "ave_pr_val_n34e": [round(ii / 100, 2) for ii in list(range(0, 9, 2))],
                "ave_pr_val_n40e": [round(ii / 100, 2) for ii in list(range(1, 10, 2))],
                "ave_ts_val_n30e": [round(ii / 100, 2) for ii in list(range(0, 9, 2))],
                "ave_ts_val_n34e": [round(ii / 100, 2) for ii in list(range(0, 9, 2))],
                "ave_ts_val_n40e": [round(ii / 100, 2) for ii in list(range(0, 9, 2))],
                "ave_tx_val_n30e": [round(ii / 10, 1) for ii in list(range(0, 5, 1))],
                "ave_tx_val_n34e": [round(ii / 10, 1) for ii in list(range(0, 9, 2))],
                "ave_tx_val_n40e": [round(ii / 10, 1) for ii in list(range(0, 9, 2))],
                "ave_ty_val_n30e": [round(ii / 100, 2) for ii in list(range(0, 61, 15))],
                "ave_ty_val_n34e": [round(ii / 100, 2) for ii in list(range(0, 61, 15))],
                "ave_ty_val_n40e": [round(ii / 100, 2) for ii in list(range(0, 29, 7))],
                "ske_pr_ano_n30e": [round(ii / 100, 2) for ii in list(range(0, 81, 20))],
                "ske_pr_ano_n34e": [round(ii / 100, 2) for ii in list(range(0, 81, 20))],
                "ske_pr_ano_n40e": [round(ii / 100, 2) for ii in list(range(3, 24, 5))],
                "ske_ts_ano_n30e": [round(ii / 100, 2) for ii in list(range(4, 17, 3))],
                "ske_ts_ano_n34e": [round(ii / 100, 2) for ii in list(range(4, 17, 3))],
                "ske_ts_ano_n40e": [round(ii / 100, 2) for ii in list(range(5, 14, 2))],
                "ske_tx_ano_n30e": [round(ii / 100, 2) for ii in list(range(3, 20, 4))],
                "ske_tx_ano_n34e": [round(ii / 100, 2) for ii in list(range(3, 20, 4))],
                "ske_tx_ano_n40e": [round(ii / 100, 2) for ii in list(range(3, 20, 4))],
                "ske_ty_ano_n30e": [round(ii / 100, 2) for ii in list(range(4, 17, 3))],
                "ske_ty_ano_n34e": [round(ii / 100, 2) for ii in list(range(0, 29, 7))],
                "ske_ty_ano_n40e": [round(ii / 100, 2) for ii in list(range(0, 29, 7))],
                "var_pr_ano_n30e": [round(ii / 100, 2) for ii in list(range(0, 61, 15))],
                "var_pr_ano_n34e": [round(ii / 100, 2) for ii in list(range(0, 81, 20))],
                "var_pr_ano_n40e": [round(ii / 100, 2) for ii in list(range(0, 81, 20))],
                "var_ts_ano_n30e": [round(ii / 100, 2) for ii in list(range(0, 17, 4))],
                "var_ts_ano_n34e": [round(ii / 100, 2) for ii in list(range(0, 17, 4))],
                "var_ts_ano_n40e": [round(ii / 100, 2) for ii in list(range(0, 13, 3))],
                "var_tx_ano_n30e": list(range(0, 9, 2)),
                "var_tx_ano_n34e": list(range(0, 17, 4)),
                "var_tx_ano_n40e": list(range(0, 33, 8)),
                "var_ty_ano_n30e": [round(ii / 10, 1) for ii in list(range(0, 25, 6))],
                "var_ty_ano_n34e": [round(ii / 10, 1) for ii in list(range(0, 41, 10))],
                "var_ty_ano_n40e": [round(ii / 10, 1) for ii in list(range(0, 61, 15))],
            },
            "090_year_epoch": {
                "ave_pr_val_n30e": [round(ii / 100, 2) for ii in list(range(1, 6, 1))],
                "ave_pr_val_n34e": [round(ii / 100, 2) for ii in list(range(0, 9, 2))],
                "ave_pr_val_n40e": [round(ii / 100, 2) for ii in list(range(1, 10, 2))],
                "ave_ts_val_n30e": [round(ii / 100, 2) for ii in list(range(0, 9, 2))],
                "ave_ts_val_n34e": [round(ii / 100, 2) for ii in list(range(0, 9, 2))],
                "ave_ts_val_n40e": [round(ii / 100, 2) for ii in list(range(0, 9, 2))],
                "ave_tx_val_n30e": [round(ii / 10, 1) for ii in list(range(0, 5, 1))],
                "ave_tx_val_n34e": [round(ii / 10, 1) for ii in list(range(1, 6, 1))],
                "ave_tx_val_n40e": [round(ii / 10, 1) for ii in list(range(0, 9, 2))],
                "ave_ty_val_n30e": [round(ii / 100, 2) for ii in list(range(10, 51, 10))],
                "ave_ty_val_n34e": [round(ii / 100, 2) for ii in list(range(10, 51, 10))],
                "ave_ty_val_n40e": [round(ii / 100, 2) for ii in list(range(5, 26, 5))],
                "ske_pr_ano_n30e": [round(ii / 100, 2) for ii in list(range(0, 81, 20))],
                "ske_pr_ano_n34e": [round(ii / 100, 2) for ii in list(range(0, 101, 25))],
                "ske_pr_ano_n40e": [round(ii / 100, 2) for ii in list(range(0, 21, 5))],
                "ske_ts_ano_n30e": [round(ii / 100, 2) for ii in list(range(4, 21, 4))],
                "ske_ts_ano_n34e": [round(ii / 100, 2) for ii in list(range(4, 17, 3))],
                "ske_ts_ano_n40e": [round(ii / 100, 2) for ii in list(range(5, 13, 2))],
                "ske_tx_ano_n30e": [round(ii / 100, 2) for ii in list(range(2, 11, 2))],
                "ske_tx_ano_n34e": [round(ii / 100, 2) for ii in list(range(2, 15, 3))],
                "ske_tx_ano_n40e": [round(ii / 100, 2) for ii in list(range(1, 22, 5))],
                "ske_ty_ano_n30e": [round(ii / 100, 2) for ii in list(range(2, 19, 4))],
                "ske_ty_ano_n34e": [round(ii / 100, 2) for ii in list(range(0, 29, 7))],
                "ske_ty_ano_n40e": [round(ii / 100, 2) for ii in list(range(0, 29, 7))],
                "var_pr_ano_n30e": [round(ii / 100, 2) for ii in list(range(0, 61, 15))],
                "var_pr_ano_n34e": [round(ii / 100, 2) for ii in list(range(0, 81, 20))],
                "var_pr_ano_n40e": [round(ii / 100, 2) for ii in list(range(0, 81, 20))],
                "var_ts_ano_n30e": [round(ii / 100, 2) for ii in list(range(0, 17, 4))],
                "var_ts_ano_n34e": [round(ii / 100, 2) for ii in list(range(0, 17, 4))],
                "var_ts_ano_n40e": [round(ii / 100, 2) for ii in list(range(0, 13, 3))],
                "var_tx_ano_n30e": [round(ii / 10, 1) for ii in list(range(2, 19, 4))],
                "var_tx_ano_n34e": list(range(0, 9, 2)),
                "var_tx_ano_n40e": list(range(0, 13, 3)),
                "var_ty_ano_n30e": [round(ii / 10, 1) for ii in list(range(0, 25, 6))],
                "var_ty_ano_n34e": [round(ii / 10, 1) for ii in list(range(0, 41, 10))],
                "var_ty_ano_n40e": [round(ii / 10, 1) for ii in list(range(0, 61, 15))],
            },
        },
    },
    # titles
    "fig_titles": default_parameters["fig_titles"],
    # panel parameters (to modify default values in fig_panel.py)
    "panel_param": {"title_row_x": 45},
}
# ---------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------------------------------------------------------------------------#
# Main
# ---------------------------------------------------------------------------------------------------------------------#
def f05_hi_vs_pi(
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
        uncertainty_historical_epoch: str = default["uncertainty_historical_epoch"],
        uncertainty_relative: bool = default["uncertainty_relative"],
        uncertainty_resamples: int = default["uncertainty_resamples"],
        uncertainty_theory: bool = default["uncertainty_theory"],
        fig_colors: dict = default["fig_colors"],
        fig_format: str = default["fig_format"],
        fig_legend_position: str = default["fig_legend_position"],
        fig_markers: dict = default["fig_markers"],
        fig_marker_size: float = default["fig_marker_size"],
        fig_name_add: str = default["fig_name_add"],
        fig_name_details: bool = default["fig_name_details"],
        fig_orientation: str = default["fig_orientation"],
        fig_panel_size: dict = default["fig_panel_size"],
        fig_ticks: dict = default["fig_ticks"],
        fig_titles: dict = default["fig_titles"],
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
    # -- Compute uncertainty with the same sample size for piControl and historical
    #
    uncertainties = nest_compute_uncertainty_hi_vs_pi(
        values, uncertainty_confidence_interval, uncertainty_distribution, uncertainty_relative,
        uncertainty_combinations, uncertainty_resamples, uncertainty_theory, uncertainty_historical_epoch,
        reference_experiment="piControl")
    #
    # -- Organize data to for figure
    #
    figure_ticks = {}
    method = "relative" if uncertainty_relative is True else "absolute"
    for dur in list(uncertainties.keys()):
        for dia in list(uncertainties[dur].keys()):
            units = ""
            if method == "absolute" and metadata[dia]["units"] != "":
                units = " (" + str(metadata[dia]["units"]) + ")"
            elif method == "relative":
                units = " (%)"
            # x-axis
            name = str(fig_titles[method]) + " in piControl" + str(units)
            if "x_axis" in list(fig_titles.keys()) and isinstance(fig_titles["x_axis"], dict) is True and \
                    dia in list(fig_titles["x_axis"].keys()) and isinstance(fig_titles["x_axis"][dia], str) is True:
                pass
            else:
                fig_titles = tool_put_in_dict(fig_titles, name, "x_axis", dia)
            # y-axis
            name = str(fig_titles[method]) + " in historical "
            if uncertainty_historical_epoch == "averaged":
                name += str(uncertainty_historical_epoch) + "\nacross epochs"
            else:
                name += str(uncertainty_historical_epoch) + "\nepoch"
            name += str(units)
            if "y_axis" in list(fig_titles.keys()) and isinstance(fig_titles["y_axis"], dict) is True and \
                    dia in list(fig_titles["y_axis"].keys()) and isinstance(fig_titles["y_axis"][dia], str) is True:
                pass
            else:
                fig_titles = tool_put_in_dict(fig_titles, name, "y_axis", dia)
            # x-y tics
            for k1 in ["x_axis", "y_axis"]:
                k2 = "y_axis" if k1 == "x_axis" else "x_axis"
                list_ticks = None
                if k1 in list(fig_ticks.keys()) and isinstance(fig_ticks[k1], dict) is True and \
                        dia in list(fig_ticks[k1].keys()) and isinstance(fig_ticks[k1][dia], list) is True:
                    list_ticks = fig_ticks[k1][dia]
                elif k1 in list(fig_ticks.keys()) and isinstance(fig_ticks[k1], dict) is True and \
                        dur in list(fig_ticks[k1].keys()) and isinstance(fig_ticks[k1][dur], dict) is True and \
                        dia in list(fig_ticks[k1][dur].keys()) and isinstance(fig_ticks[k1][dur][dia], list) is True:
                    list_ticks = fig_ticks[k1][dur][dia]
                elif k2 in list(fig_ticks.keys()) and isinstance(fig_ticks[k2], dict) is True and \
                        dia in list(fig_ticks[k2].keys()) and isinstance(fig_ticks[k2][dia], list) is True:
                    list_ticks = fig_ticks[k2][dia]
                elif k2 in list(fig_ticks.keys()) and isinstance(fig_ticks[k2], dict) is True and \
                        dur in list(fig_ticks[k2].keys()) and isinstance(fig_ticks[k2][dur], dict) is True and \
                        dia in list(fig_ticks[k2][dur].keys()) and isinstance(fig_ticks[k2][dur][dia], list) is True:
                    list_ticks = fig_ticks[k2][dur][dia]
                figure_ticks = tool_put_in_dict(figure_ticks, list_ticks, dur, k1, dia)
    #
    # -- Figure
    #
    for dur in list(uncertainties.keys()):
        # output figure name will be the file name (path removed and extension removed)
        fig_name = __file__.split("/")[-1].split(".")[0] + str(fig_name_add) + "_" + str(dur)
        if fig_name_details is True:
            # add details of the computation to the figure name
            fig_name += "_data_" + str(len(data_projects)) + "pro_" + str(len(data_experiments)) + "exp_" + \
                        str(data_smile_minimum_size) + "mem_" + str(len(data_diagnostics)) + "dia"
            if len(data_epoch_lengths) == 1:
                fig_name += "_" + str(data_epoch_lengths[0])
            else:
                fig_name += "_" + str(len(data_epoch_lengths)) + "dur"
            if data_mme_create is True:
                fig_name += "_mme"
                fig_name += "_of_em" if data_mme_use_smile_mean is True else "_of_1m"
                fig_name += "_all_smile" if data_mme_use_all_smiles is True else "_1st_smile"
            fig_name += "_relative_uncertainty" if uncertainty_relative is True else "_absolute_uncertainty"
            fig_name += "_theory" if uncertainty_theory is True else "_random"
            fig_name += "_" + str(uncertainty_confidence_interval) + "ci"
            if uncertainty_theory is True:
                fig_name += "_" + str(uncertainty_distribution) + "_distribution"
            fig_name += "_" + str(uncertainty_historical_epoch) + "_epoch"
            fig_name += "_" + str(fig_orientation)
        fig_scatter_and_regression(uncertainties[dur], data_diagnostics, fig_format, fig_name, fig_colors, fig_markers,
                                   fig_marker_size, fig_orientation, fig_panel_size, figure_ticks[dur], fig_titles,
                                   fig_legend_position=fig_legend_position, panel_param=panel_param)
# ---------------------------------------------------------------------------------------------------------------------#
