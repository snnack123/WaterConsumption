import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error

# === 1. Config ===
input_folder = "csvs"
output_root = "results"
split_point = pd.to_datetime("2025-04-04 00:00")

# === 2. Loop prin fiecare fișier ===
for filename in os.listdir(input_folder):
    if filename.endswith(".csv"):
        file_path = os.path.join(input_folder, filename)
        name = os.path.splitext(filename)[0]
        output_dir = os.path.join(output_root, name)
        os.makedirs(output_dir, exist_ok=True)

        print(f"📦 Processing: {filename}")

        # === Load & preprocess ===
        df = pd.read_csv(file_path, sep=';', engine='python')
        df["x"] = pd.to_datetime(df["x"], dayfirst=True)
        df.set_index("x", inplace=True) # Set the datetime column as index
        df = df.sort_index()
        df = df[["y"]].copy()
        df = df.asfreq("H") # Resample to hourly frequency
        df["y"] = df["y"].interpolate() # Fill NaN values with interpolation

        # === Feature engineering ===
        df["hour"] = df.index.hour
        df["dayofweek"] = df.index.dayofweek
        df["day"] = df.index.day
        df["month"] = df.index.month
        df["is_weekend"] = df["dayofweek"].isin([5, 6]).astype(int)

        # === Train/test split ===
        train_size = int(len(df) * 0.8)
        train = df.iloc[:train_size]
        test = df.iloc[train_size:]

        X_train = train.drop(columns=["y"])
        y_train = train["y"]
        X_test = test.drop(columns=["y"])
        y_test = test["y"]

        # === Model training ===
        model = XGBRegressor(n_estimators=200, max_depth=4, learning_rate=0.1, random_state=42)
        model.fit(X_train, y_train)

        # === Predict ===
        y_pred = model.predict(X_test)

        # === Save predictions ===
        result_df = pd.DataFrame({
            "Timestamp": test.index,
            "Observed": y_test.values,
            "Predicted": y_pred,
            "Deviation": y_test.values - y_pred
        })
        result_df.to_csv(os.path.join(output_dir, "xgboost_predictions_full.csv"), index=False)

        # === Root Mean Squared Error analysis ===
        result_df["Timestamp"] = pd.to_datetime(result_df["Timestamp"])
        result_df.set_index("Timestamp", inplace=True) # Set the datetime column as index to can separate the two zones
        df_before = result_df[result_df.index < split_point]
        df_after = result_df[result_df.index >= split_point]

        rmse_total = np.sqrt(mean_squared_error(result_df["Observed"], result_df["Predicted"]))
        rmse_before = np.sqrt(mean_squared_error(df_before["Observed"], df_before["Predicted"]))
        rmse_after = np.sqrt(mean_squared_error(df_after["Observed"], df_after["Predicted"]))

        # === Save RMSE TXT ===
        txt_path = os.path.join(output_dir, "rmse_comparison.txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write("XGBoost Forecast RMSE Breakdown\n")
            f.write("------------------------------------\n")
            f.write(f"📊 Full test period RMSE: {rmse_total:.2f} m³/h\n")
            f.write(f"✅ Before anomaly (normal zone) RMSE: {rmse_before:.2f} m³/h\n")
            f.write(f"⚠️  After anomaly (spike zone) RMSE: {rmse_after:.2f} m³/h\n")

        # === Plot 1: basic test forecast ===
        plt.figure(figsize=(20, 8))
        plt.plot(result_df.index, result_df["Observed"], label="Observed", color="black")
        plt.plot(result_df.index, result_df["Predicted"], label="XGBoost Forecast", color="blue", linestyle="--")
        plt.title(f"{name} | XGBoost Forecast (test only)")
        plt.xlabel("Time")
        plt.ylabel("Water Consumption (m³/h)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "xgboost_forecast_plot.png"))
        plt.close()

        # === Plot 2: RMSE zones (test only) ===
        plt.figure(figsize=(20, 8))
        plt.plot(result_df.index, result_df["Observed"], label="Observed", color="black")
        plt.plot(result_df.index, result_df["Predicted"], label="XGBoost Forecast", color="purple", linestyle="--")
        plt.axvspan(df_before.index[0], df_before.index[-1], color='green', alpha=0.1, label="Normal Zone")
        plt.axvspan(df_after.index[0], df_after.index[-1], color='red', alpha=0.1, label="Anomaly Zone")
        plt.title(f"{name} | RMSE: {rmse_total:.2f} | Normal: {rmse_before:.2f} | Anomaly: {rmse_after:.2f}")
        plt.xlabel("Time")
        plt.ylabel("Water Consumption (m³/h)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "rmse_breakdown_plot.png"))
        plt.close()

        # === Plot 3: FULL month with spike zone ===
        df_full = df.copy()
        df_full["Predicted"] = np.nan
        df_full.loc[result_df.index, "Predicted"] = result_df["Predicted"]

        plt.figure(figsize=(20, 8))
        plt.plot(df_full.index, df_full["y"], label="Observed", color="black")
        plt.plot(df_full.index, df_full["Predicted"], label="XGBoost Forecast", color="darkorange", linestyle="--")
        plt.axvspan(split_point, df_full.index[-1], color='red', alpha=0.1, label="Anomaly Zone (full series)")
        plt.title(f"{name} | Full Series Forecast with Anomaly Highlighted")
        plt.xlabel("Time")
        plt.ylabel("Water Consumption (m³/h)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "full_series_forecast_with_anomaly.png"))
        plt.close()

        print(f"✅ Finalized: {name}\n")
