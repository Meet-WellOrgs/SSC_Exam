from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.environ["GROQ_API_KEY"]

client = Groq(api_key=GROQ_API_KEY)

def generate_precis_answer(passage):
    prompt = f"""
    You are an expert in crafting model answers for SSC CGL descriptive papers. Your task is to write a **50 marks model précis** adhering to the SSC CGL format and marking scheme described below.

    **Marking Scheme**:
    - **Relevance (10 Marks)**:
      - Summarize the passage with utmost relevance, retaining all key points.
    - **Spelling & Grammar (5 Marks)**:
      - Ensure impeccable grammar and spelling.
    - **Word Limit (5 Marks)**:
      - Strict adherence to the word count (100-150 words).
    - **Content Quality (8 Marks)**:
      - Collect and summarize all essential points while avoiding unnecessary details.
    - **Format (5 Marks)**:
      - Final précis should be a single paragraph with a clear flow.
    - **Writing Neatness (5 Marks)**:
      - Use concise and meaningful sentences.
    - **Effective Sentences (7 Marks)**:
      - Ensure impactful and precise communication.
    - **Cohesiveness (5 Marks)**:
      - Maintain logical flow and transition between ideas.

    **Précis Writing Requirements**:
    - Your précis should be approximately **one-third the length of the original passage**.
    - Write the précis in your own words while retaining the author's voice.
    - Avoid copying sentences directly from the passage.
    - Highlight the main idea and exclude irrelevant details.
    - Write the précis in a **formal and exam-appropriate tone**.

    **Passage for Précis**:
    {passage}

    **Final Expected Output**:
    Write a single-paragraph précis that meets all the above criteria and adheres to the SSC CGL précis-writing format. The précis should reflect the core essence of the passage and be strictly within the word limit.
    """

    response = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    try:
        result = {
            "50 Marks SSC Précis": response.choices[0].message.content.strip()
        }
        return result
    except Exception as e:
        return {"Error": str(e)}
