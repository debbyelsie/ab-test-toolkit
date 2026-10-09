import math
from scipy.stats import norm, chisquare

def sample_size_per_group(baseline, mde_relative, alpha=0.05, power=0.8):
    """Users needed per group for a two-sided, two-proportion z-test."""
    p1 = baseline
    p2 = baseline * (1 + mde_relative)
    if not 0 < p2 < 1:
        raise ValueError("Baseline x (1 + lift) must be between 0% and 100%.")

    z_alpha = norm.ppf(1 - alpha / 2)
    z_beta = norm.ppf(power)
    p_bar = (p1 + p2) / 2

    numerator = (
        z_alpha * math.sqrt(2 * p_bar * (1 - p_bar))
        + z_beta * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))
    ) ** 2
    return math.ceil(numerator / (p2 - p1) ** 2)

def estimate_duration_days(n_per_group, daily_traffic, n_groups=2):
    """Days needed if all daily traffic is split evenly across groups."""
    return math.ceil(n_per_group * n_groups / daily_traffic)

def srm_check(observed_counts, expected_ratios=None, threshold=0.001):
    """Chi-square test for sample ratio mismatch."""
    if expected_ratios is None:
        expected_ratios = [1] * len(observed_counts)
    total = sum(observed_counts)
    ratio_sum = sum(expected_ratios)
    expected = [total * r / ratio_sum for r in expected_ratios]
    stat, p_value = chisquare(observed_counts, expected)
    return {
        "chi2": float(stat),
        "p_value": float(p_value),
        "srm_detected": bool(p_value < threshold),
        "expected": expected,
    }