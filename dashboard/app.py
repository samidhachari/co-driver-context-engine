import streamlit as st
import requests
import pandas as pd
import json
import os

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Co-Driver Dashboard", layout="wide")

st.title("Co-Driver Context Engine Dashboard")

# -------------------------------
# SECTION 1: INPUT + PREDICTION
# -------------------------------
st.header("Live Context Prediction")

col1, col2 = st.columns(2)

with col1:
    user_text = st.text_input("Driver Input", "I feel tired")
    battery = st.slider("Battery Level", 0, 100, 20)

with col2:
    time = st.text_input("Time (HH:MM)", "23:30")
    location = st.selectbox("Location", ["city", "highway", "rural"])

if st.button("Analyze"):
    try:
        response = requests.post(
            f"{API_URL}/analyze",
            json={
                "user_text": user_text,
                "battery": battery,
                "time": time,
                "location": location
            },
            timeout=5
        )

        if response.status_code == 200:
            data = response.json()

            st.subheader("Prediction Result")
            st.json(data)

            st.metric("Final Risk", data.get("risk_level", "N/A"))
            st.metric("ML Confidence", data.get("confidence_score", 0))
            st.metric("Decision Source", data.get("decision_source", "N/A"))

        else:
            st.error(f"API Error: {response.status_code}")

    except requests.exceptions.RequestException:
        st.error("Cannot connect to FastAPI. Is backend running?")

# -------------------------------
# SECTION 2: RULE ANALYTICS
# -------------------------------
st.header("Rule Frequency Analytics")

if st.button("Load Rule Stats"):
    try:
        res = requests.get(f"{API_URL}/analytics/rules", timeout=5)

        if res.status_code == 200:
            data = res.json().get("rule_frequency", {})

            if data:
                df = pd.DataFrame(list(data.items()), columns=["Rule", "Count"])
                st.bar_chart(df.set_index("Rule"))
            else:
                st.info("No data yet")

        else:
            st.error(f"API Error: {res.status_code}")

    except requests.exceptions.RequestException:
        st.error("Cannot fetch rule analytics")

# -------------------------------
# SECTION 3: DRIFT ANALYTICS
# -------------------------------
st.header("Drift Detection")

if st.button("Check Drift"):
    try:
        res = requests.get(f"{API_URL}/analytics/drift", timeout=5)

        if res.status_code == 200:
            data = res.json()

            st.metric("Drift Rate", data.get("drift_rate", 0))
            st.metric("Total Samples", data.get("total_samples", 0))
            st.metric("Mismatch Count", data.get("mismatch_count", 0))

        else:
            st.error(f"API Error: {res.status_code}")

    except requests.exceptions.RequestException:
        st.error("Cannot fetch drift data")

# -------------------------------
# SECTION 4: RECENT LOGS
# -------------------------------
st.header("Recent Decisions")

LOG_PATH = os.path.join(os.path.dirname(__file__), "..", "logs", "decisions.jsonl")

try:
    logs = []

    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r") as f:
            lines = f.readlines()[-10:]  # last 10 logs

            for line in lines:
                logs.append(pd.json_normalize(json.loads(line)))

        if logs:
            df_logs = pd.concat(logs, ignore_index=True)
            st.dataframe(df_logs)
        else:
            st.info("No logs yet")

    else:
        st.warning("No logs file found")

except Exception as e:
    st.error(f"Error reading logs: {str(e)}")





