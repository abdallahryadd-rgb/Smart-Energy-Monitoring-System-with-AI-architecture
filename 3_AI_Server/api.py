from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd

app = FastAPI(title="Industrial Energy Monitor API", version="1.0")

print("⏳ Loading Models from directory...")
# تحميل نفس الملفات اللي ظهرت عندك في السكرين شوت
energy_model = joblib.load('energy_model.pkl')
energy_scaler = joblib.load('energy_scaler.pkl')
isolation_model = joblib.load('isolation_forest_model.pkl')
logistic_model = joblib.load('state_model.pkl')
rf_model = joblib.load('device_state_rf_model.pkl')
rf_scaler = joblib.load('device_state_scaler.pkl')
print("✅ All 6 models loaded successfully!")

# تعريف شكل البيانات اللي هنستقبلها
class PowerInputs(BaseModel):
    p1: float; p1_t1: float; p1_t2: float
    p2: float; p2_t1: float; p2_t2: float
    p3: float; p3_t1: float; p3_t2: float

@app.post("/predict")
def predict_system_state(data: PowerInputs):
    # 1. تجهيز البيانات
    # موديل التوقع بياخد 9 فيتشرز بدون سكيل (زي ما دبرته أول مرة)
    input_9_raw = np.array([[data.p1, data.p1_t1, data.p1_t2, 
                             data.p2, data.p2_t1, data.p2_t2, 
                             data.p3, data.p3_t1, data.p3_t2]])
    
    input_3_raw = np.array([[data.p1, data.p2, data.p3]])
    
    imbalance = max(data.p1, data.p2, data.p3) - min(data.p1, data.p2, data.p3)
    imbalance_df = pd.DataFrame({'imbalance': [imbalance]})

    # 2. التوقع (Forecasting)
    predicted_power = energy_model.predict(input_9_raw)[0]
    
    # 3. اكتشاف الأعطال (Isolation Forest)
    anomaly_pred = isolation_model.predict(imbalance_df)[0]
    is_anomaly = bool(anomaly_pred == -1)
    
    # 4. مراقبة الأحمال (Logistic Regression)
    overload_pred = logistic_model.predict(input_3_raw)[0]
    is_overload = bool(overload_pred == 1)
    
    # 5. حالة النظام (Random Forest Classifier)
    rf_scaled_3 = rf_scaler.transform(input_3_raw)
    state_pred = rf_model.predict(rf_scaled_3)[0]

    # الرد النهائي بتاع الـ API
    return {
        "status": "success",
        "forecast": {
            "p1_next_30min": round(predicted_power[0], 2),
            "p2_next_30min": round(predicted_power[1], 2),
            "p3_next_30min": round(predicted_power[2], 2)
        },
        "diagnostics": {
            "anomaly_detected": is_anomaly,
            "overload_warning": is_overload,
            "system_state": str(state_pred)
        }
    }