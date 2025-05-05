import pandas as pd
from mldrift.drift import compute_psi, compute_ks

def test_drift_functions():
    train = pd.Series([1, 2, 3, 4, 5])
    test = pd.Series([2, 3, 4, 5, 6])
    
    psi = compute_psi(train, test)
    ks_stat, ks_p = compute_ks(train, test)
    
    assert isinstance(psi, float)
    assert 0 <= ks_p <= 1
