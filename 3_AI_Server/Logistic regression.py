# MODEL 3: Binary Device State Classification (FIXED & INDEPENDENT)
# =====================================================================
import os
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay

# 1) Load Dataset
data_path = "final_augmented_dataset.csv"
df = pd.read_csv(data_path) 

# 2) Create Threshold Target based on mean
threshold = df['p1_next_30min'].mean()
df['target'] = (df['p1_next_30min'] > threshold).astype(int)

# Define Features and Target
X = df[['p1', 'p2', 'p3']]
y = df['target']

# 3) Split Data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4) Train Model
model = LogisticRegression()
model.fit(X_train, y_train)

# 5) Save Model Artifact for Dashboard
joblib.dump(model, 'state_model.pkl')
print("\n✅ Saved Model 3 to: state_model.pkl")

# 6) Print Metrics to Terminal
y_pred = model.predict(X_test)
print("="*50)
print("📊 LOGISTIC REGRESSION BINARY METRICS (TEST DATA)")
print("="*50)
print(f"🔹 Global Model Accuracy: {accuracy_score(y_test, y_pred)*100:.2f}%")
print("\n🔹 Detailed Classification Report:")
print(classification_report(y_test, y_pred, target_names=['Normal Capacity', 'High Power Alert']))

# 7) Plot and Save Confusion 
plots_dir = "independent_metrics/binary_classification"
os.makedirs(plots_dir, exist_ok=True)

cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Normal Capacity', 'High Power Alert'])

fig, ax = plt.subplots(figsize=(6, 5))
disp.plot(cmap=plt.cm.Blues, ax=ax, values_format='d')
plt.title("Logistic Regression - Confusion Matrix", fontsize=12, weight='bold', pad=15)
plt.tight_layout()

filename = os.path.join(plots_dir, "device_state_binary_chart.png")
plt.savefig(filename, dpi=300)
plt.close()
print(f"\n✅ Done! Saved Confusion Matrix plot inside: '{filename}'")