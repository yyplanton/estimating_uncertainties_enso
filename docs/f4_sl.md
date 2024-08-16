[back to README](../README.md)

## 2. What is the influence of epoch length?
The uncertainty of the ensemble mean should decrease with the square root of the number of independent time steps. There are large inter-model differences.
This remains true for other variables: [Net Surface Heat flux](f4_hf.md), [NHF regressed on SST](f4_hf_fbk.md), [PR](f4_pr.md), [SST regressed on SSH](f4_sl_fbk.md), [SST](f4_ts.md), [Taux](f4_tx.md), [Taux regressed on SST](f4_tx_fbk.md), [Tauy](f4_ty.md)  


- project: CMIP6

- experiment: historical

- epoch lengths: 30, 45, 60, 75, 90, 105, 120, 135, 150-year

- regions: Niño4 (5N-5S, 160E-150W), Niño3.4 (5N-5S, 120-170W), Niño3 (5N-5S, 90-150W)

- variable: Sea Surface Height (seasonal cycle removed for variance and skewness)

- statistics: mean, variance, skewness

Computed using equation (9) from Planton et al. ([preprint](https://doi.org/10.22541/essoar.170196744.48068128/v1))


<iframe src="f04_uncertainty_vs_epoch_length_sl.pdf" width="100%" height="500" frameborder="0" />

