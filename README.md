# Simulation Dashboard

A monitoring and analytics dashboard for simulation logbooks, built with **Angular** (frontend) and **Flask** (backend).  
The system provides daily, weekly, monthly, and yearly statistics, including technical notes (IP, SimTech) and summary charts.

---

## Key Features

### Frontend (Angular)
- Mode selection: **Day**, **Week**, **Month**, **Year**
- Dynamic filters:
  - Date range for day mode
  - Week range (1–52)
  - Month selection
  - Year range
- Results table:
  - Grouping by week
  - Side-by-side daily tables with a shared vertical header
  - Dynamic rows per device
  - Display of technical notes (IP and SimTech)
- Integrated chart (Chart.js) below the notes section
- Modern responsive layout

### Backend (Flask)
- Generates outcomes via the `Day` class
- Converts Python objects to JSON for frontend consumption
- Automatically excludes Saturdays and Sundays in day mode
- Handles IP and SimTech separately as lists
- Returns structured JSON with multiple devices and daily results

---


---

## Installation

### 1. Backend (Flask)

```bash
cd backend-flask
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

pip install -r requirements.txt
flask run


