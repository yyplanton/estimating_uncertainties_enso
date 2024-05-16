# Estimating uncertainty in simulated ENSO statistics

#### Paper [preprint](https://doi.org/10.22541/essoar.170196744.48068128/v1)

#### GitHub [repository](https://github.com/yyplanton/estimating_uncertainties_enso/)


## Project
To model the climate, scientists often generate an ensemble of simulations with a given climate model and given forcings (e.g., volcanic eruptions, greenhouse gas emissions) but different plausible initial conditions. These different initial conditions represent the uncertainties on the Earth’s climate conditions at the start of the simulation. As Earth’s climate naturally fluctuates on multiple timescales (‘internal variability’), each simulation of the ensemble represents a possible evolution of the climate. By averaging the climate over a large enough ensemble, one can separate the internal variability from forced changes (e.g., changes forced by greenhouse gas emissions). But what does ‘large enough’ means?  
This paper explores this question and provides a way to estimate the ensemble size depending on one's needs.  
First, two parameters reducing the influence of internal variability are analyzed: [ensemble size](#1-what-is-the-influence-of-ensemble-size) and [epoch length](#2-what-is-the-influence-of-epoch-length). Then piControl simulations (long unforced simulation) are compared to historical ensembles to check if the former can be used to estimate, *a priori*, the size of the latter: [piControl vs. historical](#3-can-piControl-be-used-to-estimate-historical-ensemble-size). Finally, several methods to estimate the ensemble size are presented: [estimating the ensemble size](#4-how-to-estimate-the-ensemble-size).

The codes in this [repository](https://github.com/yyplanton/estimating_uncertainties_enso/) are used to generate the figures for the [paper](https://doi.org/10.22541/essoar.170196744.48068128/v1).  
The climate data analysis was performed using the [CLIVAR ENSO Metrics Package](https://github.com/CLIVAR-PRP/ENSO_metrics) (Planton et al. [2021](https://doi.org/10.1175/BAMS-D-19-0337.1)) via the [PCMDI Metrics Package framework](https://github.com/PCMDI/pcmdi_metrics) (Lee et al., [2024](https://doi.org/10.5194/gmd-17-3919-2024)).  
These webpages present some key results of the paper as well as additional information.


## 1. What is the influence of ensemble size?<a id='1-what-is-the-influence-of-ensemble-size'></a>
According to theory, the uncertainty of the ensemble mean decreases with the square root of the ensemble size (equation 9 of Planton et al. [preprint](https://doi.org/10.22541/essoar.170196744.48068128/v1)).  
This is confirmed by our analysis: [PR](docs/f3_pr.md), [TS](docs/f3_ts.md), [Taux](docs/f3_tx.md), [Tauy](docs/f3_ty.md)


## 2. What is the influence of epoch length?<a id='2-what-is-the-influence-of-epoch-length'></a>
According to theory, if time series' distributions are normal and samples are independent, the uncertainty of the ensemble mean decreases with the square root of the number of time steps (equations 5, 6 and 7 of Planton et al. [preprint](https://doi.org/10.22541/essoar.170196744.48068128/v1)).  
On average the uncertainty reduces with increasing epoch length: [PR](docs/f4_pr.md), [TS](docs/f4_ts.md), [Taux](docs/f4_tx.md), [Tauy](docs/f4_ty.md)  
However there are large inter-model differences, linked to the non-normality of the distributions (see Figure 1 of Planton et al. [preprint](https://doi.org/10.22541/essoar.170196744.48068128/v1)) and the relatively small ensemble sizes (see Figure S3 of Planton et al. [preprint](https://doi.org/10.22541/essoar.170196744.48068128/v1)). Note that changing the epoch length generally does not change the uncertainty of the multi-model ensemble mean: increasing the epoch length does not reduce the inter-model differences.  


## 3. Can piControl be used to estimate historical ensemble size?<a id='3-can-piControl-be-used-to-estimate-historical-ensemble-size'></a>
The uncertainty of the ensemble mean is generally similar when computed with an historical ensemble and the corresponding piControl experiment: [PR](docs/f5_pr.md), [TS](docs/f5_ts.md), [Taux](docs/f5_tx.md), [Tauy](docs/f5_ty.md)  
This implies that the piControl experiment, which is computed before other experiment types, can be used to estimate *a priori* the size of the ensemble required to reduce the impact of internal variability and detect forced changes.


## 4. How to estimate the ensemble size?<a id='4-how-to-estimate-the-ensemble-size'></a>
Using the results of sections [1](#1-what-is-the-influence-of-ensemble-size) and [3](#3-can-piControl-be-used-to-estimate-historical-ensemble-size), we can use a very simple equation (equation 10 of Planton et al. [preprint](https://doi.org/10.22541/essoar.170196744.48068128/v1)) to estimate the ensemble size. One only need to measure the internal variability of a given statistic and decide of an acceptable level of uncertainty.  
Several methods to select an acceptable level of uncertainty are presented in Planton et al. [preprint](https://doi.org/10.22541/essoar.170196744.48068128/v1). Here we only provide ensemble size estimates for each model, several regions, variables, statistics and epoch lengths.

#### 30-year epochs

|  | PR | SST | Taux | Tauy |
| --- | --- | --- | --- | --- |
| mean | [Niño4](docs/res_ave_pr_val_n40e_030_year.md) [Niño3.4](docs/res_ave_pr_val_n34e_030_year.md) [Niño3](docs/res_ave_pr_val_n30e_030_year.md) | [Niño4](docs/res_ave_ts_val_n40e_030_year.md) [Niño3.4](docs/res_ave_ts_val_n34e_030_year.md) [Niño3](docs/res_ave_ts_val_n30e_030_year.md) | [Niño4](docs/res_ave_tx_val_n40e_030_year.md) [Niño3.4](docs/res_ave_tx_val_n34e_030_year.md) [Niño3](docs/res_ave_tx_val_n30e_030_year.md) | [Niño4](docs/res_ave_ty_val_n40e_030_year.md) [Niño3.4](docs/res_ave_ty_val_n34e_030_year.md) [Niño3](docs/res_ave_ty_val_n30e_030_year.md) |
| variance | [Niño4](docs/res_var_pr_ano_n40e_030_year.md) [Niño3.4](docs/res_var_pr_ano_n34e_030_year.md) [Niño3](docs/res_var_pr_ano_n30e_030_year.md) | [Niño4](docs/res_var_ts_ano_n40e_030_year.md) [Niño3.4](docs/res_var_ts_ano_n34e_030_year.md) [Niño3](docs/res_var_ts_ano_n30e_030_year.md) | [Niño4](docs/res_var_tx_ano_n40e_030_year.md) [Niño3.4](docs/res_var_tx_ano_n34e_030_year.md) [Niño3](docs/res_var_tx_ano_n30e_030_year.md) | [Niño4](docs/res_var_ty_ano_n40e_030_year.md) [Niño3.4](docs/res_var_ty_ano_n34e_030_year.md) [Niño3](docs/res_var_ty_ano_n30e_030_year.md) |
| skewness | [Niño4](docs/res_ske_pr_ano_n40e_030_year.md) [Niño3.4](docs/res_ske_pr_ano_n34e_030_year.md) [Niño3](docs/res_ske_pr_ano_n30e_030_year.md) | [Niño4](docs/res_ske_ts_ano_n40e_030_year.md) [Niño3.4](docs/res_ske_ts_ano_n34e_030_year.md) [Niño3](docs/res_ske_ts_ano_n30e_030_year.md) | [Niño4](docs/res_ske_tx_ano_n40e_030_year.md) [Niño3.4](docs/res_ske_tx_ano_n34e_030_year.md) [Niño3](docs/res_ske_tx_ano_n30e_030_year.md) | [Niño4](docs/res_ske_ty_ano_n40e_030_year.md) [Niño3.4](docs/res_ske_ty_ano_n34e_030_year.md) [Niño3](docs/res_ske_ty_ano_n30e_030_year.md) |


#### 60-year epochs

|  | PR | SST | Taux | Tauy |
| --- | --- | --- | --- | --- |
| mean | [Niño4](docs/res_ave_pr_val_n40e_060_year.md) [Niño3.4](docs/res_ave_pr_val_n34e_060_year.md) [Niño3](docs/res_ave_pr_val_n30e_060_year.md) | [Niño4](docs/res_ave_ts_val_n40e_060_year.md) [Niño3.4](docs/res_ave_ts_val_n34e_060_year.md) [Niño3](docs/res_ave_ts_val_n30e_060_year.md) | [Niño4](docs/res_ave_tx_val_n40e_060_year.md) [Niño3.4](docs/res_ave_tx_val_n34e_060_year.md) [Niño3](docs/res_ave_tx_val_n30e_060_year.md) | [Niño4](docs/res_ave_ty_val_n40e_060_year.md) [Niño3.4](docs/res_ave_ty_val_n34e_060_year.md) [Niño3](docs/res_ave_ty_val_n30e_060_year.md) |
| variance | [Niño4](docs/res_var_pr_ano_n40e_060_year.md) [Niño3.4](docs/res_var_pr_ano_n34e_060_year.md) [Niño3](docs/res_var_pr_ano_n30e_060_year.md) | [Niño4](docs/res_var_ts_ano_n40e_060_year.md) [Niño3.4](docs/res_var_ts_ano_n34e_060_year.md) [Niño3](docs/res_var_ts_ano_n30e_060_year.md) | [Niño4](docs/res_var_tx_ano_n40e_060_year.md) [Niño3.4](docs/res_var_tx_ano_n34e_060_year.md) [Niño3](docs/res_var_tx_ano_n30e_060_year.md) | [Niño4](docs/res_var_ty_ano_n40e_060_year.md) [Niño3.4](docs/res_var_ty_ano_n34e_060_year.md) [Niño3](docs/res_var_ty_ano_n30e_060_year.md) |
| skewness | [Niño4](docs/res_ske_pr_ano_n40e_060_year.md) [Niño3.4](docs/res_ske_pr_ano_n34e_060_year.md) [Niño3](docs/res_ske_pr_ano_n30e_060_year.md) | [Niño4](docs/res_ske_ts_ano_n40e_060_year.md) [Niño3.4](docs/res_ske_ts_ano_n34e_060_year.md) [Niño3](docs/res_ske_ts_ano_n30e_060_year.md) | [Niño4](docs/res_ske_tx_ano_n40e_060_year.md) [Niño3.4](docs/res_ske_tx_ano_n34e_060_year.md) [Niño3](docs/res_ske_tx_ano_n30e_060_year.md) | [Niño4](docs/res_ske_ty_ano_n40e_060_year.md) [Niño3.4](docs/res_ske_ty_ano_n34e_060_year.md) [Niño3](docs/res_ske_ty_ano_n30e_060_year.md) |
