"""
llm_factory.py
--------------
Central LLM provider factory.
Reads LLM_PROVIDER from .env to decide which backend to use:
  - "ollama"  → local Ollama (no API key needed)  [DEFAULT]
  - "openai"  → OpenAI / Azure OpenAI

Set in .env:
  LLM_PROVIDER=ollama
  OLLAMA_MODEL=qwen2.5-coder:7b
  OLLAMA_BASE_URL=http://localhost:11434

  # OR for OpenAI:
  LLM_PROVIDER=openai
  OPENAI_API_KEY=sk-...
  OPENAI_MODEL=gpt-4o
"""

import os
from dotenv import load_dotenv

load_dotenv()


def get_llm(temperature: float = 0.2):
    """
    Returns a LangChain chat model based on LLM_PROVIDER env variable.
    Defaults to Ollama if not set.
    """
    provider = os.environ.get("LLM_PROVIDER", "ollama").lower()

    if provider == "openai":
        from langchain_openai import ChatOpenAI
        model = os.environ.get("OPENAI_MODEL", "gpt-4o")
        print(f"[LLM] Using OpenAI → {model}")
        return ChatOpenAI(model=model, temperature=temperature)

    else:  # default: ollama
        from langchain_ollama import ChatOllama
        model = os.environ.get("OLLAMA_MODEL", "qwen2.5-coder:7b")
        base_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
        print(f"[LLM] Using Ollama → {model}  ({base_url})")
        return ChatOllama(model=model, base_url=base_url, temperature=temperature)
