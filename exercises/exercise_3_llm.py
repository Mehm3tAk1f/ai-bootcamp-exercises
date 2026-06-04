"""
Exercise 3: LLM API & Prompt Engineering
==========================================

Build a script that uses an LLM API to extract structured information
from company descriptions.

--- LLM Access Options (pick one) ---

1. Ollama (FREE, local) — recommended if you have no paid API access
   Install: https://ollama.com/download
   Then run: ollama pull llama3.2
   API runs at: http://localhost:11434

2. Hugging Face Inference API (FREE tier)
   Get token: https://huggingface.co/settings/tokens
   pip install huggingface-hub

3. Google Gemini (FREE tier) — 15 requests/min free
   Get API key: https://aistudio.google.com/apikey
   pip install google-generativeai

4. Groq (FREE tier) — fast inference, free tier available
   Get API key: https://console.groq.com
   pip install groq

5. OpenAI / Azure OpenAI (PAID) — if you already have access
   pip install openai

Configure your provider in: exercises/utils/llm_client.py
Document your choice in SOLUTION.md.
"""

import json
from pathlib import Path

from utils import call_llm  # noqa: configured in utils/llm_client.py


DATA_PATH = Path(__file__).parent.parent / "data" / "company_descriptions.txt"


# ============================================================
# BASE LEVEL — Simple LLM interaction
# ============================================================

def summarize_text(text: str) -> str:
    """
    Use the LLM to generate a short summary (2-3 sentences) of the input text.
    Just call the LLM with a clear prompt and return the response.
    """
    # TODO: Write a prompt and call call_llm()
    pass


def classify_sentiment(text: str) -> str:
    """
    Use the LLM to classify the sentiment of the text.
    Return one of: "positive", "neutral", "negative"
    """
    # TODO: Write a prompt that returns only one word
    pass


def ask_question(text: str, question: str) -> str:
    """
    Given a text and a question, use the LLM to answer the question
    based only on the information in the text.
    """
    # TODO: Implement basic Q&A with context
    pass


# ============================================================
# STANDARD LEVEL — Structured extraction and prompt design
# ============================================================

def extract_company_info(text: str) -> list[dict]:
    """
    Given unstructured text containing company descriptions,
    extract for each company:
    - company_name: str
    - industry: str
    - founded_year: int | None
    - num_employees: int | None
    - key_products: list[str]

    Return a list of dictionaries with valid JSON-parseable output.
    """
    # TODO: Implement LLM API call with appropriate prompt
    pass


def extract_with_prompt_v1(text: str) -> list[dict]:
    """First prompt approach for extraction."""
    # TODO: Implement your first prompt strategy
    pass


def extract_with_prompt_v2(text: str) -> list[dict]:
    """Second prompt approach for extraction."""
    # TODO: Implement your second prompt strategy
    pass


def compare_prompts(text: str) -> None:
    """
    Run both prompts and print a comparison.
    Explain which works better and why (print your explanation).
    """
    # TODO: Implement comparison logic
    pass


# ============================================================
# ADVANCED LEVEL — Robustness, cost, and production-readiness
# ============================================================

def safe_llm_call(prompt: str, max_retries: int = 3) -> str:
    """
    Make an LLM API call with proper error handling:
    - Handle connection errors
    - Handle rate limiting (with exponential backoff)
    - Handle invalid/empty responses
    - Log each attempt

    Return the response text or raise a descriptive exception.
    """
    # TODO: Implement robust API call with error handling
    pass


def extract_with_validation(text: str) -> list[dict]:
    """
    Extract company info AND validate the output:
    - Ensure the response is valid JSON
    - Verify all required fields are present
    - If extraction fails, retry with a modified prompt
    - Return only validated results

    This simulates production-grade LLM integration.
    """
    # TODO: Implement extraction with validation loop
    pass


def estimate_cost(prompt: str, response: str, model: str = "gpt-4o-mini") -> dict:
    """
    Estimate the cost of an API call.
    Return a dict with:
    - input_tokens: int (approximate)
    - output_tokens: int (approximate)
    - estimated_cost_usd: float
    """
    # TODO: Implement token counting and cost estimation
    pass


def batch_extract_with_budget(texts: list[str], max_budget_usd: float = 0.10) -> list[dict]:
    """
    Process multiple texts but stop if the estimated cost exceeds the budget.
    Return results processed so far + a summary of cost spent.

    Return: {"results": [...], "processed": int, "total": int, "cost_usd": float}
    """
    # TODO: Implement budget-aware batch processing
    pass


# --- Main ---

if __name__ == "__main__":
    # Load data
    text = DATA_PATH.read_text(encoding="utf-8")
    first_paragraph = text.split("\n\n")[0]

    print("=" * 60)
    print("  Exercise 3: LLM API & Prompt Engineering")
    print("=" * 60)

    # --- BASE ---
    print("\n--- BASE LEVEL ---")

    summary = summarize_text(first_paragraph)
    if summary:
        print(f"Summary: {summary}")
    else:
        print("summarize_text() not implemented yet")

    sentiment = classify_sentiment(first_paragraph)
    if sentiment:
        print(f"Sentiment: {sentiment}")

    answer = ask_question(first_paragraph, "What year was the company founded?")
    if answer:
        print(f"Q&A answer: {answer}")

    # --- STANDARD ---
    print("\n--- STANDARD LEVEL ---")

    results = extract_company_info(text)
    if results:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print("extract_company_info() not implemented yet")

    print("\nPrompt comparison:")
    compare_prompts(text)

    # --- ADVANCED ---
    print("\n--- ADVANCED LEVEL ---")

    validated = extract_with_validation(text)
    if validated:
        print(f"Validated extraction: {len(validated)} companies")
    else:
        print("extract_with_validation() not implemented yet")

    # Cost estimation demo
    if results:
        cost = estimate_cost("sample prompt", "sample response")
        if cost:
            print(f"Cost estimate: {cost}")
