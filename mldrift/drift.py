import numpy as np
import pandas as pd
from scipy.stats import ks_2samp

def compute_psi(expected: pd.Series, actual: pd.Series, buckets: int = 10) -> float:
    def scale_range(series, min_val, max_val):
        return (series - min_val) / (max_val - min_val)

    min_val = min(expected.min(), actual.min())
    max_val = max(expected.max(), actual.max())
    expected_scaled = scale_range(expected, min_val, max_val)
    actual_scaled = scale_range(actual, min_val, max_val)
    
    breakpoints = np.linspace(0, 1, buckets + 1)
    expected_percents = np.histogram(expected_scaled, bins=breakpoints)[0] / len(expected)
    actual_percents = np.histogram(actual_scaled, bins=breakpoints)[0] / len(actual)

    psi = np.sum((expected_percents - actual_percents) * np.log((expected_percents + 1e-6) / (actual_percents + 1e-6)))
    return psi

def compute_ks(expected: pd.Series, actual: pd.Series):
    return ks_2samp(expected.dropna(), actual.dropna())
