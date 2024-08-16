[back to README](../README.md)

## 1. What is the influence of ensemble size?
The uncertainty of the ensemble mean decreases with the square root of the ensemble size.
This remains true for other variables: [Net Surface Heat flux](f3_hf.md), [NHF regressed on SST](f3_hf_fbk.md), [PR](f3_pr.md), [Sea Surface Height](f3_sl.md), [SST](f3_ts.md), [Taux](f3_tx.md), [Taux regressed on SST](f3_tx_fbk.md), [Tauy](f3_ty.md)  


- project: CMIP6

- experiments: piControl, historical

- epoch lengths: 30, 45, 60, 75, 90, 105, 120, 135, 150-year

- regions: Niño4 (5N-5S, 160E-150W), Niño3.4 (5N-5S, 120-170W), Niño3 (5N-5S, 90-150W)

- variable: SST regressed on SSH (seasonal cycle removed)

- statistics: correlation, slope

Computed using equation (9) from Planton et al. ([preprint](https://doi.org/10.22541/essoar.170196744.48068128/v1))


<iframe src="f03_uncertainty_vs_ensemble_size_sl_fbk.pdf" width="100%" height="500" frameborder="0" />

