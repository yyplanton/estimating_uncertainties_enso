[back to README](../README.md)

## 3. Can piControl be used to estimate historical ensemble size?
The uncertainty of the ensemble mean is generally similar when computed with an historical ensemble and the corresponding piControl experiment.  
This remains true for other epoch lengths: [30](f5_tx_fbk_030.md), [45](f5_tx_fbk_045.md), [60](f5_tx_fbk_060.md), [75](f5_tx_fbk_075.md)-year epochs  
and other variables:  
Net Surface Heat flux: [30](f5_hf_030.md), [45](f5_hf_045.md), [60](f5_hf_060.md), [75](f5_hf_075.md), [90](f5_hf_090.md)-year epochs  
NHF regressed on SST: [30](f5_hf_fbk_030.md), [45](f5_hf_fbk_045.md), [60](f5_hf_fbk_060.md), [75](f5_hf_fbk_075.md), [90](f5_hf_fbk_090.md)-year epochs  
PR: [30](f5_pr_030.md), [45](f5_pr_045.md), [60](f5_pr_060.md), [75](f5_pr_075.md), [90](f5_pr_090.md)-year epochs  
Sea Surface Height: [30](f5_sl_030.md), [45](f5_sl_045.md), [60](f5_sl_060.md), [75](f5_sl_075.md), [90](f5_sl_090.md)-year epochs  
SST regressed on SSH: [30](f5_sl_fbk_030.md), [45](f5_sl_fbk_045.md), [60](f5_sl_fbk_060.md), [75](f5_sl_fbk_075.md), [90](f5_sl_fbk_090.md)-year epochs  
SST: [30](f5_ts_030.md), [45](f5_ts_045.md), [60](f5_ts_060.md), [75](f5_ts_075.md), [90](f5_ts_090.md)-year epochs  
Taux: [30](f5_tx_030.md), [45](f5_tx_045.md), [60](f5_tx_060.md), [75](f5_tx_075.md), [90](f5_tx_090.md)-year epochs  
Tauy: [30](f5_ty_030.md), [45](f5_ty_045.md), [60](f5_ty_060.md), [75](f5_ty_075.md), [90](f5_ty_090.md)-year epochs  


- project: CMIP6

- experiments: piControl, historical

- epoch length: 90-year

- regions: Niño4 (5N-5S, 160E-150W), Niño3.4 (5N-5S, 120-170W), Niño3 (5N-5S, 90-150W)

- variable: Taux regressed on SST (seasonal cycle removed)

- statistics: correlation, slope

Computed using equation (9) from Planton et al. ([preprint](https://doi.org/10.22541/essoar.170196744.48068128/v1))


<iframe src="f05_uncertainty_hi_vs_pi_tx_fbk_090_year_epoch.pdf" width="100%" height="500" frameborder="0" />

