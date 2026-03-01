from app.questionnaire_parser import parse_questionnaire
from app.qa_service import answer_question


def process_questionnaire(file_path: str):
    questions = parse_questionnaire(file_path)

    results = []

    for question in questions:
        result = answer_question(question)
        results.append(result)

    return results