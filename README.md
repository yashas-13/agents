

# PraviChain SCM: AI-Powered Supply Chain Agents

[][Platform-url]
[][Status-url]
[][License-url]

This repository contains the code for the **PraviChain Supply Chain Management (SCM)** system, a powerful, privacy-focused automation platform for manufacturers and retailers. It leverages a suite of offline, locally-executed AI agents to optimize inventory, forecast demand, and automate key operational workflows without relying on cloud services.

This document outlines the core architecture and operational instructions. For original design notes, see [`SCMS_Architecture.md`](https://www.google.com/search?q=SCMS_Architecture.md).

-----

## 🔑 Key Features

  - **📈 AI-Powered Forecasting**: Predict SKU-level demand using time-series models.
  - **📦 Intelligent Inventory Optimization**: Automatically calculate reorder points and EOQ to minimize costs.
  - **🚚 Logistics & Routing AI**: Optimize delivery routes for time and cost savings.
  - **🧾 Automated Invoice Matching**: Reconcile invoices against purchase orders and delivery receipts using AI.
  - **🤖 Conversational AI Assistant**: An integrated, offline chatbot for natural language queries about stock and orders.
  - **📊 Interactive Dashboard**: A central UI for visualizing the entire SCM workflow, running what-if scenarios, and generating reports.
  - **🔒 100% Offline & Secure**: All agents run locally. No data ever leaves your premises.
  - **📝 Manufacturer Admin Registration**: Simple web form at `/register` to create manufacturer admin accounts.

## 🏛️ System Architecture & Agent Roles

PraviChain SCM operates through a series of interconnected agents that create a seamless, automated workflow.

| Agent | File(s) | AI/Core Technology | Role & Advanced Capabilities |
| :--- | :--- | :--- | :--- |
| **Forecast Agent** | `agents/forecast.py` | **Prophet** | Analyzes historical sales data to generate accurate demand forecasts. Features an **Auto-Learner** module for scheduled, automated retraining to prevent model drift. |
| **Inventory Agent** | `agents/inventory.py` | **PuLP** | Takes forecast data to calculate optimal reorder points & EOQ using constraint optimization. Triggers **smart alerts** for critically low stock. |
| **Logistics Agent** | `agents/logistics.py` | **Graph Optimization** | Calculates the most efficient delivery routes based on order locations, traffic data (if available), and vehicle capacity to minimize fuel costs and delivery time. |
| **Invoice Agent** | `agents/invoice_match.py` | **OCR + Rules Engine** | Automates financial reconciliation by using Optical Character Recognition (OCR) to extract data from invoices (PDFs/scans) and match it against purchase orders and delivery logs. |
| **Chatbot Agent** | `agents/chatbot/` | **Local LLM (Mistral)** | Provides a natural language interface for queries. Features **role-aware dialogue** (Manufacturer vs. Retailer) and performs real-time **SKU lookups**. |
| **Dashboard Agent**| `dashboards/app.py` | **Streamlit / Dash** | Provides an interactive web UI for visualizing data. Features **drill-down analytics** and **what-if scenario modeling** to simulate the impact of demand or lead time changes. |

### Directory Layout

```
pravichain-scm/
├── agents/              # Core logic for each AI agent
│   ├── forecast.py
│   ├── inventory.py
│   ├── logistics.py
│   ├── invoice_match.py
│   └── chatbot/
│       └── llama_runner.sh
├── api/                 # API endpoints to expose agent functions
│   ├── main.py
│   ├── forecast_routes.py
│   └── inventory_routes.py
├── dashboards/          # Interactive Streamlit/Dash application
│   └── app.py
├── models/              # Saved AI models (e.g., forecast.pkl, mistral.gguf)
├── uploads/             # For uploaded invoices, etc.
├── db/                  # Local database files or configuration
└── scripts/             # Utility and setup scripts
```

## 🚀 Local Setup (Offline)

Follow these steps to configure the project for local, offline execution.

```bash
# 1. Clone the repository
git clone https://github.com/your-org/pravichain-scm.git
cd pravichain-scm

# 2. Create and activate a Python virtual environment
python3 -m venv venv
source venv/bin/activate
# On Windows, use: venv\Scripts\activate

# 3. Install all required packages
pip install -r requirements.txt

# 4. Prepare the local SQLite database with sample data
python scripts/populate_sample_db.py

# 5. Download required AI models (e.g., the chatbot LLM)
# Ensure the correct .gguf model file is placed in the models/ directory
```

### One-Step Setup (Ubuntu)

For new Ubuntu systems, the provided script installs system dependencies, builds `llama.cpp` for the chatbot, and sets up a local SQLite database.

```bash
bash scripts/setup_ubuntu.sh
```

## ⚙️ Running the Platform

Each component can be run from the command line. The examples below assume you are in the root `pravichain-scm` directory.

### 1\. Run Individual Agents (for testing/manual runs)

```bash
# Generate a demand forecast
python agents/forecast.py

# Calculate optimal inventory levels
python agents/inventory.py

# Optimize logistics routing
python agents/logistics.py

# Reconcile a specific invoice
python agents/invoice_match.py uploads/invoice_to_process.pdf

# Query the chatbot directly
./agents/chatbot/llama_runner.sh "What is the stock level for SKU #A124?"
```

### 2\. Start the API Server

The API server exposes agent functionalities over a local network.

```bash
uvicorn api.main:app --host 127.0.0.1 --port 8000
```
Then open `http://127.0.0.1:8000/register` in your browser to create a manufacturer admin account.

### 3\. Launch the Interactive Dashboard

This is the primary user interface for visualizing data and reports.

```bash
python dashboards/app.py
```

### 4\. Run Automated Tests

After installing the requirements you can execute the test suite to verify that
all agents operate correctly:

```bash
pytest -q
```
