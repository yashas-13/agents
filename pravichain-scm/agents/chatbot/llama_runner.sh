#!/bin/bash
# Simple wrapper to run llama.cpp model
MODEL_PATH="../models/tinyllama.gguf"
PROMPT="$1"

if [ -z "$PROMPT" ]; then
  echo "Usage: $0 'your question'"
  exit 1
fi

llama.cpp -m "$MODEL_PATH" -p "$PROMPT"
