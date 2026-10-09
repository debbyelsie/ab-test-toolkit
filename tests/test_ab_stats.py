from ab_stats import sample_size_per_group, estimate_duration_days, srm_check

def test_known_sample_size():
    n = sample_size_per_group(0.10, 0.10)
    assert 14_700 <= n <= 14_800

def test_duration():
    assert estimate_duration_days(5_000, 1_000) == 10


def test_srm_cookie_cats_passes():
    result = srm_check([44_700, 45_489])
    assert not result["srm_detected"]
    assert 0.005 < result["p_value"] < 0.01


def test_srm_detects_mismatch():
    result = srm_check([50_000, 48_000])
    assert result["srm_detected"]