# -*- coding:UTF-8 -*-
# ---------------------------------------------------------------------------------------------------------------------#
# Figure S3 of the paper about estimating_uncertainties_in_simulated_ENSO submitted to JAMES
# Plot: influence of the ensemble size on the uncertainty of the ensemble mean
# ---------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------#
# Import packages
# ---------------------------------------------------#
# estimating_uncertainties_enso package
from . params import default_parameters
from estimating_uncertainties_enso.compute_lib.data_lib import data_organize_json
from estimating_uncertainties_enso.compute_lib.nest_lib import deepcopy, nest_compute_statistic, \
    nest_influence_of_ensemble_size, nest_standardize_distributions
from estimating_uncertainties_enso.compute_lib.stat_lib import stat_uncertainty_select_and_compute
from estimating_uncertainties_enso.compute_lib.tool_lib import tool_put_in_dict
from estimating_uncertainties_enso.figure_templates.fig_template import fig_distribution_and_ensemble_size
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
    "data_diagnostics": ["var_pr_ano_n30e"],
    # list of epoch lengths
    "data_epoch_lengths": ["030_year_epoch"],
    # list of projects
    "data_projects": ["cmip6"],
    # list of experiments
    "data_experiments": default_parameters["data_experiments"],
    # create the MME: True, False
    "data_mme_create": default_parameters["data_mme_create"],
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
    # SMILE to plot: str
    "fig_smile_selected": "MPI-ESM1-2-LR",
    # threshold for outliers: float
    "fig_threshold": 4,
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
    # size of each panel
    "fig_panel_size": {
        "x_delt_box": 30, "x_frac_box": 0.05, "x_size_box": 80, "y_delt_box": 40, "y_frac_box": 0.05, "y_size_box": 7,
        "x_size_cur": 80, "y_size_cur": 80,
    },
    # color per dataset
    "fig_colors": {"DATASET": "dodgerblue", "DAT w/o outliers": "r", "other LEs": "grey"},
    # boxplots param
    "fig_box_linestyle": "-",
    "fig_box_linewidth": 1,
    "fig_box_mean_size": 4,
    "fig_box_outlier_size": 3,
    # linewidth: all lines have the same width
    "fig_linewidth": 3.,
    # linezorder: all lines have the same zorder; e.g., zorder = 2 is plotted over zorder = 1
    "fig_linezorder": 1,
    # marker per dataset
    "fig_markers": {"DATASET": "s", "DAT w/o outliers": "s", "other LEs": "s"},
    # ticks
    "fig_ticks": {
        "distribution": {
            "x_axis": {
                "var_pr_ano_n30e": list(range(-4, 13, 4)),
            },
            "y_axis": None,
        },
        "influence": {
            "x_axis": {
                "maximum": [round(k / 10, 1) for k in list(range(2, 11, 2))],
            },
            "y_axis": {
                "maximum": {
                    "ave_pr_val_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "ave_pr_val_n34e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "ave_pr_val_n40e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "ave_ts_val_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "ave_ts_val_n34e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "ave_ts_val_n40e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "ave_tx_val_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "ave_tx_val_n34e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "ave_tx_val_n40e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "ave_ty_val_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "ave_ty_val_n34e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "ave_ty_val_n40e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "ske_pr_ano_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "ske_pr_ano_n34e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "ske_pr_ano_n40e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "ske_ts_ano_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "ske_ts_ano_n34e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "ske_ts_ano_n40e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "ske_tx_ano_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "ske_tx_ano_n34e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "ske_tx_ano_n40e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "ske_ty_ano_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "ske_ty_ano_n34e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "ske_ty_ano_n40e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "var_pr_ano_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "var_pr_ano_n34e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "var_pr_ano_n40e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "var_ts_ano_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "var_ts_ano_n34e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "var_ts_ano_n40e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "var_tx_ano_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "var_tx_ano_n34e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "var_tx_ano_n40e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "var_ty_ano_n30e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "var_ty_ano_n34e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                    "var_ty_ano_n40e": [round(k / 10, 1) for k in list(range(10, 31, 5))],
                },
            },
        },
    },
    # titles
    "fig_titles": {
        "distribution": {
            "x_axis": "standardized distribution\nof ",
        },
        "influence": {
            "x_axis": {
                "maximum": "fraction of ensemble used",
            },
            "y_axis": {
                "maximum": "ratio",
            },
        },
        **default_parameters["fig_titles"],  # add diagnostics, experiments and absolute / relative uncertainty
    },
    # panel parameters (to modify default values of fig_panel.py)
    "panel_param_distributions": {"y_nbr_minor": 0},
    "panel_param_influence": {},
}
# ---------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------------------------------------------------------------------------#
# Main
# ---------------------------------------------------------------------------------------------------------------------#
def s03_ensemble_size_mpi(
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
        fig_box_linestyle: str = default["fig_box_linestyle"],
        fig_box_linewidth: float = default["fig_box_linewidth"],
        fig_box_mean_size: float = default["fig_box_mean_size"],
        fig_box_outlier_size: float = default["fig_box_outlier_size"],
        fig_colors: dict = default["fig_colors"],
        fig_name_add: str = default["fig_name_add"],
        fig_name_details: bool = default["fig_name_details"],
        fig_format: str = default["fig_format"],
        fig_linewidth: float = default["fig_linewidth"],
        fig_linezorder: int = default["fig_linezorder"],
        fig_markers: dict = default["fig_markers"],
        fig_orientation: str = default["fig_orientation"],
        fig_panel_size: dict = default["fig_panel_size"],
        fig_smile_selected: str = default["fig_smile_selected"],
        fig_threshold: float = default["fig_threshold"],
        fig_ticks: dict = default["fig_ticks"],
        fig_titles: dict = default["fig_titles"],
        fig_uncertainty_reference: str = default["fig_uncertainty_reference"],
        panel_param_distributions: dict = default["panel_param_distributions"],
        panel_param_influence: dict = default["panel_param_distributions"],
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
    # -- Standardize SMILE distributions
    #
    standard, _, _ = nest_standardize_distributions(values)
    #
    # -- Compute skewness
    #
    skewness, _, _ = nest_compute_statistic(values, "ske")
    #
    # -- Compute uncertainty (fig_smile_selected only)
    #
    uncertainties = {}
    for dia in list(values.keys()):
        for dur in list(values[dia].keys()):
            for pro in list(values[dia][dur].keys()):
                exp = deepcopy(data_experiments[0])
                if exp in list(values[dia][dur][pro].keys()):
                    for dat in list(values[dia][dur][pro][exp].keys()):
                        for epo in list(values[dia][dur][pro][exp][dat].keys()):
                            # list tests
                            list_test = ["DATASET", "DAT w/o outliers"] if dat == fig_smile_selected else ["other LEs"]
                            for k1 in list_test:
                                # arrays
                                arr1 = deepcopy(values[dia][dur][pro][exp][dat][epo])
                                arr2 = standard[dia][dur][pro][exp][dat][epo]
                                # remove outliers
                                if k1 == "DAT w/o outliers":
                                    arr1 = [k2 for k2, k3 in zip(arr1, arr2) if k3 < fig_threshold]
                                # list sample sizes to use
                                sample_sizes = [k for k in uncertainty_sample_sizes if isinstance(k, int) and
                                                k < len(arr1)] + [len(arr1)]
                                # compute uncertainty as a function of ensemble size
                                for k2 in sample_sizes:
                                    val = stat_uncertainty_select_and_compute(
                                        arr1, uncertainty_confidence_interval, uncertainty_distribution,
                                        uncertainty_relative, uncertainty_combinations, uncertainty_resamples,
                                        uncertainty_theory, k2)
                                    # save values
                                    name = str(k2).zfill(3) + "_members" if len(uncertainty_sample_sizes) > 0 else \
                                        "max_members"
                                    uncertainties = tool_put_in_dict(
                                        uncertainties, val, dia, dur, pro, exp, str(dat) + "--" + str(k1), epo, name)
    #
    # -- Compute the influence of the ensemble size on uncertainty
    #
    influence = nest_influence_of_ensemble_size(uncertainties, fig_uncertainty_reference)
    #
    # -- Organize data to for figure
    #
    # experiment to plot
    list_experiments = data_experiments[:1]
    # list all available datasets
    list_dat = list(set([dat for dia in list(standard.keys()) for dur in list(standard[dia].keys())
                         for pro in list(standard[dia][dur].keys()) for exp in list(standard[dia][dur][pro].keys())
                         for dat in list(standard[dia][dur][pro][exp].keys())]))
    list_dat = list(reversed(sorted(list_dat, key=str.casefold)))
    # adapt panel size
    fig_panel_size["y_size_box"] = fig_panel_size["y_size_box"] * len(list_dat)
    # organize distributions
    distributions = {}
    for dia in list(standard.keys()):
        for dur in list(standard[dia].keys())[:1]:  # keep only the first epoch length
            for pro in list(standard[dia][dur].keys()):
                # temporary dictionary
                d1 = deepcopy(standard[dia][dur][pro])
                # get distributions for each experiment and dataset
                for ii, exp in enumerate(list_experiments):
                    for jj, dat in enumerate(list_dat):
                        if exp in list(d1.keys()) and dat in list(d1[exp].keys()):
                            # parameters for x values
                            n_exp = len(list_experiments)
                            dx = 1 / n_exp
                            x_val = [jj - dx * (n_exp - 1) / 2 + ii * dx]
                            # standardized distribution (get first epoch)
                            epo = sorted(list(d1[exp][dat].keys()), key=str.casefold)[0]
                            y_val = [d1[exp][dat][epo]]
                            # skewness
                            z_val = [skewness[dia][dur][pro][exp][dat][epo]]
                            # save values
                            tmp = "DATASET" if dat == fig_smile_selected else "other LEs"
                            distributions = tool_put_in_dict(distributions, deepcopy(x_val), dia, tmp, "x")
                            distributions = tool_put_in_dict(distributions, deepcopy(y_val), dia, tmp, "y")
                            distributions = tool_put_in_dict(distributions, deepcopy(z_val), dia, tmp, "z")
                            if "x_tick_labels" not in list(distributions[dia][tmp].keys()):
                                distributions = tool_put_in_dict(distributions, list_dat, dia, tmp, "x_tick_labels")
    ens_size_influence = {}
    for dia in list(influence.keys()):
        for dat in list(influence[dia].keys()):
            for exp in list(influence[dia][dat].keys()):
                for dur in list(influence[dia][dat][exp].keys()):
                    for k in list(influence[dia][dat][exp][dur].keys()):
                        ens_size_influence = tool_put_in_dict(ens_size_influence, [influence[dia][dat][exp][dur][k]],
                                                              dia, dat.split("--")[-1], exp, dur, k)
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
    fig_distribution_and_ensemble_size(
        distributions, ens_size_influence, data_diagnostics, data_experiments, fig_format, fig_name, fig_box_linestyle,
        fig_box_linewidth, fig_box_mean_size, fig_box_outlier_size, fig_colors, fig_linewidth, fig_linezorder,
        fig_markers, fig_panel_size, fig_smile_selected, fig_threshold, fig_ticks, fig_titles,
        fig_uncertainty_reference, panel_param_distributions=panel_param_distributions,
        panel_param_influence=panel_param_influence)
# ---------------------------------------------------------------------------------------------------------------------#
