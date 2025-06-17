# PraviChain SCM Agents

This repository contains the code and notes for the PraviChain Supply Chain Management system.

See [SCMS_Architecture.md](SCMS_Architecture.md) for the original architecture notes.

## Directory Layout

```
pravichain-scm/
    agents/
        forecast.py
        inventory.py
        logistics.py
        invoice_match.py
        chatbot/
            llama_runner.sh
    api/
        forecast_routes.py
        inventory_routes.py
        chat_routes.py
    dashboards/
        app.py
    models/
    uploads/
    db/
    scripts/
```

## Running Agents

Each agent can be executed directly from the command line. The examples below assume you are inside the `pravichain-scm` directory.

### Demand Forecast Agent
```
python agents/forecast.py
```

### Inventory Optimization Agent
```
python agents/inventory.py
```

### Logistics Routing Agent
```
python agents/logistics.py
```

### Invoice Reconciliation Agent
```
python agents/invoice_match.py /path/to/invoice.pdf
```

### Chatbot Agent
```
./agents/chatbot/llama_runner.sh "Hello"
```

### Dashboard Agent
```
python dashboards/app.py
```

These modules use placeholder logic but provide the entry points and directory structure required for the PraviChain SCM system.

## Local Setup (Offline)

Follow these steps to run the project without internet access:

```bash
# 1. Clone & Install
git clone https://github.com/your-org/pravichain-scm.git
cd pravichain-scm
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 2. Run Agents
python agents/forecast.py
python agents/inventory.py
python agents/logistics.py
python agents/invoice_match.py
bash agents/chatbot/llama_runner.sh

# 3. Start API
uvicorn api.main:app --host 127.0.0.1 --port 8000

# 4. Start Dashboard
cd dashboards && python app.py

# 5. Optional: Dev Automation with Codex
ollama run deepseek-coder:1.3b
codex generate agent forecast --inputs sales.csv --output forecast.pkl --model prophet
```

## One-step Setup (Ubuntu)

For new Ubuntu systems, run the provided script to install all required packages
and prepare a local database:

```bash
bash setup_ubuntu.sh
```

The script installs system dependencies, creates a Python virtual environment,
builds `llama.cpp` for the chatbot agent, and sets up a PostgreSQL database
`scm` with username `user` and password `pass`.
