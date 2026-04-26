#!/usr/bin/env bash
# Collect LangChain and LangGraph docs (markdown only) into data/raw/
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
RAW_DIR="$ROOT_DIR/data/raw"
TMP_DIR="$ROOT_DIR/data/.tmp"

mkdir -p "$RAW_DIR/langchain" "$RAW_DIR/langgraph" "$TMP_DIR"

clone_sparse() {
  local repo_url=$1
  local docs_path=$2
  local dest_name=$3
  local clone_dir="$TMP_DIR/$dest_name"

  echo ">>> Cloning $dest_name docs..."
  rm -rf "$clone_dir"
  git clone --depth=1 --filter=blob:none --sparse "$repo_url" "$clone_dir"
  cd "$clone_dir"
  git sparse-checkout set "$docs_path"
  cd "$ROOT_DIR"

  echo ">>> Copying .md files to data/raw/$dest_name ..."
  find "$clone_dir" -not -path "*/.git/*" -name "*.md" | while read -r f; do
    rel="${f#$clone_dir/}"
    dest="$RAW_DIR/$dest_name/$rel"
    mkdir -p "$(dirname "$dest")"
    cp "$f" "$dest"
  done

  local count
  count=$(find "$RAW_DIR/$dest_name" -name "*.md" | wc -l)
  echo ">>> $dest_name done. ($count files)"
}

clone_sparse "https://github.com/langchain-ai/langchain.git" "docs" "langchain"
clone_sparse "https://github.com/langchain-ai/langgraph.git" "docs" "langgraph"

echo ">>> Cleaning up tmp..."
rm -rf "$TMP_DIR"

echo ""
echo "=== Collected ==="
echo "langchain: $(find "$RAW_DIR/langchain" -name "*.md" | wc -l) files"
echo "langgraph: $(find "$RAW_DIR/langgraph" -name "*.md" | wc -l) files"
echo "total:     $(find "$RAW_DIR" -name "*.md" | wc -l) files"
