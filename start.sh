#!/bin/bash
# Quick start script for InternHub AI Platform

echo "🚀 Starting InternHub AI Platform..."
echo ""

# Check if vLLM server is running
echo "Checking vLLM server..."
if curl -s http://localhost:2525/v1/models > /dev/null 2>&1; then
    echo "✅ vLLM server is running"
else
    echo "❌ vLLM server is NOT running!"
    echo "Please start the vLLM server first:"
    echo "  cd ../vLLM-server && bash start.sh"
    exit 1
fi

echo ""
echo "Starting FastAPI server..."
echo "Access the web interface at: http://localhost:8000"
echo "API documentation at: http://localhost:8000/docs"
echo ""

# Activate conda environment and start server
source $(conda info --base)/etc/profile.d/conda.sh
conda activate LangGraph
python api.py
