# NeuroCare AI – Stroke Risk Prediction Dashboard

NeuroCare AI is a Machine Learning-powered healthcare dashboard that predicts a patient’s stroke risk using clinical and lifestyle inputs.  
The application provides stroke risk prediction, probability score, risk factor highlights, clinical interpretation, precautions, healthy lifestyle tips, and diet guidance through an interactive Streamlit dashboard.

---

## Project Overview

Stroke is one of the major health conditions where early risk assessment can help in prevention and better lifestyle management.  
This project uses a trained Machine Learning model to estimate stroke risk based on patient details such as age, hypertension, heart disease, glucose level, BMI, work type, smoking status, and residence type.

The dashboard is designed to make prediction results more useful by also showing:
- **risk probability**
- **key risk factor highlights**
- **clinical interpretation**
- **recommended precautions**
- **healthy lifestyle tips**
- **diet and nutrition guidance**

---

## Features

- Stroke risk prediction using Machine Learning
- Interactive **Streamlit dashboard**
- Patient health data input form
- Probability-based stroke risk score
- Clinical interpretation of prediction result
- Risk factor highlights for important health indicators
- Recommended precautions based on risk level
- Healthy lifestyle guidance
- Diet and nutrition recommendations
- Clean healthcare dashboard UI

---

## Tech Stack

- **Python**
- **Pandas**
- **NumPy**
- **Scikit-learn**
- **Joblib**
- **Streamlit**

---

## Project Structure

```bash
neurocare-ai-stroke-risk-dashboard/
│
├── app.py
├── predict.py
├── train_model.py
├── stroke_model.pkl
├── stroke_scaler.pkl
├── stroke_columns.pkl
├── requirements.txt
└── README.md
