
# 📈 Water Consumption Forecasting and Anomaly Detection

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![XGBoost](https://img.shields.io/badge/Model-XGBoost-orange)](https://xgboost.readthedocs.io/)

---

## 📚 Overview

This project focuses on **forecasting hourly water consumption** and **detecting anomalies** (such as leaks or unauthorized usage) based on real-world time series data collected from different water supply points (CUPS).

Using machine learning models — especially **XGBoost Regressor** — it predicts future consumption values and identifies deviations from expected behavior.

---

## 🏗️ Project Structure

```
csvs/                  # Raw input CSV files (one per CUPS)
results/               # Output folders with predictions, RMSE analysis, and plots
sarima_forecast.py      # Main processing script
Anexa_2_completata.docx # Summary report (optional)
```

---

## 🛠️ Technologies Used

- **Python 3.11**
- **pandas**
- **numpy**
- **matplotlib**
- **xgboost**
- **scikit-learn**

---

## ⚙️ Main Workflow

1. **Load and preprocess** each CSV file:
   - Parse timestamps.
   - Force hourly frequency and interpolate missing values.
   - Generate time-based features (hour, day, month, is_weekend).

2. **Train/Test split**:
   - 80% for training, 20% for testing.

3. **Model training**:
   - Use XGBoost Regressor to predict water consumption.

4. **Evaluation**:
   - Compute RMSE overall, before anomaly, and after anomaly.

5. **Outputs**:
   - CSV with predictions.
   - TXT file with RMSE breakdown.
   - Several visualizations.

---

## 📦 How to Run

> Make sure you have Python 3.11 installed and the required libraries.

1. Install dependencies:

```bash
pip install pandas numpy matplotlib xgboost scikit-learn
```

2. Place your raw CSV files inside the `csvs/` directory.

3. Run the script:

```bash
python sarima_forecast.py
```

4. Outputs will be generated under the `results/` folder.

---

## 📊 Example Outputs

- `xgboost_predictions_full.csv` – Observed vs Predicted consumption
- `rmse_comparison.txt` – RMSE summary (full test, normal zone, anomaly zone)
- `xgboost_forecast_plot.png` – Test forecast plot
- `rmse_breakdown_plot.png` – Normal vs Anomaly zones visualization
- `full_series_forecast_with_anomaly.png` – Full month prediction with anomaly highlighted

---

## 🧠 Key Concepts

- **Time Series Forecasting**
- **Anomaly Detection**
- **Gradient Boosting Trees (XGBoost)**
- **Water Consumption Analysis**

---

## 📜 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT) – free for educational and scientific purposes.

---

## ✍️ Author

- **Mihai Lungu**
- 2025
