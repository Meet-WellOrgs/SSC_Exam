import streamlit as st
import json
import random
import re
from evaluation.precise_evaluation import evaluate_ssc_precis
from evaluation.essay_evaluation import evaluate_ssc_essay
from evaluation.letter_evaluation import evaluate_ssc_letter


def load_questions():
    with open('questions/data.json', 'r') as file:
        question_sets = json.load(file)
    selected_set = random.choice(question_sets)
    return selected_set["data"]


# To find the type of question (essay/letter/precise)
def detect_question_type(question):
    if re.search(r'\bessay\b', question, re.IGNORECASE):
        return 'essay'
    elif re.search(r'\bletter\b', question, re.IGNORECASE):
        return 'letter'
    elif re.search(r'\bprecis\b', question, re.IGNORECASE):
        return 'precis'
    else:
        return 'unknown'


# Evaluating question
def evaluate_question(question_type, question, answer, difficulty):
    if question_type == "essay":
        return evaluate_ssc_essay(question, answer, difficulty)
    elif question_type == "letter":
        return evaluate_ssc_letter(question, answer, difficulty)
    elif question_type == "precis":
        return evaluate_ssc_precis(question, answer, difficulty)
    else:
        return {"error": "Unable to evaluate question type"}


# Evaluation results (structured)
# def display_evaluation_results(col, question, answer, result):
#     col.write(f"### {question}")
#     col.write(f"**Your Answer:** {answer}")
    
#     for key, value in result.items():
#         if isinstance(value, list) and len(value) == 2:
#             col.write(f"**{key.replace('_', ' ')}:** {value[0]}")
#             col.write(f"**Explanation:** {value[1]}")
#         elif isinstance(value, str):
#             col.write(f"**{key.replace('_', ' ')}:** {value}")

def display_evaluation_results_side_by_side(result1, result2):
    metrics = result1.keys() 
    for metric in metrics:
        col1, col2 = st.columns(2)
        if isinstance(result1[metric], list) and len(result1[metric]) == 2:
            # Marks and explanation for metric
            col1.markdown(f"**{metric.replace('_', ' ').capitalize()}:** {result1[metric][0]}")
            col2.markdown(f"**{metric.replace('_', ' ').capitalize()}:** {result2[metric][0]}")
            col1.markdown(f"_Explanation_: {result1[metric][1]}")
            col2.markdown(f"_Explanation_: {result2[metric][1]}")
        elif isinstance(result1[metric], str):
            # For textual metrics
            col1.markdown(f"**{metric.replace('_', ' ').capitalize()}:** {result1[metric]}")
            col2.markdown(f"**{metric.replace('_', ' ').capitalize()}:** {result2[metric]}")


def main():
    st.title("SSC Descriptive Question Evaluator")

    # # Load question sets
    # question_data = load_questions()
    # question1 = question_data[0]["question"]
    # question2 = question_data[1]["question"]

    # Select random question set only once and store it in session_state
    if "question_data" not in st.session_state:
        st.session_state.question_data = load_questions()
        st.session_state.question1 = st.session_state.question_data[0]["question"]
        st.session_state.question2 = st.session_state.question_data[1]["question"]

    # Maintain session state
    if "current_question" not in st.session_state:
        st.session_state.current_question = 1
        st.session_state.answers = ["", ""]  # Stores answers for both questions
        st.session_state.results = [None, None]  # Stores evaluation results
    
    # Question Display and Answer Input
    if st.session_state.current_question == 1:
        st.write(f"**Question 1:** {st.session_state.question1}")
        st.session_state.answers[0] = st.text_area(
            "Write your answer here", value=st.session_state.answers[0]
        )
        if st.button("Next"):
            st.session_state.current_question = 2

    elif st.session_state.current_question == 2:
        st.write(f"**Question 2:** {st.session_state.question2}")
        st.session_state.answers[1] = st.text_area(
            "Write your answer here", value=st.session_state.answers[1]
        )
        if st.button("Submit"):
            # Detect question types
            q1_type = detect_question_type(st.session_state.question1)
            q2_type = detect_question_type(st.session_state.question2)

            # Evaluate both answers
            st.session_state.results[0] = evaluate_question(q1_type, st.session_state.question1, st.session_state.answers[0], "easy")
            st.session_state.results[1] = evaluate_question(q2_type, st.session_state.question2, st.session_state.answers[1], "easy")
            st.session_state.current_question = 3


    # Display Evaluation Results
    # if st.session_state.current_question == 3:
    #     st.write("### Evaluation Results")
    #     col1, col2 = st.columns(2)

    #     display_evaluation_results(col1, st.session_state.question1, st.session_state.answers[0], st.session_state.results[0])
    #     display_evaluation_results(col2, st.session_state.question2, st.session_state.answers[1], st.session_state.results[1])
    
    if st.session_state.current_question == 3:
        st.write("### Evaluation Results")
        st.write(f"**Question 1:** {st.session_state.question1}")
        st.write(f"**Question 2:** {st.session_state.question2}")
        st.write("---")
        
        display_evaluation_results_side_by_side(
            st.session_state.results[0], st.session_state.results[1]
        )

    
if __name__ == "__main__":
    main()
