# -*- coding:UTF-8 -*-
# ---------------------------------------------------------------------------------------------------------------------#
# Main script to execute scripts for the paper about estimating_uncertainties_in_simulated_ENSO submitted to JAMES
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
    "f2": fig.f02_ensemble_size,
    "f3": fig.f03_epoch_length,
    "f4": fig.f04_hi_vs_pi,
    "f5": fig.f05_required_ensemble_size,
    "s1": fig.s01_quality_control,
    "s2": fig.s02_creating_distributions,
    "s3": fig.s03_theory_vs_bootstrap,
    "s4": fig.s04_epoch_length,
    "s5": fig.s05_theory_vs_bootstrap,
}
figure_calling_names = ", ".join(figure_scripts.keys())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    figure_number = input("Which figure do you want to plot?\n     Please enter one of: %s\n" % figure_calling_names)
    while figure_number not in list(figure_scripts.keys()):
        figure_number = input("Given value %s does not correspond to a figure\n     Please enter one of: %s\n" % (
            figure_number, figure_calling_names))
    figure_scripts[figure_number]()
