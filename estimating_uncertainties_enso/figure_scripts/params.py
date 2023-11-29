# -*- coding:UTF-8 -*-
# ---------------------------------------------------------------------------------------------------------------------#
# Default parameters used in many modules for the paper about estimating_uncertainties_in_simulated_ENSO submitted to
# JAMES
# ---------------------------------------------------------------------------------------------------------------------#
default_parameters = {
    #
    # -- Data
    #
    # list of diagnostics
    "data_diagnostics": ["ave_pr_val_n30e", "ave_ts_val_n30e", "var_pr_ano_n30e", "var_ts_ano_n30e", "ske_pr_ano_n30e",
                         "ske_ts_ano_n30e"],
    # list of epoch lengths
    "data_epoch_lengths": ["030_year_epoch", "045_year_epoch", "060_year_epoch", "075_year_epoch", "090_year_epoch",
                           "105_year_epoch", "120_year_epoch", "135_year_epoch", "150_year_epoch"],
    # list of projects
    "data_projects": ["cmip6", "observations"],
    # list of experiments
    "data_experiments": ["piControl", "historical"],
    # create the MME: True, False
    "data_mme_create": False,
    # MME made with all available SMILEs (or 1st SMILE of each model): True, False
    "data_mme_use_all_smiles": True,
    # MME made with ensemble means (or 1st member of each SMILE): True, False
    "data_mme_use_smile_mean": False,
    # dictionary of desired observational datasets per diagnostic
    "data_observations_desired": {
        "ave_pr_val_n30e": ["GPCPv2.3"],  # 'CMAP' is also available
        "ave_ts_val_n30e": ["OISSTv2"],  # 'COBE2', 'ERSSTv5', 'HadISST' are also available
        "ske_pr_ano_n30e": ["GPCPv2.3"],
        "ske_ts_ano_n30e": ["OISSTv2"],
        "var_pr_ano_n30e": ["GPCPv2.3"],
        "var_ts_ano_n30e": ["OISSTv2"],
    },
    # minimum number of member for SMILEs: int [1, 100]
    "data_smile_minimum_size": 10,
    # list of rejected SMILEs:
    #      - CAS-ESM2-0 has clear change in precipitation variability between piControl and historical runs
    #      - KACE-1-0-G's GMST from the piControl run has a clear trend of ~0.33°C/century throughout the simulation
    "data_smile_rejected": ["CAS-ESM2-0", "KACE-1-0-G"],
    # require all experiments to keep SMILE: True, False
    "data_smile_require_all_experiments": True,
    #
    # -- Uncertainty
    #
    # compute uncertainty based on theory (or bootstrap): True, False
    "uncertainty_theory": True,
    # compute relative uncertainty (or absolute): True, False
    "uncertainty_relative": False,
    # confidence interval of the uncertainty: float [0, 100]
    "uncertainty_confidence_interval": 95,
    # distribution used to compute the confidence interval if uncertainty_theory is True: 'normal', 'student'
    "uncertainty_distribution": "normal",
    # maximum number of combinations used if uncertainty_theory is True and smile_size > sample_size: int [10, 1e10]
    "uncertainty_combinations": int(1e4),
    # number of resamples used for the bootstrap if uncertainty_theory is False: int [10, 1e10]
    "uncertainty_resamples": int(1e6),
    # list of sample sizes for which the uncertainty will be computed
    "uncertainty_sample_sizes": [k for k in range(10, 101, 5)],
    # uncertainty computed for a given experiment
    "uncertainty_experiment": "piControl",
    # uncertainty to reach per diagnostic per method
    "uncertainty_threshold": {
        "ave_pr_val_n30e": {
            "unc": {"uncertainty_relative": True, "threshold": 5},
            "mme": {"threshold": 0.1, "range": [25, 75]},
            "obs": {"reference": "GPCPv2.3", "epoch": "last"}},  # 'CMAP' is also available
        "ave_ts_val_n30e": {
            "unc": {"uncertainty_relative": False, "threshold": 0.05},
            "mme": {"threshold": 0.1, "range": [25, 75]},
            "obs": {"reference": "OISSTv2", "epoch": "last"}},  # 'COBE2', 'ERSSTv5', 'HadISST' are also available
        "ske_pr_ano_n30e": {
            "unc": {"uncertainty_relative": True, "threshold": 20},
            "mme": {"threshold": 0.1, "range": [25, 75]},
            "obs": {"reference": "GPCPv2.3", "epoch": "last"}},  # 'CMAP' is also available
        "ske_ts_ano_n30e": {
            "unc": {"uncertainty_relative": False, "threshold": 0.1},
            "mme": {"threshold": 0.1, "range": [25, 75]},
            "obs": {"reference": "OISSTv2", "epoch": "last"}},  # 'COBE2', 'ERSSTv5', 'HadISST' are also available
        "var_pr_ano_n30e": {
            "unc": {"uncertainty_relative": True, "threshold": 20},
            "mme": {"threshold": 0.1, "range": [25, 75]},
            "obs": {"reference": "GPCPv2.3", "epoch": "last"}},  # 'CMAP' is also available
        "var_ts_ano_n30e": {
            "unc": {"uncertainty_relative": True, "threshold": 20},
            "mme": {"threshold": 0.1, "range": [25, 75]},
            "obs": {"reference": "OISSTv2", "epoch": "last"}},  # 'COBE2', 'ERSSTv5', 'HadISST' are also available
    },
    #
    # -- Figure
    #
    # figure format: eps, pdf, png, svg
    "fig_format": "pdf",
    # figure orientation: column (column = variables, row = statistics), row  (column = statistics, row = statistics)
    "fig_orientation": "column",
    # position of the legend on the plot: bottom, right
    "fig_legend_position": "bottom",
    # SMILE to plot separately
    "fig_smile_selected": "IPSL-CM6A-LR",
    # colors
    "fig_colors": {
        # experiments
        "historical": "r",
        "piControl": "dodgerblue",
        # observations: precipitation
        "GPCPv2.3": "k",
        "OISSTv2": "k",
        # SMILEs
        "ACCESS-CM2": "orange",
        "ACCESS-ESM1-5": "forestgreen",
        "CanESM5_p1": "deepskyblue",
        "CanESM5_p2": "m",
        "CanESM5-1": "y",
        "CESM2": "orange",
        "CNRM-CM6-1": "forestgreen",
        "CNRM-ESM2-1": "deepskyblue",
        "E3SM-2-0": "m",
        "EC-Earth3": "y",
        "EC-Earth3-CC": "orange",
        "GISS-E2-1-G_p1f1": "forestgreen",
        "GISS-E2-1-G_p1f2": "deepskyblue",
        "GISS-E2-1-H_p1f1": "m",
        "HadGEM3-GC31-LL": "y",
        "INM-CM5-0": "orange",
        "IPSL-CM6A-LR": "forestgreen",
        "MIROC-ES2L": "deepskyblue",
        "MIROC6": "m",
        "MPI-ESM1-2-HR": "y",
        "MPI-ESM1-2-LR": "orange",
        "MRI-ESM2-0": "forestgreen",
        "NorCPM1": "deepskyblue",
        "UKESM1-0-LL": "m",
        # MME
        "MME--CMIP6": "r",
    },
    # colorbars
    "fig_colorbars": {
        "ave_pr_val": "cmo.rain",
        "ave_ts_val": "cmo.thermal",
        "ske_pr_ano": "cmo.balance",
        "ske_ts_ano": "cmo.balance",
        "var_pr_ano": "cmo.amp",
        "var_ts_ano": "cmo.amp",
    },
    # linestyles
    "fig_linestyles": {
        "historical": "-",
        "piControl": ":",
    },
    # markers
    "fig_markers": {
        # SMILEs
        "ACCESS-CM2": "^",
        "ACCESS-ESM1-5": "^",
        "CanESM5_p1": "^",
        "CanESM5_p2": "^",
        "CanESM5-1": "^",
        "CESM2": ">",
        "CNRM-CM6-1": ">",
        "CNRM-ESM2-1": ">",
        "E3SM-2-0": ">",
        "EC-Earth3": ">",
        "EC-Earth3-CC": "v",
        "GISS-E2-1-G_p1f1": "v",
        "GISS-E2-1-G_p1f2": "v",
        "GISS-E2-1-H_p1f1": "v",
        "HadGEM3-GC31-LL": "v",
        "INM-CM5-0": "<",
        "IPSL-CM6A-LR": "<",
        "MIROC-ES2L": "<",
        "MIROC6": "<",
        "MPI-ESM1-2-HR": "<",
        "MPI-ESM1-2-LR": "X",
        "MRI-ESM2-0": "X",
        "NorCPM1": "X",
        "UKESM1-0-LL": "X",
        # MME
        "MME--CMIP6": "D",
    },
    # titles
    "fig_titles": {
        # diagnostics
        "ave_pr_val": {"x": "PR", "y": "mean", "z": r"$\bar{x}$"},
        "ave_ts_val": {"x": "SST", "y": "mean", "z": r"$\bar{x}$"},
        "ske_pr_ano": {"x": "PRA", "y": "skewness", "z": "g$_{1}$"},
        "ske_ts_ano": {"x": "SSTA", "y": "skewness", "z": "g$_{1}$"},
        "var_pr_ano": {"x": "PRA", "y": "variance", "z": r"$\sigma^{2}$"},
        "var_ts_ano": {"x": "SSTA", "y": "variance", "z": r"$\sigma^{2}$"},
        "ave_pr_val_n30e": {"x": "N3 PR", "y": "mean", "z": r"$\bar{x}$"},
        "ave_ts_val_n30e": {"x": "N3 SST", "y": "mean", "z": r"$\bar{x}$"},
        "ske_pr_ano_n30e": {"x": "N3 PRA", "y": "skewness", "z": "g$_{1}$"},
        "ske_ts_ano_n30e": {"x": "N3 SSTA", "y": "skewness", "z": "g$_{1}$"},
        "var_pr_ano_n30e": {"x": "N3 PRA", "y": "variance", "z": r"$\sigma^{2}$"},
        "var_ts_ano_n30e": {"x": "N3 SSTA", "y": "variance", "z": r"$\sigma^{2}$"},
        # time series
        "tim_ts_val_glob": {"x": "GMST", "y": "", "z": ""},
        "tim_ts_val_n30e": {"x": "N3 SST", "y": "", "z": ""},
        # experiments
        "historical": "HI",
        "piControl": "PI",
        # uncertainties: absolute or relative
        "absolute": r"$\Delta$",
        "relative": r"$\Delta_r$",
    },
}
