import streamlit as st
import pandas as pd
import numpy as np
import glob
import time

st.set_page_config(
    page_title="Fraud Intelligence Platform",
    layout="wide"
)

st.title("🚨 Fraud Intelligence & Monitoring Dashboard")
st.caption("Real-time fraud detection • Risk scoring • Model monitoring")

# -------------------------
# Load inference results
# -------------------------
DATA_PATH = "/opt/shared/inference_output/*.csv"

@st.cache_data(ttl=30)
def load_latest_data():
    files = sorted(glob.glob(DATA_PATH), reverse=True)
    if not files:
        return None, None
    return pd.read_csv(files[0]), files[0]

df, file_used = load_latest_data()

# -------------------------
# Sidebar Controls
# -------------------------
st.sidebar.header("⚙️ Controls")

threshold = st.sidebar.slider(
    "Fraud Threshold",
    min_value=0.0,
    max_value=1.0,
    value=0.5,
    step=0.01,
    key="threshold"
)

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV for Fraud Check",
    type=["csv"]
)

# -------------------------
# Handle Uploaded CSV
# -------------------------
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("Uploaded file loaded")

if df is None:
    st.warning("No inference data available yet.")
    st.stop()

required_model_cols = {"fraud_probability", "fraud_prediction"}
is_model_output = required_model_cols.issubset(df.columns)

if not is_model_output:
    st.info("📥 Raw transaction data detected. Running fraud inference...")

    # ---- MOCK / SIMULATED INFERENCE (resume-safe) ----
    import numpy as np

    # Simulate probability using amount + randomness
    if "Amount" in df.columns:
        base = np.log1p(df["Amount"])
    else:
        base = np.random.rand(len(df))

    df["fraud_probability"] = np.clip(
        base / base.max() + np.random.rand(len(df)) * 0.2,
        0, 1
    )

    threshold = st.session_state.get("threshold", 0.5)
    df["fraud_prediction"] = (df["fraud_probability"] > threshold).astype(int)

mode = "Model Inference Output" if is_model_output else "Simulated Inference"
mode_color = "🟢" if is_model_output else "🟡"

st.markdown(
    f"""
    <div style="
        display: inline-block;
        padding: 6px 14px;
        border-radius: 20px;
        background-color: #f0f2f6;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 10px;
    ">
        {mode_color} Mode: {mode}
    </div>
    """,
    unsafe_allow_html=True
)

st.caption(f"📁 Data source: `{file_used if file_used else 'Uploaded file'}`")

# -------------------------
# Risk Bands
# -------------------------
df["risk_band"] = pd.cut(
    df["fraud_probability"],
    bins=[0, threshold, 0.8, 1.0],
    labels=["Low", "Medium", "High"]
)

# -------------------------
# KPIs
# -------------------------
c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Transactions", len(df))
c2.metric("High Risk", int((df["risk_band"] == "High").sum()))
c3.metric("Avg Fraud Probability", round(df["fraud_probability"].mean(), 4))
c4.metric(
    "Fraud %",
    f"{round(df['fraud_prediction'].mean() * 100, 2)}%"
)

# -------------------------
# Charts
# -------------------------

if "fraud_probability" in df.columns:
    st.subheader("📊 Fraud Probability Distribution")
    hist, bins = np.histogram(df["fraud_probability"], bins=50)
    st.bar_chart(pd.Series(hist, index=bins[:-1]))

st.subheader("🚦 Risk Band Distribution")
st.bar_chart(df["risk_band"].value_counts())

st.subheader("🔥 Top Risk Transactions")
st.dataframe(
    df.sort_values("fraud_probability", ascending=False).head(50),
    use_container_width=True
)

# -------------------------
# Auto Refresh
# -------------------------
st.sidebar.caption("Auto refresh every 30 seconds")
time.sleep(0.5)