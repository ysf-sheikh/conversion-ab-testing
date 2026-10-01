# Conversion A/B Testing

The project simulates a 14-day website experiment comparing an existing **Control** design against a redesigned **Variant**. It generates synthetic visitor and conversion data, calculates conversion metrics, performs a two-proportion Z-test, and presents the results through an interactive Streamlit dashboard.

The project is designed to demonstrate practical application of statistical hypothesis testing, data analysis, visualization, and business-oriented interpretation.

---

## Table of Contents

- [Overview](#overview)
- [Business Problem](#business-problem)
- [Objectives](#objectives)
- [Methodology](#methodology)
- [Statistical Approach](#statistical-approach)
- [Dataset](#dataset)
- [Dashboard](#dashboard)
- [Project Structure](#project-structure)
- [Technologies](#technologies)
- [Installation](#installation)
- [Usage](#usage)
- [Running the Tests](#running-the-tests)
- [Results](#results)
- [Interpretation](#interpretation)
- [Limitations](#limitations)
- [Reproducibility](#reproducibility)
- [Future Improvements](#future-improvements)
- [Author](#author)

---

## Overview

A/B testing is a controlled experimentation method used to compare two versions of a product, website, feature, or user experience.

In this project, two website designs are simulated:

- **Control (A):** The existing website design.
- **Variant (B):** A redesigned version of the website.

Synthetic traffic and conversion events are generated for both groups over a 14-day period. The resulting data is analyzed to determine whether the observed difference in conversion rates is statistically significant.

The project combines statistical analysis with an interactive dashboard so that the results can be explored without manually running individual analysis cells.

---

## Business Problem

Suppose a company is considering replacing its existing website design with a new version.

The redesigned website appears to generate more sign-ups during an initial experiment. However, a higher observed conversion rate does not automatically mean that the new design genuinely performs better.

Random variation can cause one group to perform better than another even when the underlying conversion rates are identical.

The purpose of an A/B test is therefore to determine whether the observed difference provides sufficient statistical evidence that the underlying conversion rates differ.

This project simulates that process using synthetic website traffic data.

---

## Objectives

The project was developed to:

1. Generate realistic synthetic website traffic for two experimental groups.
2. Simulate conversion events using a binomial distribution.
3. Calculate daily and overall conversion rates.
4. Compare Control and Variant performance.
5. Calculate absolute conversion-rate differences.
6. Calculate relative conversion-rate lift.
7. Perform a two-proportion Z-test.
8. Calculate the resulting p-value.
9. Calculate a 95% confidence interval for the difference in conversion rates.
10. Determine statistical significance using a 5% significance level.
11. Visualize traffic and conversion trends.
12. Provide an interactive Streamlit dashboard.
13. Make the entire experiment reproducible through a configurable random seed.
14. Provide automated tests for the core data and statistical calculations.

---

## Methodology

The simulation follows a simplified A/B testing workflow.

### 1. Experiment Design

The experiment contains two groups:

| Group   | Description             |
| ------- | ----------------------- |
| Control | Existing website design |
| Variant | Redesigned website      |

The default simulation runs for 14 days.

Each group receives a variable number of simulated visitors each day.

### 2. Traffic Generation

Daily visitor counts are generated within a configurable range.

The default configuration produces approximately 800–1,500 visitors per group per day.

The number of visitors varies between days to better represent natural fluctuations in website traffic.

### 3. Conversion Generation

Conversions are generated using a binomial distribution.

For each group:

```text
Conversions ~ Binomial(Visitors, Conversion Probability)
```

The default baseline conversion probabilities are approximately:

```text
Control: 8%
Variant: 10%
```

The exact observed conversion rates vary because the conversion events are randomly simulated.

### 4. Conversion Rate

The conversion rate is calculated as:

```text
Conversion Rate = Conversions / Visitors
```

The calculation is performed separately for each day and for the experiment as a whole.

### 5. Performance Comparison

The project calculates both:

- Absolute conversion-rate difference
- Relative conversion-rate lift

These metrics provide different perspectives on the observed performance difference.

---

## Statistical Approach

### Hypotheses

The project uses a two-sided two-proportion Z-test.

#### Null Hypothesis

```text
H0: p_control = p_variant
```

The underlying conversion rates of the two groups are equal.

#### Alternative Hypothesis

```text
H1: p_control != p_variant
```

The underlying conversion rates are different.

The significance level is:

```text
alpha = 0.05
```

### P-Value Interpretation

The p-value measures how compatible the observed difference is with the null hypothesis under the assumptions of the statistical test.

The decision rule used by the project is:

```text
p-value < 0.05
```

The observed difference is considered statistically significant at the 5% level.

```text
p-value >= 0.05
```

There is insufficient statistical evidence to conclude that the underlying conversion rates differ at the 5% level.

Statistical significance is not interpreted as proof that one website design is universally better. The observed effect size, experimental assumptions, and practical business impact should also be considered.

---

## Absolute Conversion Difference

The absolute difference is calculated as:

```text
Variant Conversion Rate - Control Conversion Rate
```

The result is reported in percentage points.

For example:

```text
Control: 8.0%
Variant: 10.0%

Absolute Difference: +2.0 percentage points
```

Percentage points and relative percentage increases are not interchangeable.

---

## Relative Conversion Lift

Relative lift is calculated as:

```text
((Variant Rate - Control Rate) / Control Rate) * 100
```

For example:

```text
Control: 8.0%
Variant: 10.0%

Relative Lift:
((10.0 - 8.0) / 8.0) * 100
= 25%
```

This means the Variant's observed conversion rate is 25% higher relative to the Control rate in this example.

---

## Confidence Interval

The project also calculates a 95% confidence interval for the difference between the two conversion proportions.

The confidence interval provides additional information about the estimated size and uncertainty of the observed difference.

It is presented alongside the hypothesis-test results rather than being treated as a replacement for the statistical test.

---

## Dataset

The dataset used by this project is **synthetically generated**.

No real customer information or personally identifiable information is used.

The simulation generates website visitors and conversion events using configurable parameters and a fixed random seed.

The generated dataset contains:

| Column            | Description                          |
| ----------------- | ------------------------------------ |
| `date`            | Date of the simulated experiment     |
| `group`           | Control or Variant                   |
| `visitors`        | Number of simulated website visitors |
| `conversions`     | Number of simulated sign-ups         |
| `conversion_rate` | Conversions divided by visitors      |

The dataset can be regenerated at any time using:

```bash
python generate_data.py
```

---

## Dashboard

The project includes an interactive Streamlit dashboard.

The dashboard provides:

### Key Performance Indicators

- Control conversion rate
- Variant conversion rate
- Absolute conversion-rate difference
- Relative conversion lift
- Z-statistic
- P-value
- Statistical significance result

### Visualizations

#### Daily Website Traffic

Displays the number of visitors received by the Control and Variant groups over the 14-day experiment.

#### Daily Conversion Rate

Shows how the conversion rates of both groups change over time.

#### Overall Conversion Rate

Provides a direct comparison between the overall Control and Variant conversion rates.

#### Daily Conversions

Displays the number of conversions generated by each group on each day.

### Statistical Analysis

The dashboard displays the underlying statistical calculations, including:

- Visitor counts
- Conversion counts
- Conversion rates
- Z-statistic
- P-value
- Significance threshold
- Confidence interval
- Statistical conclusion

### Raw Data

The dashboard also provides an expandable raw-data section and allows the generated dataset to be downloaded as a CSV file.

---

## Project Structure

```text
DS_10_ABTestingSimulator_BYTE/
│
├── app.py
├── generate_data.py
├── analysis.py
├── config.py
│
├── data/
│   └── ab_test_data.csv
│
├── screenshots/
│   ├── dashboard_overview.png
│   ├── traffic_chart.png
│   ├── conversion_chart.png
│   └── statistical_results.png
│
├── tests/
│   ├── __init__.py
│   ├── test_data_generation.py
│   └── test_analysis.py
│
├── README.md
├── requirements.txt
├── .gitignore
└── LICENSE
```

---

## Technologies

The project uses the following technologies:

| Technology | Purpose                                              |
| ---------- | ---------------------------------------------------- |
| Python     | Core programming language                            |
| Pandas     | Data manipulation and analysis                       |
| NumPy      | Numerical calculations and synthetic data generation |
| SciPy      | Statistical hypothesis testing                       |
| Plotly     | Interactive data visualizations                      |
| Streamlit  | Interactive dashboard                                |
| Pytest     | Automated testing                                    |
| Git        | Version control                                      |

---

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd DS_10_ABTestingSimulator_BYTE
```

Replace `<repository-url>` with the URL of this GitHub repository.

### 2. Create a Virtual Environment

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

On macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Usage

### Generate the Dataset

From the project root:

```bash
python generate_data.py
```

This generates the synthetic A/B testing dataset and saves it to:

```text
data/ab_test_data.csv
```

### Launch the Dashboard

Run:

```bash
streamlit run app.py
```

Streamlit will provide a local URL where the dashboard can be accessed.

---

## Running the Tests

The project uses Pytest for automated testing.

Run:

```bash
pytest
```

The tests verify the correctness of:

- Dataset generation
- Visitor and conversion constraints
- Conversion-rate calculations
- Lift calculations
- Statistical testing
- Significance decisions
- Dataset integrity

---

## Results

The results are generated dynamically from the synthetic experiment.

The primary metrics include:

| Metric                   | Description                                                      |
| ------------------------ | ---------------------------------------------------------------- |
| Control Conversion Rate  | Overall conversion rate of the Control group                     |
| Variant Conversion Rate  | Overall conversion rate of the Variant group                     |
| Absolute Difference      | Difference between the two conversion rates in percentage points |
| Relative Lift            | Relative change compared with Control                            |
| Z-Statistic              | Test statistic produced by the two-proportion Z-test             |
| P-Value                  | Statistical evidence against the null hypothesis                 |
| 95% Confidence Interval  | Estimated interval for the conversion-rate difference            |
| Statistical Significance | Whether the p-value is below α = 0.05                            |

Because the dataset is generated using a fixed random seed, the default experiment is reproducible.

---

## Interpretation

The project separates **statistical significance** from **practical significance**.

A statistically significant result indicates that the observed difference would be relatively unlikely under the null hypothesis, given the assumptions of the statistical test.

However, statistical significance does not automatically mean that the observed difference is commercially important.

For example, a very small conversion improvement could become statistically significant when a website receives a very large amount of traffic. Conversely, a potentially meaningful improvement may fail to reach statistical significance when the sample size is small.

For this reason, the dashboard reports:

- Conversion rates
- Absolute difference
- Relative lift
- P-value
- Confidence interval

together rather than relying on a single metric.

---

## Limitations

This project is a statistical simulation and therefore has several limitations.

### Synthetic Data

The dataset is generated rather than collected from an actual website.

The results should not be interpreted as evidence about real customer behavior.

### Simulated Experiment

The project does not perform actual random assignment of real users to experimental groups.

### No Revenue Analysis

The experiment measures sign-up conversions rather than revenue, customer lifetime value, retention, or other downstream business metrics.

### Statistical Assumptions

The validity of the two-proportion Z-test depends on assumptions related to the experimental design and sample size.

### No External Factors

Real-world experiments can be affected by factors such as:

- marketing campaigns
- seasonality
- device type
- geography
- traffic source
- returning users
- technical issues

These factors are not fully represented by this simulation.

### Statistical vs Practical Significance

A statistically significant result does not necessarily imply that implementing the Variant would produce a meaningful business benefit.

---

## Reproducibility

The project uses a configurable random seed.

The default seed is:

```text
42
```

Using the same configuration and random seed produces the same synthetic dataset.

The dataset can therefore be regenerated with:

```bash
python generate_data.py
```

This makes the experiment reproducible without requiring an external data source.

---

## Future Improvements

Potential extensions to the project include:

- Adding Bayesian A/B testing
- Adding multiple experiment variants
- Adding power analysis and sample-size calculations
- Adding sequential testing considerations
- Adding segmentation by device type
- Adding segmentation by traffic source
- Adding revenue-per-visitor analysis
- Adding retention metrics
- Adding experiment-duration controls
- Deploying the Streamlit dashboard publicly
- Adding automated CI testing with GitHub Actions

These features are outside the core requirements of the AVIP 2026 Task 10 specification but could extend the project into a more advanced experimentation analytics system.

---

## AVIP 2026 Task Requirements

This project addresses the core requirements of **Task 10 — The "Conversion" A/B Testing Simulator (Statistical Dashboard)**:

- [x] Generate synthetic web traffic for Control and Variant
- [x] Simulate data over a 14-day period
- [x] Calculate daily conversion rates
- [x] Calculate total conversion rates
- [x] Perform a statistical hypothesis test
- [x] Calculate a p-value
- [x] Determine statistical significance
- [x] Build an interactive dashboard
- [x] Visualize traffic trends
- [x] Visualize conversion rates
- [x] Provide a statistical conclusion
- [x] Provide reproducible synthetic data generation
- [x] Provide project documentation
- [x] Provide automated tests

---

## Author

**Yousuf Sheikh**

BSc Cybersecurity
Minor in Finance
Rochester Institute of Technology Dubai

GitHub: [ysf-sheikh](https://github.com/ysf-sheikh)

---
