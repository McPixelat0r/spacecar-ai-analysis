import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from statsmodels.stats.outliers_influence import variance_inflation_factor
import os


def generate_correlation_heatmap(df, output_dir="outputs", threshold=0.8):
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


def calculate_vif(df, output_dir="outputs"):
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


def generate_residual_plots(df, target_column, output_dir="outputs"):
    os.makedirs(output_dir, exist_ok=True)
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
    return model.summary()


def generate_pairplot(df, output_dir="outputs", selected_features=None):
    os.makedirs(output_dir, exist_ok=True)
    plot_df = df[selected_features] if selected_features else df
    pairplot_path = os.path.join(output_dir, "pairplot.png")
    sns.pairplot(plot_df)
    plt.savefig(pairplot_path)
    plt.close()
    return pairplot_path


def run_full_feature_analysis(df, target_column, output_dir="outputs", feature_columns=None, tag="default"):
    output_dir = os.path.join(output_dir, tag)
    os.makedirs(output_dir, exist_ok=True)
    if feature_columns is None:
        feature_columns = [col for col in df.columns if col != target_column]
    df_subset = df[feature_columns + [target_column]]
    corr_matrix, high_corrs = generate_correlation_heatmap(df_subset, output_dir=output_dir)
    vif_data = calculate_vif(df_subset[feature_columns], output_dir=output_dir)
    regression_summary = generate_residual_plots(df_subset, target_column=target_column, output_dir=output_dir)
    generate_pairplot(df_subset, output_dir=output_dir)
    print(f"✅ Diagnostics complete for: {tag}")
    return {
        "corr_matrix": corr_matrix,
        "high_corr_pairs": high_corrs,
        "vif_data": vif_data,
        "regression_summary": regression_summary
    }
