# -*- coding:UTF-8 -*-
# ---------------------------------------------------------------------------------------------------------------------#
# Main program to analyze data for the paper about estimating_uncertainties_in_simulated_ENSO submitted to JAMES
# ---------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------#
# Import packages
# ---------------------------------------------------#
# estimating_uncertainties_enso package
import estimating_uncertainties_enso.figure_scripts as fig
# ---------------------------------------------------#

# collect the figure scripts
figure_scripts = {
    "f1": fig.f01_model_uncertainties,
    "f2": fig.f02_creating_distributions,
    "f3": fig.f03_ensemble_size,
    "f4": fig.f04_epoch_length,
    "f5": fig.f05_hi_vs_pi,
    "f6": fig.f06_required_ensemble_size,
    "s1": fig.s01_quality_control,
    "s2": fig.s02_theory_vs_bootstrap,
    "s3": fig.s03_ensemble_size_mpi,
    "s4": fig.s04_epoch_length_ensemble_size,
    "s5": fig.s05_epoch_length_pi,
    "s6": fig.s06_theory_vs_bootstrap,
    "r7": fig.r07_departure_from_theory,
    "r8": fig.r08_ensemble_mea_vs_std,
    "r9": fig.r09_mean_mean_vs_variance,
    "r14": fig.r14_epoch_length_detrending,
    "z1": fig.z01_print_res,
}
figure_calling_names = ", ".join(figure_scripts.keys())

# Each figure requires a set of keywords that you can modify (see each script for details).
# One of the main claim of the paper is that you can use the standard error equation to compute the uncertainty of the
# ensemble mean instead of a bootstrap (random sampling).
# You can create figures 3, 4, 5, 6 and S3 using the theory or a bootstrap by setting the keyword 'uncertainty_theory'
# to True or False.
# Creating the figures using the default number of combinations (theory; 10,000) or resamples (bootstrap; 1,000,000) can
# take a very long time. To do a quick test we recommend to use smaller values.
user_defined_parameters = {
    # list of diagnostics: list[str]
    # "data_diagnostics": ["ave_pr_val_n40e", "ave_pr_val_n34e", "ave_pr_val_n30e",
    #                      "var_pr_ano_n40e", "var_pr_ano_n34e", "var_pr_ano_n30e",
    #                      "ske_pr_ano_n40e", "ske_pr_ano_n34e", "ske_pr_ano_n30e"],
    # "data_diagnostics": ["ave_ts_val_n40e", "ave_ts_val_n34e", "ave_ts_val_n30e",
    #                      "var_ts_ano_n40e", "var_ts_ano_n34e", "var_ts_ano_n30e",
    #                      "ske_ts_ano_n40e", "ske_ts_ano_n34e", "ske_ts_ano_n30e"],
    # "data_diagnostics": ["ave_tx_val_n40e", "ave_tx_val_n34e", "ave_tx_val_n30e",
    #                      "var_tx_ano_n40e", "var_tx_ano_n34e", "var_tx_ano_n30e",
    #                      "ske_tx_ano_n40e", "ske_tx_ano_n34e", "ske_tx_ano_n30e"],
    # "data_diagnostics": ["ave_ty_val_n40e", "ave_ty_val_n34e", "ave_ty_val_n30e",
    #                      "var_ty_ano_n40e", "var_ty_ano_n34e", "var_ty_ano_n30e",
    #                      "ske_ty_ano_n40e", "ske_ty_ano_n34e", "ske_ty_ano_n30e"],
    # compute uncertainty based on theory (or bootstrap): True, False
    "uncertainty_theory": True,
    # compute relative uncertainty (or absolute): True, False
    "uncertainty_relative": False,
    # confidence interval of the uncertainty: float [0, 100]
    "uncertainty_confidence_interval": 95,
    # maximum number of combinations used if uncertainty_theory is True and smile_size > sample_size: int [10, 1e10]
    "uncertainty_combinations": 10000,
    # "uncertainty_combinations": 1000,
    # number of resamples used for the bootstrap if uncertainty_theory is False: int [10, 1e10]
    "uncertainty_resamples": 1000000,
    # "uncertainty_resamples": 10000,
    # if you changed any default parameter, you should create your own axis ticks for the figure or pass an empty
    # dictionary (i.e., fig_ticks = {}). To create your own axis ticks, the general structure is:
    # fig_ticks = {"x_axis": {"diagnostic_1": []}, "y_axis": {"diagnostic_1": []}}
    # "fig_ticks": {},
    # something added to figure name to make it different from the standard name: str
    # "fig_name_add": "_pr",
}

if __name__ == '__main__':
    figure_number = input("Which figure do you want to plot?\n     Please enter one of: %s\n" % figure_calling_names)
    while figure_number not in list(figure_scripts.keys()):
        figure_number = input("Given value %s does not correspond to a figure\n     Please enter one of: %s\n" % (
            figure_number, figure_calling_names))
    figure_scripts[figure_number](**user_defined_parameters)
