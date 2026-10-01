"""
Streamlit dashboard application for the Conversion A/B Testing Simulator.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from config import (
    RANDOM_SEED,
    DEFAULT_DAYS,
    DEFAULT_CONTROL_RATE,
    DEFAULT_VARIANT_RATE,
    DEFAULT_MIN_VISITORS,
    DEFAULT_MAX_VISITORS,
    ALPHA,
)
from generate_data import generate_ab_test_data
from analysis import summarize_experiment

# Page Configuration
st.set_page_config(
    page_title="Conversion A/B Testing Simulator",
    page_icon="📊",
    layout="wide",
)

# Sidebar Controls
st.sidebar.header("⚙️ Simulation Controls")
random_seed = st.sidebar.number_input("Random Seed", value=RANDOM_SEED, step=1)
control_rate = st.sidebar.slider(
    "Control Baseline Rate", 0.01, 0.20, DEFAULT_CONTROL_RATE, 0.005, format="%.3f"
)
variant_rate = st.sidebar.slider(
    "Variant Baseline Rate", 0.01, 0.20, DEFAULT_VARIANT_RATE, 0.005, format="%.3f"
)
min_v = st.sidebar.number_input("Min Daily Visitors", value=DEFAULT_MIN_VISITORS, step=50)
max_v = st.sidebar.number_input("Max Daily Visitors", value=DEFAULT_MAX_VISITORS, step=50)
days = st.sidebar.number_input("Simulation Days", value=DEFAULT_DAYS, min_value=7, max_value=30, step=1)

# Generate Dataset based on Sidebar inputs
try:
    df = generate_ab_test_data(
        days=int(days),
        control_base_rate=control_rate,
        variant_base_rate=variant_rate,
        min_visitors=int(min_v),
        max_visitors=int(max_v),
        seed=int(random_seed),
    )
except Exception as e:
    st.error(f"Data Generation Error: {e}")
    st.stop()

# Run Analysis
stats = summarize_experiment(df, alpha=ALPHA)

# Dashboard Header
st.title("📊 Conversion A/B Testing Simulator")
st.markdown("### 14-Day Statistical Analysis of Control vs Variant Website Designs")
st.markdown(
    "This interactive dashboard simulates visitor traffic and sign-up conversions over a 14-day period, "
    "evaluating design performance using rigorous statistical hypothesis testing (Two-Proportion Z-Test)."
)
st.markdown("---")

# KPI Metric Cards
st.markdown("### 📈 Key Performance Indicators")
col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric("Control Rate", f"{stats['control_rate']*100:.2f}%")
col2.metric("Variant Rate", f"{stats['variant_rate']*100:.2f}%")
col3.metric("Absolute Diff", f"{stats['absolute_difference_pp']:+.2f} pp")
col4.metric("Relative Lift", f"{stats['relative_lift']:+.1f}%")
col5.metric("P-Value", f"{stats['p_value']:.4f}")
sig_label = "Significant" if stats["is_significant"] else "Not Significant"
col6.metric("Statistical Result", sig_label)

st.markdown("---")

# Charts Section
col_left, col_right = st.columns(2)

with col_left:
    st.markdown("#### Daily Website Traffic")
    fig_traffic = px.line(
        df,
        x="date",
        y="visitors",
        color="group",
        markers=True,
        labels={"visitors": "Visitors", "date": "Date", "group": "Design Group"},
        template="plotly_white",
    )
    fig_traffic.update_layout(margin=dict(t=20, b=20, l=20, r=20))
    st.plotly_chart(fig_traffic, use_container_width=True)

with col_right:
    st.markdown("#### Daily Conversion Rate")
    fig_cr = px.line(
        df,
        x="date",
        y="conversion_rate",
        color="group",
        markers=True,
        labels={"conversion_rate": "Conversion Rate", "date": "Date", "group": "Design Group"},
        template="plotly_white",
    )
    fig_cr.yaxis.tickformat = ".1%"
    fig_cr.update_layout(margin=dict(t=20, b=20, l=20, r=20))
    st.plotly_chart(fig_cr, use_container_width=True)

col_left_2, col_right_2 = st.columns(2)

with col_left_2:
    st.markdown("#### Daily Conversions")
    fig_conv = px.bar(
        df,
        x="date",
        y="conversions",
        color="group",
        barmode="group",
        labels={"conversions": "Conversions", "date": "Date", "group": "Design Group"},
        template="plotly_white",
    )
    fig_conv.update_layout(margin=dict(t=20, b=20, l=20, r=20))
    st.plotly_chart(fig_conv, use_container_width=True)

with col_right_2:
    st.markdown("#### Overall Conversion Rate Comparison")
    overall_df = pd.DataFrame(
        {
            "Group": ["Control", "Variant"],
            "Conversion Rate": [stats["control_rate"], stats["variant_rate"]],
        }
    )
    fig_bar = px.bar(
        overall_df,
        x="Group",
        y="Conversion Rate",
        color="Group",
        text_auto=".2%",
        template="plotly_white",
    )
    fig_bar.yaxis.tickformat = ".1%"
    fig_bar.update_layout(showlegend=False, margin=dict(t=20, b=20, l=20, r=20))
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

# Statistical Analysis Section
st.markdown("### 🔬 Statistical Analysis")
stat_table = pd.DataFrame(
    {
        "Metric / Parameter": [
            "Total Visitors",
            "Total Conversions",
            "Observed Conversion Rate",
            "Z-Statistic",
            "P-Value",
            "Significance Level (alpha)",
            "95% Confidence Interval (Diff)",
            "Statistical Conclusion",
        ],
        "Control (A)": [
            f"{stats['control_visitors']:,}",
            f"{stats['control_conversions']:,}",
            f"{stats['control_rate']*100:.2f}%",
            "-",
            "-",
            "-",
            "-",
            "-",
        ],
        "Variant (B)": [
            f"{stats['variant_visitors']:,}",
            f"{stats['variant_conversions']:,}",
            f"{stats['variant_rate']*100:.2f}%",
            f"{stats['z_statistic']:.4f}",
            f"{stats['p_value']:.4f}",
            f"{stats['alpha']}",
            f"[{stats['ci_lower']*100:.2f}%, {stats['ci_upper']*100:.2f}%]",
            sig_label,
        ],
    }
)
st.table(stat_table)

# Business Interpretation Section
st.markdown("### 💡 Business Interpretation")
if stats["is_significant"]:
    interp_text = (
        f"The Variant produced a higher observed conversion rate (**{stats['variant_rate']*100:.2f}%**) than "
        f"the Control (**{stats['control_rate']*100:.2f}%**), yielding an absolute difference of "
        f"**{stats['absolute_difference_pp']:+.2f} percentage points** and a relative lift of **{stats['relative_lift']:+.1f}%**. "
        f"Because the resulting p-value (**{stats['p_value']:.4f}**) is less than the significance threshold ($\alpha = {stats['alpha']}$), "
        f"the difference is **statistically significant**.\n\n"
        f"*Caveat:* While statistical significance confirms that the performance disparity is extremely unlikely to be due to random chance alone, "
        f"business teams should weigh implementation costs against the expected conversion lift before rolling out the redesign universally."
    )
else:
    interp_text = (
        f"The Variant produced an observed conversion rate of **{stats['variant_rate']*100:.2f}%** compared to "
        f"**{stats['control_rate']*100:.2f}%** for Control (absolute difference: **{stats['absolute_difference_pp']:+.2f} pp**, "
        f"relative lift: **{stats['relative_lift']:+.1f}%**). However, because the resulting p-value (**{stats['p_value']:.4f}**) "
        f"is greater than or equal to the significance threshold ($\alpha = {stats['alpha']}$), there is **insufficient statistical evidence** "
        f"to reject the null hypothesis.\n\n"
        f"*Caveat:* This does not guarantee that the designs are identical; rather, it indicates that current sample sizes and variance "
        f"do not allow us to rule out random variation as the cause of the observed difference."
    )
st.info(interp_text)

# Raw Data Expander
with st.expander("📄 View Raw Dataset"):
    st.dataframe(df, use_container_width=True)
    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download CSV Dataset",
        data=csv_data,
        file_name="ab_test_data.csv",
        mime="text/csv",
    )

# Methodology Expander
with st.expander("📚 Methodology & Statistical Guide"):
    st.markdown(
        """
        - **What is A/B Testing?** A controlled experiment comparing two versions (Control vs Variant) to determine which performs better.
        - **Conversion Rate:** Calculated as $\\text{Conversions} / \\text{Visitors}$.
        - **Null Hypothesis ($H_0$):** $p_{\\text{control}} = p_{\\text{variant}}$ (No underlying difference).
        - **P-Value Explanation:** The probability of observing a test statistic as extreme as (or more extreme than) the observed value, assuming the null hypothesis is true.
        - **Two-Proportion Z-Test:** Evaluates whether two population proportions differ significantly using a pooled proportion estimate.
        """
    )