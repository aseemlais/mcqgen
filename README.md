# 📝 AI-Powered MCQ Generator using LLMs, LangChain and Groq

## 📌 Project Overview

This project is an AI-powered application that automatically generates and evaluates Multiple Choice Questions (MCQs) from PDF and text-based educational content.

The application uses a Large Language Model (LLM) with LangChain prompt templates and sequential chains to generate relevant questions, multiple-choice options, correct answers, and explanations from the provided content. Groq is used for efficient LLM inference, while Streamlit provides an interactive web interface.

The project demonstrates an end-to-end Generative AI workflow, covering document processing, prompt engineering, LLM inference, structured MCQ generation, evaluation, interactive visualization, and cloud deployment using AWS EC2.

---

## 🎯 Objectives

- Generate MCQs automatically from PDF and text-based content
- Generate relevant questions and multiple-choice options using an LLM
- Identify the correct answer for each generated question
- Provide explanations for generated answers
- Implement structured LLM workflows using LangChain
- Use prompt templates for consistent MCQ generation
- Provide an interactive interface using Streamlit
- Deploy the application on AWS EC2

---

## 🛠️ Technologies Used

- **Python** – Application development and processing
- **Large Language Models (LLMs)** – MCQ generation
- **LangChain** – LLM application framework
- **Groq** – Fast LLM inference
- **Streamlit** – Interactive web interface
- **PyPDF** – PDF content extraction
- **Prompt Templates** – Structured prompt generation
- **Sequential Chains** – Sequential LLM workflow
- **python-dotenv** – Environment variable management
- **AWS EC2** – Cloud deployment

---

## 📂 Project Structure

```text
MCQ-Generator/
│
├── data/
│   └── input files
│
├── src/
│   └── mcqgenerator/
│       ├── __init__.py
│       ├── MCQGenerator.py
│       ├── utils.py
│       └── logger.py
│
├── templates/
│   └── ...
│
├── app.py
├── requirements.txt
├── setup.py
├── .gitignore
└── README.md