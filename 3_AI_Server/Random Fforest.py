# MODEL 4: Load States Classification (FIXED & INDEPENDENT)
# =====================================================================
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, confusion_matrix,
                             classification_report, ConfusionMatrixDisplay)
 
# 1) Load Dataset
data_path = "final_augmented_dataset.csv"
df = pd.read_csv(data_path) 
X = df[['p1', 'p2', 'p3']].values
 
# 2) Unsupervised Clustering to Synthesize Labels
total_power = X.sum(axis=1).reshape(-1, 1)
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
kmeans.fit(total_power)
 
# Order clusters logically: 0=Idle, 1=Normal, 2=High Load
centers  = kmeans.cluster_centers_.flatten()
idx_sort = np.argsort(centers)
mapping  = {idx_sort[0]: 0, idx_sort[1]: 1, idx_sort[2]: 2}
y        = np.array([mapping[c] for c in kmeans.labels_])
 
# 3) Feature Scaling
scaler   = StandardScaler()
X_scaled = scaler.fit_transform(X)
 
#
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)
_, X_test_raw, _, _ = train_test_split(
    X, y, test_size=0.2, random_state=42
)
 
# 4) Supervised Training with GridSearch Optimization
rf = RandomForestClassifier(random_state=42)
param_grid = {
    'n_estimators':    [100, 200],
    'max_depth':       [None, 5, 10],
    'min_samples_split': [2, 5, 10],
    'max_features':    ['sqrt', 'log2'],
}
 
grid = GridSearchCV(rf, param_grid, cv=5, scoring='accuracy', n_jobs=-1, verbose=1)
grid.fit(X_train, y_train)
 
best_model = grid.best_estimator_
y_pred     = best_model.predict(X_test)
 
# 5) Print Metrics to Terminal
print("="*50)
print("📊 RANDOM FOREST CLASSIFIER METRICS (TEST DATA)")
print("="*50)
print(f"🔹 Best Found Params: {grid.best_params_}")
print(f"🔹 Global Model Accuracy: {accuracy_score(y_test, y_pred)*100:.2f}%")
print("\n🔹 Detailed Classification Report:")
print(classification_report(y_test, y_pred, target_names=['Idle', 'Normal', 'High Load']))
 
# 6) Save Artifacts
joblib.dump(best_model, 'device_state_rf_model.pkl')
joblib.dump(scaler,     'device_state_scaler.pkl')
joblib.dump(kmeans,     'device_state_kmeans.pkl')
print("\n✅ Saved Model 4 Artifacts successfully!")
 
# 7) Plots Generation 
plots_dir = "independent_metrics/multi_classification"
os.makedirs(plots_dir, exist_ok=True)
 

fig, ax = plt.subplots(figsize=(7, 5))
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Idle', 'Normal', 'High Load'])
disp.plot(cmap='Blues', values_format='d', ax=ax)
plt.title('Random Forest - Multi-Class Confusion Matrix', weight='bold', pad=15)
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'essential_confusion_matrix.png'), dpi=300)
plt.close()
 
plt.figure(figsize=(8, 5))
scatter = plt.scatter(X_test_raw[:, 0], X_test_raw[:, 1], c=y_pred, cmap='viridis', alpha=0.7, edgecolors='k', s=30)
plt.xlabel('Power Reading 1 (P1) [Watts]', fontsize=11)
plt.ylabel('Power Reading 2 (P2) [Watts]', fontsize=11)
plt.title('AI Decision Boundaries for Device Load States (Test Data)', weight='bold', pad=15)
plt.legend(handles=scatter.legend_elements()[0], labels=['Idle', 'Normal', 'High Load'])
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'essential_cluster_graph.png'), dpi=300)
plt.close()

print(f"\n✅ Done! Saved Multi-Class plots inside: '{plots_dir}'")
