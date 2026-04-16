import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="🌍 Climate Trend Analyzer",
    layout="wide",
    page_icon="🌍"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: white;
}
h1, h2, h3 {
    color: #00adb5;
}
.stButton>button {
    background: linear-gradient(90deg, #00adb5, #393e46);
    color: white;
    border-radius: 12px;
    height: 3em;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
# 🌍 Climate Trend Analyzer
### 📊 Analyze | ⚠️ Detect | 🔮 Predict Climate Patterns
---
""")

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚙️ Controls")

uploaded_file = st.sidebar.file_uploader("Upload Climate Dataset (CSV)", type=["csv"])
feature = st.sidebar.selectbox("Select Feature", ["Temperature", "Rainfall", "CO2"])
show_forecast = st.sidebar.checkbox("Enable Forecasting")

# ---------------- DATA LOADING FUNCTION ----------------
@st.cache_data
def load_data(file):
    df = pd.read_csv(file)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')
    return df

# ---------------- DATA LOADING WITH SPINNER ----------------
with st.spinner("🔄 Analyzing climate data... Please wait"):
    time.sleep(1)

    if uploaded_file:
        df = load_data(uploaded_file)
    else:
        # Generate synthetic data (FIXED: freq='ME')
        dates = pd.date_range(start="2000-01-01", periods=300, freq='ME')
        df = pd.DataFrame({
            "Date": dates,
            "Temperature": np.linspace(20, 30, 300) + np.random.normal(0, 1, 300),
            "Rainfall": np.random.normal(100, 20, 300),
            "CO2": np.linspace(300, 420, 300) + np.random.normal(0, 5, 300)
        })

# ---------------- METRICS ----------------
col1, col2, col3 = st.columns(3)

col1.metric("Avg Value", round(df[feature].mean(), 2))
col2.metric("Max Value", round(df[feature].max(), 2))
col3.metric("Min Value", round(df[feature].min(), 2))

# ---------------- MAIN LAYOUT ----------------
col1, col2 = st.columns([2, 1])

# ---------------- TREND GRAPH ----------------
with col1:
    st.subheader(f"📈 {feature} Trend Over Time")

    fig, ax = plt.subplots()
    ax.plot(df['Date'], df[feature], label=feature)
    ax.set_title(f"{feature} Trend")
    ax.legend()
    st.pyplot(fig)

# ---------------- ANOMALY DETECTION ----------------
with col2:
    st.subheader("⚠️ Anomaly Detection")

    mean = df[feature].mean()
    std = df[feature].std()

    df['Anomaly'] = (df[feature] > mean + 2*std) | (df[feature] < mean - 2*std)
    anomalies = df[df['Anomaly']]

    st.write(f"Detected Anomalies: {len(anomalies)}")

    if not anomalies.empty:
        st.dataframe(anomalies[['Date', feature]])

# ---------------- FORECASTING ----------------
if show_forecast:
    st.subheader("🔮 Forecasting Future Trend")

    with st.spinner("📊 Generating forecast..."):
        time.sleep(1)

        df['Time'] = np.arange(len(df))

        model = LinearRegression()
        model.fit(df[['Time']], df[feature])

        future_steps = 50
        future_time = np.arange(len(df), len(df) + future_steps).reshape(-1, 1)
        predictions = model.predict(future_time)

        # FIXED: freq='ME'
        future_dates = pd.date_range(df['Date'].iloc[-1], periods=future_steps, freq='ME')

        fig2, ax2 = plt.subplots()
        ax2.plot(df['Date'], df[feature], label="Actual")
        ax2.plot(future_dates, predictions, label="Forecast", linestyle="dashed")
        ax2.legend()
        st.pyplot(fig2)

# ---------------- HEATMAP ----------------
st.subheader("🔥 Correlation Heatmap")

corr = df[['Temperature', 'Rainfall', 'CO2']].corr()

fig3, ax3 = plt.subplots()
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax3)
st.pyplot(fig3)

# ---------------- FOOTER ----------------
st.markdown("""
---
👨‍💻 Developed by **Om Navgire**  
🎓 Guided by **Umesh Yadav Sir (EDC IIT Delhi)**  
""")