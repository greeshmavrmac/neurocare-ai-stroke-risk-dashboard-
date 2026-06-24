import streamlit as st
from predict import predict_stroke

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="NeuroCare Stroke Risk Dashboard",
    page_icon="🧠",
    layout="wide"
)

# =========================================================
# SESSION STATE
# =========================================================
if "prediction_done" not in st.session_state:
    st.session_state.prediction_done = False
if "prediction" not in st.session_state:
    st.session_state.prediction = None
if "probability" not in st.session_state:
    st.session_state.probability = None
if "patient_data" not in st.session_state:
    st.session_state.patient_data = {}
if "error_message" not in st.session_state:
    st.session_state.error_message = None

# =========================================================
# CSS
# =========================================================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #fffaf8 0%, #fff6f8 100%);
    color: #1f2937;
}
.block-container {
    max-width: 1450px;
    padding-top: 0.9rem;
    padding-bottom: 1.2rem;
}
[data-testid="stHeader"] {
    background: transparent;
}
[data-testid="stToolbar"] {
    right: 1rem;
}

/* Header */
.hero-wrap {
    padding-top: 4px;
}
.hero-title {
    font-size: 2.3rem;
    font-weight: 800;
    color: #1f2a5a;
    line-height: 1.2;
    margin: 0;
}
.hero-title span {
    color: #b0235d;
}
.hero-sub {
    font-size: 1rem;
    color: #616a78;
    margin-top: 8px;
    line-height: 1.6;
}

/* Main cards */
.main-card,
.soft-card,
.guidance-card {
    background: linear-gradient(180deg, #fffdfd 0%, #fff9f8 100%);
    border: 1px solid #eadfdf;
    border-radius: 22px;
    box-shadow: 0 8px 22px rgba(0,0,0,0.05);
    padding: 18px;
    height: 100%;
}
.soft-card {
    background: linear-gradient(180deg, #fffdfd 0%, #fff7fb 100%);
    border: 1px solid #efdee6;
}
.card-head {
    font-size: 1.75rem;
    font-weight: 700;
    color: #1f2a52;
    margin-bottom: 2px;
}
.card-sub {
    color: #6b7280;
    font-size: 0.97rem;
    margin-bottom: 14px;
}
.small-head {
    font-size: 1.18rem;
    font-weight: 700;
    color: #243152;
    margin-bottom: 10px;
}

/* Top feature cards */
.top-feature {
    background: linear-gradient(180deg, #fffdfd 0%, #fff7f9 100%);
    border: 1px solid #eadfe3;
    border-radius: 18px;
    padding: 12px;
    min-height: 88px;
    display: flex;
    align-items: center;
    gap: 10px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.04);
}
.top-icon {
    width: 42px;
    height: 42px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #faf4f7;
    font-size: 20px;
    flex-shrink: 0;
}
.top-title {
    font-size: 0.96rem;
    font-weight: 700;
    color: #243152;
    margin-bottom: 2px;
}
.top-sub {
    color: #6b7280;
    font-size: 0.90rem;
    line-height: 1.35;
}

/* Details box */
.details-box {
    background: linear-gradient(180deg, #fffdfb 0%, #fff8f4 100%);
    border: 1px solid #ece0d6;
    border-radius: 16px;
    padding: 14px 16px;
    margin-top: 14px;
}
.details-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #1f2a52;
    margin-bottom: 8px;
}
.details-box ul {
    margin: 0;
    padding-left: 18px;
}
.details-box li {
    margin-bottom: 6px;
    color: #374151;
    font-size: 0.95rem;
}

/* Button */
div.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #b81f56 0%, #ef445d 100%);
    color: white;
    border: none;
    border-radius: 14px;
    padding: 14px 16px;
    font-size: 1.05rem;
    font-weight: 700;
    box-shadow: 0 10px 20px rgba(214, 51, 102, 0.26);
}
div.stButton > button:hover {
    background: linear-gradient(90deg, #ad1c50 0%, #e53e5b 100%);
}

/* Result banner */
.result-banner {
    background: linear-gradient(180deg, #fff7f7 0%, #fff4f4 100%);
    border: 1px solid #f1d9d9;
    border-radius: 18px;
    padding: 16px;
    min-height: 118px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.result-title-high {
    font-size: 1.8rem;
    font-weight: 800;
    color: #dc2626;
    margin-bottom: 4px;
}
.result-title-low {
    font-size: 1.8rem;
    font-weight: 800;
    color: #15803d;
    margin-bottom: 4px;
}
.result-desc {
    color: #374151;
    font-size: 1rem;
    line-height: 1.6;
}

/* Probability box */
.prob-box {
    background: linear-gradient(180deg, #fffdfd 0%, #fff7f7 100%);
    border: 1px solid #efd7d7;
    border-radius: 16px;
    text-align: center;
    padding: 14px;
    min-height: 118px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.prob-label {
    color: #374151;
    font-size: 1rem;
    font-weight: 700;
    margin-bottom: 6px;
}
.prob-high {
    color: #dc2626;
    font-size: 2rem;
    font-weight: 800;
}
.prob-mid {
    color: #d97706;
    font-size: 2rem;
    font-weight: 800;
}
.prob-low {
    color: #15803d;
    font-size: 2rem;
    font-weight: 800;
}

/* Risk bar */
.risk-bar {
    width: 100%;
    height: 18px;
    border-radius: 999px;
    background: linear-gradient(90deg, #22c55e 0%, #facc15 50%, #ef4444 100%);
    position: relative;
    margin-top: 16px;
    box-shadow: inset 0 1px 3px rgba(0,0,0,0.08);
}
.risk-thumb {
    position: absolute;
    top: 50%;
    transform: translate(-50%, -50%);
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: white;
    border: 2px solid #f3f4f6;
    box-shadow: 0 3px 10px rgba(0,0,0,0.18);
}
.risk-labels {
    display: flex;
    justify-content: space-between;
    margin-top: 8px;
    color: #4b5563;
    font-size: 0.94rem;
    font-weight: 500;
}

/* Metric cards */
.metric-card {
    background: linear-gradient(180deg, #fffdfd 0%, #fff9f5 100%);
    border: 1px solid #ece2de;
    border-radius: 16px;
    padding: 16px;
    min-height: 118px;
}
.metric-title {
    font-size: 1rem;
    color: #374151;
    margin-bottom: 6px;
}
.metric-value {
    font-size: 1.95rem;
    font-weight: 800;
    color: #1f2937;
    line-height: 1.1;
}
.metric-sub {
    font-size: 0.98rem;
    color: #4b5563;
    margin-top: 3px;
}

/* Risk factors */
.section-box {
    background: linear-gradient(180deg, #fffdfd 0%, #fff8f8 100%);
    border: 1px solid #f0dddd;
    border-radius: 16px;
    padding: 16px;
    margin-top: 16px;
}
.chips-wrap {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    margin-top: 10px;
}
.chip {
    display: inline-block;
    background: linear-gradient(180deg, #fff9f9 0%, #fff4f4 100%);
    border: 1px solid #efd7d7;
    color: #374151;
    padding: 10px 14px;
    border-radius: 14px;
    font-size: 0.95rem;
}

/* Clinical box */
.clinical-box {
    background: linear-gradient(180deg, #fff7f7 0%, #fffdfd 100%);
    border: 1.5px solid #ef4444;
    border-radius: 18px;
    padding: 16px;
    margin-top: 16px;
}
.badge-critical {
    background: linear-gradient(90deg, #b91c1c 0%, #be123c 100%);
    color: white;
    padding: 8px 16px;
    border-radius: 12px;
    font-size: 0.92rem;
    font-weight: 700;
    text-align: center;
}
.badge-moderate {
    background: linear-gradient(90deg, #d97706 0%, #ea580c 100%);
    color: white;
    padding: 8px 16px;
    border-radius: 12px;
    font-size: 0.92rem;
    font-weight: 700;
    text-align: center;
}
.badge-low {
    background: linear-gradient(90deg, #15803d 0%, #16a34a 100%);
    color: white;
    padding: 8px 16px;
    border-radius: 12px;
    font-size: 0.92rem;
    font-weight: 700;
    text-align: center;
}
.clinical-body {
    background: white;
    border: 1px solid #f3e2e2;
    border-radius: 14px;
    padding: 16px;
    color: #374151;
    font-size: 1rem;
    line-height: 1.7;
    margin-top: 12px;
}

/* Bottom guidance */
.guidance-list {
    margin-top: 10px;
    padding-left: 18px;
}
.guidance-list li {
    margin-bottom: 10px;
    color: #374151;
    line-height: 1.65;
}
.guidance-mini {
    background: white;
    border: 1px solid #ece2de;
    border-radius: 16px;
    padding: 14px 16px;
    height: 100%;
}
.note-text {
    text-align: center;
    color: #6b7280;
    font-size: 0.9rem;
    margin-top: 8px;
}

/* Inputs */
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    border-radius: 12px !important;
}
label {
    font-weight: 600 !important;
    color: #374151 !important;
}

@media (max-width: 1200px) {
    .hero-title {
        font-size: 2rem;
    }
    .top-feature {
        min-height: 76px;
        padding: 10px;
    }
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# HELPERS
# =========================================================
def bmi_label(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    return "Obesity"

def risk_badge(prob):
    if prob >= 0.70:
        return "HIGH", "badge-critical"
    elif prob >= 0.40:
        return "MODERATE", "badge-moderate"
    return "LOW", "badge-low"

def get_risk_factors(data):
    factors = []
    if data.get("age", 0) >= 55:
        factors.append("🧓 Age above 55")
    if data.get("hypertension", 0) == 1:
        factors.append("❤️ Hypertension")
    if data.get("avg_glucose_level", 0) > 140:
        factors.append("🩸 High glucose level")
    if data.get("bmi", 0) >= 27:
        factors.append("⚖️ High BMI / obesity")
    if data.get("smoking_status", "") in ["smokes", "formerly smoked"]:
        factors.append("🚬 Smoking history")
    if data.get("heart_disease", 0) == 1:
        factors.append("🫀 Heart disease")
    return factors

def clinical_message(prob):
    if prob >= 0.70:
        return (
            "The patient shows a high stroke risk profile based on the entered health indicators. "
            "Risk appears elevated due to one or more important clinical factors such as blood pressure, glucose level, BMI, heart condition, or smoking history. "
            "This case needs stronger lifestyle control, regular medical monitoring, and early preventive action to reduce future stroke complications."
        )
    elif prob >= 0.40:
        return (
            "The patient falls into a moderate stroke risk category. "
            "While the current condition may not indicate immediate danger, some health indicators suggest that stroke risk could increase over time if not managed properly. "
            "At this stage, improving diet, physical activity, sleep, stress control, and routine health monitoring can make a major difference."
        )
    else:
        return (
            "The patient currently shows a relatively stable and lower stroke risk profile based on the provided details. "
            "No major warning pattern is strongly indicated by the model at this time. "
            "However, stroke prevention should still focus on maintaining healthy blood pressure, good glucose control, balanced body weight, regular exercise, and periodic health checkups."
        )

def generate_precautions(data, prob):
    precautions = []

    if prob >= 0.70:
        precautions.extend([
            "Consult a physician or neurologist for a detailed stroke risk evaluation and ongoing monitoring.",
            "Maintain strict blood pressure control through medication adherence, low-salt diet and regular BP tracking.",
            "Control blood sugar aggressively with diet planning, doctor follow-up and reduced refined carbohydrates.",
            "Follow a structured weight-management and daily walking plan to improve cardiovascular health.",
            "Completely avoid smoking and tobacco exposure; it significantly increases stroke and heart disease risk."
        ])
    elif prob >= 0.40:
        precautions.extend([
            "Start regular monitoring of blood pressure, glucose and weight to prevent progression of stroke risk.",
            "Reduce fried foods, excess salt, bakery items and sugary drinks from the diet.",
            "Include at least 30 minutes of walking or light exercise on most days of the week.",
            "If there is smoking history, work on complete smoking cessation and better lung-heart health.",
            "Schedule routine health checkups and follow your doctor’s advice for early prevention."
        ])
    else:
        precautions.extend([
            "Continue maintaining a healthy routine with balanced food, regular sleep and physical activity.",
            "Do preventive screening for blood pressure, glucose and cholesterol at regular intervals.",
            "Avoid smoking, stress overload and long sedentary hours to keep stroke risk low.",
            "Stay hydrated and keep body weight within a healthy range.",
            "Follow annual or periodic health checkups to maintain long-term cardiovascular health."
        ])

    return precautions[:5]

def generate_healthy_tips(prob):
    if prob >= 0.70:
        return [
            "Walk regularly if medically safe, and avoid prolonged sitting for many hours.",
            "Sleep 7–8 hours daily because poor sleep can worsen BP, sugar and heart health.",
            "Practice stress reduction using meditation, breathing exercises or light yoga.",
            "Take medicines on time if you already have BP, diabetes or heart-related conditions.",
            "Keep a weekly record of BP, sugar, weight and daily activity for follow-up."
        ]
    elif prob >= 0.40:
        return [
            "Exercise for at least 30 minutes on most days, even brisk walking helps.",
            "Stay hydrated and avoid long inactive sitting periods during the day.",
            "Improve sleep quality and reduce late-night snacking or irregular meal timing.",
            "Do stress management through stretching, walking, meditation or breathing exercises.",
            "Aim for gradual weight reduction if BMI is elevated."
        ]
    else:
        return [
            "Continue regular exercise such as walking, cycling or yoga to maintain heart health.",
            "Eat on time, stay hydrated and avoid a highly sedentary routine.",
            "Maintain 7–8 hours of quality sleep and consistent daily routine.",
            "Manage stress with relaxation habits, hobbies or light meditation.",
            "Keep monitoring health parameters periodically even if current risk is low."
        ]

def generate_diet_tips(prob):
    if prob >= 0.70:
        return [
            "Follow a low-salt, low-sugar diet with more vegetables, leafy greens and high-fiber foods.",
            "Choose oats, brown rice, millets, dal, sprouts and whole grains instead of refined foods.",
            "Avoid deep-fried foods, bakery items, processed snacks, packaged juices and sugary beverages.",
            "Prefer boiled, steamed or lightly cooked meals with lean protein like dal, paneer, egg white or fish if suitable.",
            "Limit red meat, excess oil and restaurant food; prioritize simple home-cooked meals."
        ]
    elif prob >= 0.40:
        return [
            "Choose home-cooked meals over processed or fast food whenever possible.",
            "Increase fiber intake using fruits, vegetables, oats, brown rice and pulses.",
            "Reduce sugar, excess salt, deep-fried snacks and soft drinks.",
            "Prefer healthy fats like nuts, seeds and limited oil instead of repeated fried foods.",
            "Balance each meal with protein + vegetables + complex carbs."
        ]
    else:
        return [
            "Maintain a balanced diet with fruits, vegetables, whole grains and protein sources.",
            "Keep processed food, sugary drinks and fried snacks limited even if risk is low.",
            "Use healthy meal portions and avoid overeating late at night.",
            "Include nuts, seeds, curd, dal and fresh home-cooked foods regularly.",
            "Continue a heart-friendly diet to preserve your current low-risk profile."
        ]

# =========================================================
# DEFAULT VALUES
# =========================================================
if st.session_state.prediction_done:
    pdata = st.session_state.patient_data
    default_gender = pdata.get("gender", "Male")
    default_age = int(pdata.get("age", 45))
    default_hypertension = int(pdata.get("hypertension", 0))
    default_heart_disease = int(pdata.get("heart_disease", 0))
    default_ever_married = pdata.get("ever_married", "No")
    default_work_type = pdata.get("work_type", "Private")
    default_residence_type = pdata.get("residence_type", "Urban")
    default_glucose = float(pdata.get("avg_glucose_level", 100.0))
    default_bmi = float(pdata.get("bmi", 24.0))
    default_smoking = pdata.get("smoking_status", "never smoked")
else:
    default_gender = "Male"
    default_age = 45
    default_hypertension = 0
    default_heart_disease = 0
    default_ever_married = "No"
    default_work_type = "Private"
    default_residence_type = "Urban"
    default_glucose = 100.0
    default_bmi = 24.0
    default_smoking = "never smoked"

# =========================================================
# HEADER
# =========================================================
header_left, header_right = st.columns([1.65, 1.05], gap="large")

with header_left:
    st.markdown('<div class="hero-wrap">', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-title">🧠 NeuroCare <span>Stroke Risk Dashboard</span></div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="hero-sub">AI-Powered risk assessment with preventive insights for better health outcomes</div>',
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

with header_right:
    t1, t2, t3 = st.columns(3)
    with t1:
        st.markdown("""
        <div class="top-feature">
            <div class="top-icon" style="color:#2563eb;">ⓘ</div>
            <div>
                <div class="top-title">Early Detection</div>
                <div class="top-sub">Better Prevention</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with t2:
        st.markdown("""
        <div class="top-feature">
            <div class="top-icon" style="color:#16a34a;">🛡️</div>
            <div>
                <div class="top-title">Know Your Risk</div>
                <div class="top-sub">Protect Your Future</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with t3:
        st.markdown("""
        <div class="top-feature">
            <div class="top-icon" style="color:#e11d48;">♡</div>
            <div>
                <div class="top-title">Stay Healthy</div>
                <div class="top-sub">Live Better</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)

# =========================================================
# MAIN LAYOUT
# =========================================================
left_col, right_col = st.columns([1.02, 1.18], gap="large")

# =========================================================
# LEFT - FORM
# =========================================================
with left_col:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-head">🧾 Patient Intake Form</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-sub">Enter patient details to assess stroke risk</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        gender = st.selectbox("Gender", ["Male", "Female"], index=["Male", "Female"].index(default_gender))
        age = st.number_input("Age (Years)", min_value=1, max_value=120, value=default_age)
        hypertension = st.selectbox(
            "Hypertension", [0, 1],
            index=[0, 1].index(default_hypertension),
            format_func=lambda x: "Yes (1)" if x == 1 else "No (0)"
        )
        heart_disease = st.selectbox(
            "Heart Disease", [0, 1],
            index=[0, 1].index(default_heart_disease),
            format_func=lambda x: "Yes (1)" if x == 1 else "No (0)"
        )
        ever_married = st.selectbox("Ever Married", ["Yes", "No"], index=["Yes", "No"].index(default_ever_married))

    with c2:
        work_type = st.selectbox(
            "Work Type",
            ["Private", "Self-employed", "Govt_job", "children", "Never_worked"],
            index=["Private", "Self-employed", "Govt_job", "children", "Never_worked"].index(default_work_type)
        )
        residence_type = st.selectbox(
            "Residence Type", ["Urban", "Rural"],
            index=["Urban", "Rural"].index(default_residence_type)
        )
        avg_glucose_level = st.number_input("Average Glucose Level", min_value=0.0, value=default_glucose)
        bmi = st.number_input("BMI", min_value=0.0, value=default_bmi)
        smoking_status = st.selectbox(
            "Smoking Status",
            ["formerly smoked", "never smoked", "smokes", "Unknown"],
            index=["formerly smoked", "never smoked", "smokes", "Unknown"].index(default_smoking)
        )

    st.markdown('<div class="details-box">', unsafe_allow_html=True)
    st.markdown('<div class="details-title">📋 Details Given:</div>', unsafe_allow_html=True)

    d1, d2 = st.columns(2)
    with d1:
        st.markdown(f"""
        <ul>
            <li><b>Gender:</b> {gender}</li>
            <li><b>Age:</b> {age}</li>
            <li><b>Hypertension:</b> {"Yes" if hypertension == 1 else "No"}</li>
            <li><b>Heart Disease:</b> {"Yes" if heart_disease == 1 else "No"}</li>
            <li><b>Ever Married:</b> {ever_married}</li>
        </ul>
        """, unsafe_allow_html=True)

    with d2:
        st.markdown(f"""
        <ul>
            <li><b>Work Type:</b> {work_type}</li>
            <li><b>Residence:</b> {residence_type}</li>
            <li><b>Glucose Level:</b> {avg_glucose_level}</li>
            <li><b>BMI:</b> {bmi}</li>
            <li><b>Smoking:</b> {smoking_status}</li>
        </ul>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🫀 Predict Stroke Risk"):
        try:
            prediction, probability = predict_stroke(
                age,
                hypertension,
                heart_disease,
                avg_glucose_level,
                bmi,
                gender,
                ever_married,
                work_type,
                residence_type,
                smoking_status
            )

            st.session_state.prediction_done = True
            st.session_state.prediction = prediction
            st.session_state.probability = probability
            st.session_state.error_message = None
            st.session_state.patient_data = {
                "age": age,
                "hypertension": hypertension,
                "heart_disease": heart_disease,
                "avg_glucose_level": avg_glucose_level,
                "bmi": bmi,
                "gender": gender,
                "ever_married": ever_married,
                "work_type": work_type,
                "residence_type": residence_type,
                "smoking_status": smoking_status
            }
            st.rerun()

        except Exception as e:
            st.session_state.error_message = str(e)
            st.session_state.prediction_done = False

    if st.session_state.error_message:
        st.error(st.session_state.error_message)

    st.markdown('<div class="note-text">Note: Please enter accurate details for reliable prediction results.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# RIGHT - RESULTS
# =========================================================
with right_col:
    st.markdown('<div class="soft-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-head">📊 Prediction Results</div>', unsafe_allow_html=True)

    if st.session_state.prediction_done:
        pdata = st.session_state.patient_data
        pred = st.session_state.prediction
        prob = st.session_state.probability

        banner_left, banner_right = st.columns([1.15, 0.42])

        with banner_left:
            st.markdown('<div class="result-banner">', unsafe_allow_html=True)
            if pred == 1:
                st.markdown('<div class="result-title-high">HIGHER STROKE RISK</div>', unsafe_allow_html=True)
                st.markdown('<div class="result-desc">This patient is at higher risk of stroke based on the clinical risk profile and model evaluation.</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="result-title-low">LOWER STROKE RISK</div>', unsafe_allow_html=True)
                st.markdown('<div class="result-desc">This patient is currently in a lower risk category based on the entered health indicators.</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with banner_right:
            if prob >= 0.70:
                prob_class = "prob-high"
            elif prob >= 0.40:
                prob_class = "prob-mid"
            else:
                prob_class = "prob-low"

            st.markdown(f"""
            <div class="prob-box">
                <div class="prob-label">Probability Score</div>
                <div class="{prob_class}">{prob*100:.2f}%</div>
            </div>
            """, unsafe_allow_html=True)

        thumb_position = min(max(prob * 100, 2), 98)
        st.markdown(f"""
        <div class="risk-bar">
            <div class="risk-thumb" style="left:{thumb_position}%;"></div>
        </div>
        <div class="risk-labels">
            <span>Low Risk</span>
            <span>Moderate Risk</span>
            <span>High Risk</span>
        </div>
        """, unsafe_allow_html=True)

        m1, m2, m3 = st.columns(3)

        with m1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Age</div>
                <div class="metric-value">{pdata['age']}</div>
                <div class="metric-sub">years</div>
            </div>
            """, unsafe_allow_html=True)

        with m2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">BMI</div>
                <div class="metric-value" style="color:#15803d;">{pdata['bmi']}</div>
                <div class="metric-sub">{bmi_label(pdata['bmi'])}</div>
            </div>
            """, unsafe_allow_html=True)

        with m3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Glucose Level</div>
                <div class="metric-value" style="color:#ea580c;">{pdata['avg_glucose_level']}</div>
                <div class="metric-sub">mg/dL</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.markdown('<div class="small-head">🧬 Risk Factor Highlights</div>', unsafe_allow_html=True)
        factors = get_risk_factors(pdata)

        if factors:
            chips_html = "".join([f"<div class='chip'>{item}</div>" for item in factors])
            st.markdown(f"<div class='chips-wrap'>{chips_html}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='chips-wrap'><div class='chip'>✅ No major risk factors highlighted</div></div>", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        badge_text, badge_class = risk_badge(prob)
        st.markdown('<div class="clinical-box">', unsafe_allow_html=True)

        c_title, c_badge = st.columns([1, 0.28])
        with c_title:
            st.markdown('<div class="small-head">🛡️ Clinical Interpretation</div>', unsafe_allow_html=True)
        with c_badge:
            st.markdown(f'<div class="{badge_class}">{badge_text}</div>', unsafe_allow_html=True)

        st.markdown(f'<div class="clinical-body">{clinical_message(prob)}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.info("Fill the patient form and click Predict Stroke Risk to generate the dashboard.")

    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# BOTTOM SECTION
# =========================================================
b1, b2 = st.columns([1.0, 1.18], gap="large")

with b1:
    st.markdown('<div class="guidance-card">', unsafe_allow_html=True)
    st.markdown('<div class="small-head" style="color:#15803d;">🛡️ Recommended Precautions</div>', unsafe_allow_html=True)

    if st.session_state.prediction_done:
        precautions = generate_precautions(
            st.session_state.patient_data,
            st.session_state.probability
        )
        precaution_html = "".join([f"<li>{item}</li>" for item in precautions])
        st.markdown(f'<ul class="guidance-list">{precaution_html}</ul>', unsafe_allow_html=True)
    else:
        st.markdown('<ul class="guidance-list"><li>Run a patient prediction to generate recommended precautions.</li></ul>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

with b2:
    st.markdown('<div class="guidance-card">', unsafe_allow_html=True)
    st.markdown('<div class="small-head" style="color:#7c3aed;">💜 Healthy Tips & Diet Guidance</div>', unsafe_allow_html=True)

    if st.session_state.prediction_done:
        healthy = generate_healthy_tips(st.session_state.probability)
        diet = generate_diet_tips(st.session_state.probability)

        g1, g2 = st.columns(2)

        with g1:
            healthy_html = "".join([f"<li>{item}</li>" for item in healthy])
            st.markdown(f"""
            <div class="guidance-mini">
                <h4 style="color:#7c3aed; margin-bottom:8px;">Healthy Lifestyle Tips</h4>
                <ul class="guidance-list">{healthy_html}</ul>
            </div>
            """, unsafe_allow_html=True)

        with g2:
            diet_html = "".join([f"<li>{item}</li>" for item in diet])
            st.markdown(f"""
            <div class="guidance-mini">
                <h4 style="color:#ea580c; margin-bottom:8px;">Diet & Nutrition Guidance</h4>
                <ul class="guidance-list">{diet_html}</ul>
            </div>
            """, unsafe_allow_html=True)
    else:
        g1, g2 = st.columns(2)
        with g1:
            st.markdown('<div class="guidance-mini">Healthy lifestyle tips will appear here after prediction.</div>', unsafe_allow_html=True)
        with g2:
            st.markdown('<div class="guidance-mini">Diet guidance will appear here after prediction.</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)