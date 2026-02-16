import streamlit as st
import joblib
import os

# Load trained model safely
model_path = os.path.join(os.getcwd(), "student_model.pkl")
model = joblib.load(model_path)

# Title
st.title("Student Result Prediction System")

st.write("Enter student details to predict result")

# Inputs
study = st.number_input("Study Hours", min_value=0.0)

attendance = st.number_input(
    "Attendance (%)",
    min_value=0.0,
    max_value=100.0
)

internal = st.number_input(
    "Internal Marks",
    min_value=0.0
)

# New Inputs
assignment = st.selectbox(
    "Assignment Submitted?",
    ["No", "Yes"]
)

previous_result = st.selectbox(
    "Previous Semester Result",
    ["Fail", "Pass"]
)

# Convert text input to numeric
assignment_val = 1 if assignment == "Yes" else 0
previous_val = 1 if previous_result == "Pass" else 0


# Prediction Button
if st.button("Predict Result"):

    # Prediction
    result = model.predict([[
        study,
        attendance,
        internal,
        assignment_val,
        previous_val
    ]])

    prob = model.predict_proba([[
        study,
        attendance,
        internal,
        assignment_val,
        previous_val
    ]])

    confidence = max(prob[0]) * 100

    # Result Display
    st.subheader("Prediction Result")
    st.success("Result: " + result[0])

    # Confidence
    st.write("Confidence Level:", round(confidence, 2), "%")
    st.progress(int(confidence))

    # Confidence category
    if confidence < 50:
        st.warning("Confidence: Low")
    elif confidence < 75:
        st.info("Confidence: Medium")
    else:
        st.success("Confidence: High")

    # Risk Analysis
    st.subheader("Risk Analysis")

    if result[0] == "Fail":
        st.error("High Risk Student")
    else:
        if confidence < 60:
            st.warning("Medium Risk Student")
        else:
            st.success("Low Risk Student")

