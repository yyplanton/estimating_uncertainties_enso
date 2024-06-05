# -*- coding:UTF-8 -*-
# ---------------------------------------------------------------------------------------------------------------------#
# Print Required Ensemble Sizes (RESs) for several relative or absolute uncertainties
# ---------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------#
# Import packages
# ---------------------------------------------------#
# estimating_uncertainties_enso package
from . params import default_parameters
from estimating_uncertainties_enso.compute_lib.data_lib import data_organize_json
from estimating_uncertainties_enso.compute_lib.nest_lib import nest_compute_res, nest_define_uncertainty_threshold
# ---------------------------------------------------#


# ---------------------------------------------------------------------------------------------------------------------#
# Default arguments
# ---------------------------------------------------------------------------------------------------------------------#
default = {
    #
    # -- Data
    #
    # list of diagnostics
    "data_diagnostics": ["ske_ts_ano_n40e"],
    # list of epoch lengths
    "data_epoch_lengths": ["030_year_epoch"],
    # list of projects
    "data_projects": default_parameters["data_projects"],
    # list of experiments
    "data_experiments": ["piControl"],
    # create the MME: True, False
    "data_mme_create": False,
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
    # maximum number of combinations used if uncertainty_theory is True and smile_size > sample_size: int [10, 1e10]
    "uncertainty_combinations": default_parameters["uncertainty_combinations"],
    # number of resamples used for the bootstrap if uncertainty_theory is False: int [10, 1e10]
    "uncertainty_resamples": default_parameters["uncertainty_resamples"],
    # uncertainty to reach per diagnostic per method
    "uncertainty_threshold": {
        "ave_pr_val_n30e": {"unc": {"uncertainty_relative": True, "threshold": list(range(1, 11, 1))}},
        "ave_pr_val_n34e": {"unc": {"uncertainty_relative": True, "threshold": list(range(1, 11, 1))}},
        "ave_pr_val_n40e": {"unc": {"uncertainty_relative": True, "threshold": list(range(1, 11, 1))}},
        "ave_ts_val_n30e": {"unc": {"uncertainty_relative": False, "threshold": [k / 100 for k in list(range(1, 11))]}},
        "ave_ts_val_n34e": {"unc": {"uncertainty_relative": False, "threshold": [k / 100 for k in list(range(1, 11))]}},
        "ave_ts_val_n40e": {"unc": {"uncertainty_relative": False, "threshold": [k / 100 for k in list(range(1, 11))]}},
        "ske_pr_ano_n30e": {
            "unc": {"uncertainty_relative": False, "threshold": [k / 100 for k in list(range(5, 51, 5))]}},
        "ske_pr_ano_n34e": {
            "unc": {"uncertainty_relative": False, "threshold": [k / 100 for k in list(range(5, 51, 5))]}},
        "ske_pr_ano_n40e": {
            "unc": {"uncertainty_relative": False, "threshold": [k / 100 for k in list(range(5, 51, 5))]}},
        "ske_ts_ano_n30e": {
            "unc": {"uncertainty_relative": False, "threshold": [k / 100 for k in list(range(5, 51, 5))]}},
        "ske_ts_ano_n34e": {
            "unc": {"uncertainty_relative": False, "threshold": [k / 100 for k in list(range(5, 51, 5))]}},
        "ske_ts_ano_n40e": {
            "unc": {"uncertainty_relative": False, "threshold": [k / 100 for k in list(range(5, 51, 5))]}},
        "var_pr_ano_n30e": {"unc": {"uncertainty_relative": True, "threshold": list(range(5, 51, 5))}},
        "var_pr_ano_n34e": {"unc": {"uncertainty_relative": True, "threshold": list(range(5, 51, 5))}},
        "var_pr_ano_n40e": {"unc": {"uncertainty_relative": True, "threshold": list(range(5, 51, 5))}},
        "var_ts_ano_n30e": {"unc": {"uncertainty_relative": True, "threshold": list(range(5, 51, 5))}},
        "var_ts_ano_n34e": {"unc": {"uncertainty_relative": True, "threshold": list(range(5, 51, 5))}},
        "var_ts_ano_n40e": {"unc": {"uncertainty_relative": True, "threshold": list(range(5, 51, 5))}},
    },
    #
    # -- Required Ensemble size
    #
    # maximum ensemble size
    "res_maximum": 10000,
}
# ---------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------------------------------------------------------------------------#
# Main
# ---------------------------------------------------------------------------------------------------------------------#
def z01_print_res(
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
        res_maximum: int = default["res_maximum"],
        uncertainty_combinations: int = default["uncertainty_combinations"],
        uncertainty_confidence_interval: float = default["uncertainty_confidence_interval"],
        uncertainty_resamples: int = default["uncertainty_resamples"],
        uncertainty_threshold: dict = default["uncertainty_threshold"],
        **kwargs):
    #
    # -- Read json
    #
    values, metadata = data_organize_json(
        data_diagnostics, data_epoch_lengths, data_projects, data_experiments, data_mme_create=data_mme_create,
        data_mme_use_all_smiles=data_mme_use_all_smiles, data_mme_use_smile_mean=data_mme_use_smile_mean,
        data_smile_minimum_size=data_smile_minimum_size, data_smile_rejected=data_smile_rejected,
        data_smile_require_all_experiments=data_smile_require_all_experiments)
    print("data_organize_json", sorted(list(values.keys()), key=str.casefold))
    #
    # -- Define thresholds for each method
    #
    values, thresholds = nest_define_uncertainty_threshold(values, uncertainty_threshold)
    print("nest_define_uncertainty_threshold", sorted(list(thresholds.keys()), key=str.casefold))
    #
    # -- Compute required ensemble size (RES) to reach an uncertainty smaller than the desired ones
    #
    res_theory, _, _ = nest_compute_res(
        values, thresholds, res_maximum, uncertainty_confidence_interval, "normal",
        uncertainty_combinations, uncertainty_resamples, True)
    print("nest_compute_res", sorted(list(res_theory.keys()), key=str.casefold))
    #
    # -- Print
    #
    for dia in list(res_theory.keys()):
        for dur in list(res_theory[dia].keys()):
            for pro in list(res_theory[dia][dur].keys()):
                for exp in list(res_theory[dia][dur][pro].keys()):
                    print("diagnostic: " + str(dia))
                    print("epoch length: " + str(dur))
                    print("project: " + str(pro))
                    print("experiment: " + str(exp))
                    print("datasets:")
                    for dat in list(res_theory[dia][dur][pro][exp].keys()):
                        print(dat)
                    print("required ensemble size")
                    print("relative uncertainty: " + str(uncertainty_threshold[dia]["unc"]["uncertainty_relative"]))
                    for thr in uncertainty_threshold[dia]["unc"]["threshold"]:
                        print("threshold: " + str(thr))
                        for dat in list(res_theory[dia][dur][pro][exp].keys()):
                            for epo in list(res_theory[dia][dur][pro][exp][dat].keys()):
                                for method in list(res_theory[dia][dur][pro][exp][dat][epo].keys()):
                                    print(res_theory[dia][dur][pro][exp][dat][epo][method][thr])
    # diagnostic, epoch_length, project, experiment, dataset, epoch, method
    # "uncertainty_threshold": {
    #     "ave_pr_val_n30e": {"unc": {"uncertainty_relative": True, "threshold": list(range(5, 101, 5))}},
    #     "ave_ts_val_n30e": {"unc": {"uncertainty_relative": True, "threshold": [k / 10 for k in list(range(1, 11))]}},
    #     "ske_pr_ano_n30e": {"unc": {"uncertainty_relative": True, "threshold": list(range(5, 101, 5))}},
    #     "ske_ts_ano_n30e": {"unc": {"uncertainty_relative": True, "threshold": list(range(5, 101, 5))}},
    #     "var_pr_ano_n30e": {"unc": {"uncertainty_relative": True, "threshold": list(range(5, 101, 5))}},
    #     "var_ts_ano_n30e": {"unc": {"uncertainty_relative": True, "threshold": list(range(5, 101, 5))}},
    # },
# ---------------------------------------------------------------------------------------------------------------------#
