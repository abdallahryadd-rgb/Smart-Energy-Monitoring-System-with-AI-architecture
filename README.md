<div align="center">

# ⚡ Smart Multi-Point Energy Monitoring and AI-Based Forecasting System

### Intelligent IoT-Based Energy Monitoring with Real-Time Analytics and Machine Learning

**Bachelor Graduation Project (2026)**

Faculty of Engineering – Electronics and Communications Engineering  
Alamein International University (AIU)

---

An intelligent energy monitoring platform that combines **ESP32**, **Desktop Applications**, **Machine Learning**, and **Artificial Intelligence** to monitor electrical loads, predict future energy consumption, detect abnormal operating conditions, and provide intelligent recommendations for energy optimization.

---

![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python)

![CSharp](https://img.shields.io/badge/C%23-.NET-purple?style=for-the-badge&logo=csharp)

![ESP32](https://img.shields.io/badge/ESP32-IoT-red?style=for-the-badge)

![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green?style=for-the-badge&logo=fastapi)

![Docker](https://img.shields.io/badge/Docker-Container-blue?style=for-the-badge&logo=docker)

![GitHub Actions](https://img.shields.io/badge/GitHub-Actions-orange?style=for-the-badge&logo=githubactions)

</div>


# 📖 Project Overview

Monitoring electrical energy consumption is an essential task for improving energy efficiency, reducing operational costs, and ensuring the safe operation of electrical systems. Traditional monitoring systems typically provide only instantaneous measurements, leaving users responsible for analyzing historical trends and identifying abnormal operating conditions manually.

This project introduces a **Smart Multi-Point Energy Monitoring and AI-Based Forecasting System** that transforms conventional monitoring into an intelligent decision-support platform. The system integrates embedded hardware, desktop software, machine learning, and prescriptive analytics into a unified architecture capable of real-time monitoring, demand forecasting, anomaly detection, overload prediction, and intelligent energy management.

The hardware subsystem is built around an **ESP32 microcontroller** connected to multiple voltage and current sensors. Real-time electrical measurements are transmitted to a Windows desktop application developed in **C#**, where data is visualized, logged, and forwarded to a **FastAPI-based AI server**. The AI engine analyzes incoming measurements using multiple machine learning models to generate predictions, detect abnormal behavior, classify operating conditions, and provide actionable recommendations for system operators.

The proposed platform demonstrates how low-cost IoT hardware can be combined with Artificial Intelligence to build scalable and intelligent energy management systems suitable for residential buildings, laboratories, educational environments, and small industrial facilities.

---

# ✨ Key Features

- ⚡ Real-Time Multi-Point Power Monitoring
- 📈 AI-Based Energy Forecasting
- 🚨 Automatic Fault Detection
- 🧠 Intelligent Load Classification
- 🔥 Electrical Overload Prediction
- 💰 Egyptian Residential Electricity Tariff Estimation
- 📊 Interactive Desktop Dashboard
- 💾 Automatic CSV Data Logging
- 🐳 Docker Deployment Support
- 🌐 FastAPI REST Backend
- 🔄 GitHub Actions Continuous Integration
- 📡 ESP32 Embedded Data Acquisition
- ---

# 🏗️ System Architecture

The proposed system follows a layered architecture that integrates embedded sensing, real-time monitoring, and Artificial Intelligence into a single intelligent energy management platform. Electrical measurements are acquired through multiple sensors, processed by an ESP32 microcontroller, visualized using a C# desktop application, and analyzed by a FastAPI-based AI server that performs forecasting, fault detection, load classification, and intelligent decision support.



## 🔄 End-to-End Workflow

```text
Electrical Loads
        │
        ▼
Voltage & Current Sensors
        │
        ▼
ESP32 Microcontroller
        │
        ▼
Serial Communication (UART)
        │
        ▼
C# Desktop Application
        │
        ├── Live Monitoring
        ├── Data Logging
        ├── CSV Export
        └── AI Request
                │
                ▼
FastAPI AI Server
                │
                ▼
+-----------------------------------------+
| Random Forest Regressor                 |
| Isolation Forest                        |
| Logistic Regression                     |
| Random Forest Classifier                |
+-----------------------------------------+
                │
                ▼
AI Dashboard & Prescriptive Recommendations
```

---

# ⚡ Hardware Implementation

The hardware subsystem is designed around the ESP32 microcontroller, providing a low-cost and scalable solution for monitoring multiple electrical loads simultaneously. Each monitoring point is equipped with dedicated voltage and current sensors, allowing independent measurement of electrical parameters.
![Dashboard Overview](images/dashboard/Screenshot%202026-07-24%20195115.png)


## Hardware Components

| Component | Description |
|-----------|-------------|
| ESP32 DevKit | Main embedded controller |
| ZMPT101B | AC Voltage Sensor |
| ACS712 | AC Current Sensor |
| Breadboard | Prototype assembly |
| AC Loads | Electrical appliances |
| USB Serial | Communication with PC |

---

## Voltage Measurement

The ZMPT101B voltage sensor safely steps down the AC mains voltage into a low-level analog signal suitable for the ESP32 ADC. Proper calibration is applied to ensure accurate RMS voltage estimation.


---

## Current Measurement

Current is measured using ACS712 Hall-effect current sensors. Each sensor provides an isolated analog output proportional to the measured AC current, enabling safe and reliable monitoring.


## Multi-Point Monitoring

Unlike conventional energy meters, the proposed platform supports **three independent monitoring channels**, allowing simultaneous measurement and comparison between multiple electrical loads.

Each channel continuously measures:

- Voltage (V)
- Current (A)
- Active Power (W)

---

# 💻 Embedded Processing

The ESP32 firmware continuously samples analog sensor values, performs calibration, calculates active power, and transmits formatted measurements to the desktop application through UART serial communication.

Main responsibilities include:

- Analog Data Acquisition
- Sensor Calibration
- RMS Voltage Calculation
- RMS Current Calculation
- Active Power Computation
- Multi-Channel Processing
- UART Communication

---

# 🖥️ Desktop Monitoring Application

A Windows Forms application developed in **C#** serves as the main user interface of the system.

### Features

- Automatic COM Port Detection
- Real-Time Monitoring
- Live Sensor Visualization
- Historical Data Logging
- CSV Export
- AI Communication

![AI Dashboard Detailed View](images/dashboard/Screenshot%202026-07-24%20221120.png)

---

# 🔄 Data Flow

The following workflow summarizes how data travels through the system.

```text
Electrical Load
      │
      ▼
Voltage & Current Sensors
      │
      ▼
ESP32
      │
      ▼
Power Calculation
      │
      ▼
Serial Communication
      │
      ▼
Desktop Application
      │
      ├── Live Dashboard
      ├── CSV Storage
      └── FastAPI Request
              │
              ▼
Machine Learning Models
              │
              ▼
Forecasts • Alerts • Recommendations
```
---

# 🤖 Artificial Intelligence Pipeline

One of the main objectives of this project is to transform conventional electrical monitoring into an intelligent decision-support platform. Instead of displaying raw electrical measurements only, the system analyzes historical and real-time data to predict future energy consumption, detect abnormal operating conditions, classify electrical load states, and generate actionable recommendations.

The AI engine is implemented as a **FastAPI-based backend** that loads pre-trained machine learning models and performs inference in real time using measurements received from the desktop application.

---

## 🧠 AI Workflow

```text
Historical Dataset
        │
        ▼
Data Cleaning & Feature Engineering
        │
        ▼
Model Training
        │
        ▼
Model Evaluation
        │
        ▼
Save Trained Models (.pkl)
        │
        ▼
FastAPI AI Server
        │
        ▼
Desktop Application
        │
        ▼
Prediction • Alerts • Recommendations
```

---

# 📊 Machine Learning Models

The AI engine consists of four complementary machine learning models, each responsible for a specific analytical task.

| Model | Purpose |
|---------|--------------------------------|
| 🌲 Random Forest Regressor | 30-Minute Energy Forecasting |
| 🚨 Isolation Forest | Electrical Fault Detection |
| ⚡ Logistic Regression | Overload Prediction |
| 🧠 Random Forest Classifier | Load-State Classification |

---

## 📈 1. Random Forest Regressor

The forecasting model predicts future electrical power consumption for all monitored channels using historical measurements and temporal features.

### Input Features

- Historical Power Measurements
- Hour
- Minute
- Day of Week

### Output

- Predicted Power P1
- Predicted Power P2
- Predicted Power P3

### Model Performance

| Target | R² Score |
|---------|----------|
| P1 | 0.861 |
| P2 | 0.930 |
| P3 | 0.800 |


## 🚨 2. Isolation Forest

The Isolation Forest model identifies abnormal operating conditions without requiring labelled fault data.

Detected anomalies include:

- Electrical Faults
- Phase Imbalance
- Unexpected Load Increase
- Abnormal Consumption

### Performance

- Fault Recall: **91%**
- Normal Precision: **97%**


---

## ⚡ 3. Logistic Regression

This model predicts whether the monitored electrical system is approaching an overload condition.

Possible outputs:

- Safe Operation
- High Load Warning

### Performance

- Accuracy: **93.6%**
- F1 Score: **0.94**


---

## 🧠 4. Random Forest Classifier

The classification model categorizes the operating condition into one of three electrical states.

Classes:

- 🟢 Idle
- 🟡 Normal
- 🔴 High Load

### Performance

- Accuracy: **90.7%**



---

# 💰 Egyptian Residential Tariff Engine

To provide meaningful financial insights, the system estimates electricity costs using the official Egyptian residential electricity tariff.

The calculated power consumption is converted into energy usage and matched against the corresponding tariff category to estimate operational cost.

The dashboard continuously updates estimated electricity expenses alongside the monitored electrical measurements.



---

# 🧠 Prescriptive Analytics Engine

Unlike conventional monitoring systems, the proposed platform generates intelligent recommendations based on AI predictions and detected operating conditions.

Typical recommendations include:

✅ Reduce unnecessary electrical loads

✅ Schedule preventive maintenance

✅ Investigate abnormal consumption

✅ Isolate faulty phases

✅ Delay high-power appliances

✅ Prepare for expected peak demand

These recommendations assist operators in making proactive maintenance and energy management decisions.

---

# 📊 AI Dashboard Case Studies

The dashboard dynamically changes according to the detected operating condition.

### 🟢 Case Study A — Ready State

The system has started successfully and is waiting for incoming measurements.

![Case A](images/dashboard/Screenshot%202026-06-09%20184420.png)

---

### 🔵 Case Study B — Maintenance Advisory

Low electrical activity is detected for an extended period.

The AI recommends scheduling preventive maintenance.

![Case B](images/dashboard/Screenshot%202026-06-09%20184552.png)

---

### 🟡 Case Study C — Normal Operation

Electrical measurements remain within expected operating limits.

The dashboard reports healthy system behavior.
![Case C](images/dashboard/Screenshot%202026-06-09%20184640.png)


---

### 🔴 Case Study D — Severe Overload

The predicted electrical demand exceeds predefined thresholds.

The dashboard immediately recommends load shedding.

![Case D](images/dashboard/Screenshot%202026-06-10%20111821.png)

### 🚨 Case Study E — Phase Imbalance

A significant power difference is detected between monitored channels.

The AI engine flags the condition and recommends immediate inspection.

![Case E](images/dashboard/Screenshot%202026-06-09%20184259.png)

### 🚀 MLOps & FastAPI Deployment

#### 1. Docker Image Build Process
![Docker Build](images/ai/Screenshot%202026-07-25%20184043.png)

#### 2. Container Execution & Uvicorn Server Logs
![Docker Container Running](images/ai/Screenshot%202026-07-25%20184213.png)

#### 3. FastAPI Interactive API Documentation (Swagger UI)
![FastAPI Swagger UI](images/ai/Screenshot%202026-07-25%20184308.png)

#### 4. Automated CI/CD Pipeline (GitHub Actions)
![GitHub Actions CI](images/ai/actions.png)
# 📂 Repository Structure

```text
Smart-Energy-Monitoring-System-with-AI-architecture
│
├── 0_Dataset_and_EDA/
│   └── final_augmented_dataset.csv
│
├── 1_Arduino_Node/
│   └── 1_Arduino_Node.ino
│
├── 2_C# Desktop Application/
│   ├── AI_Power_Agent.sln
│   └── AI_Power_Agent/
│
├── 3_AI_Server/
│   ├── api.py
│   ├── dash.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── *.pkl
│
├── docs/
│   ├── images/
│   ├── hardware.md
│   ├── software.md
│   ├── ai-models.md
│   └── deployment.md
│
├── .github/
│   └── workflows/
│
├── docker-compose.yml
│
└── README.md
```

---

# 🚀 Getting Started

## Prerequisites

Before running the project, make sure the following software is installed:

- Python 3.10 or later
- Visual Studio 2022
- Arduino IDE
- Docker Desktop
- Git

---

## Clone Repository

```bash
git clone https://github.com/abdallahryadd-rgb/Smart-Energy-Monitoring-System-with-AI-architecture.git

cd Smart-Energy-Monitoring-System-with-AI-architecture
```

---

# 🔌 Running the ESP32 Firmware

1. Open Arduino IDE.
2. Install the ESP32 Board Package.
3. Open `1_Arduino_Node.ino`.
4. Select the correct COM Port.
5. Upload the firmware to the ESP32.

---

# 🖥️ Running the Desktop Application

Open:

```text
2_C# Desktop Application/
```

Launch:

```text
AI_Power_Agent.sln
```

using Visual Studio.

Build and run the project.


---

# 🤖 Running the AI Server

Navigate to:

```bash
cd 3_AI_Server
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the FastAPI server:

```bash
python api.py
```

The AI backend is now ready to receive requests from the desktop application.

---

# 🐳 Docker Deployment

The project also supports containerized deployment using Docker Compose.

```bash
docker-compose up --build
```

Docker automatically builds the AI backend and starts all required services.

---

# 🔄 Continuous Integration

GitHub Actions automatically validates the project whenever changes are pushed to the repository.

The CI workflow performs:

- Repository Checkout
- Python Environment Setup
- Dependency Installation
- Docker Build Validation
- Basic Project Verification


---

# 📈 Experimental Highlights

✔ Real-Time Monitoring

✔ Multi-Point Energy Measurement

✔ AI-Based Power Forecasting

✔ Automatic Fault Detection

✔ Electrical Load Classification

✔ Overload Prediction

✔ Egyptian Tariff Estimation

✔ Prescriptive Analytics

✔ CSV Export

✔ Docker Deployment

✔ GitHub Actions Integration

---

# 🔮 Future Improvements

Potential future enhancements include:

- Cloud Deployment (Azure / AWS)
- MQTT Communication
- Web-Based Dashboard
- Mobile Application
- Firebase Integration
- Time-Series Database
- Deep Learning Forecasting
- Edge AI Deployment
- Smart Home Automation
- Renewable Energy Integration
- Solar Panel Monitoring
- Battery Management Support

---

# 👨‍💻 Team Members

| Name | Role |
|------|------|
| Abdallah Ahmed Riyad | Team Member |
| Mohamed Mahmoud Adawi | Team Member |
| Ahmed Mohamed Farouk | Team Member |
| Tasneem Ahmed Abdelaziz | Team Member |
| Samar Yasser Helmy | Team Member |

---

# 🎓 Academic Supervision

**Supervisor**

- Assoc. Prof. Mohamed Abdelkarim

**Teaching Assistant**

- Eng. Mohamed Tarek

---

# 🏛️ Institution

Faculty of Engineering

Electronics and Communications Engineering Department

Alamein International University (AIU)

Graduation Project – 2026

---

# 📚 Citation

If you use this project in your research, publications, or academic work, please cite:

```text
Smart Multi-Point Energy Monitoring and AI-Based Forecasting System

Bachelor Graduation Project

Faculty of Engineering

Alamein International University

2026
```

---

# 📄 License

This repository is released under the **MIT License**.

See the LICENSE file for additional information.

---

# 🙏 Acknowledgments

The authors would like to express their sincere appreciation to the Faculty of Engineering at Alamein International University and to the project supervisors for their continuous guidance, valuable feedback, and technical support throughout the development of this project.

Special thanks are extended to everyone who contributed to the successful completion of this work.

---

<div align="center">

## ⭐ If you found this project useful, please consider giving it a Star ⭐

It motivates us to continue improving the project and developing more open-source engineering solutions.

Made with ❤️ using ESP32, C#, FastAPI, Docker, and Machine Learning.

</div>
- 📉 Historical Energy Analysis
- 📢 Prescriptive Maintenance Recommendations
