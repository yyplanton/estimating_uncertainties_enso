# -*- coding:UTF-8 -*-
# ---------------------------------------------------------------------------------------------------------------------#
# Figure 5 of the paper about estimating_uncertainties_in_simulated_ENSO submitted to JAMES
# Plot: required ensemble sizes for several required uncertainty
# ---------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------#
# Import packages
# ---------------------------------------------------#
# estimating_uncertainties_enso package
from . params import default_parameters
from estimating_uncertainties_enso.compute_lib.data_lib import data_organize_json
from estimating_uncertainties_enso.compute_lib.nest_lib import nest_compute_res, nest_define_uncertainty_threshold,\
    nest_examples_of_res_method
from estimating_uncertainties_enso.compute_lib.tool_lib import tool_put_in_dict
from estimating_uncertainties_enso.figure_templates.fig_template import fig_examples_of_res
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
    "data_smile_minimum_size": default_parameters["data_smile_minimum_size"],
    # list of rejected SMILEs
    "data_smile_rejected": default_parameters["data_smile_rejected"],
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
    # maximum number of combinations used if uncertainty_theory is True and smile_size > sample_size: int [0, 1e10]
    "uncertainty_combinations": default_parameters["uncertainty_combinations"],
    # number of resamples used for the bootstrap if uncertainty_theory is False: int [0, 1e10]
    "uncertainty_resamples": default_parameters["uncertainty_resamples"],
    # uncertainty computed for a given experiment
    "uncertainty_experiment": "piControl",
    # uncertainty to reach per diagnostic per method
    "uncertainty_threshold": {
        "ave_pr_val_n30e": {
            "unc": {"uncertainty_relative": True, "threshold": 5},
            "obs": {"reference": "GPCPv2.3", "epoch": "last"},  # 'CMAP' is also available
            "mme": {"threshold": 0.1, "range": [25, 75]}},
        "ave_ts_val_n30e": {
            "unc": {"uncertainty_relative": False, "threshold": 0.05},
            "obs": {"reference": "OISSTv2", "epoch": "last"},  # 'COBE2', 'ERSSTv5', 'HadISST' are also available
            "mme": {"threshold": 0.1, "range": [25, 75]}},
        "ske_pr_ano_n30e": {
            "unc": {"uncertainty_relative": True, "threshold": 20},
            "obs": {"reference": "GPCPv2.3", "epoch": "last"},  # 'CMAP' is also available
            "mme": {"threshold": 0.1, "range": [25, 75]}},
        "ske_ts_ano_n30e": {
            "unc": {"uncertainty_relative": False, "threshold": 0.1},
            "obs": {"reference": "OISSTv2", "epoch": "last"},  # 'COBE2', 'ERSSTv5', 'HadISST' are also available
            "mme": {"threshold": 0.1, "range": [25, 75]}},
        "var_pr_ano_n30e": {
            "unc": {"uncertainty_relative": True, "threshold": 20},
            "obs": {"reference": "GPCPv2.3", "epoch": "last"},  # 'CMAP' is also available
            "mme": {"threshold": 0.1, "range": [25, 75]}},
        "var_ts_ano_n30e": {
            "unc": {"uncertainty_relative": True, "threshold": 20},
            "obs": {"reference": "OISSTv2", "epoch": "last"},  # 'COBE2', 'ERSSTv5', 'HadISST' are also available
            "mme": {"threshold": 0.1, "range": [25, 75]}},
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
    # figure orientation: column (column = variables, row = statistics), row (column = statistics, row = statistics)
    "fig_orientation": default_parameters["fig_orientation"],
    # size of each panel
    "fig_panel_size": {"x_delt": 2, "x_frac": 0.5, "x_size": 5, "y_delt": 3, "y_frac": 0.5, "y_size": 8},
    # color per dataset
    "fig_colors": {
        "unc": "goldenrod",
        "obs": "black",
        "mme": "r",
        **default_parameters["fig_colors"],  # add colors per dataset
    },
    # marker per dataset
    "fig_markers": default_parameters["fig_markers"],
    # marker size: all marker have the same size
    "fig_marker_size": 150.,
    # ranges
    "fig_ranges": {
        "x_axis": list(range(0, 3)),
        "y_axis": list(range(0, 61, 15)),
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
def f05_required_ensemble_size(data_diagnostics: list = default["data_diagnostics"],
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
                               uncertainty_distribution: str = default["uncertainty_distribution"],
                               uncertainty_experiment: str = default["uncertainty_experiment"],
                               uncertainty_resamples: int = default["uncertainty_resamples"],
                               uncertainty_theory: bool = default["uncertainty_theory"],
                               uncertainty_threshold: dict = default["uncertainty_threshold"],
                               fig_colors: dict = default["fig_colors"],
                               fig_detailed_name: bool = default["fig_detailed_name"],
                               fig_format: str = default["fig_format"],
                               fig_markers: dict = default["fig_markers"],
                               fig_marker_size: float = default["fig_marker_size"],
                               fig_orientation: str = default["fig_orientation"],
                               fig_panel_size: dict = default["fig_panel_size"],
                               fig_ranges: dict = default["fig_ranges"],
                               fig_smile_selected: str = default["fig_smile_selected"],
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
    values, thresholds = nest_define_uncertainty_threshold(values, uncertainty_threshold, uncertainty_experiment)
    #
    # -- Compute required ensemble size (RES) to reach an uncertainty smaller than the desired ones
    #
    res, _, _ = nest_compute_res(
        values, thresholds, res_maximum, uncertainty_confidence_interval, uncertainty_distribution,
        uncertainty_combinations, uncertainty_resamples, uncertainty_theory)
    #
    # -- Organize data for the plot
    #
    examples = nest_examples_of_res_method(res, fig_smile_selected)
    for dia in sorted(list(examples.keys()), key=str.casefold):
        for method in sorted(list(examples[dia].keys()), key=str.casefold):
            for dur in sorted(list(examples[dia][method].keys()), key=str.casefold):
                for pro in sorted(list(examples[dia][method][dur].keys()), key=str.casefold):
                    for exp in sorted(list(examples[dia][method][dur][pro].keys()), key=str.casefold):
                        print(dia, method, dur, pro, exp)
                        arr = examples[dia][method][dur][pro][exp]["boxplot"]
                        nbr_cap = sum([1 for k in arr if k == res_maximum])
                        print(str("RES of " + str(fig_smile_selected) + ": ").rjust(25) +
                              str(examples[dia][method][dur][pro][exp]["marker"]).rjust(2))
                        print(str("nbr of RES set to " + str(res_maximum) + ": ").rjust(25) + str(nbr_cap).rjust(2) +
                              str("(" + "{0:.1f}".format(round(nbr_cap * 100 / len(arr), 1)) + "%)").rjust(8))
    for dia in list(uncertainty_threshold.keys()):
        for method in list(uncertainty_threshold[dia].keys()):
            dict_method = uncertainty_threshold[dia][method]
            if method == "unc":
                tmp = "relative" if dict_method["uncertainty_relative"] is True else "absolute"
                lab = str(fig_titles[tmp]) + " = " + str(dict_method["threshold"])
                if tmp == "absolute" and metadata[dia]["units"] != "":
                    lab += metadata[dia]["units"]
                elif tmp == "relative":
                    lab += "%"
            elif method == "mme":
                if dict_method["range"] == [25, 75]:
                    tmp = " MME's IQR"
                elif dict_method["range"] == [0, 100]:
                    tmp = " MME's range"
                else:
                    tmp = " MME's P$_{" + str(dict_method["range"][0]) + "-" + str(dict_method["range"][1]) + "}$"
                lab = str(fig_titles["absolute"]) + " = " + str(dict_method["threshold"]) + str(tmp)
            else:
                tmp = "P$_{" + str(100 - uncertainty_confidence_interval) + "}$"
                lab = str(fig_titles["absolute"]) + " = " + str(tmp) + "(" + r"$\vert$" + "mod - obs" + r"$\vert$" + ")"
            fig_titles = tool_put_in_dict(fig_titles, lab, "x_axis", dia, method)
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
        fig_name += "_theory" if uncertainty_theory is True else "_random"
        fig_name += "_" + str(95) + "ci"
        fig_name += "_" + str(fig_orientation)
    fig_examples_of_res(examples, data_diagnostics, fig_format, fig_name, fig_colors, fig_markers, fig_marker_size,
                        fig_orientation, fig_panel_size, fig_ranges, fig_smile_selected, fig_titles,
                        panel_param=panel_param)
# ---------------------------------------------------------------------------------------------------------------------#
