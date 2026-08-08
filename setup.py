from setuptools import setup, find_packages

setup(
    name="mcq-generator",
    version="0.1.0",
    description="MCQ Generator using LangChain and Groq",
    author="Aseem",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "langchain",
        "langchain-core",
        "langchain-groq",
        "python-dotenv",
    ],
)