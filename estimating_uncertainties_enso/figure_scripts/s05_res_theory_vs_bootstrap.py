# -*- coding:UTF-8 -*-
# ---------------------------------------------------------------------------------------------------------------------#
# Figure S5 of the paper about estimating_uncertainties_in_simulated_ENSO submitted to JAMES
# Plot: required ensemble sizes computed using the theory (standard error) vs bootstrap
# ---------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------#
# Import packages
# ---------------------------------------------------#
# estimating_uncertainties_enso package
from . params import default_parameters
from estimating_uncertainties_enso.compute_lib.data_lib import data_organize_json
from estimating_uncertainties_enso.compute_lib.nest_lib import nest_compute_res, nest_define_uncertainty_threshold
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
    "data_smile_minimum_size": default_parameters["data_smile_minimum_size"],
    # list of rejected SMILEs
    "data_smile_rejected": default_parameters["data_smile_rejected"],
    # require all experiments to keep SMILE: True, False
    "data_smile_require_all_experiments": False,
    #
    # -- Uncertainty
    #
    # confidence interval of the uncertainty: float [0, 100]
    "uncertainty_confidence_interval": default_parameters["uncertainty_confidence_interval"],
    # maximum number of combinations used if uncertainty_theory is True and smile_size > sample_size: int [0, 1e10]
    "uncertainty_combinations": default_parameters["uncertainty_combinations"],
    # number of resamples used for the bootstrap if uncertainty_theory is False: int [0, 1e10]
    "uncertainty_resamples": default_parameters["uncertainty_resamples"],
    # uncertainty to reach per diagnostic per method
    "uncertainty_threshold": {
        "ave_pr_val_n30e": {"unc": {"uncertainty_relative": True, "threshold": list(range(5, 101, 5))}},
        "ave_ts_val_n30e": {"unc": {"uncertainty_relative": True, "threshold": [k / 10 for k in list(range(1, 11))]}},
        "ske_pr_ano_n30e": {"unc": {"uncertainty_relative": True, "threshold": list(range(5, 101, 5))}},
        "ske_ts_ano_n30e": {"unc": {"uncertainty_relative": True, "threshold": list(range(5, 101, 5))}},
        "var_pr_ano_n30e": {"unc": {"uncertainty_relative": True, "threshold": list(range(5, 101, 5))}},
        "var_ts_ano_n30e": {"unc": {"uncertainty_relative": True, "threshold": list(range(5, 101, 5))}},
    },
    #
    # -- Required Ensemble size
    #
    # maximum ensemble size
    "res_maximum": 60,
    #
    # -- Figure
    #
    # SMILE to plot as a marker
    "fig_smile_selected": default_parameters["fig_smile_selected"],
    # figure format: eps, pdf, png, svg
    "fig_format": default_parameters["fig_format"],
    # figure name includes input parameters (may create a very long figure name)
    "fig_detailed_name": False,
    # size of each panel
    "fig_panel_size": {"x_delt": 0, "x_frac": 1, "x_size": 4, "y_delt": 0, "y_frac": 1, "y_size": 4},
    # marker shape, color and size: all markers are the same
    "fig_marker": "o",
    "fig_marker_color": "grey",
    "fig_marker_size": 50.,
    # ranges
    "fig_ranges": {
        "res": list(range(0, 61, 15)),
    },
    # titles
    "fig_titles": {
        "x_axis": {"res": "RES from random sampling"},
        "y_axis": {"res": "RES from theory"},
    },
    # panel parameters (to modify default values in fig_panel.py)
    "panel_param": {},
}
# ---------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------------------------------------------------------------------------#
# Main
# ---------------------------------------------------------------------------------------------------------------------#
def s05_theory_vs_bootstrap(data_diagnostics: list = default["data_diagnostics"],
                            data_epoch_lengths: list = default["data_epoch_lengths"],
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
                            uncertainty_resamples: int = default["uncertainty_resamples"],
                            uncertainty_threshold: dict = default["uncertainty_threshold"],
                            fig_detailed_name: bool = default["fig_detailed_name"],
                            fig_format: str = default["fig_format"],
                            fig_marker: str = default["fig_marker"],
                            fig_marker_color: str = default["fig_marker_color"],
                            fig_marker_size: float = default["fig_marker_size"],
                            fig_panel_size: dict = default["fig_panel_size"],
                            fig_ranges: dict = default["fig_ranges"],
                            fig_titles: dict = default["fig_titles"],
                            panel_param: dict = default["panel_param"]):
    #
    # -- Read json
    #
    values, metadata = data_organize_json(
        data_diagnostics, data_epoch_lengths, data_projects, data_experiments, data_mme_create=data_mme_create,
        data_mme_use_all_smiles=data_mme_use_all_smiles, data_mme_use_smile_mean=data_mme_use_smile_mean,
        data_smile_minimum_size=data_smile_minimum_size, data_smile_rejected=data_smile_rejected,
        data_smile_require_all_experiments=data_smile_require_all_experiments)
    #
    # -- Define thresholds for each method
    #
    values, thresholds = nest_define_uncertainty_threshold(values, uncertainty_threshold)
    #
    # -- Compute required ensemble size (RES) to reach an uncertainty smaller than the desired ones
    #
    res_bootstrap, _, _ = nest_compute_res(
        values, thresholds, res_maximum, uncertainty_confidence_interval, "normal",
        uncertainty_combinations, uncertainty_resamples, False)
    res_theory, _, _ = nest_compute_res(
        values, thresholds, res_maximum, uncertainty_confidence_interval, "normal",
        uncertainty_combinations, uncertainty_resamples, True)
    #
    # -- Organize data for the plot
    #
    # [diagnostic, epoch_length, project, experiment, dataset, epoch, method]
    data_to_plot = {}
    for dia in list(res_bootstrap.keys()):
        for dur in list(res_bootstrap[dia].keys()):
            for pro in list(res_bootstrap[dia][dur].keys()):
                for exp in list(res_bootstrap[dia][dur][pro].keys()):
                    for dat in list(res_bootstrap[dia][dur][pro][exp].keys()):
                        for epo in list(res_bootstrap[dia][dur][pro][exp][dat].keys()):
                            for method in list(res_bootstrap[dia][dur][pro][exp][dat][epo].keys()):
                                for threshold in list(res_bootstrap[dia][dur][pro][exp][dat][epo][method].keys()):
                                    if threshold in list(res_theory[dia][dur][pro][exp][dat][epo][method].keys()):
                                        # RES computed using the bootstrap as x values
                                        arr_x = res_bootstrap[dia][dur][pro][exp][dat][epo][method][threshold]
                                        # RES computed using the theory as y values
                                        arr_y = res_theory[dia][dur][pro][exp][dat][epo][method][threshold]
                                        # save values
                                        data_to_plot = tool_put_in_dict(data_to_plot, [arr_x], "res", dat, "x")
                                        data_to_plot = tool_put_in_dict(data_to_plot, [arr_y], "res", dat, "y")
    fig_colors, fig_markers = {}, {}
    for dia in list(data_to_plot.keys()):
        # x-y ranges
        if dia not in list(fig_ranges.keys()):
            fig_ranges = tool_put_in_dict(fig_ranges, None, dia)
        # x-y titles
        if "x_axis" not in list(fig_titles.keys()) or (
                "x_axis" in list(fig_titles.keys()) and dia not in list(fig_titles["x_axis"].keys())):
            fig_titles = tool_put_in_dict(fig_titles, "", "x_axis", dia)
        if "y_axis" not in list(fig_titles.keys()) or (
                "y_axis" in list(fig_titles.keys()) and dia not in list(fig_titles["y_axis"].keys())):
            fig_titles = tool_put_in_dict(fig_titles, "", "y_axis", dia)
        # colors and markers
        for dat in list(data_to_plot[dia].keys()):
            if dat not in list(fig_colors.keys()):
                fig_colors = tool_put_in_dict(fig_colors, fig_marker_color, dat)
            if dat not in list(fig_markers.keys()):
                fig_markers = tool_put_in_dict(fig_markers, fig_marker, dat)
    #
    # -- Figure
    #
    # output figure name will be the file name (path removed and extension removed)
    fig_name = __file__.split("/")[-1].split(".")[0]
    if fig_detailed_name is True:
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
        fig_name += "_" + str(95) + "ci"
    fig_scatter_and_regression(data_to_plot, ["res"], fig_format, fig_name, fig_colors, fig_markers, fig_marker_size,
                               "row", fig_panel_size, fig_ranges, fig_titles, fig_legend_bool=False,
                               fig_title_bool=False, panel_param=panel_param)
# ---------------------------------------------------------------------------------------------------------------------#
