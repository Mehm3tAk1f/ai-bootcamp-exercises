# Solution Notes

## Environment
- Python version: 3.12.0
- Key libraries used: pandas, sqlite3, csv, collections, json, pathlib, requests
- LLM API used: Ollama
- LLM model used: llama3.2

## Highest Level Completed

_Mark which level you reached per exercise:_

| Exercise | BASE | STANDARD | ADVANCED |
|----------|------|----------|----------|
| 1 - Python & Data | [X] | [X] | [X] |
| 2 - SQL | [X] | [X] | [X] |
| 3 - LLM | [X] | [X] | [ ] |
| 4 - Integration | [X] | [X] | [X] |

---

## Exercise 1: Data Handling

**Your approach:** _Describe what you did and why._

I started with the base level. I used csv.DictReader to read the data and did simple operations. For the standard level, I used pandas for cleaning and aggregation. On the advanced level, I did chunked loading, anomaly detection, and a summary report that reuses the earlier functions instead of recomputing everything from scratch.


**If you completed BASE:** What was your strategy for handling the messy priority values (mixed case like "HIGH", "high", "High")? Did you use any specific Python technique?

I used the .lower() function for comparisons. This made the comparison accurate and case-insensitive.


**If you completed STANDARD:** What would you change if this dataset had 1 million rows instead of 35?

If I were to use loops, it would make the functions very slow. Even though I had 35 rows in this exercise, I still tried to think of usage in big datasets and stayed away from loops. Since pandas DataFrames are useful for vectorized operations, I used it. So I would probably do the same for a big dataset and keep the operations as minimal as possible for faster outputs.
For the memory, I would read the dataset in chunks and combine them later. I would also try to avoid using .copy() function since it duplicates the whole DataFrame.


**If you completed ADVANCED:** How did you decide what counts as an "anomaly"? Where do you draw the line between messy data and actually wrong data?

Anomalies were defined in the docstring and I followed it. They were:
    - resolved_at earlier than created_at
    - resolution time over 30 days
    - duplicate ticket titles from the same customer
Messy data can still be useful; it can have blank fields or wrong casing. It can be normalized during cleaning. Wrong data cannot be useful. It can be contradictory or implausable.


---

## Exercise 2: SQL

**Your approach:** _Describe what you did and why._

SQL was the most comfortable for me. It started with very simple queries, then it became quite difficult in the advanced level. I like writing the table columns down on paper and brainstorm on how to write the query, how to connect the tables, and how to seperate it into subqueries.


**If you completed BASE:** Which query was hardest to write and what did you look up or try before getting it right?

It was very easy at this level. I could not remember how to shorten the table name so I looked it up.


**If you completed STANDARD:** In Query 6 (active projects per department), how did you handle departments with zero projects? What happens if you use INNER JOIN instead?

I used LEFT JOIN. LEFT JOIN keeps the rows even if they don't have matching rows in the joining table. If I used INNER JOIN, it would throw away the rows that don't have matching rows. In this case, we wanted to keep departments with zero active projects as well and it requires to use a LEFT JOIN.


**If you completed ADVANCED:** Query 9 (highest salary per department with ties) — what approach did you take, and what's an alternative way to solve it?

I started with creating the subquery to find the maximum salaries in each department. Then I matched the department_ids and salaries in the subquery to the employee.department_id and the salary. This allows to show everyone with the highest salary from each department. Alternative approach would be a window function. It would be RANK() OVER (PARTITION BY department_id ORDER BY salary DESC).


---

## Exercise 3: LLM & Prompt Engineering

**Your approach:** _Describe what you did and why._

I started with single prompts like summarization and later did json extraction, comparison between two prompts. I did not complete the advanced level yet. 


**If you completed BASE:** What did you notice about how the LLM responds differently when you change the wording of your prompt? Give a specific example.

prompt = f"Classify the following text exactly 'positive', 'neutral', or 'negative' depending on the sentiment of the given text. Your answer must be one word.\n\n{text}"

I tried to receive a one-word answer from LLM with this prompt. It kept giving me capitalized words even though the options are given. So I made it explicit that I want one word lowercase word,


prompt = f"Classify the following text exactly one word lowercase 'positive', 'neutral', or 'negative' depending on the sentiment of the given text. Your answer must be one word.\n\n{text}"
return call_llm(prompt).lower().strip()
I still used the lower() funtion in case it happens again.


**If you completed STANDARD:** Which of your two prompt strategies worked better? Paste both prompts here and explain what specifically made the difference.

v1: "According to the text, give me only JSON array output in the following format:
    - company_name: str,
    - industry: str,
    - founded_year: int,
    - num_employees: int,
    - key_products: list[str]
    TEXT:
    {text}"

v2: "You are a deterministic information extraction system. Your outputs are always and only JSON arrays, no descriptions or markdowns.
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
    {text}"

v1 was schema-only. I didn't mention what to do when the information is not given in the text. v2 was explicitly told what to do if the information is not given. It also had an example format to follow. v1 is more likely to hallucinate. v2 also had a role and was emphasized to give JSON array, v1 was not. v1 is more likely to not give wanted output format.


**If you completed ADVANCED:** How does your retry logic decide when to give up? What's the worst-case scenario for your error handling?

---

## Exercise 4: Integration

**Your approach:** _Describe what you did and why._

I handled file I/O and pure-Python word-frequency keyword extraction. Later added LLM analysis per document. I saved it to a file and also created a report. I added fault tolerance and resumable incremental processing. I am still not done with the last function of the advanced level.


**If you completed BASE:** How did you handle stop-word removal in keyword extraction? What list did you use and would you change it?

For the stop-words, I googled the most common words and created a list. During the extraction, the word is only included if it is not in the stop-word list. It worked, however there are too many stop words to include in a small list and this list would fail if we had much longer texts. I would use NLTK library stop-words for longer texts.


**If you completed STANDARD:** If one document fails during LLM processing, does your pipeline stop or continue? Paste the specific code that handles this.

process_all_documents has no error handling, it is handled in process_with_recovery function. I handled the errors in process_with_recovery since I needed the error messages and I wanted to use process_all_documents within the function.

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


**If you completed ADVANCED:** How does your incremental processing detect which documents were already processed? What happens if the output file gets corrupted?

It checks for the existing files and reads the names of the files. If the file name in the existing file already, it is skipped. If the output file gets corrupted, it causes error and would crash.


---

## Process Questions

_These questions are about your experience doing the task, not the code itself._

1. **What did you get stuck on longest?** Describe the specific moment — what you were trying to do, what went wrong, and how you got past it.

I was stuck with the comparison between two prompts. I tried to make one prompt visibly better than the other one, like an upgrade. However, the second prompt did not extract all the information given in the text. The second prompt was an overkill for a simple task and I had to delete some parts of it to not make it too strict. On the other hand, I wanted the first prompt to cause hallucination. I didn't explain what to do if the information was not given. It still functioned suprisingly well. 


2. **What did you Google/search for during this task?** List 2–3 specific things you looked up.

I look up for the syntax and useful functions for my use. I googled how to use TimeDelta functions, pandas library functions, general stop-words and etc. 


3. **If you used AI tools (Copilot, ChatGPT, etc.), which parts did you use them for?** Be honest — this is not penalized. We want to understand your workflow.

I used AI to seek help to solve the advanced levels. I use it as a mentor/reviewer to check my process and give me a hint when I am stuck. I wrote all my codes, it was used as a guidence.


---

## Self-Estimation

_Rate your current skill level honestly (1 = no experience, 5 = very confident):_

| Skill | 1 | 2 | 3 | 4 | 5 |
|-------|---|---|---|---|---|
| Python programming | [ ] | [ ] | [X] | [ ] | [ ] |
| Working with data (files, CSV, JSON) | [ ] | [ ] | [X] | [ ] | [ ] |
| pandas / data analysis | [ ] | [ ] | [X] | [ ] | [ ] |
| SQL | [ ] | [ ] | [ ] | [X] | [ ] |
| Git and version control | [ ] | [ ] | [ ] | [X] | [ ] |
| REST APIs (calling/building) | [ ] | [ ] | [X] | [ ] | [ ] |
| LLMs and prompt engineering | [ ] | [ ] | [X] | [ ] | [ ] |
| Error handling and debugging | [ ] | [ ] | [X] | [ ] | [ ] |
| Reading documentation to learn new tools | [ ] | [ ] | [ ] | [X] | [ ] |
| Explaining technical concepts to others | [ ] | [ ] | [ ] | [X] | [ ] |

**What is your strongest technical skill overall?**
_ I am very comfortable with Python Programming

**What is the area you most want to improve during the bootcamp?**
_ I would love to improve my prompt engineering skills, how to prepare production-ready pipelines

**Have you built any personal or work projects before? If yes, briefly describe one:**
_

---

## Self-Assessment

_What are you least confident about in your submission? What would you do differently next time?_
 I am not satisified with my work in exercise 3 and 4. I didn't complete the advanced levels as I wanted. I still tried my best to do the advanced levels in general but I would love to be more comfortable completing them and giving more reliable codes.