"""
Feature Analysis Module

This module provides utilities for analyzing dataset features, including correlation matrices,
variance inflation factors (VIF), residual plots, and pairplots, to assist in feature engineering
and multicollinearity diagnostics.
"""

import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from statsmodels.stats.outliers_influence import variance_inflation_factor
from typing import List, Optional, Tuple


def generate_correlation_heatmap(df: pd.DataFrame, output_dir: str = "outputs", threshold: float = 0.8) -> Tuple[
    pd.DataFrame, List[Tuple[str, str, float]]]:
    """
    Generate a heatmap of feature correlations and report highly correlated pairs.

    Args:
        df (pd.DataFrame): Input dataframe.
        output_dir (str, optional): Directory to save the heatmap image. Defaults to 'outputs'.
        threshold (float, optional): Correlation threshold to report pairs. Defaults to 0.8.

    Returns:
        Tuple[pd.DataFrame, List[Tuple[str, str, float]]]: Correlation matrix and list of highly correlated feature pairs.
    """
    os.makedirs(output_dir, exist_ok=True)
    corr_matrix = df.corr()

    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
    plt.title("Correlation Matrix")
    heatmap_path = os.path.join(output_dir, "correlation_heatmap.png")
    plt.savefig(heatmap_path)
    plt.close()

    high_corr_pairs = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i):
            corr = corr_matrix.iloc[i, j]
            if abs(corr) > threshold:
                high_corr_pairs.append((corr_matrix.columns[i], corr_matrix.columns[j], corr))

    return corr_matrix, high_corr_pairs


def calculate_vif(df: pd.DataFrame, output_dir: str = "outputs") -> pd.DataFrame:
    """
    Calculate Variance Inflation Factors (VIF) for features.

    Args:
        df (pd.DataFrame): Input dataframe with only numeric features.
        output_dir (str, optional): Directory to save the VIF barplot. Defaults to 'outputs'.

    Returns:
        pd.DataFrame: VIF values for each feature.
    """
    os.makedirs(output_dir, exist_ok=True)
    scaler = StandardScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)

    vif_data = pd.DataFrame()
    vif_data["Feature"] = df_scaled.columns
    vif_data["VIF"] = [variance_inflation_factor(df_scaled.values, i) for i in range(df_scaled.shape[1])]

    plt.figure(figsize=(10, 6))
    sns.barplot(x="VIF", y="Feature", data=vif_data.sort_values("VIF", ascending=False))
    plt.title("VIF Scores by Feature")
    plt.tight_layout()
    vif_plot_path = os.path.join(output_dir, "vif_barplot.png")
    plt.savefig(vif_plot_path)
    plt.close()

    return vif_data


def generate_residual_plots(df: pd.DataFrame, target_column: str,
                            output_dir: str = "outputs") -> sm.regression.linear_model.RegressionResultsWrapper:
    """
    Generate residual plots for a simple linear regression.

    Args:
        df (pd.DataFrame): Input dataframe.
        target_column (str): Name of the target column.
        output_dir (str, optional): Directory to save the residual plot. Defaults to 'outputs'.

    Returns:
        statsmodels.regression.linear_model.RegressionResultsWrapper: Fitted regression model.
    """
    os.makedirs(output_dir, exist_ok=True)

    if target_column not in df.columns:
        raise ValueError(f"Target column '{target_column}' not found in dataframe.")

    X = df.drop(columns=[target_column])
    y = df[target_column]
    X_with_const = sm.add_constant(X)

    model = sm.OLS(y, X_with_const).fit()
    predictions = model.predict(X_with_const)
    residuals = y - predictions

    plt.figure(figsize=(8, 6))
    sns.residplot(x=predictions, y=residuals, lowess=True, line_kws={"color": "red"})
    plt.xlabel("Predicted Values")
    plt.ylabel("Residuals")
    plt.title("Residual Plot")
    residual_plot_path = os.path.join(output_dir, "residual_plot.png")
    plt.savefig(residual_plot_path)
    plt.close()

    return model


def generate_pairplot(df: pd.DataFrame, output_dir: str = "outputs",
                      selected_features: Optional[List[str]] = None) -> str:
    """
    Generate a pairplot for selected features or all features.

    Args:
        df (pd.DataFrame): Input dataframe.
        output_dir (str, optional): Directory to save the pairplot. Defaults to 'outputs'.
        selected_features (Optional[List[str]], optional): List of feature names to plot. Defaults to None.

    Returns:
        str: Path to the saved pairplot image.
    """
    os.makedirs(output_dir, exist_ok=True)
    plot_df = df[selected_features] if selected_features else df.copy()
    pairplot_path = os.path.join(output_dir, "pairplot.png")

    sns.pairplot(plot_df)
    plt.savefig(pairplot_path)
    plt.close()

    return pairplot_path


def run_full_feature_analysis(df: pd.DataFrame, target_column: str, output_dir: str = "outputs",
                              feature_columns: Optional[List[str]] = None, tag: str = "default") -> None:
    """
    Run a full feature analysis including correlation heatmap, VIF, residual plot, and pairplot.

    Args:
        df (pd.DataFrame): Input dataframe.
        target_column (str): Name of the target column.
        output_dir (str, optional): Root directory to save outputs. Defaults to 'outputs'.
        feature_columns (Optional[List[str]], optional): Specific features to include. Defaults to None (all features).
        tag (str, optional): Subfolder tag for output organization. Defaults to 'default'.
    """
    output_dir = os.path.join(output_dir, tag)
    os.makedirs(output_dir, exist_ok=True)

    if feature_columns is None:
        feature_columns = df.columns.tolist()

    selected_df = df[feature_columns]

    print(f"🔍 Running feature analysis in {output_dir}...")

    generate_correlation_heatmap(selected_df, output_dir=output_dir)
    calculate_vif(selected_df, output_dir=output_dir)
    generate_residual_plots(selected_df, target_column=target_column, output_dir=output_dir)
    generate_pairplot(selected_df, output_dir=output_dir)
