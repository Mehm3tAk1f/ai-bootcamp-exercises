# Data & AI Bootcamp — Selection Task

## Overview

Welcome to the practical selection task for the Data & AI Bootcamp.

This task evaluates your ability to work with Python, data, SQL, and Large Language Models (LLMs). It consists of **4 exercises** that you should complete and submit as a GitHub repository.

**Estimated time:** 4–6 hours total

---

## Submission Instructions

1. Fork or clone this repository.
2. Complete all exercises in the designated files.
3. Commit your work with clear, meaningful commit messages.
4. Push your solution to your own GitHub repository (public or invite the reviewers).
5. Include a short `SOLUTION.md` file (see below).

---

## Exercises

Each exercise has **three levels**. Complete as far as you can:

| Level | Who it's for | What it shows |
|-------|-------------|---------------|
| **BASE** | Beginners / career changers | Basic programming ability and logical thinking |
| **STANDARD** | Intermediate developers | Working knowledge of tools and libraries |
| **ADVANCED** | Experienced developers | Production thinking, edge cases, optimization |

**You are NOT expected to complete everything.** Go as far as your skills allow. A fully completed BASE level is better than a broken ADVANCED attempt.

| # | Exercise | Skills Tested | Estimated Time |
|---|----------|---------------|----------------|
| 1 | Python & Data Handling | Python, data processing, pandas | 1–2 hours |
| 2 | SQL | Queries, JOINs, aggregation, subqueries | 30–60 min |
| 3 | LLM API & Prompt Engineering | API usage, prompt design, structured output | 1–2 hours |
| 4 | Integration Challenge | File I/O, LLM pipeline, reporting | 1–2 hours |

---

## Exercise 1: Python & Data Handling

**File:** `exercises/exercise_1_data.py`

You are given a dataset of customer support tickets (`data/support_tickets.csv`).

| Level | Tasks |
|-------|-------|
| **BASE** | Load CSV with pure Python (no pandas), count tickets by status, filter by priority, find missing data |
| **STANDARD** | Use pandas to clean data (normalize priorities, parse dates, remove nulls), compute monthly counts, avg resolution time, worst category |
| **ADVANCED** | Detect anomalies (impossible dates, duplicates), chunked loading for large files, generate a formatted summary report |

**Run:** `python exercises/exercise_1_data.py`

---

## Exercise 2: SQL

**File:** `exercises/exercise_2_sql.sql`

Given the schema in `data/schema.sql` (employees, departments, projects tables):

| Level | Queries |
|-------|---------|
| **BASE** | List employees sorted by name; JOIN employees with departments; count employees per department |
| **STANDARD** | Top 3 departments by avg salary; departments over budget; active project counts (including zeros) |
| **ADVANCED** | Employees hired recently in departments with completed projects; project success rate ranking; highest-paid employee per department |

**Run:** `python exercises/run_sql.py`

---

## Exercise 3: LLM API & Prompt Engineering

**File:** `exercises/exercise_3_llm.py`

**Setup — Free LLM Options (no paid account needed):**

| Option | Setup | Notes |
|--------|-------|-------|
| **Ollama** (recommended) | [ollama.com/download](https://ollama.com/download), then `ollama pull llama3.2` | Runs locally, completely free, no API key |
| **Hugging Face** | [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) | Free Inference API, many models available |
| **Google Gemini** | [aistudio.google.com/apikey](https://aistudio.google.com/apikey) | Free tier: 15 requests/min |
| **Groq** | [console.groq.com](https://console.groq.com) | Free tier, very fast inference |
| **OpenAI / Azure OpenAI** | If you already have access | Paid, not required |

Configure your provider in `exercises/utils/llm_client.py`. Document your choice in `SOLUTION.md`.

| Level | Tasks |
|-------|-------|
| **BASE** | Summarize a text, classify sentiment, answer a question based on context |
| **STANDARD** | Extract structured company data as JSON, write two prompt versions and compare them |
| **ADVANCED** | Retry with exponential backoff, validate JSON output, estimate token cost, budget-aware batch processing |

**Run:** `python exercises/exercise_3_llm.py`

---

## Exercise 4: Integration Challenge

**File:** `exercises/exercise_4_integration.py`

Process a folder of text documents (`data/documents/`) into structured insights.

| Level | Tasks |
|-------|-------|
| **BASE** | Read all files, count words, extract keywords by frequency (no LLM needed), compute basic stats |
| **STANDARD** | Use LLM to summarize, tag keywords, detect sentiment per doc; save to JSON; generate report |
| **ADVANCED** | Fault-tolerant processing (skip failures, retry), incremental/resumable pipeline, topic clustering |

**Run:** `python exercises/exercise_4_integration.py`

---

## SOLUTION.md Template

Create a `SOLUTION.md` file that includes:

```markdown
# Solution Notes

## Environment
- Python version:
- Key libraries used:
- LLM API used:

## Approach
Brief description of your approach for each exercise.

## Challenges
What was difficult? How did you solve it?

## Time Spent
Approximate time per exercise.

## Self-Assessment
What would you improve with more time?
```

---

## Evaluation Rubric

Your submission will be evaluated on:

| Criteria | Weight |
|----------|--------|
| Correctness (code works, outputs are valid) | 30% |
| Code quality (readability, structure, naming) | 20% |
| Problem-solving approach | 20% |
| LLM/prompt engineering quality | 15% |
| Documentation and communication | 15% |

---

## Important Notes

- You may use any Python libraries you find appropriate.
- You may use AI coding assistants, but **you must be able to explain every line of your code**.
- Focus on working, clean solutions rather than over-engineering.
- If you get stuck on one exercise, move on and come back later.
- Partial solutions are better than no submission.
- **Commit your work incrementally** — show your progress, not just the final result.

## Live Code Walkthrough

Be prepared to explain **why** you made specific choices, not just **what** the code does.

---

Good luck!
