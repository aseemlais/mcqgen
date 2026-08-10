import json
import traceback
import pandas as pd
import streamlit as st

from src.mcqgenerators.utils import read_file, get_table_data
from src.mcqgenerators.MCQGenerator import generate_evaluate_chain
from src.mcqgenerators.logger import logging


# --------------------------------------------------
# Load response JSON
# --------------------------------------------------

with open("response.json", "r", encoding="utf-8") as file:
    RESPONSE_JSON = json.load(file)


# --------------------------------------------------
# Streamlit Application
# --------------------------------------------------

st.title("MCQs Creator Application with LangChain 🦜⛓️")


# --------------------------------------------------
# User Input Form
# --------------------------------------------------

with st.form("user_inputs"):

    # File upload
    uploaded_file = st.file_uploader(
        "Upload a PDF or TXT file",
        type=["pdf", "txt"]
    )

    # Number of MCQs
    mcq_count = st.number_input(
        "No. of MCQs",
        min_value=3,
        max_value=50,
        value=5,
        step=1
    )

    # Subject
    subject = st.text_input(
        "Insert Subject",
        max_chars=50
    )

    # Tone / difficulty
    tone = st.text_input(
        "Complexity Level of Questions",
        max_chars=20,
        placeholder="Simple"
    )

    # Submit button
    button = st.form_submit_button("Create MCQs")


# --------------------------------------------------
# Generate MCQs
# --------------------------------------------------

if button:

    if uploaded_file is None:
        st.warning("Please upload a PDF or TXT file.")

    elif not subject:
        st.warning("Please enter the subject.")

    elif not tone:
        st.warning("Please enter the complexity level.")

    else:

        with st.spinner("Generating MCQs..."):

            try:

                # ----------------------------------
                # Read uploaded file
                # ----------------------------------

                text = read_file(uploaded_file)

                logging.info(
                    f"File uploaded: {uploaded_file.name}"
                )

                logging.info(
                    f"Extracted text length: {len(text)}"
                )


                # ----------------------------------
                # Generate quiz + review
                # ----------------------------------

                response = generate_evaluate_chain.invoke(
                    {
                        "text": text,
                        "number": mcq_count,
                        "subject": subject,
                        "tone": tone,
                        "response_json": json.dumps(RESPONSE_JSON)
                    }
                )


                logging.info(
                    "MCQ generation and evaluation completed"
                )


                # ----------------------------------
                # Extract quiz
                # ----------------------------------

                quiz = response.get("quiz")
            

                review = response.get("review")


                if quiz is None:

                    st.error(
                        "MCQ generation failed. No quiz was returned."
                    )

                else:

                    # ------------------------------
                    # Convert JSON → table data
                    # ------------------------------

                    table_data = get_table_data(quiz)


                    if table_data:

                        df = pd.DataFrame(table_data)

                        # Start index from 1
                        df.index = df.index + 1


                        # --------------------------
                        # Display MCQs
                        # --------------------------

                        st.subheader("Generated MCQs")

                        st.table(df)


                        # --------------------------
                        # Display Review
                        # --------------------------

                        if review:

                            st.subheader("Quiz Review")

                            st.text_area(
                                label="Evaluation",
                                value=review,
                                height=200
                            )

                    else:

                        st.error(
                            "Error while processing the generated MCQs."
                        )


            except Exception as e:

                logging.error(
                    f"Error in Streamlit application: {e}"
                )

                traceback.print_exception(
                    type(e),
                    e,
                    e.__traceback__
                )

                st.error(
                    "An error occurred while generating the MCQs."
                )


                
