
QA_PAIRS = {

    "what is a computer":
    "A computer is an electronic device that processes data and performs tasks according to instructions.",

    "what is python":
    "Python is a high-level programming language known for its simplicity and readability.",

    "what is machine learning":
    "Machine Learning is a subset of AI that enables systems to learn from data without explicit programming.",

    "what is ai":
    "Artificial Intelligence is the simulation of human intelligence by machines.",

    "what is sql":
    "SQL is a language used to manage and query relational databases.",

    "who developed python":
    "Python was created by Guido van Rossum and released in 1991.",

    "what is streamlit":
    "Streamlit is a Python framework used to build interactive web applications."
}

def get_response(question):

    if question is None:
        return ""

    question = question.lower().strip()

    return QA_PAIRS.get(
        question,
        "Sorry, I don't know the answer to that question yet."
    )