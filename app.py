import streamlit as st
from ab_stats import sample_size_per_group, estimate_duration_days, srm_check

st.set_page_config(page_title="MEA A/B Test Toolkit", page_icon="🧪")
st.title("MEA A/B Test Toolkit")

tab_size, tab_srm, tab_results = st.tabs(["Sample size", "SRM check", "Analyze results"])

with tab_size:
    st.subheader("How many users do I need?")
    baseline = st.number_input("Baseline conversion rate (%)", 0.1, 99.9, 10.0, step=0.5) / 100
    mde = st.number_input("Minimum detectable lift (relative %)", 0.5, 500.0, 10.0, step=0.5) / 100
    traffic = st.number_input("Daily visitors entering the test", min_value=1, value=1000, step=100)

    with st.expander("Advanced settings"):
        alpha = st.select_slider("Significance level (α)", [0.01, 0.05, 0.10], value=0.05)
        power = st.select_slider("Power (1 − β)", [0.80, 0.85, 0.90, 0.95], value=0.80)

    try:
        n = sample_size_per_group(baseline, mde, alpha, power)
        days = estimate_duration_days(n, traffic)
        c1, c2, c3 = st.columns(3)
        c1.metric("Users per group", f"{n:,}")
        c2.metric("Total users", f"{2 * n:,}")
        c3.metric("Duration", f"{days} days")
        st.caption(
            f"To detect a lift from {baseline:.1%} to {baseline * (1 + mde):.2%} "
            f"with {power:.0%} power at α = {alpha}, run the test for about {days} days. "
            "Consider rounding up to full weeks to cover day-of-week effects."
        )
    except ValueError as e:
        st.error(str(e))

with tab_srm:
    st.subheader("Did traffic split the way you planned?")
    col_a, col_b = st.columns(2)
    control = col_a.number_input("Users in control", min_value=0, value=44_700, step=100)
    treatment = col_b.number_input("Users in treatment", min_value=0, value=45_489, step=100)
    planned = st.slider("Planned share in control (%)", 1, 99, 50)

    if control + treatment > 0:
        result = srm_check([control, treatment], [planned, 100 - planned])
        c1, c2, c3 = st.columns(3)
        c1.metric("Expected control", f"{result['expected'][0]:,.0f}")
        c2.metric("Chi-square", f"{result['chi2']:.2f}")
        c3.metric("p-value", f"{result['p_value']:.4f}")

        if result["srm_detected"]:
            st.error(
                "SRM detected (p < 0.001). The split is off from what you planned, "
                "so don't trust this test's results until you find out why "
                "(bugs in assignment, bot filtering, redirects, logging gaps)."
            )
        else:
            st.success(
                "No SRM detected. The observed split is consistent with your plan, "
                "so you can move on to analyzing results."
            )