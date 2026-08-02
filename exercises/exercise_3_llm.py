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
    prompt = f"Summarize the following text with 2-3 sentences.\n\n{text}"
    return call_llm(prompt)


def classify_sentiment(text: str) -> str:
    """
    Use the LLM to classify the sentiment of the text.
    Return one of: "positive", "neutral", "negative"
    """
    prompt = f"Classify the following text exactly one word lowercase 'positive', 'neutral', or 'negative' depending on the sentiment of the given text. Your answer must be one word.\n\n{text}"
    return call_llm(prompt).lower().strip() # prevents answer from being capitalized and extra space

def ask_question(text: str, question: str) -> str:
    """
    Given a text and a question, use the LLM to answer the question
    based only on the information in the text.
    """
    prompt = f"Answer the given question, only according to the given text. If the answer is not in the text, say 'I don't know'\n\n{text}\n{question}"
    return call_llm(prompt)


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
    prompt = f"""In the given text, give me the followings for each company;
    - company_name: str
    - industry: str
    - founded_year: int or None
    - num_employees: int or None
    - key_products: list[str]
    Only return a JSON array, no markdown or description.
    Do not make assumptions, use only the information given in the text.
    TEXT:
    {text}"""
    resulting_json = call_llm(prompt) # storing the resulting json file from the llm call
    return json.loads(resulting_json)

def extract_with_prompt_v1(text: str) -> list[dict]:
    """First prompt approach for extraction."""
    prompt = f"""According to the text, give me only JSON array output in the following format:
    - company_name: str,
    - industry: str,
    - founded_year: int,
    - num_employees: int,
    - key_products: list[str]
    TEXT:
    {text}"""
    resulting_json = call_llm(prompt)
    return json.loads(resulting_json)


def extract_with_prompt_v2(text: str) -> list[dict]:
    """Second prompt approach for extraction."""
    prompt = f"""You are a deterministic information extraction system. Your outputs are always and only JSON arrays, no descriptions or markdowns.
    Each object in the output must follow this format:
    company_name: "string",
    industry: "string",
    founded_year: 2020,
    num_employees: 100,
    key_products: ["product1", "product2"]
    
    Use only the information given in the text, don't make assumptions. 
    If the company_name or the industry is not given in the text, leave it empty string.
    If the founded_year or the num_employees is not given in the text, leave it None.
    If the key_products is not given in the text, leave it empty list.
    
    TEXT:
    {text}
    """
    resulting_json = call_llm(prompt)
    return json.loads(resulting_json)


def compare_prompts(text: str) -> None:
    """
    Run both prompts and print a comparison.
    Explain which works better and why (print your explanation).
    """
    # try except in case the extraction fails
    try:
        prompt1_json = extract_with_prompt_v1(text)
    except:
        print("The first prompt extraction failed. Try again.")
        prompt1_json = None
    try:
        prompt2_json = extract_with_prompt_v2(text)
    except:
        print("The second prompt extraction failed. Try again.")
        prompt2_json = None
    
    # comparison table
    w = 35 # width of each column
    categories = ["company_name", "industry", "founded_year", "num_employees", "key_products"]

    len_prompt1_json = len(prompt1_json) if prompt1_json is not None else 0
    len_prompt2_json = len(prompt2_json) if prompt2_json is not None else 0
    length = max(len_prompt1_json, len_prompt2_json, 5) # table will be the maximum of the two extraction, if they are too long it is limited to 5
    for i in range(length):
        row1 = ""
        row2 = ""
        for category in categories:
            try:
                prompt1_result = str(prompt1_json[i][category])
            except:
                prompt1_result = ""
            row1 += f'{prompt1_result:<{w}}'

            try:
                prompt2_result = str(prompt2_json[i][category])
            except:
                prompt2_result = ""
            row2 += f'{prompt2_result:<{w}}'
        print(f'{"company_name_v1":<{w}}{"industry_v1":<{w}}{"founded_year_v1":<{w}}{"num_employees_v1":<{w}}{"key_products_v1":<{w}}')
        print(row1)
        print(f'{"company_name_v2":<{w}}{"industry_v2":<{w}}{"founded_year_v2":<{w}}{"num_employees_v2":<{w}}{"key_products_v2":<{w}}')
        print(row2)
        print()


    # explanation
    print(f"""\nAfter multiple tries, it is visible that both prompts are not fully reliable.
The first prompt is not told what to do when the information is not given. It is more likely to hallucinate.
Also it is told to give JSON file as the output, but it still fails sometimes during the extraction.
On the other hand, the second prompt is more reliable to give correct format. However, the suprising part is, it is
more likely to miss information given in the text. I belive it is too strict to prevent hallucination, and this 
caused under extraction. At the end, the first prompt can extract everything, but can hallucinate or fail to extract. 
The second prompt always extracts, but can under extract. It seems better to use the second prompt since it is 
a safer option even though it can miss a few information given.""")


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
