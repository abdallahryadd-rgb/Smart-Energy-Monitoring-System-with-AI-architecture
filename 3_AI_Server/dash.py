import customtkinter as ctk
import tkinter as tk
import numpy as np
import requests  # المكتبة الجديدة المسئولة عن الاتصال بالـ API
import warnings

warnings.filterwarnings("ignore", category=UserWarning)
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# رابط الـ API بتاعنا اللي شغال جوه الـ Docker
API_URL = "http://127.0.0.1:8000/predict"

app = ctk.CTk()
app.geometry("1100x880") 
app.title("Industrial Energy Monitor | Prescriptive AI Edition (MLOps)")

# =====================================================================
class SpeedometerGauge(tk.Canvas):
    def __init__(self, parent, size=180, thickness=20, color="#27ae60", bg_color="#ecf0f1"):
        super().__init__(parent, width=size, height=size//2 + 10, bg="#ffffff", highlightthickness=0)
        self.size = size
        self.thickness = thickness
        self.color = color
        self.bg_color = bg_color
        
        self.create_arc(self.thickness, self.thickness,
                        self.size - self.thickness, self.size - self.thickness,
                        start=0, extent=180, outline=self.bg_color,
                        width=self.thickness, style=tk.ARC)

    def set_value(self, progress, dynamic_color=None):
        self.delete("progress")
        if dynamic_color:
            self.color = dynamic_color
            
        progress = max(0.0, min(1.0, progress))
        extent = -int(progress * 180)
        
        self.create_arc(self.thickness, self.thickness,
                        self.size - self.thickness, self.size - self.thickness,
                        start=180, extent=extent, outline=self.color,
                        width=self.thickness, style=tk.ARC, tags="progress")

# =====================================================================
def parse_sequence(input_str):
    try:
        parts = [float(x.strip()) for x in input_str.split(',')]
        if len(parts) >= 3: return parts[0], parts[1], parts[2]
        else: return parts[0], parts[0], parts[0]
    except: return 0.0, 0.0, 0.0

def analyze_data():
    try:
        # 1. قراءة البيانات من الشاشة
        p1_0, p1_1, p1_2 = parse_sequence(entry_p1.get())
        p2_0, p2_1, p2_2 = parse_sequence(entry_p2.get())
        p3_0, p3_1, p3_2 = parse_sequence(entry_p3.get())
        
        # 2. تجهيز البيانات في شكل JSON عشان تتبعت للـ API
        payload = {
            "p1": p1_0, "p1_t1": p1_1, "p1_t2": p1_2,
            "p2": p2_0, "p2_t1": p2_1, "p2_t2": p2_2,
            "p3": p3_0, "p3_t1": p3_1, "p3_t2": p3_2
        }

        # 3. إرسال البيانات للـ Docker Container واستلام الرد
        lbl_recommendation.configure(text="⏳ Connecting to AI Server...", text_color="#7f8c8d")
        app.update()
        
        response = requests.post(API_URL, json=payload, timeout=5)
        
        # التأكد إن الرد سليم
        if response.status_code == 200:
            api_data = response.json()
            
            # 4. تفريغ الداتا اللي راجعة من السيرفر
            pred_p1 = api_data["forecast"]["p1_next_30min"]
            pred_p2 = api_data["forecast"]["p2_next_30min"]
            pred_p3 = api_data["forecast"]["p3_next_30min"]
            
            anomaly_detected = api_data["diagnostics"]["anomaly_detected"]
            overload_warning = api_data["diagnostics"]["overload_warning"]
            rf_pred_str = str(api_data["diagnostics"]["system_state"]).lower()

            # 5. تحديث الشاشة بالأرقام الجديدة
            lbl_pred_p1.configure(text=f"{pred_p1:.1f} W"); bar_p1.set(min(max(pred_p1 / 500, 0), 1.0)) 
            lbl_pred_p2.configure(text=f"{pred_p2:.1f} W"); bar_p2.set(min(max(pred_p2 / 500, 0), 1.0))
            lbl_pred_p3.configure(text=f"{pred_p3:.1f} W"); bar_p3.set(min(max(pred_p3 / 500, 0), 1.0))
            
            total_pred_kw = (pred_p1 + pred_p2 + pred_p3) / 1000
            cost_per_day = total_pred_kw * 24 * 0.48
            cost_per_week = cost_per_day * 7
            monthly_kwh = total_pred_kw * 24 * 30 
            
            lbl_cost_day.configure(text=f"{cost_per_day:.2f} EGP")
            gauge_day.set_value(cost_per_day / 20.0) 
            
            lbl_cost_week.configure(text=f"{cost_per_week:.2f} EGP")
            gauge_week.set_value(cost_per_week / 140.0) 
            
            if monthly_kwh <= 250: tier_num, t_color = 1, "#2ecc71"
            elif monthly_kwh <= 500: tier_num, t_color = 2, "#f1c40f"
            elif monthly_kwh <= 750: tier_num, t_color = 3, "#e67e22"
            else: tier_num, t_color = 4, "#e74c3c"
                
            lbl_tier.configure(text=f"Tier {tier_num}", text_color=t_color)
            gauge_tier.set_value(monthly_kwh / 1000.0, dynamic_color=t_color)

            # تحديث حالات الخطر
            if anomaly_detected: lbl_iso_status.configure(text="⚠️ FAULT DETECTED", text_color="white", fg_color="#e74c3c")
            else: lbl_iso_status.configure(text="✅ NORMAL OP", text_color="white", fg_color="#2ecc71")
                
            if overload_warning: lbl_log_status.configure(text="🚨 OVERLOAD", text_color="white", fg_color="#e74c3c")
            else: lbl_log_status.configure(text="✅ SAFE CAPACITY", text_color="white", fg_color="#2ecc71")
                
            if rf_pred_str in ['0', 'idle']: lbl_rf_status.configure(text="💤 SYSTEM IDLE", text_color="black", fg_color="#f1c40f")
            elif rf_pred_str in ['1', 'normal', 'normal op', 'active normal']: lbl_rf_status.configure(text="⚡ ACTIVE NORMAL", text_color="white", fg_color="#3498db")
            else: lbl_rf_status.configure(text="🔥 CRITICAL HIGH", text_color="white", fg_color="#e67e22")

            # نظام التوصيات بناءً على الرد
            rec_text = "✅ System is running optimally. No immediate action required."
            rec_color = "#27ae60"

            if anomaly_detected:
                rec_text = "🛑 CRITICAL ACTION: Imbalance Detected! Isolate the abnormal phase immediately and inspect wiring to prevent motor burnout."
                rec_color = "#c0392b"
            elif overload_warning:
                rec_text = "⚠️ LOAD WARNING: Shed non-essential loads (e.g., HVAC, secondary lighting) to stabilize the network and prevent breakers from tripping."
                rec_color = "#e67e22"
            elif tier_num >= 3:
                rec_text = "💡 COST OPTIMIZATION: Approaching high tariff tiers. Consider shifting heavy machinery operations to off-peak night shifts."
                rec_color = "#d35400"
            elif rf_pred_str in ['0', 'idle']:
                rec_text = "🔧 MAINTENANCE WINDOW: System utilization is low. This is the optimal time to perform routine maintenance or calibrations."
                rec_color = "#2980b9"

            lbl_recommendation.configure(text=rec_text, text_color=rec_color)
            
        else:
            lbl_recommendation.configure(text=f"⚠️ Server Error: Received status code {response.status_code}", text_color="#c0392b")

    except requests.exceptions.ConnectionError:
        lbl_recommendation.configure(text="⚠️ CONNECTION FAILED: Make sure the Docker Container (API) is running!", text_color="#c0392b")
    except Exception as e:
        lbl_recommendation.configure(text=f"⚠️ Critical Execution Error: {e}", text_color="#c0392b")

# =====================================================================
left_frame = ctk.CTkFrame(app, width=260, corner_radius=0, fg_color="#f1f2f6")
left_frame.pack(side="left", fill="y", padx=10, pady=10)

ctk.CTkLabel(left_frame, text="⚡ Phase Trend Inputs", font=("Arial", 18, "bold"), text_color="#2c3e50").pack(pady=15)
ctk.CTkLabel(left_frame, text="Format: [Now], [t-1], [t-2]", font=("Arial", 11), text_color="#7f8c8d").pack(pady=0)

entry_p1 = ctk.CTkEntry(left_frame, height=40, font=("Arial", 14)); entry_p1.pack(pady=12, padx=20, fill="x"); entry_p1.insert(0, "100, 95, 90") 
entry_p2 = ctk.CTkEntry(left_frame, height=40, font=("Arial", 14)); entry_p2.pack(pady=12, padx=20, fill="x"); entry_p2.insert(0, "150, 145, 140")
entry_p3 = ctk.CTkEntry(left_frame, height=40, font=("Arial", 14)); entry_p3.pack(pady=12, padx=20, fill="x"); entry_p3.insert(0, "120, 115, 110")

btn_analyze = ctk.CTkButton(left_frame, text="FIRE REAL INFERENCE 🚀", height=50, font=("Arial", 15, "bold"), command=analyze_data, fg_color="#2ecc71"); btn_analyze.pack(pady=30, padx=20, fill="x")

right_frame = ctk.CTkFrame(app, fg_color="transparent"); right_frame.pack(side="right", fill="both", expand=True, padx=20, pady=10)
ctk.CTkLabel(right_frame, text="Live Predictive & Diagnostics Dashboard", font=("Arial", 24, "bold"), text_color="#2c3e50").pack(pady=15)

top_card = ctk.CTkFrame(right_frame, fg_color="#ffffff", corner_radius=15); top_card.pack(fill="x", pady=10, ipady=15)
ctk.CTkLabel(top_card, text="Forecasting Framework (Next 30 Mins)", font=("Arial", 15, "bold"), text_color="#7f8c8d").pack(pady=5)

gauges_container = ctk.CTkFrame(top_card, fg_color="transparent"); gauges_container.pack(fill="x", padx=20)
f1 = ctk.CTkFrame(gauges_container, fg_color="transparent"); f1.pack(side="left", expand=True)
ctk.CTkLabel(f1, text="Predicted P1", font=("Arial", 13, "bold"), text_color="#34495e").pack()
lbl_pred_p1 = ctk.CTkLabel(f1, text="0.0 W", font=("Arial", 22, "bold"), text_color="#2980b9"); lbl_pred_p1.pack()
bar_p1 = ctk.CTkProgressBar(f1, width=130, height=12, progress_color="#2980b9"); bar_p1.set(0); bar_p1.pack(pady=5)

f2 = ctk.CTkFrame(gauges_container, fg_color="transparent"); f2.pack(side="left", expand=True)
ctk.CTkLabel(f2, text="Predicted P2", font=("Arial", 13, "bold"), text_color="#34495e").pack()
lbl_pred_p2 = ctk.CTkLabel(f2, text="0.0 W", font=("Arial", 22, "bold"), text_color="#e67e22"); lbl_pred_p2.pack()
bar_p2 = ctk.CTkProgressBar(f2, width=130, height=12, progress_color="#e67e22"); bar_p2.set(0); bar_p2.pack(pady=5)

f3 = ctk.CTkFrame(gauges_container, fg_color="transparent"); f3.pack(side="left", expand=True)
ctk.CTkLabel(f3, text="Predicted P3", font=("Arial", 13, "bold"), text_color="#34495e").pack()
lbl_pred_p3 = ctk.CTkLabel(f3, text="0.0 W", font=("Arial", 22, "bold"), text_color="#2ecc71"); lbl_pred_p3.pack()
bar_p3 = ctk.CTkProgressBar(f3, width=130, height=12, progress_color="#2ecc71"); bar_p3.set(0); bar_p3.pack(pady=5)

mid_card = ctk.CTkFrame(right_frame, fg_color="#ffffff", corner_radius=15); mid_card.pack(fill="x", pady=10, ipady=15)
ctk.CTkLabel(mid_card, text="AI Safety Status & Diagnostics Registry", font=("Arial", 15, "bold"), text_color="#7f8c8d").pack(pady=10)

leds_container = ctk.CTkFrame(mid_card, fg_color="transparent"); leds_container.pack(fill="x", padx=20, pady=5)
sf1 = ctk.CTkFrame(leds_container, fg_color="transparent"); sf1.pack(side="left", expand=True)
ctk.CTkLabel(sf1, text="Isolation Forest\n(Unsupervised Faults)", font=("Arial", 13, "bold"), text_color="#2c3e50").pack(pady=8)
lbl_iso_status = ctk.CTkLabel(sf1, text="READY", font=("Arial", 14, "bold"), width=160, height=45, corner_radius=10, text_color="white", fg_color="#bdc3c7"); lbl_iso_status.pack()

sf2 = ctk.CTkFrame(leds_container, fg_color="transparent"); sf2.pack(side="left", expand=True)
ctk.CTkLabel(sf2, text="Logistic Regression\n(Overload Monitor)", font=("Arial", 13, "bold"), text_color="#2c3e50").pack(pady=8)
lbl_log_status = ctk.CTkLabel(sf2, text="READY", font=("Arial", 14, "bold"), width=160, height=45, corner_radius=10, text_color="white", fg_color="#bdc3c7"); lbl_log_status.pack()

sf3 = ctk.CTkFrame(leds_container, fg_color="transparent"); sf3.pack(side="left", expand=True)
ctk.CTkLabel(sf3, text="Random Forest\n(System Classification)", font=("Arial", 13, "bold"), text_color="#2c3e50").pack(pady=8)
lbl_rf_status = ctk.CTkLabel(sf3, text="READY", font=("Arial", 14, "bold"), width=160, height=45, corner_radius=10, text_color="white", fg_color="#bdc3c7"); lbl_rf_status.pack()

bottom_card = ctk.CTkFrame(right_frame, fg_color="#ffffff", corner_radius=15); bottom_card.pack(fill="x", pady=10, ipady=10)
ctk.CTkLabel(bottom_card, text="💰 Financial & Utility Cost Estimates", font=("Arial", 15, "bold"), text_color="#7f8c8d").pack(pady=5)

cost_container = ctk.CTkFrame(bottom_card, fg_color="transparent"); cost_container.pack(fill="x", padx=10)

c1 = ctk.CTkFrame(cost_container, fg_color="transparent"); c1.pack(side="left", expand=True, fill="x", padx=10)
gauge_day = SpeedometerGauge(c1, size=140, thickness=16, color="#27ae60"); gauge_day.pack(pady=(10, 5))
ctk.CTkLabel(c1, text="Daily Est. Bill", font=("Arial", 13, "bold"), text_color="#34495e").pack()
lbl_cost_day = ctk.CTkLabel(c1, text="0.00 EGP", font=("Arial", 18, "bold"), text_color="#27ae60"); lbl_cost_day.pack()

c2 = ctk.CTkFrame(cost_container, fg_color="transparent"); c2.pack(side="left", expand=True, fill="x", padx=10)
gauge_week = SpeedometerGauge(c2, size=140, thickness=16, color="#16a085"); gauge_week.pack(pady=(10, 5))
ctk.CTkLabel(c2, text="Weekly Est. Bill", font=("Arial", 13, "bold"), text_color="#34495e").pack()
lbl_cost_week = ctk.CTkLabel(c2, text="0.00 EGP", font=("Arial", 18, "bold"), text_color="#16a085"); lbl_cost_week.pack()

c3 = ctk.CTkFrame(cost_container, fg_color="transparent"); c3.pack(side="left", expand=True, fill="x", padx=10)
gauge_tier = SpeedometerGauge(c3, size=140, thickness=16, color="#bdc3c7"); gauge_tier.pack(pady=(10, 5)) 
ctk.CTkLabel(c3, text="Est. Monthly Tier", font=("Arial", 13, "bold"), text_color="#34495e").pack()
lbl_tier = ctk.CTkLabel(c3, text="Tier 1", font=("Arial", 18, "bold"), text_color="#bdc3c7"); lbl_tier.pack()

# 
rec_card = ctk.CTkFrame(right_frame, fg_color="#ecf0f1", corner_radius=15, border_width=2, border_color="#bdc3c7")
rec_card.pack(fill="x", pady=10, ipady=15)
ctk.CTkLabel(rec_card, text="🧠 AI Prescriptive Action Engine", font=("Arial", 15, "bold"), text_color="#2c3e50").pack(pady=5)
lbl_recommendation = ctk.CTkLabel(rec_card, text="Awaiting system analysis...", font=("Arial", 16, "bold"), text_color="#7f8c8d", wraplength=700)
lbl_recommendation.pack(pady=10)

app.mainloop()