import os
import pandas as pd
import joblib
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import IsolationForest

# 1) Load Dataset
data_path = "final_augmented_dataset.csv"
df = pd.read_csv(data_path)[['p1', 'p2', 'p3']].dropna()

# 2) Split Data
split_idx = int(len(df) * 0.8)
train_df = df.iloc[:split_idx]
test_df = df.iloc[split_idx:].copy()

# 3) Scaling
scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(train_df)
X_test_scaled = scaler.transform(test_df)
joblib.dump(scaler, "energy_scaler.pkl")

# 4) Train Isolation Forest
# contamination=0.05
model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
model.fit(X_train_scaled)
joblib.dump(model, "isolation_forest_model.pkl")

# 5) Testing and Extrating Metrics
test_predictions = model.predict(X_test_scaled)
test_df['anomaly_label'] = test_predictions

total_test_samples = len(test_df)
detected_anomalies = np.sum(test_predictions == -1)
normal_samples = np.sum(test_predictions == 1)

print("="*50)
print("📊 ANOMALY DETECTION MODEL METRICS (TEST DATA)")
print("="*50)
print(f"- Total Unseen Samples Tested  : {total_test_samples}")
print(f"- Normal System Operations Detected : {normal_samples} ({normal_samples/total_test_samples*100:.2f}%)")
print(f"- Anomalies / Faults Isolated      : {detected_anomalies} ({detected_anomalies/total_test_samples*100:.2f}%)")

# 6) Generation of Graphs 
plots_dir = "independent_metrics/anomaly_detection"
os.makedirs(plots_dir, exist_ok=True)

plt.figure(figsize=(15, 6))
#
power_signal = test_df['p1'].values
plt.plot(power_signal, color='#95a5a6', alpha=0.6, label='Live Power Signal (P1)')

anomaly_indices = np.where(test_predictions == -1)[0]
anomaly_values = power_signal[anomaly_indices]

#
plt.scatter(anomaly_indices, anomaly_values, color='#c0392b', s=35, label='AI Isolated Faults (Anomalies)', zorder=5)

plt.title("Unsupervised Fault Isolation Output (Corrected Timeline Evaluation)", fontsize=14, weight='bold')
plt.xlabel("Test Data Time Indices", fontsize=12)
plt.ylabel("Power Consumption (Watts)", fontsize=12)
plt.legend(loc="upper right")
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(f"{plots_dir}/isolated_faults_chart.png", dpi=300)
plt.close()
print("✅ Done! Saved Corrected Anomaly Detection plot.")
