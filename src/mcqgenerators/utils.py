import json
import traceback

import PyPDF2


def read_file(file):
    """
    Read PDF or TXT files and return their contents as text.
    """

    if file.name.lower().endswith(".pdf"):

        try:
            pdf_reader = PyPDF2.PdfReader(file)

            text = ""

            for page in pdf_reader.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text

            return text

        except Exception as e:
            raise Exception(f"Error reading the PDF file: {e}")

    elif file.name.lower().endswith(".txt"):

        return file.read().decode("utf-8")

    else:

        raise Exception(
            "Unsupported file format. "
            "Only PDF and TXT files are supported."
        )

def get_table_data(quiz_str):
    """
    Convert the LLM-generated MCQ response into
    table-ready data.
    """

    try:

        # -----------------------------------------
        # Make sure we have a string
        # -----------------------------------------

        if not isinstance(quiz_str, str):
            raise ValueError("Quiz response is not a string.")

        quiz_str = quiz_str.strip()


        # -----------------------------------------
        # Remove Markdown code fences
        # -----------------------------------------

        quiz_str = quiz_str.replace("```json", "")
        quiz_str = quiz_str.replace("```", "")

        quiz_str = quiz_str.strip()


        # -----------------------------------------
        # Find the actual JSON object
        # -----------------------------------------

        start = quiz_str.find("{")
        end = quiz_str.rfind("}")

        if start == -1 or end == -1:
            raise ValueError(
                "No JSON object found in the LLM response."
            )


        # Extract only JSON
        quiz_str = quiz_str[start:end + 1]


        # -----------------------------------------
        # Convert JSON string → Python dictionary
        # -----------------------------------------

        quiz_dict = json.loads(quiz_str)


        # -----------------------------------------
        # Convert dictionary → table data
        # -----------------------------------------

        quiz_table_data = []

        for key, value in quiz_dict.items():

            mcq = value["mcq"]

            options = " || ".join(
                [
                    f"{option} -> {option_value}"
                    for option, option_value
                    in value["options"].items()
                ]
            )

            correct = value["correct"]

            quiz_table_data.append(
                {
                    "MCQ": mcq,
                    "Choices": options,
                    "Correct": correct
                }
            )


        return quiz_table_data


    except Exception as e:

        traceback.print_exception(
            type(e),
            e,
            e.__traceback__
        )

        return False

    
def get_response_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    except Exception as e:
        traceback.print_exception(
            type(e),
            e,
            e.__traceback__
        )
        return False

     
