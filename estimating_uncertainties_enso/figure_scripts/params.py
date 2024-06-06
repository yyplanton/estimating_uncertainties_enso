# -*- coding:UTF-8 -*-
# ---------------------------------------------------------------------------------------------------------------------#
# Default parameters used in many modules for the paper about estimating_uncertainties_in_simulated_ENSO submitted to
# JAMES
# ---------------------------------------------------------------------------------------------------------------------#
default_parameters = {
    #
    # -- Data
    #
    # file name: str
    "data_filename": "estimating_uncertainties_in_simulated_enso.json",
    # list of diagnostics: list[str]
    "data_diagnostics": ["ave_pr_val_n30e", "ave_ts_val_n30e", "var_pr_ano_n30e", "var_ts_ano_n30e", "ske_pr_ano_n30e",
                         "ske_ts_ano_n30e"],
    # list of epoch lengths: list[str]
    "data_epoch_lengths": ["030_year_epoch", "045_year_epoch", "060_year_epoch", "075_year_epoch", "090_year_epoch",
                           "105_year_epoch", "120_year_epoch", "135_year_epoch", "150_year_epoch"],
    # list of projects: list[str]
    "data_projects": ["cmip6", "observations"],
    # list of experiments: list[str]
    "data_experiments": ["piControl", "historical"],
    # create the MME: True, False
    "data_mme_create": False,
    # MME made with all available SMILEs (or 1st SMILE of each model): True, False
    "data_mme_use_all_smiles": True,
    # MME made with ensemble means (or 1st member of each SMILE): True, False
    "data_mme_use_smile_mean": False,
    # dictionary of desired observational datasets per diagnostic: dict[str, list[str]]
    "data_observations_desired": {
        "ave_pr_val_n30e": ["GPCPv2.3"],  # 'CMAP' is also available
        "ave_pr_val_n34e": ["GPCPv2.3"],
        "ave_pr_val_n40e": ["GPCPv2.3"],
        "ave_ts_val_n30e": ["OISSTv2"],  # 'COBE2', 'ERSSTv5', 'HadISST' are also available
        "ave_ts_val_n34e": ["OISSTv2"],
        "ave_ts_val_n40e": ["OISSTv2"],
        "ske_pr_ano_n30e": ["GPCPv2.3"],
        "ske_pr_ano_n34e": ["GPCPv2.3"],
        "ske_pr_ano_n40e": ["GPCPv2.3"],
        "ske_ts_ano_n30e": ["OISSTv2"],
        "ske_ts_ano_n34e": ["OISSTv2"],
        "ske_ts_ano_n40e": ["OISSTv2"],
        "var_pr_ano_n30e": ["GPCPv2.3"],
        "var_pr_ano_n34e": ["GPCPv2.3"],
        "var_pr_ano_n40e": ["GPCPv2.3"],
        "var_ts_ano_n30e": ["OISSTv2"],
        "var_ts_ano_n34e": ["OISSTv2"],
        "var_ts_ano_n40e": ["OISSTv2"],
    },
    # minimum number of member for SMILEs: int [1, 100]
    "data_smile_minimum_size": 10,
    # list of rejected SMILEs: list[str]
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
    # list of sample sizes for which the uncertainty will be computed: list[int]
    "uncertainty_sample_sizes": [k for k in range(10, 101, 5)],
    # uncertainty computed for a given experiment: str
    "uncertainty_experiment": "piControl",
    # uncertainty to reach per diagnostic per method: dict[str, dict[str, dict[str, bool | float | int | list | str]]]
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
    # figure format: 'eps', 'pdf', 'png', 'svg'
    "fig_format": "pdf",
    # figure orientation: 'column' (column = variables, row = statistics), 'row' (column = statistics, row = statistics)
    "fig_orientation": "column",
    # position of the legend on the plot: 'bottom', 'right'
    "fig_legend_position": "bottom",
    # SMILE to plot separately: str
    "fig_smile_selected": "IPSL-CM6A-LR",
    # colors: dict[str, str]
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
        "CMCC-CM2-SR5": "forestgreen",
        "CMCC-CM2-SR5_p2": "forestgreen",
        "CNRM-CM6-1": "deepskyblue",
        "CNRM-ESM2-1": "m",
        "E3SM-2-0": "y",
        "EC-Earth3": "orange",
        "EC-Earth3-CC": "forestgreen",
        "EC-Earth3-Veg": "deepskyblue",
        "GISS-E2-1-G_p1f1": "m",
        "GISS-E2-1-G_p1f2": "y",
        "GISS-E2-1-H_p1f1": "orange",
        "HadGEM3-GC31-LL": "forestgreen",
        "INM-CM5-0": "deepskyblue",
        "IPSL-CM6A-LR": "m",
        "MIROC-ES2L": "y",
        "MIROC6": "orange",
        "MPI-ESM1-2-HR": "forestgreen",
        "MPI-ESM1-2-LR": "deepskyblue",
        "MRI-ESM2-0": "m",
        "NorCPM1": "y",
        "UKESM1-0-LL": "orange",
        # MME
        "MME--CMIP6": "r",
    },
    # colorbars: dict[str, str]
    "fig_colorbars": {
        "ave_hf_val": "cmo.balance",
        "ave_pr_val": "cmo.rain",
        "ave_sl_val": "cmo.thermal",
        "ave_ts_val": "cmo.thermal",
        "ave_tx_val": "cmo.balance",
        "ave_ty_val": "cmo.balance",
        "ske_hf_ano": "cmo.balance",
        "ske_pr_ano": "cmo.balance",
        "ske_sl_ano": "cmo.balance",
        "ske_ts_ano": "cmo.balance",
        "ske_tx_ano": "cmo.balance",
        "ske_ty_ano": "cmo.balance",
        "var_hf_ano": "cmo.amp",
        "var_pr_ano": "cmo.amp",
        "var_sl_ano": "cmo.amp",
        "var_ts_ano": "cmo.amp",
        "var_tx_ano": "cmo.amp",
        "var_ty_ano": "cmo.amp",
    },
    # linestyles: dict[str, str]
    "fig_linestyles": {
        "historical": "-",
        "piControl": ":",
    },
    # markers: dict[str, str]
    "fig_markers": {
        # SMILEs
        "ACCESS-CM2": "^",
        "ACCESS-ESM1-5": "^",
        "CanESM5_p1": "^",
        "CanESM5_p2": "^",
        "CanESM5-1": "^",
        "CESM2": ">",
        "CMCC-CM2-SR5": ">",
        "CMCC-CM2-SR5_p2": ">",
        "CNRM-CM6-1": ">",
        "CNRM-ESM2-1": ">",
        "E3SM-2-0": ">",
        "EC-Earth3": "v",
        "EC-Earth3-CC": "v",
        "EC-Earth3-Veg": "v",
        "GISS-E2-1-G_p1f1": "v",
        "GISS-E2-1-G_p1f2": "v",
        "GISS-E2-1-H_p1f1": "<",
        "HadGEM3-GC31-LL": "<",
        "INM-CM5-0": "<",
        "IPSL-CM6A-LR": "<",
        "MIROC-ES2L": "<",
        "MIROC6": "X",
        "MPI-ESM1-2-HR": "X",
        "MPI-ESM1-2-LR": "X",
        "MRI-ESM2-0": "X",
        "NorCPM1": "X",
        "UKESM1-0-LL": "P",
        # MME
        "MME--CMIP6": "D",
    },
    # titles: dict[str, dict[str, str] | str]
    "fig_titles": {
        # diagnostics
        "ave_hf_val": {"x": "NHF", "y": "mean", "z": r"$\bar{x}$"},
        "ave_pr_val": {"x": "PR", "y": "mean", "z": r"$\bar{x}$"},
        "ave_sl_val": {"x": "SSH", "y": "mean", "z": r"$\bar{x}$"},
        "ave_ts_val": {"x": "SST", "y": "mean", "z": r"$\bar{x}$"},
        "ave_tx_val": {"x": "Taux", "y": "mean", "z": r"$\bar{x}$"},
        "ave_ty_val": {"x": "Tauy", "y": "mean", "z": r"$\bar{x}$"},
        "ske_hf_ano": {"x": "NHFA", "y": "skewness", "z": "g$_{1}$"},
        "ske_pr_ano": {"x": "PRA", "y": "skewness", "z": "g$_{1}$"},
        "ske_sl_ano": {"x": "SSHA", "y": "skewness", "z": "g$_{1}$"},
        "ske_ts_ano": {"x": "SSTA", "y": "skewness", "z": "g$_{1}$"},
        "ske_tx_ano": {"x": "TauxA", "y": "skewness", "z": "g$_{1}$"},
        "ske_ty_ano": {"x": "TauyA", "y": "skewness", "z": "g$_{1}$"},
        "var_hf_ano": {"x": "NHFA", "y": "variance", "z": r"$\sigma^{2}$"},
        "var_pr_ano": {"x": "PRA", "y": "variance", "z": r"$\sigma^{2}$"},
        "var_sl_ano": {"x": "SSHA", "y": "variance", "z": r"$\sigma^{2}$"},
        "var_ts_ano": {"x": "SSTA", "y": "variance", "z": r"$\sigma^{2}$"},
        "var_tx_ano": {"x": "TauxA", "y": "variance", "z": r"$\sigma^{2}$"},
        "var_ty_ano": {"x": "TauyA", "y": "variance", "z": r"$\sigma^{2}$"},
        "ave_hf_val_glob": {"x": "global NHF", "y": "mean", "z": r"$\bar{x}$"},
        "ave_hf_val_n30e": {"x": "N3 NHF", "y": "mean", "z": r"$\bar{x}$"},
        "ave_hf_val_n34e": {"x": "N3.4 NHF", "y": "mean", "z": r"$\bar{x}$"},
        "ave_hf_val_n40e": {"x": "N4 NHF", "y": "mean", "z": r"$\bar{x}$"},
        "ave_pr_val_glob": {"x": "global PR", "y": "mean", "z": r"$\bar{x}$"},
        "ave_pr_val_n30e": {"x": "N3 PR", "y": "mean", "z": r"$\bar{x}$"},
        "ave_pr_val_n30e_d0": {"x": "N3 PR", "y": "mean", "z": r"$\bar{x}$"},
        "ave_pr_val_n30e_d1": {"x": "N3 PR", "y": "mean", "z": r"$\bar{x}$"},
        "ave_pr_val_n30e_d2": {"x": "N3 PR", "y": "mean", "z": r"$\bar{x}$"},
        "ave_pr_val_n30e_de": {"x": "N3 PR", "y": "mean", "z": r"$\bar{x}$"},
        "ave_pr_val_n34e": {"x": "N3.4 PR", "y": "mean", "z": r"$\bar{x}$"},
        "ave_pr_val_n40e": {"x": "N4 PR", "y": "mean", "z": r"$\bar{x}$"},
        "ave_sl_val_glob": {"x": "GMSL", "y": "mean", "z": r"$\bar{x}$"},
        "ave_sl_val_n30e": {"x": "N3 SSH", "y": "mean", "z": r"$\bar{x}$"},
        "ave_sl_val_n34e": {"x": "N3.4 SSH", "y": "mean", "z": r"$\bar{x}$"},
        "ave_sl_val_n40e": {"x": "N4 SSH", "y": "mean", "z": r"$\bar{x}$"},
        "ave_ts_val_glob": {"x": "GMST", "y": "mean", "z": r"$\bar{x}$"},
        "ave_ts_val_n30e": {"x": "N3 SST", "y": "mean", "z": r"$\bar{x}$"},
        "ave_ts_val_n30e_d0": {"x": "N3 SST", "y": "mean", "z": r"$\bar{x}$"},
        "ave_ts_val_n30e_d1": {"x": "N3 SST", "y": "mean", "z": r"$\bar{x}$"},
        "ave_ts_val_n30e_d2": {"x": "N3 SST", "y": "mean", "z": r"$\bar{x}$"},
        "ave_ts_val_n30e_de": {"x": "N3 SST", "y": "mean", "z": r"$\bar{x}$"},
        "ave_ts_val_n34e": {"x": "N3.4 SST", "y": "mean", "z": r"$\bar{x}$"},
        "ave_ts_val_n40e": {"x": "N4 SST", "y": "mean", "z": r"$\bar{x}$"},
        "ave_tx_val_n30e": {"x": "N3 Taux", "y": "mean", "z": r"$\bar{x}$"},
        "ave_tx_val_n34e": {"x": "N3.4 Taux", "y": "mean", "z": r"$\bar{x}$"},
        "ave_tx_val_n40e": {"x": "N4 Taux", "y": "mean", "z": r"$\bar{x}$"},
        "ave_ty_val_n30e": {"x": "N3 Tauy", "y": "mean", "z": r"$\bar{x}$"},
        "ave_ty_val_n34e": {"x": "N3.4 Tauy", "y": "mean", "z": r"$\bar{x}$"},
        "ave_ty_val_n40e": {"x": "N4 Tauy", "y": "mean", "z": r"$\bar{x}$"},
        "ske_hf_ano_n30e": {"x": "N3 NHFA", "y": "skewness", "z": "g$_{1}$"},
        "ske_hf_ano_n34e": {"x": "N3.4 NHFA", "y": "skewness", "z": "g$_{1}$"},
        "ske_hf_ano_n40e": {"x": "N4 NHFA", "y": "skewness", "z": "g$_{1}$"},
        "ske_pr_ano_n30e": {"x": "N3 PRA", "y": "skewness", "z": "g$_{1}$"},
        "ske_pr_ano_n30e_d0": {"x": "N3 PRA", "y": "skewness", "z": "g$_{1}$"},
        "ske_pr_ano_n30e_d1": {"x": "N3 PRA", "y": "skewness", "z": "g$_{1}$"},
        "ske_pr_ano_n30e_d2": {"x": "N3 PRA", "y": "skewness", "z": "g$_{1}$"},
        "ske_pr_ano_n30e_de": {"x": "N3 PRA", "y": "skewness", "z": "g$_{1}$"},
        "ske_pr_ano_n34e": {"x": "N3.4 PRA", "y": "skewness", "z": "g$_{1}$"},
        "ske_pr_ano_n40e": {"x": "N4 PRA", "y": "skewness", "z": "g$_{1}$"},
        "ske_sl_ano_n30e": {"x": "N3 SSHA", "y": "skewness", "z": "g$_{1}$"},
        "ske_sl_ano_n34e": {"x": "N3.4 SSHA", "y": "skewness", "z": "g$_{1}$"},
        "ske_sl_ano_n40e": {"x": "N4 SSHA", "y": "skewness", "z": "g$_{1}$"},
        "ske_ts_ano_n30e": {"x": "N3 SSTA", "y": "skewness", "z": "g$_{1}$"},
        "ske_ts_ano_n30e_d0": {"x": "N3 SSTA", "y": "skewness", "z": "g$_{1}$"},
        "ske_ts_ano_n30e_d1": {"x": "N3 SSTA", "y": "skewness", "z": "g$_{1}$"},
        "ske_ts_ano_n30e_d2": {"x": "N3 SSTA", "y": "skewness", "z": "g$_{1}$"},
        "ske_ts_ano_n30e_de": {"x": "N3 SSTA", "y": "skewness", "z": "g$_{1}$"},
        "ske_ts_ano_n34e": {"x": "N3.4 SSTA", "y": "skewness", "z": "g$_{1}$"},
        "ske_ts_ano_n40e": {"x": "N4 SSTA", "y": "skewness", "z": "g$_{1}$"},
        "ske_tx_ano_n30e": {"x": "N3 TauxA", "y": "skewness", "z": "g$_{1}$"},
        "ske_tx_ano_n34e": {"x": "N3.4 TauxA", "y": "skewness", "z": "g$_{1}$"},
        "ske_tx_ano_n40e": {"x": "N4 TauxA", "y": "skewness", "z": "g$_{1}$"},
        "ske_ty_ano_n30e": {"x": "N3 TauyA", "y": "skewness", "z": "g$_{1}$"},
        "ske_ty_ano_n34e": {"x": "N3.4 TauyA", "y": "skewness", "z": "g$_{1}$"},
        "ske_ty_ano_n40e": {"x": "N4 TauyA", "y": "skewness", "z": "g$_{1}$"},
        "var_hf_ano_n30e": {"x": "N3 NHFA", "y": "variance", "z": r"$\sigma^{2}$"},
        "var_hf_ano_n34e": {"x": "N3.4 NHFA", "y": "variance", "z": r"$\sigma^{2}$"},
        "var_hf_ano_n40e": {"x": "N4 NHFA", "y": "variance", "z": r"$\sigma^{2}$"},
        "var_pr_ano_n30e": {"x": "N3 PRA", "y": "variance", "z": r"$\sigma^{2}$"},
        "var_pr_ano_n30e_d0": {"x": "N3 PRA", "y": "variance", "z": r"$\sigma^{2}$"},
        "var_pr_ano_n30e_d1": {"x": "N3 PRA", "y": "variance", "z": r"$\sigma^{2}$"},
        "var_pr_ano_n30e_d2": {"x": "N3 PRA", "y": "variance", "z": r"$\sigma^{2}$"},
        "var_pr_ano_n30e_de": {"x": "N3 PRA", "y": "variance", "z": r"$\sigma^{2}$"},
        "var_pr_ano_n34e": {"x": "N3.4 PRA", "y": "variance", "z": r"$\sigma^{2}$"},
        "var_pr_ano_n40e": {"x": "N4 PRA", "y": "variance", "z": r"$\sigma^{2}$"},
        "var_sl_ano_n30e": {"x": "N3 SSHA", "y": "variance", "z": r"$\sigma^{2}$"},
        "var_sl_ano_n34e": {"x": "N3.4 SSHA", "y": "variance", "z": r"$\sigma^{2}$"},
        "var_sl_ano_n40e": {"x": "N4 SSHA", "y": "variance", "z": r"$\sigma^{2}$"},
        "var_ts_ano_n30e": {"x": "N3 SSTA", "y": "variance", "z": r"$\sigma^{2}$"},
        "var_ts_ano_n30e_d0": {"x": "N3 SSTA", "y": "variance", "z": r"$\sigma^{2}$"},
        "var_ts_ano_n30e_d1": {"x": "N3 SSTA", "y": "variance", "z": r"$\sigma^{2}$"},
        "var_ts_ano_n30e_d2": {"x": "N3 SSTA", "y": "variance", "z": r"$\sigma^{2}$"},
        "var_ts_ano_n30e_de": {"x": "N3 SSTA", "y": "variance", "z": r"$\sigma^{2}$"},
        "var_ts_ano_n34e": {"x": "N3.4 SSTA", "y": "variance", "z": r"$\sigma^{2}$"},
        "var_ts_ano_n40e": {"x": "N4 SSTA", "y": "variance", "z": r"$\sigma^{2}$"},
        "var_tx_ano_n30e": {"x": "N3 TauxA", "y": "variance", "z": r"$\sigma^{2}$"},
        "var_tx_ano_n34e": {"x": "N3.4 TauxA", "y": "variance", "z": r"$\sigma^{2}$"},
        "var_tx_ano_n40e": {"x": "N4 TauxA", "y": "variance", "z": r"$\sigma^{2}$"},
        "var_ty_ano_n30e": {"x": "N3 TauyA", "y": "variance", "z": r"$\sigma^{2}$"},
        "var_ty_ano_n34e": {"x": "N3.4 TauyA", "y": "variance", "z": r"$\sigma^{2}$"},
        "var_ty_ano_n40e": {"x": "N4 TauyA", "y": "variance", "z": r"$\sigma^{2}$"},
        # time series
        "tim_hf_val_glob": {"x": "Global NHF", "y": "", "z": ""},
        "tim_hf_val_n30e": {"x": "N3 NHF", "y": "", "z": ""},
        "tim_hf_val_n34e": {"x": "N3.4 NHF", "y": "", "z": ""},
        "tim_hf_val_n40e": {"x": "N4 NHF", "y": "", "z": ""},
        "tim_pr_val_glob": {"x": "Global PR", "y": "", "z": ""},
        "tim_pr_val_n30e": {"x": "N3 PR", "y": "", "z": ""},
        "tim_pr_val_n34e": {"x": "N3.4 PR", "y": "", "z": ""},
        "tim_pr_val_n40e": {"x": "N4 PR", "y": "", "z": ""},
        "tim_sl_val_glob": {"x": "GMSL", "y": "", "z": ""},
        "tim_sl_val_n30e": {"x": "N3 SSH", "y": "", "z": ""},
        "tim_sl_val_n34e": {"x": "N3.4 SSH", "y": "", "z": ""},
        "tim_sl_val_n40e": {"x": "N4 SSH", "y": "", "z": ""},
        "tim_ts_val_glob": {"x": "GMST", "y": "", "z": ""},
        "tim_ts_val_n30e": {"x": "N3 SST", "y": "", "z": ""},
        "tim_ts_val_n34e": {"x": "N3.4 SST", "y": "", "z": ""},
        "tim_ts_val_n40e": {"x": "N4 SST", "y": "", "z": ""},
        "tim_tx_val_n30e": {"x": "N3 Taux", "y": "", "z": ""},
        "tim_tx_val_n34e": {"x": "N3.4 Taux", "y": "", "z": ""},
        "tim_tx_val_n40e": {"x": "N4 Taux", "y": "", "z": ""},
        "tim_ty_val_n30e": {"x": "N3 Tauy", "y": "", "z": ""},
        "tim_ty_val_n34e": {"x": "N3.4 Tauy", "y": "", "z": ""},
        "tim_ty_val_n40e": {"x": "N4 Tauy", "y": "", "z": ""},
        # experiments
        "historical": "HI",
        "piControl": "PI",
        # uncertainties: absolute or relative
        "absolute": r"$\Delta$",
        "relative": r"$\Delta_r$",
        # ensemble statistics
        "ensemble_mea": "E" + r"$_{\bar{x}}$",
        "ensemble_std": "E" + r"$_{\sigma}$",
        "ensemble_var": "E" + r"$_{\sigma^{2}}$",
    },
}
