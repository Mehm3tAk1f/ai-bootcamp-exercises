"""
LLM Client Utilities
=====================

Ready-to-use client functions for various LLM providers.
Pick the one that matches your setup and set it in config below.

--- Free Options ---
1. Ollama        — local, no API key needed (https://ollama.com/download)
2. Hugging Face  — free Inference API (https://huggingface.co/settings/tokens)
3. Google Gemini — 15 req/min free tier (https://aistudio.google.com/apikey)
4. Groq          — free tier available (https://console.groq.com)

--- Paid Options ---
5. OpenAI / Azure OpenAI
"""

import os


# === Provider Clients ===


def call_ollama(prompt: str, model: str = "llama3.2") -> str:
    """
    Call a local Ollama model. Completely free, no API key needed.

    Setup:
        1. Install Ollama: https://ollama.com/download
        2. Pull a model: ollama pull llama3.2
        3. Ollama runs at http://localhost:11434 by default
    """
    import requests

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt, "stream": False},
    )
    response.raise_for_status()
    return response.json()["response"]


def call_huggingface(prompt: str, model: str = "mistralai/Mistral-7B-Instruct-v0.3") -> str:
    """
    Call Hugging Face Inference API. Free tier available.

    Setup:
        1. Create account: https://huggingface.co
        2. Get token: https://huggingface.co/settings/tokens
        3. Set env var: export HF_API_KEY=hf_...
        4. pip install huggingface-hub

    Free models: mistralai/Mistral-7B-Instruct-v0.3, meta-llama/Llama-3.2-3B-Instruct,
                 microsoft/Phi-3-mini-4k-instruct
    """
    from huggingface_hub import InferenceClient

    client = InferenceClient(token=os.environ["HF_API_KEY"])
    response = client.text_generation(
        prompt,
        model=model,
        max_new_tokens=1024,
    )
    return response


def call_gemini(prompt: str, model: str = "gemini-2.0-flash") -> str:
    """
    Call Google Gemini API. Free tier: 15 req/min.

    Setup:
        1. Get API key: https://aistudio.google.com/apikey
        2. Set env var: export GEMINI_API_KEY=...
        3. pip install google-generativeai
    """
    import google.generativeai as genai

    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model_instance = genai.GenerativeModel(model)
    response = model_instance.generate_content(prompt)
    return response.text


def call_groq(prompt: str, model: str = "llama-3.3-70b-versatile") -> str:
    """
    Call Groq API. Free tier available.

    Setup:
        1. Get API key: https://console.groq.com
        2. Set env var: export GROQ_API_KEY=...
        3. pip install groq
    """
    from groq import Groq

    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


def call_openai(prompt: str, model: str = "gpt-4o-mini") -> str:
    """
    Call OpenAI API. Paid.

    Setup:
        1. Set env var: export OPENAI_API_KEY=sk-...
        2. pip install openai
    """
    from openai import OpenAI

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


# ============================================================
# CONFIGURATION: Select your LLM provider here.
# Change this to the function matching your setup.
# ============================================================

call_llm = call_ollama
# call_llm = call_huggingface
# call_llm = call_gemini
# call_llm = call_groq
# call_llm = call_openai
