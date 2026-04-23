#!/usr/bin/env bash
# Pull required Ollama models after the container is up
set -e

OLLAMA_URL=${OLLAMA_BASE_URL:-http://localhost:11434}

echo "Pulling LLM model..."
curl -s "$OLLAMA_URL/api/pull" -d '{"name":"llama3"}'

echo "Pulling embedding model..."
curl -s "$OLLAMA_URL/api/pull" -d '{"name":"nomic-embed-text"}'

echo "Done."
