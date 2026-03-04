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

from config.project_config import (
    LLM_PROVIDER,
    OPENROUTER_API_KEY, OPENROUTER_MODEL, OPENROUTER_MAX_TOKENS,
    OLLAMA_MODEL, OLLAMA_BASE_URL,
    OPENAI_MODEL, OPENAI_API_KEY,
)

# Providers that reliably support LangChain tool-calling / function-calling
_TOOL_CALLING_PROVIDERS = {"openai", "openrouter"}


def get_provider() -> str:
    """Return the normalised LLM_PROVIDER string."""
    return LLM_PROVIDER.lower()


def supports_tool_calling() -> bool:
    """
    Returns True when the configured provider natively supports tool/function
    calling — meaning the ReAct CoderAgent can be used instead of static RAG.
    Free-tier OpenRouter models (model id ending in ':free') do NOT support
    function/tool calling reliably, so they fall back to the RAG path.
    """
    if get_provider() not in _TOOL_CALLING_PROVIDERS:
        return False
    # Free-tier models (e.g. arcee-ai/trinity-large-preview:free) don't support tool calling
    model = OPENROUTER_MODEL or OPENAI_MODEL
    if model.endswith(":free"):
        return False
    return True


def get_llm(temperature: float = 0.2):
    """
    Returns a LangChain chat model based on LLM_PROVIDER in project_config.py.
    """
    provider = get_provider()

    if provider == "openrouter":
        from langchain_openai import ChatOpenAI
        if not OPENROUTER_API_KEY:
            raise EnvironmentError(
                "LLM_PROVIDER=openrouter but OPENROUTER_API_KEY is not set in project_config.py"
            )
        print(f"[LLM] Using OpenRouter → {OPENROUTER_MODEL}  (max_tokens={OPENROUTER_MAX_TOKENS})")
        return ChatOpenAI(
            model=OPENROUTER_MODEL,
            temperature=temperature,
            max_tokens=OPENROUTER_MAX_TOKENS,
            openai_api_key=OPENROUTER_API_KEY,
            openai_api_base="https://openrouter.ai/api/v1",
            default_headers={
                "HTTP-Referer": "https://github.com/balaji-muthukumaran-12086/AI_AUTOMATION_CODE_GENERATOR",
                "X-Title": "AutomaterSelenium AI Agent",
            },
        )

    elif provider == "openai":
        from langchain_openai import ChatOpenAI
        print(f"[LLM] Using OpenAI → {OPENAI_MODEL}")
        return ChatOpenAI(model=OPENAI_MODEL, api_key=OPENAI_API_KEY, temperature=temperature)

    else:  # default: ollama
        from langchain_ollama import ChatOllama
        print(f"[LLM] Using Ollama → {OLLAMA_MODEL}  ({OLLAMA_BASE_URL})")
        return ChatOllama(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL, temperature=temperature)
