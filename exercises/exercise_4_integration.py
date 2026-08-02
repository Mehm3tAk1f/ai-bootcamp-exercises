"""
Exercise 4: Integration Challenge
===================================

Build a mini data pipeline that processes text documents.
This exercise has three levels — complete as far as you can.

- BASE: File reading and text processing (no LLM needed)
- STANDARD: Add LLM-based analysis
- ADVANCED: Production-grade pipeline with error recovery

Uses the same LLM provider configured in utils/llm_client.py.
"""

import json
from pathlib import Path
from collections import Counter

from utils import call_llm  # noqa: configured in utils/llm_client.py


DOCUMENTS_PATH = Path(__file__).parent.parent / "data" / "documents"
OUTPUT_PATH = Path(__file__).parent.parent / "output"


# ============================================================
# BASE LEVEL — File I/O and text processing (no LLM needed)
# ============================================================

def read_documents(folder: Path) -> list[dict]:
    """
    Read all .txt files from the given folder.
    Return a list of dicts: [{"filename": str, "content": str}, ...]
    """
    # findind the txt files in the folder
    path = Path(folder)
    files = list(path.glob("*.txt"))

    # preparing the return list
    files_list = []
    filename = ""
    text = ""

    for file in files:
        # filename and the content
        filename = file.name
        text = file.read_text()

        # appending the dictionary with the name and the content to the list
        files_list.append({"filename": filename, "content": text})

    return files_list


def word_count(text: str) -> int:
    """Return the number of words in a text."""

    number = len(text.split())
    return number


def extract_keywords_simple(text: str, top_n: int = 5) -> list[str]:
    """
    Extract the top N most frequent meaningful words from text.
    Exclude common stop words (the, a, is, in, of, and, to, for, etc.)
    Return as a list of lowercase words.
    """
    # for removing the punctuations
    import re

    stop_words = ["the", "a", "is", "in", "of", "and", "to", "for", "because", "an", "as", "at", "but", "with", "are", "by", "that", "has"]
    new_text = text.lower() # lowercase words for comparing correctly
    clean_text = re.sub(r'[^\w\s]', '', new_text) # regex to remove punctuations

    word_list = clean_text.split() # removing whitespaces
    result = [word for word in word_list if word not in stop_words] # creating a word list with no stop words included
    most_common_words_numbers = Counter(result).most_common(top_n) # most common words as tuples (word, frequency)

    most_common_words = []
    for word, number in most_common_words_numbers:
        most_common_words.append(word)
    return most_common_words


def basic_stats(documents: list[dict]) -> dict:
    """
    Return basic statistics about the document set:
    - total_documents: int
    - total_words: int
    - avg_words_per_doc: float
    - shortest_doc: str (filename)
    - longest_doc: str (filename)
    """
    total_documents = len(documents)

    # dictionary with each filename and word count for each to easily find the min, max, and total
    documents_dict = {document["filename"]: word_count(document["content"]) for document in documents}

    total_words = sum(documents_dict.values())

    avg_words_per_doc = total_words / total_documents

    shortest_doc = min(documents_dict, key=documents_dict.get)

    longest_doc = max(documents_dict, key=documents_dict.get)

    result = {"total_documents": total_documents, "total_words": total_words, "avg_words_per_doc": avg_words_per_doc, "shortest_doc": shortest_doc, "longest_doc": longest_doc}

    return result


# ============================================================
# STANDARD LEVEL — LLM-powered analysis
# ============================================================

def analyze_document(content: str) -> dict:
    """
    Use an LLM to analyze a single document and return:
    - summary: str (one sentence)
    - keywords: list[str] (3-5 keywords)
    - sentiment: str (positive/neutral/negative)
    """
    prompt = f"""Analyze the given text and return JSON file output in the following format.
summary: the summary of the text in one sentence,
keywords: 3 to 5 keywords in a list,
sentiment: choose one of the following options according to the given text; 'positive', 'neutral', 'negative'
    
Example output: {{"summary": "this is the summary", "keywords": ["some", "keywords"], "sentiment": "neutral"}}
    
Keys are in order: 'summary', 'keywords', 'sentiment'
The output must be a JSON parseable, no description or markdown included.
    
TEXT:
{content}
    """
    final_text = json.loads(call_llm(prompt))
    return final_text


def process_all_documents(documents: list[dict]) -> list[dict]:
    """
    Process all documents and return enriched results.
    Each result should contain: filename, summary, keywords, sentiment.
    """
    result = []
    for document in documents:
        text_dict = analyze_document(document["content"])
        text_dict.update({"filename":document["filename"]})
        result.append(text_dict)

    return result


def save_results(results: list[dict], output_path: Path) -> None:
    """Save results to a JSON file."""

    import os

    # if file doesn't exist, mode = x, creates it; if file exists, mode = w, overwrites it
    mode = "w" if os.path.isfile(output_path) else "x"
    
    with open(file=output_path, mode=mode) as f:
        json.dump(results, f, indent=4) # indent 4 makes the output human readable


def generate_report(results: list[dict]) -> str:
    """
    Generate a formatted summary report containing:
    - Total documents processed
    - Sentiment distribution (how many positive/neutral/negative)
    - Top 10 most common keywords across all documents
    """
    total_documents = len(results)

    # dict to count sentiments
    sentiment_dist = {"positive": 0, "neutral": 0, "negative": 0}

    # list for keywords
    keywords = []

    # adding each sentiment to the dict and keywords to the list
    for result in results:
        sentiment_dist[result["sentiment"]] += 1
        keywords.extend(result["keywords"])

    most_common_words_tuple = Counter(keywords).most_common(10) # this returns most common words with the freq (word, number)
    most_common_words = [word for word, number in most_common_words_tuple] # we just need the words

    report = f"""
Total documents processed: {total_documents}
Sentiment distribution: {sentiment_dist.items()}
Top 10 most common words: {', '.join(most_common_words)}"""

    return report


# ============================================================
# ADVANCED LEVEL — Production-ready pipeline
# ============================================================

def process_with_recovery(documents: list[dict]) -> dict:
    """
    Process documents but handle failures gracefully:
    - If a document fails, log the error and continue
    - Retry failed documents once
    - Return both results and error log

    Return: {
        "results": [...],
        "errors": [{"filename": ..., "error": ...}],
        "success_rate": float
    }
    """
    result_dict = {"results": [], "errors": [], "success_rate": float}
    for document in documents:
        results = []
        errors = []
        try:
            document_result = process_all_documents([document])[0]
            results.append(document_result)
            result_dict["results"] += results
        except:
            try:
                document_result = process_all_documents([document])[0]
                results.append(document_result)
                result_dict["results"] += results
            except Exception as e:
                errors.append({"filename": document["filename"], "error": e})
                result_dict["errors"] += errors
    rate = len(result_dict["results"]) / len(documents)
    result_dict["success_rate"] = rate
    return result_dict


def incremental_processing(documents: list[dict], output_path: Path) -> list[dict]:
    """
    Process documents incrementally:
    - Check if output file already exists
    - If yes, only process documents not already in the output
    - Append new results to existing output
    - This avoids re-processing and wasting API calls

    Return the complete results (existing + new).
    """
    new_file = []
    if not Path.exists(output_path):
        new_file = process_all_documents(documents)
    else:
        text_in_file = json.loads(output_path.read_text()) # list of dict
        file_names = [file_dict["filename"] for file_dict in text_in_file] # extracting filenames from each dict
        for document in documents:
            if document["filename"] not in file_names:
                new_file.append(process_all_documents([document])[0])
        new_file.extend(text_in_file)

    save_results(new_file,output_path)
    return new_file


def generate_comparison_report(results: list[dict]) -> str:
    """
    Generate an advanced report that also includes:
    - Document similarity (which documents cover similar topics?)
    - Topic clusters (group documents by dominant keyword overlap)
    - Confidence notes (which analyses might be unreliable and why?)
    """
    # TODO: Implement advanced reporting
    pass


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  Exercise 4: Integration Challenge")
    print("=" * 60)

    # --- BASE ---
    print("\n--- BASE LEVEL ---")
    documents = read_documents(DOCUMENTS_PATH)
    if documents:
        print(f"Loaded {len(documents)} documents")
        stats = basic_stats(documents)
        if stats:
            print(f"Total words: {stats.get('total_words')}")
            print(f"Avg words/doc: {stats.get('avg_words_per_doc', 0):.0f}")
            print(f"Shortest: {stats.get('shortest_doc')}")
            print(f"Longest: {stats.get('longest_doc')}")

        # Show simple keyword extraction for first doc
        if documents:
            kw = extract_keywords_simple(documents[0]["content"])
            if kw:
                print(f"Keywords ({documents[0]['filename']}): {kw}")
    else:
        print("read_documents() not implemented yet")

    # --- STANDARD ---
    print("\n--- STANDARD LEVEL ---")
    if documents:
        results = process_all_documents(documents)
        if results:
            OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
            save_results(results, OUTPUT_PATH / "analysis_results.json")
            print(f"Results saved to output/analysis_results.json")

            report = generate_report(results)
            if report:
                print(f"\n{report}")
        else:
            print("process_all_documents() not implemented yet")

    # --- ADVANCED ---
    print("\n--- ADVANCED LEVEL ---")
    if documents:
        recovered = process_with_recovery(documents)
        if recovered:
            print(f"Success rate: {recovered.get('success_rate', 0):.0%}")
            if recovered.get("errors"):
                print(f"Errors: {len(recovered['errors'])}")
        else:
            print("process_with_recovery() not implemented yet")
