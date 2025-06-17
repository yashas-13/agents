🧠 AI Agents Specification – PraviChain SCM (Online VPS Edition)

This document outlines the design and responsibilities of each AI agent integrated into the PraviChain Supply Chain Management system hosted on a Hostinger VPS. All agents operate without paid APIs or external SaaS dependencies. The system is designed to be deployed online, uses only open-source technologies, and ensures full control of logic and data.

👤 User Roles

Role

Description

Super Admin

Manages entire platform, agents, models, users, system settings

Manufacturer

Manages production, stock dispatch to CFA/super stockists

CFA

Handles warehouse-level receipt and forwarding to super stockists

Super Stockist

Manages regional distribution to stockists/retailers

Stockist

Local distributor or retailer interacting with end sales/demand

Auditor

Views logs, compliance flags, and reports

📦 Agent 1: Demand Forecast Agent

Helps Users:

Manufacturer gets proactive insights to adjust production volume based on future demand trends.

CFA & Super Stockist use it to prepare storage capacity and schedule replenishment.

Super Admin uses trend reports to analyze regional patterns for strategic planning.

Role: Predicts future demand for each SKU using time series forecasting models.

Input:

sales_data (via DB)

Output:

Forecasts per region/SKU accessible via dashboard

Tech Stack: Prophet, pandas, PostgreSQL

API: REST (Flask/FastAPI) exposed under /api/forecast

Runs on: Daily cronjob

📦 Agent 2: Inventory Optimization Agent

Helps Users:

CFA & Super Stockist receive reorder alerts and optimized stock levels to prevent under/over-stocking.

Stockist avoids manual calculation of stock requirements.

Super Admin monitors reorder anomalies and agent performance centrally.

Role: Calculates reorder points, safety stock, and EOQ for each product at each level (CFA, super stockist).

Input: Stock levels, forecasts, lead times

Output: Recommended reorder plans with alerts

Tech Stack: PuLP, NumPy, PostgreSQL

API: /api/inventory/optimize

🚚 Agent 3: Logistics Routing Agent

Helps Users:

CFA & Super Stockist optimize delivery time and fuel cost through intelligent route planning.

Manufacturer can dispatch multiple consignments with optimized transport.

Auditor can review cost-efficiency of routes and compliance with delivery SLAs.

Role: Plans optimal routes for delivery vehicles (TSP/VRP)

Input: Delivery addresses, vehicle constraints

Output: Route schedules with estimated delivery times

Tech Stack: OR-Tools, GeoPandas, PostGIS

API: /api/logistics/plan

🧾 Agent 4: Invoice Reconciliation Agent

Helps Users:

Manufacturer & CFA reduce errors and mismatches between invoice, delivery, and PO records.

Super Admin gets anomaly reports for compliance and audit.

Auditor tracks consistency and identifies fraud or inefficiency.

Role: Parses invoice/PO PDFs and reconciles with database entries

Input: PDF uploads via web or FTP

Output: Matched reports with anomaly detection

Tech Stack: Tesseract, pdfminer, spaCy

API: /api/invoices/reconcile

💬 Agent 5: Chatbot Agent (Offline LLM)

Helps Users:

Stockist & Super Stockist can query live stock, shipment status, reorder info without navigating UI.

Manufacturer & CFA get real-time answers to queries around dispatch and inventory.

Super Admin uses it for high-level control and explanations of system behavior.

Role: Answers stock, dispatch, invoice, and delivery queries in natural language

Input: User query via web or chatbot UI

Output: Text responses from local LLM

Tech Stack: llama.cpp, gguf models

API: Served as chatbot /chat

📊 Agent 6: Dashboard Agent

Helps Users:

All user roles gain access to role-specific visual summaries (e.g., sales chart for stockists, shipment flow for CFA).

Auditor uses built-in filters and exports to generate compliance-ready reports.

Super Admin uses analytics to monitor operations, agents, and user activity.

Role: Displays real-time stock, orders, routes, forecasts, and compliance summaries

Tech Stack: Dash, Flask, Jinja, Bootstrap 5

Features:

Dynamic charts (orders, demand, route success)

Filterable tables (stock logs, invoices, reorder alerts)

Export PDF/Excel

Access: Role-based per user

📁 Model & Data Store (Hostinger VPS)

All models are locally stored in VPS:

models/forecast.pkl

models/tinyllama.gguf

Database: PostgreSQL

Storage: /var/appdata/

Backups: Cron job to external storage/FTP

🛡️ Deployment

Environment: Hostinger VPS

OS: Ubuntu 22.04

Web Server: Nginx + Gunicorn/Uvicorn

HTTPS: Let’s Encrypt

Isolation: All agents run under isolated Docker containers

🗂️ Agent Directory

pravichain-scm/
├── agents/
│   ├── forecast.py
│   ├── inventory.py
│   ├── logistics.py
│   ├── invoice_match.py
│   └── chatbot/
│       └── llama_runner.sh
├── api/
│   ├── forecast_routes.py
│   ├── inventory_routes.py
│   └── chat_routes.py
├── dashboards/
│   └── app.py
├── models/
├── uploads/
├── db/
└── scripts/

🔒 Security & Compliance

HTTPS enforced via Certbot

Auth: JWT-based login/session, RBAC per user

Audit Logs: Every update stored with timestamps/user

No API keys or 3rd-party model calls required


## Role to Agent Matrix

| Role | Key Agents & Features |
| --- | --- |
| Super Admin | Dashboard Agent for monitoring, Demand Forecast Agent for planning, Inventory Optimization Agent, Logistics Routing Agent, Invoice Reconciliation Agent, Chatbot Agent |
| Manufacturer | Demand Forecast Agent for production planning, Logistics Routing Agent for dispatch, Invoice Reconciliation Agent, Chatbot Agent |
| CFA | Inventory Optimization Agent, Logistics Routing Agent, Invoice Reconciliation Agent, Chatbot Agent |
| Super Stockist | Demand Forecast Agent, Inventory Optimization Agent, Logistics Routing Agent, Chatbot Agent |
| Stockist | Inventory Optimization Agent for reorder alerts, Chatbot Agent for queries, Dashboard Agent for sales charts |
| Auditor | Invoice Reconciliation Agent for compliance, Logistics Routing Agent for route cost analysis, Dashboard Agent for reports |
