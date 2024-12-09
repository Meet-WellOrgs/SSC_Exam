from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()


GROQ_API_KEY = os.environ["GROQ_API_KEY"]
client = Groq(api_key=GROQ_API_KEY)

def generate_letter_answer(question, letter_type):
    # letter type would be formal or informal
    prompt = f"""
    You are an expert in crafting model answers for SSC CGL descriptive papers. Your task is to write a **50 marks model letter** adhering to the strict SSC letter-writing format and marking scheme described below.

    **Marking Scheme**:
    - **Relevance (10 Marks)**:
      - Address the topic directly and comprehensively.
    - **Spelling & Grammar (5 Marks)**:
      - Ensure impeccable grammar and spelling.
    - **Word Limit (5 Marks)**:
      - Strict adherence to the word count (150-200 words).
    - **Content Quality (8 Marks)**:
      - Explain the issue or purpose with clarity and depth.
    - **Format (5 Marks)**:
      - Follow the correct letter format exactly as described below.
    - **Writing Neatness (5 Marks)**:
      - Use concise and meaningful sentences.
    - **Effective Sentences (7 Marks)**:
      - Ensure clear and impactful communication.
    - **Cohesiveness (5 Marks)**:
      - Maintain logical flow and transitions.

    **Letter Format**:
    - **Sender's Address**: Include contact details (email, residential address).
    - **Date**: Mention the date of writing the letter.
    - **Addressee's Designation and Address**: Specify recipient's details.
    - **Subject**: State the purpose of the letter in a concise phrase.
    - **Salutation**: Use "Respected Sir/Madam" or equivalent.
    - **Introduction**:
      - Clearly state the purpose of writing.
      - Highlight the main issue/topic in 1-2 sentences.
    - **Body**:
      - Explain the issue/purpose in detail.
      - Provide relevant examples, evidence, or arguments as required.
    - **Conclusion**:
      - Reiterate the main point and end with a formal note of gratitude.
    - **Sender's Name and Designation**:
      - End with your full name and position (if applicable).

    **Letter Type**:
    - Ensure it is a **{letter_type} letter** (formal tone, direct, and concise).
    - Follow the word limit and avoid redundancy.

    **Letter question**:
    {question}

    **Final Expected Output**:
    Write a complete letter adhering strictly to the above instructions and SSC format. Ensure formal language, logical structure, and adherence to marking scheme and format.
    """

    response = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    try:
        result = {
            "50 Marks SSC Letter": response.choices[0].message.content.strip()
        }
        return result
    except Exception as e:
        return {"Error": str(e)}
