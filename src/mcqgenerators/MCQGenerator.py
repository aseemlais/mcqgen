import os
import json

from dotenv import load_dotenv

from mcqgenerators.utils import read_file, get_table_data
from mcqgenerators.logger import logging

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda


# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

load_dotenv()


# --------------------------------------------------
# Initialize Groq LLM
# --------------------------------------------------

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.3
)


# --------------------------------------------------
# MCQ Generation Prompt
# --------------------------------------------------

quiz_generation_template = """
You are an expert MCQ generator.

Given the text below, create exactly {number}
multiple-choice questions for {subject} students.

Use a {tone} tone.

Text:
{text}

Requirements:

1. Generate exactly {number} MCQs.
2. Each question must have exactly four options.
3. Options must be labeled a, b, c, and d.
4. Clearly identify the correct answer.
5. Do not repeat questions.
6. Questions must be based ONLY on the given text.
7. Do not introduce information that is not present in the text.
8. Return ONLY valid JSON.

Use the following JSON structure as a guide:

{response_json}
"""


quiz_generation_prompt = PromptTemplate(
    input_variables=[
        "text",
        "number",
        "subject",
        "tone",
        "response_json"
    ],
    template=quiz_generation_template
)


# --------------------------------------------------
# MCQ Generation Chain
# --------------------------------------------------

quiz_chain = quiz_generation_prompt | llm


# --------------------------------------------------
# MCQ Evaluation Prompt
# --------------------------------------------------

quiz_evaluation_template = """
You are an expert English grammarian, educator,
and MCQ evaluator.

You are given a multiple-choice quiz created for
{subject} students.

Evaluate the quiz based on:

1. Question clarity
2. Grammar
3. Relevance to the subject
4. Difficulty level
5. Quality of options
6. Correctness of answers
7. Whether the questions test understanding

Use a maximum of 50 words for the overall complexity analysis.

If any question is unclear, grammatically incorrect,
too easy, too difficult, or inappropriate for the
target students, identify it and suggest an improved version.

Quiz:

{quiz}

Provide your evaluation and suggested improvements.
"""


quiz_evaluation_prompt = PromptTemplate(
    input_variables=[
        "subject",
        "quiz"
    ],
    template=quiz_evaluation_template
)


# --------------------------------------------------
# Evaluation Chain
# --------------------------------------------------

review_chain = quiz_evaluation_prompt | llm


# --------------------------------------------------
# Generate + Evaluate
# --------------------------------------------------

def generate_quiz_and_review(inputs):

    logging.info("Starting MCQ generation")

    try:

        # Generate quiz
        quiz_response = quiz_chain.invoke(inputs)

        quiz = quiz_response.content

        logging.info("MCQ generation completed")

        # Prepare input for evaluation
        review_input = {
            "subject": inputs["subject"],
            "quiz": quiz
        }

        # Evaluate quiz
        review_response = review_chain.invoke(review_input)

        review = review_response.content

        logging.info("MCQ evaluation completed")

        return {
            "quiz": quiz,
            "review": review
        }

    except Exception as e:

        logging.error(f"Error during MCQ generation: {e}")

        raise e


# Convert the Python function into a LangChain Runnable
generate_evaluate_chain = RunnableLambda(
    generate_quiz_and_review
)
