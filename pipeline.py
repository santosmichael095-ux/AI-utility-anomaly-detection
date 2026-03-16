import pandas as pd
import numpy as np
from glob import glob
import datetime as dt
from sklearn.ensemble import IsolationForest
import shap
import streamlit as st
import os

# ------------------------------------
# 1 DATA INGESTION
# ------------------------------------

DATA_PATH = "data/input/*.parquet"

files = glob(DATA_PATH)

if len(files) == 0:
    raise Exception("No input files found in data/input")

dfs = [pd.read_parquet(f) for f in files]

df_raw = pd.concat(dfs, ignore_index=True)

print("Raw data shape:", df_raw.shape)

# ------------------------------------
# 2 DATA CLEANING
# ------------------------------------

df_raw["reading_datetime"] = pd.to_datetime(
    df_raw["reading_datetime"],
    errors="coerce"
)

df = df_raw.dropna(subset=["reading_datetime"])

df = df.sort_values(["asset_id", "reading_datetime"])

# ------------------------------------
# 3 FEATURE ENGINEERING
# ------------------------------------

df["year_month"] = df["reading_datetime"].dt.to_period("M")

df = df.drop_duplicates(
    subset=["asset_id", "year_month"],
    keep="last"
)

df["rolling_avg_6m"] = (
    df.groupby("asset_id")["water_consumption"]
    .rolling(6)
    .mean()
    .reset_index(level=0, drop=True)
)

df["consumption_ratio"] = (
    df["water_consumption"] / df["rolling_avg_6m"]
)

df["event_flag"] = df["event_code"].notna().astype(int)

df["events_last_6m"] = (
    df.groupby("asset_id")["event_flag"]
    .rolling(6)
    .sum()
    .reset_index(level=0, drop=True)
)

df = df.fillna(0)

# ------------------------------------
# 4 MACHINE LEARNING MODEL
# ------------------------------------

features = [
    "rolling_avg_6m",
    "consumption_ratio",
    "events_last_6m"
]

X = df[features]

model = IsolationForest(
    contamination=0.02,
    random_state=42
)

df["anomaly_score"] = model.fit_predict(X)

df["anomaly_flag"] = df["anomaly_score"].apply(
    lambda x: "anomaly" if x == -1 else "normal"
)

print(df["anomaly_flag"].value_counts())

# ------------------------------------
# 5 EXPLAINABLE AI
# ------------------------------------

explainer = shap.Explainer(model, X)

shap_values = explainer(X)

df["feature_importance"] = np.abs(shap_values.values).mean(axis=1)

# ------------------------------------
# 6 ALERT GENERATION
# ------------------------------------

alerts = df[df["anomaly_flag"] == "anomaly"]

alerts = alerts.sort_values("feature_importance", ascending=False)

os.makedirs("data/output", exist_ok=True)

alerts.to_parquet("data/output/anomaly_alerts.parquet")

print("Alerts generated:", len(alerts))

# ------------------------------------
# 7 AI REASONING OUTPUT
# ------------------------------------

def generate_reason(row):

    reasons = []

    if row["consumption_ratio"] < 0.5:
        reasons.append("sudden consumption drop")

    if row["events_last_6m"] > 2:
        reasons.append("multiple anomaly events")

    if row["rolling_avg_6m"] == 0:
        reasons.append("insufficient consumption history")

    return ", ".join(reasons)


alerts["ai_reason"] = alerts.apply(generate_reason, axis=1)

# ------------------------------------
# 8 DASHBOARD
# ------------------------------------

def run_dashboard():

    st.title("AI Utility Anomaly Detection")

    st.write("Detected anomalies:")

    st.dataframe(
        alerts[
            [
                "asset_id",
                "rolling_avg_6m",
                "consumption_ratio",
                "events_last_6m",
                "ai_reason"
            ]
        ]
    )

# ------------------------------------
# MAIN
# ------------------------------------

if __name__ == "__main__":

    print("Pipeline executed at:", dt.datetime.now())

    run_dashboard()
