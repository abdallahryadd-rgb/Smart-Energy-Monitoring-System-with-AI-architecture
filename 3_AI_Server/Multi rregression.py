# =====================================================================
# MODEL 1: 30-Minute Power Consumption Forecasting (Multi-Output)
# =====================================================================
import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import matplotlib.pyplot as plt

# 1) Load Dataset
data_path = "final_augmented_datasets.csv"
df = pd.read_csv(data_path , parse_dates=["time_sample"])

print("Shape of dataset:", df.shape)

# 2) Feature Engineering
df["hour"] = df["time_sample"].dt.hour
df["minute"] = df["time_sample"].dt.minute
df["dayofweek"] = df["time_sample"].dt.dayofweek

# Define Features (X) and Targets (y)
feature_cols = ["p1", "p2", "p3", "hour", "minute", "dayofweek"]
X = df[feature_cols]

target_cols = ["p1_next_30min", "p2_next_30min", "p3_next_30min"]
y = df[target_cols]

# 3) Train / Test Split (Keep shuffle=False for time-series order)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# 4) Build & Train Model
model = RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

# 5) Evaluation
y_pred = model.predict(X_test)
y_pred_df = pd.DataFrame(y_pred, columns=target_cols, index=y_test.index)

for col in target_cols:
    mae = mean_absolute_error(y_test[col], y_pred_df[col])
    r2 = r2_score(y_test[col], y_pred_df[col])
    print(f"\n=== Results for {col} ===")
    print(f"MAE: {mae:.3f} W")
    print(f"R² : {r2:.3f}")

# 6) Save Model Artifact for Dashboard
joblib.dump(model, 'energy_model.pkl')
print("\n Saved Model 1 to: energy_model.pkl")

# 7) Plot and Save Actual vs Predicted for Documentation
plots_dir = "plots"
os.makedirs(plots_dir, exist_ok=True)

for col in target_cols:
    plt.figure(figsize=(14, 5))
    plt.plot(y_test[col].values, label="Actual", linewidth=2)
    plt.plot(y_pred_df[col].values, label="Predicted", linewidth=2)
    plt.title(f"Actual vs Predicted for {col}", fontsize=16)
    plt.xlabel("Sample Index", fontsize=14)
    plt.ylabel("Power (W)", fontsize=14)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    
    filename = os.path.join(plots_dir, f"{col}_actual_vs_pred.png")
    plt.savefig(filename, dpi=300)
    plt.close()
print("Saved all Forecasting plots to 'plots' folder.")
