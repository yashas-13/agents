#!/bin/bash
# Simple wrapper to run llama.cpp model

# Resolve repository root relative to this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
MODEL_PATH="$REPO_ROOT/models/tinyllama.gguf"
PROMPT="$1"

if [ -z "$PROMPT" ]; then
  echo "Usage: $0 'your question'"
  exit 1
fi

# Check for llama.cpp binary
if ! command -v llama.cpp >/dev/null; then
  echo "Error: llama.cpp binary not found. Please install or build llama.cpp first." >&2
  exit 1
fi

# Ensure model exists
if [ ! -f "$MODEL_PATH" ]; then
  echo "Error: model file not found at $MODEL_PATH" >&2
  exit 1
fi

llama.cpp -m "$MODEL_PATH" -p "$PROMPT"
