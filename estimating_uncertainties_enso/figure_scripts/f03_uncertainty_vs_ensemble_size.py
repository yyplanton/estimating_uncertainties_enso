# -*- coding:UTF-8 -*-
# ---------------------------------------------------------------------------------------------------------------------#
# Figure 3 of the paper about estimating_uncertainties_in_simulated_ENSO submitted to JAMES
# Plot: influence of the ensemble size on the uncertainty of the ensemble mean
# ---------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------#
# Import packages
# ---------------------------------------------------#
# estimating_uncertainties_enso package
from . params import default_parameters
from estimating_uncertainties_enso.compute_lib.data_lib import data_organize_json
from estimating_uncertainties_enso.compute_lib.nest_lib import nest_compute_uncertainty, nest_influence_of_ensemble_size
from estimating_uncertainties_enso.compute_lib.tool_lib import tool_put_in_dict
from estimating_uncertainties_enso.figure_templates.fig_template import fig_influence_of
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
    "data_smile_minimum_size": 15,
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
    # list of sample sizes for which the uncertainty will be computed
    "uncertainty_sample_sizes": default_parameters["uncertainty_sample_sizes"],
    #
    # -- Figure
    #
    # maximum of minimum value used as a reference for the plot
    "fig_uncertainty_reference": "maximum",
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
    "fig_panel_size": {"x_delt": 3, "x_frac": 0.25, "x_size": 16, "y_delt": 2, "y_frac": 0.25, "y_size": 16},
    # color per dataset
    "fig_colors": default_parameters["fig_colors"],
    # linestyle per experiment
    "fig_linestyles": default_parameters["fig_linestyles"],
    # linewidth: all lines have the same width
    "fig_linewidth": 1.,
    # linezorder: all lines have the same zorder; e.g., zorder = 2 is plotted over zorder = 1
    "fig_linezorder": 1,
    # marker per dataset
    "fig_markers": default_parameters["fig_markers"],
    # marker size: all marker have the same size
    "fig_marker_size": 60.,
    # ticks
    "fig_ticks": {
        "x_axis": {
            "maximum": [round(k / 10, 1) for k in list(range(2, 11, 2))],
            "minimum": list(range(10, 71, 15)),
        },
        "y_axis": {
            "maximum": [round(k / 10, 1) for k in list(range(10, 31, 5))],
        },
    },
    # titles
    "fig_titles": {
        "x_axis": {
            "maximum": "fraction of ensemble used",
            "minimum": "ensemble size",
        },
        "y_axis": {
            "maximum": "ratio",
            "minimum": "ratio",
        },
        **default_parameters["fig_titles"],  # add diagnostics, experiments and absolute / relative uncertainty
    },
    # panel parameters (to modify default values of fig_panel.py)
    "panel_param": {},
}
# ---------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------------------------------------------------------------------------#
# Main
# ---------------------------------------------------------------------------------------------------------------------#
def f03_ensemble_size(
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
        uncertainty_combinations: int = default["uncertainty_combinations"],
        uncertainty_confidence_interval: float = default["uncertainty_confidence_interval"],
        uncertainty_distribution: str = default["uncertainty_distribution"],
        uncertainty_relative: bool = default["uncertainty_relative"],
        uncertainty_resamples: int = default["uncertainty_resamples"],
        uncertainty_sample_sizes: list = default["uncertainty_sample_sizes"],
        uncertainty_theory: bool = default["uncertainty_theory"],
        fig_colors: dict = default["fig_colors"],
        fig_format: str = default["fig_format"],
        fig_legend_position: str = default["fig_legend_position"],
        fig_linestyles: dict = default["fig_linestyles"],
        fig_linewidth: float = default["fig_linewidth"],
        fig_linezorder: int = default["fig_linezorder"],
        fig_markers: dict = default["fig_markers"],
        fig_marker_size: float = default["fig_marker_size"],
        fig_name_add: str = default["fig_name_add"],
        fig_name_details: bool = default["fig_name_details"],
        fig_orientation: str = default["fig_orientation"],
        fig_panel_size: dict = default["fig_panel_size"],
        fig_ticks: dict = default["fig_ticks"],
        fig_titles: dict = default["fig_titles"],
        fig_uncertainty_reference: str = default["fig_uncertainty_reference"],
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
    #
    # -- Compute uncertainty
    #
    uncertainties, _, _ = nest_compute_uncertainty(
        values, uncertainty_confidence_interval, uncertainty_distribution, uncertainty_relative,
        uncertainty_combinations, uncertainty_resamples, uncertainty_theory,
        uncertainty_sample_sizes=uncertainty_sample_sizes)
    #
    # -- Compute the influence of the ensemble size on uncertainty
    #
    influence = nest_influence_of_ensemble_size(uncertainties, fig_uncertainty_reference)
    #
    # -- Organize data to for figure
    #
    method = "relative" if uncertainty_relative is True else "absolute"
    for dia in list(influence.keys()):
        # x-y titles
        title = ""
        if "x_axis" in list(fig_titles.keys()) and fig_uncertainty_reference in list(fig_titles["x_axis"].keys()):
            title = fig_titles["x_axis"][fig_uncertainty_reference]
        fig_titles = tool_put_in_dict(fig_titles, title, "x_axis", dia)
        title = ""
        if "y_axis" in list(fig_titles.keys()) and fig_uncertainty_reference in list(fig_titles["y_axis"].keys()):
            title = str(fig_titles[method]) + " " + str(fig_titles["y_axis"][fig_uncertainty_reference])
            title = title.replace("NBR_MEM", str(data_smile_minimum_size))
        fig_titles = tool_put_in_dict(fig_titles, title, "y_axis", dia)
        # x tics
        if "x_axis" in list(fig_ticks.keys()) and isinstance(fig_ticks["x_axis"], dict) is True and \
                dia in list(fig_ticks["x_axis"].keys()) and isinstance(fig_ticks["x_axis"][dia], list) is True:
            pass
        else:
            list_ticks = None
            if "x_axis" in list(fig_ticks.keys()) and isinstance(fig_ticks["x_axis"], dict) is True and \
                    fig_uncertainty_reference in list(fig_ticks["x_axis"].keys()) and \
                    isinstance(fig_ticks["x_axis"][fig_uncertainty_reference], list) is True:
                list_ticks = fig_ticks["x_axis"][fig_uncertainty_reference]
            fig_ticks = tool_put_in_dict(fig_ticks, list_ticks, "x_axis", dia)
        # y tics
        if "y_axis" in list(fig_ticks.keys()) and isinstance(fig_ticks["y_axis"], dict) is True and \
                dia in list(fig_ticks["y_axis"].keys()) and isinstance(fig_ticks["y_axis"][dia], list) is True:
            pass
        else:
            list_ticks = None
            if "y_axis" in list(fig_ticks.keys()) and isinstance(fig_ticks["y_axis"], dict) is True and \
                    fig_uncertainty_reference in list(fig_ticks["y_axis"].keys()) and \
                    isinstance(fig_ticks["y_axis"][fig_uncertainty_reference], list) is True:
                list_ticks = fig_ticks["y_axis"][fig_uncertainty_reference]
            elif "y_axis" in list(fig_ticks.keys()) and isinstance(fig_ticks["y_axis"], dict) is True and \
                    fig_uncertainty_reference in list(fig_ticks["y_axis"].keys()) and \
                    isinstance(fig_ticks["y_axis"][fig_uncertainty_reference], dict) is True and \
                    dia in list(fig_ticks["y_axis"][fig_uncertainty_reference].keys()) and \
                    isinstance(fig_ticks["y_axis"][fig_uncertainty_reference][dia], list) is True:
                list_ticks = fig_ticks["y_axis"][fig_uncertainty_reference][dia]
            fig_ticks = tool_put_in_dict(fig_ticks, list_ticks, "y_axis", dia)
    #
    # -- Figure
    #
    # output figure name will be the file name (path removed and extension removed)
    fig_name = __file__.split("/")[-1].split(".")[0] + str(fig_name_add)
    if fig_name_details is True:
        # add details of the computation to the figure name
        fig_name += "_data_" + str(len(data_projects)) + "pro_" + str(len(data_experiments)) + "exp_" + \
                    str(data_smile_minimum_size) + "mem_" + str(len(data_diagnostics)) + "dia"
        if data_mme_create is True:
            fig_name += "_mme"
            fig_name += "_of_em" if data_mme_use_smile_mean is True else "_of_1m"
            fig_name += "_all_smile" if data_mme_use_all_smiles is True else "_1st_smile"
        fig_name += "_relative_uncertainty" if uncertainty_relative is True else "_absolute_uncertainty"
        fig_name += "_theory" if uncertainty_theory is True else "_random"
        fig_name += "_" + str(uncertainty_confidence_interval) + "ci_" + str(fig_uncertainty_reference)
        if uncertainty_theory is True:
            fig_name += "_" + str(uncertainty_distribution) + "_distribution"
        fig_name += "_" + str(fig_orientation)
    fig_influence_of(influence, data_diagnostics, data_experiments, fig_format, fig_name, fig_colors,
                     fig_legend_position, fig_linestyles, fig_linewidth, fig_linezorder, fig_markers, fig_marker_size,
                     fig_orientation, fig_panel_size, fig_ticks, fig_titles, data_smile_minimum_size, "ensemble_size",
                     fig_uncertainty_reference, panel_param=panel_param)
# ---------------------------------------------------------------------------------------------------------------------#
