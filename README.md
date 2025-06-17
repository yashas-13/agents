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
