"""
llm_factory.py
--------------
Central LLM provider factory.
Reads LLM_PROVIDER from .env to decide which backend to use:
  - "ollama"      → local Ollama (no API key needed)  [DEFAULT]
  - "openai"      → OpenAI directly
  - "openrouter"  → OpenRouter (GPT-4o, Claude, etc. via one API key)

Set in .env:
  LLM_PROVIDER=ollama
  OLLAMA_MODEL=qwen2.5-coder:7b
  OLLAMA_BASE_URL=http://localhost:11434

  # OR for OpenAI directly:
  LLM_PROVIDER=openai
  OPENAI_API_KEY=sk-...
  OPENAI_MODEL=gpt-4o

  # OR for OpenRouter (recommended — gives access to GPT-4o, Claude, etc.):
  LLM_PROVIDER=openrouter
  OPENROUTER_API_KEY=sk-or-...
  OPENROUTER_MODEL=openai/gpt-4o-mini      # cheapest tool-calling model; or openai/gpt-4o for full power

Tool-calling support (used by ReAct CoderAgent):
  - openai / openrouter → True  (GPT-4o / GPT-4o-mini / Claude natively support function calling)
  - ollama              → False (7B models do not reliably support tool calling)
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Providers that reliably support LangChain tool-calling / function-calling
_TOOL_CALLING_PROVIDERS = {"openai", "openrouter"}


def get_provider() -> str:
    """Return the normalised LLM_PROVIDER string."""
    return os.environ.get("LLM_PROVIDER", "ollama").lower()


def supports_tool_calling() -> bool:
    """
    Returns True when the configured provider natively supports tool/function
    calling — meaning the ReAct CoderAgent can be used instead of static RAG.
    """
    return get_provider() in _TOOL_CALLING_PROVIDERS


def get_llm(temperature: float = 0.2):
    """
    Returns a LangChain chat model based on LLM_PROVIDER env variable.
    Defaults to Ollama if not set.
    """
    provider = get_provider()

    if provider == "openrouter":
        from langchain_openai import ChatOpenAI
        model = os.environ.get("OPENROUTER_MODEL", "openai/gpt-4o-mini")
        api_key = os.environ.get("OPENROUTER_API_KEY", "")
        if not api_key:
            raise EnvironmentError(
                "LLM_PROVIDER=openrouter but OPENROUTER_API_KEY is not set in .env"
            )
        # max_tokens: trial accounts have ~4000 token budget; paid accounts can remove this cap.
        # Override via OPENROUTER_MAX_TOKENS env var (e.g. 8000 for paid accounts).
        max_tokens = int(os.environ.get("OPENROUTER_MAX_TOKENS", "3500"))
        print(f"[LLM] Using OpenRouter → {model}  (max_tokens={max_tokens})")
        return ChatOpenAI(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            openai_api_key=api_key,
            openai_api_base="https://openrouter.ai/api/v1",
            default_headers={
                "HTTP-Referer": "https://github.com/balaji-muthukumaran-12086/AI_AUTOMATION_CODE_GENERATOR",
                "X-Title": "AutomaterSelenium AI Agent",
            },
        )

    elif provider == "openai":
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
