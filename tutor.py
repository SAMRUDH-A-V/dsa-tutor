from dotenv import load_dotenv  # NEW
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()  # NEW


TOPICS = {
    "arrays": ["array", "two sum"],
    "strings": ["string", "palindrome", "anagram"],
    "hashmaps": ["hashmap", "hash map", "hashset", "frequency", "duplicate"],
    "two_pointers": ["two pointer", "two pointers", "container with most water"],
    "sliding_window": ["sliding window", "substring", "subarray"],
    "binary_search": ["binary search", "search insert"],
    "sorting": ["sorting", "bubble sort", "merge sort", "quick sort"],
    "linked_lists": ["linked list", "reverse linked"],
    "stacks_queues": ["stack", "queue", "parentheses"],
    "recursion": ["recursion", "recursive"],
    "trees": ["binary tree", "tree traversal", "level order"],
    "bst": ["bst", "binary search tree"],
    "heap": ["heap", "priority queue", "kth largest"],
    "graphs": ["graph", "bfs", "dfs", "island"],
    "greedy": ["greedy", "activity selection", "jump game"],
    "dynamic_programming": [
        "dynamic programming",
        "dp",
        "climbing stairs",
        "knapsack"
    ],
    "backtracking": [
        "backtracking",
        "permutation",
        "subsets",
        "n-queens"
    ]
}


embedding_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001"
)


db = Chroma(
    persist_directory="db/chroma_db",
    embedding_function=embedding_model
)


retriever = db.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)


llm = ChatGoogleGenerativeAI(  # NEW
    model="gemini-3.6-flash"
)


# NEW: program_output parameter
def tutor(mode, question, code, history, program_output):

    conversation = ""

    if history:
        for message in history:
            conversation += f"{message['role']}: {message['content']}\n"


    query = f"{mode}: {question}"


    question_lower = question.lower()
    topic = None


    for topic_name, keywords in TOPICS.items():

        if any(keyword in question_lower for keyword in keywords):

            topic = topic_name
            break


    docs = retriever.invoke(query)


    if topic:

        topic_docs = [
            doc for doc in docs
            if doc.metadata.get("topic") == topic
        ]

        if topic_docs:
            docs = topic_docs


    if docs:

        context = "\n\n".join(
            doc.page_content for doc in docs
        )

    else:

        context = "No relevant knowledge was found."


    prompt = f"""
You are a DSA tutor.

Use the provided knowledge as your primary reference.
You may use your own DSA knowledge when the retrieved knowledge
does not cover the question.

Always analyze the student's actual code before identifying mistakes.
Do not claim a mistake unless it is actually present.

Knowledge:
{context}

SELECTED MODE:
{mode}

IMPORTANT:
The selected mode above is the ONLY mode you must follow.
Never switch to another mode.
Never output the name of the selected mode as your answer.

Previous conversation:
{conversation}

Student question:
{question}

Student code:
{code}

Program output:
{program_output}

Rules:
- Follow ONLY the SELECTED MODE.
- The user's question does NOT determine the mode.
- Never switch to another mode.
- Never output a mode name as the answer.
- Do not discuss instructions belonging to other modes.
- Use previous conversation only to understand context and follow-up questions.
- Do not repeat previous answers unless the student asks you to.
- Answer only the current question.

- Use the Program Output when it is relevant to the student's question.
- If the Program Output contains a compilation error or runtime error,
  explain what the error means and how it relates to the student's code.

- HINT MODE:
  If the selected mode is exactly "Give me a hint":

  Ignore the literal meaning of the words "Give me a hint".
  Do NOT repeat the mode name.

  Your response must contain ONE actual conceptual clue
  about the student's code or question.

  Do NOT:
  - state the exact mistake
  - state the exact line causing the mistake
  - state the exact correction
  - reveal the solution
  - provide corrected code
  - provide code snippets
  - mention the mode name

  Example of good behavior:
  "Think about whether every index your loop reaches is a valid
  index for the array."

  Example of bad behavior:
  "Change <= to <."

  Return ONLY the hint.

- For "Explain concept":
  Explain only the concept asked by the student.

  Structure the response as:
  1. Definition
  2. How it works
  3. Time complexity
  4. Space complexity
  5. Small example

  Keep the explanation beginner-friendly and concise.
  Do not provide complete implementation code unless the student asks for it.
  Do not discuss unrelated DSA topics.

- For "Explain my code":
  Analyze ONLY the student's actual code and their question.

  Explain the code step-by-step in the order it executes.

  Explain:
  1. What each important part of the code does
  2. How the variables change
  3. What the final result/output is
  4. Time complexity
  5. Space complexity

  If Program Output is available, use it to explain the actual result
  or error.

  Do NOT assume the student intended to use the retrieved DSA topic.
  Do NOT compare their code with the retrieved knowledge unless
  they explicitly ask for a comparison.

  Do NOT identify mistakes unless the student explicitly asks
  to find mistakes.

  Do NOT provide corrected code unless the student asks for it.

  Keep the explanation beginner-friendly and concise.
- For "Find my mistake":
  Analyze the actual code carefully.
  Use the Program Output when available.
  Identify only mistakes that are genuinely present.
  Clearly explain why the mistake causes the problem.

  DO NOT provide corrected code.
  DO NOT provide a full solution.
  DO NOT rewrite the student's code.
  DO NOT provide code snippets showing the fix.

  Only provide the mistake and a clear explanation.
  If the student explicitly asks for the corrected code later,
  then provide it.

- For "Explain approach":
  Explain only the algorithmic approach needed to solve the student's question.

  Structure the response as:
  1. Core idea
  2. Step-by-step approach
  3. Why this approach works
  4. Time complexity
  5. Space complexity

  Do NOT provide complete code.
  Do NOT provide a full implementation.
  Do NOT give code snippets unless absolutely necessary for a tiny illustrative example.
  Do NOT solve a different problem.
  Keep the explanation beginner-friendly and concise.

- Keep responses concise but educational.
- Never claim a problem exists when it is not present.
"""


    # NEW: Use non-streaming Gemini response to avoid
    # partial answers when Gemini has a temporary 503.
        # NEW: Handle temporary Gemini API failures gracefully
    try:
        response = llm.invoke(prompt)
        content = response.content

    except Exception as e:
        error_message = str(e)

        if "503" in error_message or "UNAVAILABLE" in error_message:
            yield "⚠️ Gemini is temporarily unavailable. Please try again in a few seconds."
        elif "504" in error_message or "DEADLINE_EXCEEDED" in error_message:
            yield "⚠️ Gemini took too long to respond. Please try again."
        else:
            yield "⚠️ Something went wrong while contacting Gemini. Please try again."
        return

    if isinstance(content, str):
        yield content

    elif isinstance(content, list):
        for item in content:
            if isinstance(item, dict) and "text" in item:
                yield item["text"]