# -*- coding:UTF-8 -*-
# ---------------------------------------------------------------------------------------------------------------------#
# Figure 1 of the paper about estimating_uncertainties_in_simulated_ENSO submitted to JAMES
# Plot: presentation of uncertainty of the ensemble mean
# ---------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------#
# Import packages
# ---------------------------------------------------#
# ENSO_simulation_uncertainties package
from . params import default_parameters
from estimating_uncertainties_enso.compute_lib.data_lib import data_organize_json, data_organize_netcdf
from estimating_uncertainties_enso.compute_lib.tool_lib import tool_put_in_dict
from estimating_uncertainties_enso.figure_templates.fig_template import fig_presentation_uncertainties
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
    "data_experiments": ["historical"],
    # create the MME: True, False
    "data_mme_create": True,
    # MME made with all available SMILEs (or 1st SMILE of each model): True, False
    "data_mme_use_all_smiles": default_parameters["data_mme_use_all_smiles"],
    # MME made with ensemble means (or 1st member of each SMILE): True, False
    "data_mme_use_smile_mean": default_parameters["data_mme_use_smile_mean"],
    # dictionary of desired observational datasets per diagnostic
    "data_observations_desired": default_parameters["data_observations_desired"],
    # list of rejected SMILEs
    "data_smile_rejected": default_parameters["data_smile_rejected"],
    #
    # -- Figure
    #
    # SMILE to plot as a boxplot
    "fig_smile_selected": default_parameters["fig_smile_selected"],
    # figure format: eps, pdf, png, svg
    "fig_format": default_parameters["fig_format"],
    # figure name includes input parameters (may create a very long figure name)
    "fig_detailed_name": False,
    # figure orientation: column (column = variables, row = statistics), row  (column = statistics, row = statistics)
    "fig_orientation": default_parameters["fig_orientation"],
    # position of the legend on the plot: bottom, right
    "fig_legend_position": default_parameters["fig_legend_position"],
    # size of each panel
    "fig_panel_size": {
        "x_delt_box": 4, "x_frac_box": 0.25, "x_size_box": 6, "y_delt_box": 2, "y_frac_box": 0.25, "y_size_box": 12,
        "x_delt_map": 3, "x_size_map": 32, "y_size_map": 8,
    },
    # color per dataset
    "fig_colors": {
        **default_parameters["fig_colorbars"],
        **default_parameters["fig_colors"],
    },
    # linestyle per experiment
    "fig_linestyle": "-",
    # linewidth: all lines have the same width
    "fig_linewidth": 3.,
    # ranges
    "fig_ranges": {
        "x_axis": list(range(0, 2)),
        # boxplot
        "ave_pr_val_n30e": [round(k / 10, 1) for k in list(range(4, 41, 9))],
        "ave_ts_val_n30e": [round(k / 10, 1) for k in list(range(242, 275, 8))],
        "ske_pr_ano_n30e": [round(k / 10, 1) for k in list(range(0, 57, 14))],
        "ske_ts_ano_n30e": [round(k / 10, 1) for k in list(range(-10, 11, 5))],
        "var_pr_ano_n30e": [round(k / 10, 1) for k in list(range(1, 98, 24))],
        "var_ts_ano_n30e": [round(k / 10, 1) for k in list(range(2, 39, 9))],
        # map
        "ave_pr_val": [round(k / 10, 1) for k in list(range(0, 101, 25))],
        "ave_ts_val": list(range(22, 31, 2)),
        "ske_pr_ano": list(range(-6, 7, 3)),
        "ske_ts_ano": list(range(-2, 3, 1)),
        "var_pr_ano": list(range(0, 17, 4)),
        "var_ts_ano": [round(k / 10, 1) for k in list(range(0, 17, 4))],
    },
    # titles
    "fig_titles": default_parameters["fig_titles"],
    # panel parameters (to modify default values of fig_panel.py)
    "panel_param_box": {"x_lab_rot": 20, "x_nbr_minor": 0},
    "panel_param_map": {"title_row_x": 30},
}
# ---------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------------------------------------------------------------------------#
# Main
# ---------------------------------------------------------------------------------------------------------------------#
def f01_model_uncertainties(data_diagnostics: list = default["data_diagnostics"],
                            data_epoch_lengths: list = default["data_epoch_lengths"],
                            data_projects: list = default["data_projects"],
                            data_experiments: list = default["data_experiments"],
                            data_mme_create: bool = default["data_mme_create"],
                            data_mme_use_all_smiles: bool = default["data_mme_use_all_smiles"],
                            data_mme_use_smile_mean: bool = default["data_mme_use_smile_mean"],
                            data_observations_desired: dict = default["data_observations_desired"],
                            data_smile_rejected: list = default["data_smile_rejected"],
                            fig_colors: dict = default["fig_colors"],
                            fig_detailed_name: bool = default["fig_detailed_name"],
                            fig_format: str = default["fig_format"],
                            fig_legend_position: str = default["fig_legend_position"],
                            fig_linestyle: str = default["fig_linestyle"],
                            fig_linewidth: float = default["fig_linewidth"],
                            fig_orientation: str = default["fig_orientation"],
                            fig_panel_size: dict = default["fig_panel_size"],
                            fig_ranges: dict = default["fig_ranges"],
                            fig_smile_selected: str = default["fig_smile_selected"],
                            fig_titles: dict = default["fig_titles"],
                            panel_param_box: dict = default["panel_param_box"],
                            panel_param_map: dict = default["panel_param_map"]):
    #
    # -- Read json
    #
    values, metadata = data_organize_json(
        data_diagnostics, data_epoch_lengths, data_projects, data_experiments, data_mme_create=data_mme_create,
        data_mme_use_all_smiles=data_mme_use_all_smiles, data_mme_use_smile_mean=data_mme_use_smile_mean,
        data_observations_desired=data_observations_desired, data_smile_rejected=data_smile_rejected)
    #
    # -- Read netCDF
    #
    list_dia = [k[:-5] for k in data_diagnostics]
    dict_obs = dict((k[:-5], data_observations_desired[k]) for k in data_diagnostics)
    map_values, map_metadata = data_organize_netcdf(
        list_dia, ["observations"], ["historical"], data_observations_desired=dict_obs)
    #
    # -- Organize data for plot
    #
    maps_and_boxplots = {}
    for dia in list(values.keys()):
        for dur in list(values[dia].keys()):
            for pro in list(values[dia][dur].keys()):
                for exp in list(values[dia][dur][pro].keys()):
                    for dat in list(values[dia][dur][pro][exp].keys()):
                        # select last epoch
                        epo = sorted(list(values[dia][dur][pro][exp][dat].keys()), key=str.casefold)[-1]
                        # array
                        array = values[dia][dur][pro][exp][dat][epo]
                        # organize values
                        if pro == "observations" and dat in data_observations_desired[dia]:
                            maps_and_boxplots = tool_put_in_dict(maps_and_boxplots, array, dia, "curve", dat)
                            maps_and_boxplots = tool_put_in_dict(
                                maps_and_boxplots, map_values[dia[:-5]][pro][exp][dat], dia, "map", dat)
                        elif dat == "MME--" + str(pro).upper() or dat == fig_smile_selected:
                            maps_and_boxplots = tool_put_in_dict(maps_and_boxplots, array, dia, "boxplot", dat)
    #
    # -- Figure
    #
    # output figure name will be the file name (path removed and extension removed)
    fig_name = __file__.split("/")[-1].split(".")[0]
    if fig_detailed_name is True:
        # add details of the computation to the figure name
        fig_name += "_data_" + str(len(data_projects)) + "pro_" + str(len(data_experiments)) + "exp_" + \
                    str(len(data_diagnostics)) + "dia"
        if data_mme_create is True:
            fig_name += "_mme"
            fig_name += "_of_em" if data_mme_use_smile_mean is True else "_of_1m"
            fig_name += "_all_smile" if data_mme_use_all_smiles is True else "_1st_smile"
        fig_name += "_" + str(fig_orientation)
    fig_presentation_uncertainties(maps_and_boxplots, map_metadata, data_diagnostics, fig_format, fig_name, fig_colors,
                                   fig_legend_position, fig_linestyle, fig_linewidth, fig_orientation, fig_panel_size,
                                   fig_ranges, fig_titles, panel_param_box=panel_param_box,
                                   panel_param_map=panel_param_map)
    return
