from groq import Groq
import re
import json
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.environ("GROQ_API_KEY")

def clean_invalid_chars(text):
    return re.sub(r'[\x00-\x1F\x7F]', '', text)

def safe_json_parse(text):
    try:
        return json.loads(text), None
    except json.JSONDecodeError as e:
        return None, str(e)

def evaluate_ssc_letter(question, letter_text, difficulty_type):
    
    client = Groq(api_key=GROQ_API_KEY)  
    
    marking_scheme = {
        "Relevance": 10,
        "Spelling_Grammar": 5,
        "Word_Limit": 5,
        "Content_Quality": 8,
        "Format": 5,
        "Writing_Neatness": 5,
        "Effective_Sentences": 7,
        "Cohesiveness": 5
    }
    
    prompt = f"""
    Assume you are an examiner for the SSC CGL descriptive writing test. Your task is to evaluate the response solely based on the given prompt for the following criteria: Lexical Resource, Grammatical Range and Accuracy, Task Achievement, and Coherence and Cohesion. Assign marks from 0-50 for each criterion based on the provided description. Remain consistent in your assessment even if the same response is submitted multiple times.
    Evaluate based on the selected difficulty level: {difficulty_type}.

    1. **Lexical Resource**: The range and accuracy of vocabulary used in the letter.
    2. **Grammatical Range and Accuracy**: The complexity and correctness of the grammar used.
    3. **Task Achievement**: How well the letter addresses the question, providing relevant arguments and supporting details.
    4. **Coherence and Cohesion**: The flow and organization of ideas and the use of transitions between sentences and paragraphs.

    The letter/application is expected to follow the structure of:
    - **Sender's Address**: Include all necessary contact details (email, residential address, etc.).
    - **Date**: The date the letter is written.
    - **Designation and Address of the Addressee**: Whom the letter is being addressed to.
    - **Subject**: Clearly state the purpose of the letter.
    - **Salutation**: Use a formal greeting (e.g., Respected Sir/Ma’am).
    - **Introduction**: Briefly state the purpose of writing the letter and the issue at hand.
    - **Body**: Elucidate the details of the issue in clear, concise sentences.
    - **Conclusion**: Reiterate the purpose of writing the letter, thank the reviewer, and provide a closing salutation.
    - **Sender’s Name and Designation**: End the letter with the sender’s name and position.

    The SSC CGL letter is evaluated on the following marking scheme {marking_scheme} with description:
    - **Relevance**: How well the letter addresses the topic (10 marks).
    - **Spelling/Grammar**: Accuracy in spelling and grammar (5 marks).
    - **Word Limit**: Adherence to the word limit in 150-175 words (5 marks). 
    - **Content Quality**: Depth and clarity of content (8 marks).
    - **Format**: Proper letter format (5 marks).
    - **Writing Neatness**: Clarity and neatness of writing (5 marks).
    - **Effective Sentences**: Use of varied and clear sentence structures (7 marks).
    - **Cohesiveness**: Logical flow and transitions between ideas (5 marks).

    Please evaluate the letter based on these criteria. Provide scores for each category, explain why the scores were assigned, and suggest improvements. Also, give an example of a perfect 50-mark answer for the question.'And also the total marks given should be out of 50'.
    Remember if there is nothing like the answer is blank then all score will be 0 and also remember this strictly that if the answer is not based on the question or is in other direction then also all the scores will be 0. (please evaluate this very strictly)
    
    Application Question: "{question}"
    Letter Text: "{letter_text}"

    *Final Output (Strictly in JSON format with no extra text or comments)*:
    {{
        "Relevance_Marks": [{{Relevance_Marks}}, "{{Explanation_for_relevance_score}}"],
        "Spelling_Grammar_Marks": [{{Spelling_Grammar_Marks}}, "{{Explanation_for_spelling_grammar_score}}"],
        "Content_Quality_Marks": [{{Content_Quality_Marks}}, "{{Explanation_for_content_quality_score}}"],
        "Format_Marks": [{{Format_Marks}}, "{{Explanation_for_format_score}}"],
        "Effective_Sentences_Marks": [{{Effective_Sentences_Marks}}, "{{Explanation_for_effective_sentences_score}}"],
        "Cohesiveness_Marks": [{{Cohesiveness_Marks}}, "{{Explanation_for_cohesiveness_score}}"],
        "Total_Marks": [{{Total_Marks}}, "{{Explanation_for_Total_Marks}}"],
        "Strengths": "[List of strengths from the user's answer]",
        "Weaknesses": "[List of weaknesses from the user's answer that need improvement]",
        "50_Marks_Answer": "[Generate a 50-mark answer for the letter writing question of SSC CGL descriptive part, ensuring it addresses all marking criteria comprehensively, with 100-150 words in response to {question}]",
        "AI_Suggestions": "[Provide specific suggestions for improvement based on the user's answer in {letter_text}]",
        "Improved_Solution": "[Provide a 50-mark improved solution for the user's answer {letter_text} based on the application question asked which was {question}]"
    }}
    """
    
    try:
        response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            response_format={"type": "json_object"}
        )
        
        # Extract the response and process it
        cleaned_content = clean_invalid_chars(response.choices[0].message.content.strip())
        evaluation_result, parse_error = safe_json_parse(cleaned_content)

        result = {
            "Word_Count": len(letter_text.split()),
            "Relevance_Marks": "N/A",
            "Spelling_Grammar_Marks": "N/A",
            "Content_Quality_Marks": "N/A",
            "Format_Marks": "N/A",
            "Effective_Sentences_Marks": "N/A",
            "Cohesiveness_Marks": "N/A",
            "Total_Marks": "N/A",
            "Strengths": "N/A",
            "Weaknesses": "N/A",
            "50_Marks_Answer": "N/A",
            "AI_Suggestions": "N/A",
            "Improved_Solution": "N/A"
        }

        if parse_error:
            print(f"JSON parsing error: {parse_error}")
            result["raw_response"] = cleaned_content

        # Populate result fields
        for key in result.keys():
            if key in evaluation_result:
                result[key] = evaluation_result.get(key, "N/A")
        
        print(result)
        return result

    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        return {
            "error": "Invalid response format from AI model",
            "raw_response": cleaned_content,
            "Relevance_Marks": "N/A",
            "Spelling_Grammar_Marks": "N/A",
            "Content_Quality_Marks": "N/A",
            "Format_Marks": "N/A",
            "Effective_Sentences_Marks": "N/A",
            "Cohesiveness_Marks": "N/A",
            "Total_Marks": "N/A",
            "Strengths": "N/A",
            "Weaknesses": "N/A",
            "50_Marks_Answer": "N/A",
            "AI_Suggestions": "N/A",
            "Improved_Solution": "N/A"
        }

    except Exception as e:
        return {"error": f"An error occurred while processing the request: {str(e)}"}



