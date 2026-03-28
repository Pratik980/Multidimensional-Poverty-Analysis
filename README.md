# Global Poverty & Development Dashboard

A comprehensive data visualization dashboard built with Streamlit and Plotly to explore and analyze global poverty, inequality, and World Development Indicators. 

## 🌍 Overview

This project provides an interactive web application that allows users to explore global poverty metrics and related development indicators. Through beautiful, responsive visualizations, users can analyze trends, compare countries, and understand the multifaceted nature of global poverty and economic development.

## 🗂️ Project Structure

```text
Project/
├── app.py                  # Main Streamlit application
├── data/                   
│   ├── processed/          # Cleaned and engineered datasets ready for visualization
│   └── raw/                # Original source datasets (World Bank Poverty & WDI)
└── notebooks/              # Jupyter notebooks for Exploratory Data Analysis (EDA)
    ├── EDA-DV updated.ipynb
    └── DV_Group_Assignment_Poverty_Analysis.ipynb
```

## 🚀 Getting Started

### Prerequisites

Ensure you have Python installed (preferably 3.8+).

### Installation

1. Clone or download this repository.
2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv .venv
   .venv\Scripts\Activate.ps1  # On Windows PowerShell
   ```
3. Install the required dependencies:
   ```bash
   pip install streamlit pandas plotly numpy
   ```

### Running the Application

To start the Streamlit dashboard, run the following command in your terminal from the root directory of the project:

```bash
streamlit run app.py
```

The application will automatically open in your default web browser at `http://localhost:8501`.

## 📊 Data Sources

- **World Bank Poverty & Inequality Data**: Information on global poverty rates, income distribution, and related metrics.
- **World Development Indicators (WDI)**: Comprehensive collection of development indicators compiled from officially recognized international sources.

## 🛠️ Built With

- **[Streamlit](https://streamlit.io/)**: For creating the interactive web application.
- **[Plotly Express & Graph Objects](https://plotly.com/python/)**: For rendering interactive and dynamic charts.
- **[Pandas](https://pandas.pydata.org/) & [NumPy](https://numpy.org/)**: For data manipulation and processing.
- **Jupyter Notebooks**: For initial data exploration, cleaning, and feature engineering.
