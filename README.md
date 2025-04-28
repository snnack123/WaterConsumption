📈 Water Consumption Forecasting and Anomaly Detection
This project focuses on forecasting water consumption and detecting anomalies (such as leaks or unauthorized usage) based on real-world time series data collected from various supply points (CUPS).

It uses machine learning models — especially XGBoost Regressor — to predict future consumption values and identify deviations from expected behavior.

🚀 Project Structure
csvs/ – Contains the raw input CSV files (one for each CUPS).

results/ – The generated output, including predictions, RMSE analysis, and visualizations for each CSV.

sarima_forecast.py – Main Python script that processes each file.

Anexa_2_completata_final.docx – Summary report of the methodology and results (optional for documentation).

🛠️ Technologies Used
Python 3.11

pandas

numpy

matplotlib

xgboost

scikit-learn

🧠 Main Workflow
Load and preprocess each CSV file:

Parse datetime correctly.

Force hourly frequency and interpolate missing values.

Engineer additional time-based features (hour, day, month, is_weekend).

Split data into training (80%) and testing (20%) sets.

Train an XGBoost Regressor to predict hourly water consumption based on time features.

Evaluate predictions:

Compute global RMSE.

Compute RMSE before and after a known anomaly date.

Generate outputs for each CUPS:

CSV file with observed vs predicted consumption.

TXT file with RMSE summary.

Plots:

Predicted vs real consumption (test set only).

RMSE breakdown (normal zone vs anomaly zone).

Full month plot highlighting anomaly zones.

📦 How to Run
Install the required Python packages:

bash
Copiază
Editează
pip install pandas numpy matplotlib xgboost scikit-learn
Make sure your raw CSV files are placed inside the csvs/ folder.

Run the script:

bash
Copiază
Editează
python sarima_forecast.py
Check the generated outputs in the results/ folder.

📊 Example Outputs
xgboost_predictions_full.csv – Table with observed vs predicted consumption and deviation.

rmse_comparison.txt – RMSE values for the full test period, normal zone, and anomaly zone.

xgboost_forecast_plot.png – Graph of predictions vs real values (test period).

rmse_breakdown_plot.png – Graph showing RMSE zones.

full_series_forecast_with_anomaly.png – Graph showing full month forecast with anomalies highlighted.

📜 License
Open-source project for educational and scientific research purposes. Feel free to use and adapt!

