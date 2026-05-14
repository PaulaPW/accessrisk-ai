import streamlit as st
import pandas as pd
import plotly.express as px
import requests

st.set_page_config(page_title="AccessRisk AI", layout="wide")

st.title("🔐 AccessRisk AI Dashboard")

df = pd.read_csv("data/raw/synthetic_access_logs.csv")

st.subheader("Dataset Overview")
st.dataframe(df.head())

risk_counts = df["risk_level"].value_counts().reset_index()
risk_counts.columns = ["Risk Level", "Count"]

fig = px.bar(
    risk_counts,
    x="Risk Level",
    y="Count",
    color="Risk Level",
    title="Threat Distribution"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("High Risk Events")

high_risk = df[df["risk_level"] == "High Risk"]

st.dataframe(high_risk.head(20))

country_fig = px.histogram(
    df,
    x="country",
    color="risk_level",
    title="Risk Events by Country"
)

st.plotly_chart(country_fig, use_container_width=True)
st.subheader("🔍 Live Threat Prediction")

with st.form("prediction_form"):

    country = st.selectbox("Country", ["US", "Canada", "UK", "Nigeria", "China"])
    role = st.selectbox("Role", ["employee", "manager", "service_account"])
    app = st.selectbox("Application", ["Slack", "AWS", "Salesforce", "Payroll"])

    failed_logins = st.slider("Failed Logins", 0, 10, 1)
    mfa_failures = st.slider("MFA Failures", 0, 5, 0)
    new_device = st.checkbox("New Device")
    new_country = st.checkbox("New Country")
    impossible_travel = st.checkbox("Impossible Travel")
    after_hours = st.checkbox("After Hours")
    privileged = st.checkbox("Privileged Account")
    sensitive_app = st.checkbox("Sensitive App")
    dormant_account = st.checkbox("Dormant Account")
    contractor = st.checkbox("Contractor")
    downloads = st.slider("Large Downloads", 0, 100, 5)

    submitted = st.form_submit_button("Analyze Threat")

if submitted:

    payload = {
        "country": country,
        "role": role,
        "app": app,
        "failed_logins": failed_logins,
        "mfa_failures": mfa_failures,
        "new_device": int(new_device),
        "new_country": int(new_country),
        "impossible_travel": int(impossible_travel),
        "after_hours": int(after_hours),
        "privileged": int(privileged),
        "sensitive_app": int(sensitive_app),
        "dormant_account": int(dormant_account),
        "contractor": int(contractor),
        "downloads": downloads
    }

    response = requests.post(
        "http://127.0.0.1:8000/predict",
        json=payload
    )

    result = response.json()

    st.success(f"Risk Level: {result['risk_level']}")
    st.write(f"Prediction ID: {result['prediction']}")
    st.write(f"Confidence: {result['confidence']}")
