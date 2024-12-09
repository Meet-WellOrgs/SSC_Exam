from groq import Groq
import re
import json

def clean_invalid_chars(text):
    return re.sub(r'[\x00-\x1F\x7F]', '', text)

def safe_json_parse(text):
    try:
        return json.loads(text), None
    except json.JSONDecodeError as e:
        return None, str(e)


def evaluate_ssc_essay(question, essay_text, difficulty_type):
    
    client = Groq(api_key="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")  
    
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
    Assume you are an examiner for the SSC CGL descriptive writing test. Your task is to evaluate the response solely based on the given prompt for the following criteria: Lexical Resource, Grammatical Range and Accuracy, Task Achievement, and Coherence and Cohesion. Assign marks from 0-50 for criterion based on provided description. Remain consistent in your assessment even if the same response is submitted multiple times.
    Evaluate based on the selected difficulty level: {difficulty_type}.

    1. **Lexical Resource**: The range and accuracy of vocabulary used in the essay.
    2. **Grammatical Range and Accuracy**: The complexity and correctness of the grammar used.
    3. **Task Achievement**: How well the essay addresses the question, providing relevant arguments and supporting details.
    4. **Coherence and Cohesion**: The flow and organization of ideas and the use of transitions between sentences and paragraphs.

    The essay is expected to follow the structure of:
    - **Introduction**: Brief introduction of the topic and your thesis statement.
    - **Body**: 2-3 paragraphs with clear topic sentences, development, examples, and a summary at the end.
    - **Conclusion**: Restate your position and summarize key points.

    The SSC CGL essay is evaluated on the following marking scheme {marking_scheme} with description:
    - **Relevance**: How well the essay addresses the topic (10 marks).
    - **Spelling/Grammar**: Accuracy in spelling and grammar (5 marks).
    - **Word Limit**: Adherence to the word limit (5 marks).
    - **Content Quality**: Depth and clarity of content (8 marks).
    - **Format**: Proper essay format (5 marks).
    - **Writing Neatness**: Clarity and neatness of writing (5 marks).
    - **Effective Sentences**: Use of varied and clear sentence structures (7 marks).
    - **Cohesiveness**: Logical flow and transitions between ideas (5 marks).

    Please evaluate the essay based on these criteria. Provide scores for each category, explain why the scores were assigned, and suggest improvements. Also, give an example of a perfect 50-mark answer for the question.'And also the total marks given should be out of 50'.
    Remember if there is nothing like the answer is blank then all score will be 0 and also remember this strictly that if the answer is not based on the question or is in other direction then also all the scores will be 0. (please evaluate this very strictly)
    
    Essay Question: "{question}"
    Essay Text: "{essay_text}"

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
        "50_Marks_Answer": "[Generate a 50-mark answer for the essay question of SSC CGL descriptive part, ensuring it addresses all marking criteria comprehensively, with at least 200 words in response to {question}]",
        "AI_Suggestions": "[Provide specific suggestions for improvement based on the user's answer in {essay_text}]",
        "Improved_Solution": "[Provide a 50-mark improved solution for the user's answer {essay_text} based on the essay question asked which was {question}]"
    }}
    """
    
    try:
        # Sending essay and question to Groq API for evaluation
        response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            response_format={"type": "json_object"}
        )
        
        # Extract the response and process it
        # result = response['choices'][0]['message']['content'].strip()
        cleaned_content = clean_invalid_chars(response.choices[0].message.content.strip())
        
        evaluation_result, parse_error = safe_json_parse(cleaned_content)

        result = {
            "Word_Count": len(essay_text.split()),
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

        try:
            result["Relevance_Marks"] = evaluation_result.get("Relevance_Marks", "N/A")
        except Exception as e:
            print(f"Error extracting Relevance marks: {e}")

        try:
            result["Spelling_Grammar_Marks"] = evaluation_result.get("Spelling_Grammar_Marks", "N/A")
        except Exception as e:
            print(f"Error extracting Spelling Grammar Marks: {e}")

        try:
            result["Content_Quality_Marks"] = evaluation_result.get("Content_Quality_Marks", "N/A")
        except Exception as e:
            print(f"Error extracting Content Quality Marks: {e}")

        try:
            result["Format_Marks"] = evaluation_result.get("Format_Marks", "N/A")
        except Exception as e:
            print(f"Error extracting Format Marks: {e}")

        try:
            result["Effective_Sentences_Marks"] = evaluation_result.get("Effective_Sentences_Marks", "N/A")
        except Exception as e:
            print(f"Error extracting Effective Sentences Marks: {e}")

        try:
            result["Cohesiveness_Marks"] = evaluation_result.get("Cohesiveness_Marks", "N/A")
        except Exception as e:
            print(f"Error extracting Cohesiveness Marks: {e}")

        try:
            result["Total_Marks"] = evaluation_result.get("Total_Marks", "N/A")
        except Exception as e:
            print(f"Error extracting Total Marks: {e}")

        try:
            result["Strengths"] = evaluation_result.get("Strengths", "N/A")
        except Exception as e:
            print(f"Error extracting Strengths: {e}")

        try:
            result["Weaknesses"] = evaluation_result.get("Weaknesses", "N/A")
        except Exception as e:
            print(f"Error extracting Weaknesses: {e}")

        try:
            result["50_Marks_Answer"] = evaluation_result.get("50_Marks_Answer", "N/A")
        except Exception as e:
            print(f"Error extracting 50 Marks Answer: {e}")

        try:
            result["AI_Suggestions"] = evaluation_result.get("AI_Suggestions", "N/A")
        except Exception as e:
            print(f"Error extracting AI Suggestions: {e}")

        try:
            result["Improved_Solution"] = evaluation_result.get("Improved_Solution", "N/A")
        except Exception as e:
            print(f"Error extracting Improved Solution: {e}")

        print(result)
        return result

    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        return {
            "error": "Invalid response format from AI model",
            "raw_response":cleaned_content,
            "Relevance_Marks": "N/A",
            "Spelling_Grammar_Marks": "N/A",
            "Content_Quality_Marks": "N/A",
            "Format_Marks": "N/A",
            "Effective_Sentences_Marks": "N/A",
            "Cohesiveness_Marks": "N/A",
            "Total_Score": "N/A",
            "Strengths": "N/A",
            "Weaknesses": "N/A",
            "50_Marks_Answer": "N/A",
            "AI_Suggestions": "N/A",
            "Improved_Solution": "N/A"
        }

    except Exception as e:
        return {"error": f"An error occurred while processing the request: {str(e)}"}



