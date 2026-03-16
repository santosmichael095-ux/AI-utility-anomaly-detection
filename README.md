# AI Utility Anomaly Detection

An end-to-end AI system for detecting abnormal consumption patterns in large-scale utility meter datasets using automated data pipelines, machine learning, and explainable AI.

This project demonstrates a production-style machine learning pipeline combining data engineering, anomaly detection, and automated analytics.

---

# Overview

Utility companies manage millions of meter readings across multiple regions. Detecting anomalies in consumption data is essential for identifying:

- potential fraud
- meter malfunction
- abnormal consumption patterns
- operational incidents

This project implements an AI-driven monitoring system capable of automatically identifying anomalies in utility consumption data.

---

# Architecture

Pipeline workflow:

Data Sources  
↓  
Automated Data Ingestion  
↓  
Data Cleaning & Validation  
↓  
Feature Engineering  
↓  
Machine Learning Model  
↓  
Anomaly Detection  
↓  
Explainable AI  
↓  
Alert Generation  
↓  
Visualization Dashboard  

---

# System Components

## 1 Data Ingestion

The pipeline automatically collects data from structured datasets such as:

- parquet files
- data lakes
- SQL databases
- API endpoints

The ingestion layer consolidates all raw datasets into a unified dataframe for processing.

---

## 2 Data Cleaning

Data validation and preprocessing include:

- timestamp normalization
- missing value handling
- duplicate removal
- schema validation

These steps ensure consistent data quality for downstream ML models.

---

## 3 Feature Engineering

Key engineered features include:

| Feature | Description |
|------|------|
rolling_avg_6m | 6-month rolling average consumption |
consumption_ratio | consumption deviation from historical mean |
events_last_6m | anomaly events recorded in the last 6 months |
seasonality_index | consumption pattern variation |

These features capture temporal and behavioral patterns of utility usage.

---

## 4 Machine Learning Model

The anomaly detection model uses **Isolation Forest**, an unsupervised algorithm designed to identify rare patterns in large datasets.

Advantages:

- scalable for large datasets
- robust to noise
- effective for anomaly detection without labeled data

Model features:

- rolling_avg_6m
- consumption_ratio
- events_last_6m

Output:

- anomaly classification
- anomaly score

---

## 5 Explainable AI

To improve model transparency, the pipeline integrates **SHAP (SHapley Additive Explanations)**.

Explainability allows analysts to understand:

- which variables influenced anomaly detection
- how consumption patterns deviated from historical norms

This is critical for operational decision-making.

---

## 6 Automated Alert Generation

Detected anomalies trigger automated alerts including:

- affected asset ID
- anomaly score
- potential root causes

These alerts can be integrated into operational monitoring systems.

---

## 7 Visualization Dashboard

A lightweight dashboard built with Streamlit enables analysts to:

- view detected anomalies
- inspect feature values
- explore consumption patterns

This interface allows quick investigation of flagged records.

---

# Project Structure

