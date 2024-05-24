[back to README](../README.md)

## 1. What is the influence of ensemble size?
The uncertainty of the ensemble mean decreases with the square root of the ensemble size.


- project: CMIP6

- experiments: piControl, historical

- epoch lengths: 30, 45, 60, 75, 90, 105, 120, 135, 150-year

- regions: Niño4 (5N-5S, 160E-150W), Niño3.4 (5N-5S, 120-170W), Niño3 (5N-5S, 90-150W)

- variable: SST (seasonal cycle removed for variance and skewness)

- statistics: mean, variance, skewness

Computed using equation (9) from Planton et al. ([preprint](https://doi.org/10.22541/essoar.170196744.48068128/v1))


<iframe src="f03_uncertainty_vs_ensemble_size_ts.pdf" width="100%" height="500" frameborder="0" />
