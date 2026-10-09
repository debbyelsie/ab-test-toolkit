# A/B Test Toolkit

A free web tool to plan, sanity-check, and analyze any two-group A/B test on a yes/no metric (conversion, signup, retention, purchase), with no code required.

## Features
- **Sample size calculator**: enter baseline rate, minimum detectable lift, and daily traffic to get users needed and test duration
- **SRM checker**: chi-square test to flag sample ratio mismatch between planned and observed group sizes
- **Results analyzer** (in progress): upload any CSV, pick your group and outcome columns, and get z-tests, confidence intervals, a bootstrap chart, and a plain-English recommendation

## Planned
- Continuous metrics (e.g. revenue per user) with t-tests
- Tests with more than two variants

## Run locally
    pip install -r requirements.txt
    streamlit run app.py

## Tests
    python -m pytest
