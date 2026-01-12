"""
Configuration for InternHub AI Platform
"""

import os

# vLLM API Configuration
VLLM_BASE_URL = os.getenv("VLLM_BASE_URL", "http://localhost:2525/v1")
VLLM_API_KEY = os.getenv("VLLM_API_KEY", "token-abc123")
VLLM_MODEL = os.getenv("VLLM_MODEL", "Qwen/Qwen2.5-7B-Instruct-AWQ")

# API Server Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))

# Application Settings
MAX_TOKENS = 2048
TEMPERATURE = 0.7
TOP_P = 0.9

# ATS Scoring Weights
ATS_WEIGHTS = {
    "skill_match": 0.40,
    "experience_match": 0.25,
    "education_match": 0.15,
    "keyword_density": 0.20,
}
