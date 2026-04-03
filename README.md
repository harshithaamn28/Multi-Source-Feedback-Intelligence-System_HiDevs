# Multi-Source Feedback Intelligence System

##  Overview
The Multi-Source Feedback Intelligence System is a Python-based application designed to collect, process, and analyze customer feedback from multiple sources.

This project integrates:
- CSV-based survey feedback
- API-based feedback source using FastAPI

The system performs sentiment analysis, issue categorization, trend detection, and generates downloadable PDF reports for weekly insights.

The interactive dashboard is built using Streamlit for real-time visualization and filtering.

---

## Features

### Multi-Source Integration
The project supports multiple feedback sources:
- CSV file (`data/sample_feedback.csv`)
- API source (`/reviews` endpoint)

### Sentiment Analysis
Feedback is classified into:
- Positive
- Negative
- Neutral

using **TextBlob polarity-based sentiment analysis**.

### Smart Categorization
Feedback is automatically categorized into:
- Bug
- Performance
- Feature Request
- General

### Dashboard Filters
The Streamlit dashboard supports:
- Sentiment filter
- Source filter
- Date range filter

### Trend Detection
Displays **sentiment trend over time** using line charts.

### PDF Report Generation
Generates a weekly PDF report summarizing:
- total feedback
- sentiment counts
- insights

### Interactive Dashboard
Includes:
- summary metrics
- bar charts
- trend charts
- filterable table
- PDF export

---

## Tech Stack
- Python
- Streamlit
- FastAPI
- Pandas
- TextBlob
- Requests
- FPDF

---

## Project Structure

project/
│
├── src/
│   └── api/
│       └── endpoints.py
│
├── dashboard/
│   └── dashboard.py
│
├── data/
│   └── sample_feedback.csv
│
├── requirements.txt
└── README.md

---

## Installation & Setup

### Step 1 — Install dependencies
```bash
pip install -r requirements.txt
