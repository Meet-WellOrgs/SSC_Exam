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

def evaluate_ssc_precis(passage, precis_text, difficulty_type):
    
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
    Assume you are an examiner for the SSC CGL descriptive writing test. Your task is to evaluate the response solely based on the given prompt for the following criteria: Lexical Resource, Grammatical Range and Accuracy, Task Achievement, and Coherence and Cohesion. Assign marks from 0-50 for each criterion based on the provided description. Remain consistent in your assessment even if the same response is submitted multiple times.
    Evaluate based on the selected difficulty level: {difficulty_type}.

    1. **Lexical Resource**: The range and accuracy of vocabulary used in the précis.
    2. **Grammatical Range and Accuracy**: The complexity and correctness of the grammar used.
    3. **Task Achievement**: How well the précis summarizes the passage and captures the essential points.
    4. **Coherence and Cohesion**: The flow of ideas and how well the summary is structured in one coherent paragraph.

    The précis is expected to:
    - Be concise, ideally one-third of the original passage length.
    - Retain the central idea of the passage.
    - Include essential points and perspectives from the passage.
    - Be concluded within 100-150 words.
    - Retain the original voice of the author.
    - Be written in one paragraph.

    The SSC CGL précis is evaluated on the following marking scheme {marking_scheme} with description:
    - **Relevance**: How well the précis summarizes the key points of the passage (10 marks).
    - **Spelling/Grammar**: Accuracy in spelling and grammar (5 marks).
    - **Word Limit**: Adherence to the word limit of 100-150 (5 marks).
    - **Content Quality**: Depth and clarity of the summarized content (8 marks).
    - **Format**: Proper précis format (5 marks).
    - **Writing Neatness**: Clarity and neatness of writing (5 marks).
    - **Effective Sentences**: Use of clear, concise, and varied sentence structures (7 marks).
    - **Cohesiveness**: Logical flow and transitions between ideas (5 marks).

    Please evaluate the précis based on these criteria. Provide scores for each category, explain why the scores were assigned, and suggest improvements. Also, provide an example of a perfect 50-mark précis for the question.
    Remember if there is nothing like the answer is blank then all score will be 0 and also remember this strictly that if the answer is not based on the question or is in other direction then also all the scores will be 0. (please evaluate this very strictly)
    
    Précis Passage: "{passage}"
    Précis Text: "{precis_text}"

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
        "50_Marks_Answer": "[Generate a 50-mark précis answer for the passage, ensuring it addresses all marking criteria comprehensively,  with 80-120 words in response to {passage}]",
        "AI_Suggestions": "[Provide specific suggestions for improvement based on the user's answer in {precis_text}]",
        "Improved_Solution": "[Provide a 50-mark improved solution for the user's answer {precis_text} based on the essay question asked which was {passage}]"
    }}
    """
    
    try:
        # Sending précis and question to Groq API for evaluation
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
            "Word_Count": len(precis_text.split()),
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

# # Example usage
# question = "Write a précis of the following passage in not more than 90 words."
# passage = """The rise of artificial intelligence (AI) is one of the most profound shifts in human history. From self-driving cars to healthcare applications, AI is revolutionizing the way we live and work. However, the rapid development of this technology raises concerns about its impact on jobs, privacy, and security. As AI continues to evolve, it is crucial that we consider the ethical implications and ensure that its benefits are widely distributed."""
# precis_text = """AI is revolutionizing various sectors, including healthcare and transportation. However, it raises concerns about job losses, privacy, and security. As AI develops, it is important to address these challenges and ensure its responsible use for the benefit of all."""
# type = "medium"
# print(evaluate_ssc_precis(question, precis_text, type))
