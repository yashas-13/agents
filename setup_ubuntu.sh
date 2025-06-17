#!/bin/bash
set -e

# Enhanced setup script for new Ubuntu systems
# Installs system dependencies, Python packages, and prepares local environment

# Update package list and upgrade
sudo apt-get update && sudo apt-get -y upgrade

# Install system packages required by the agents
sudo apt-get install -y \
    python3 python3-venv python3-pip \
    build-essential git \
    sqlite3 tesseract-ocr \
    wget curl

# Create Python virtual environment if not present
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# Upgrade pip inside the venv
pip install --upgrade pip

# Install Python requirements
pip install -r requirements.txt

# Optional: build llama.cpp for chatbot agent
if [ ! -d "llama.cpp" ]; then
    git clone https://github.com/ggerganov/llama.cpp.git
    (cd llama.cpp && make)
    sudo ln -sf "$PWD/llama.cpp/main" /usr/local/bin/llama.cpp
fi

# Install package in editable mode
pip install -e .

# Initialize SQLite database
mkdir -p db
touch db/scm.sqlite

echo "Setup complete. Activate the virtual environment with 'source venv/bin/activate'"
