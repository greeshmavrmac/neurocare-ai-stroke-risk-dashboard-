import joblib
import pandas as pd

# Load saved model files
model = joblib.load("stroke_model.pkl")
scaler = joblib.load("stroke_scaler.pkl")
columns = joblib.load("stroke_columns.pkl")


def predict_stroke(age, hypertension, heart_disease, avg_glucose_level, bmi,
                   gender, ever_married, work_type, residence_type, smoking_status):

    # Create input dictionary with all training columns
    input_data = {col: 0 for col in columns}

    # Numerical features
    input_data["age"] = age
    input_data["hypertension"] = hypertension
    input_data["heart_disease"] = heart_disease
    input_data["avg_glucose_level"] = avg_glucose_level
    input_data["bmi"] = bmi

    # Gender
    if gender == "Male" and "gender_Male" in input_data:
        input_data["gender_Male"] = 1
    elif gender == "Other" and "gender_Other" in input_data:
        input_data["gender_Other"] = 1

    # Ever married
    if ever_married == "Yes" and "ever_married_Yes" in input_data:
        input_data["ever_married_Yes"] = 1

    # Work type
    work_col = f"work_type_{work_type}"
    if work_col in input_data:
        input_data[work_col] = 1

    # Residence type
    if residence_type == "Urban" and "Residence_type_Urban" in input_data:
        input_data["Residence_type_Urban"] = 1

    # Smoking status
    smoke_col = f"smoking_status_{smoking_status}"
    if smoke_col in input_data:
        input_data[smoke_col] = 1

    # Convert to DataFrame with correct column order
    input_df = pd.DataFrame([input_data])
    input_df = input_df[columns]

    # Scale the input
    input_scaled = scaler.transform(input_df)

    # Predict stroke risk
    prediction = model.predict(input_scaled)[0]
    probability = model.predict_proba(input_scaled)[0][1]

    return prediction, probability