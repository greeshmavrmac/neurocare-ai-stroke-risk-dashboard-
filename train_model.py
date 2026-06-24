import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

# Load dataset
df = pd.read_csv(r"C:\Users\150 LAB\Downloads\healthcare-dataset-stroke-data.csv")

# Fill missing BMI values
df["bmi"] = df["bmi"].fillna(df["bmi"].median())

# Drop id column
if "id" in df.columns:
    df.drop("id", axis=1, inplace=True)

# Convert categorical columns to dummy variables
df = pd.get_dummies(df, drop_first=True)

# Features and target
X = df.drop("stroke", axis=1)
y = df["stroke"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Scale data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# Train model
model = RandomForestClassifier(class_weight="balanced", random_state=42)
model.fit(X_train_scaled, y_train)

# Save model, scaler, and columns
joblib.dump(model, "stroke_model.pkl")
joblib.dump(scaler, "stroke_scaler.pkl")
joblib.dump(X.columns.tolist(), "stroke_columns.pkl")

print("Model, scaler, and columns saved successfully!")