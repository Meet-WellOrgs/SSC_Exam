from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.environ["GROQ_API_KEY"]

client = Groq(api_key=GROQ_API_KEY)

def generate_essay_answer(question):
    prompt = f"""
    You are an expert essay writer specializing in descriptive exams like SSC CGL. Your task is to craft a **50 marks model essay** for the given topic. Ensure your essay strictly adheres to the following requirements, reflecting the **perfect answer** in terms of relevance, coherence, and structure.

    **Essay Requirements:**
    - **Word Limit**: 250-300 words (strict adherence to this).
    - **Audience**: The essay should cater to a formal exam audience, ensuring clarity, precision, and depth.
    - **Tone**: Formal, objective, and neutral tone.
    - **Focus Areas**:
        - **Relevance (10 Marks)**:
          - Address the topic directly and comprehensively.
          - Avoid vague or off-topic points.
        - **Spelling & Grammar (5 Marks)**:
          - Maintain impeccable grammar and spelling throughout.
          - Use formal language with appropriate vocabulary.
        - **Word Limit Adherence (5 Marks)**:
          - Stay within the word count limit.
          - Write concisely, avoiding redundancy.
        - **Content Quality (8 Marks)**:
          - Provide clear arguments with examples, evidence, and analysis.
          - Discuss social, economic, and political aspects wherever applicable.
        - **Format (5 Marks)**:
          - Include Introduction, Body, and Conclusion.
          - Use logical paragraphing and transitions.
        - **Writing Neatness (5 Marks)**:
          - Use short, crisp sentences to maintain flow.
        - **Effective Sentences (7 Marks)**:
          - Write meaningful, impactful sentences.
        - **Cohesiveness (5 Marks)**:
          - Ensure logical progression of ideas and smooth transitions.

    **Essay Structure**:
    - **Introduction (50-70 words)**:
      - Start with a strong opening sentence introducing the topic.
      - Highlight its significance in the context of India or globally.
      - End with a thesis statement or the main argument of your essay.

    - **Body (2-3 paragraphs; 150-200 words)**:
      - **Paragraph 1**: Define the issue or explain its background.
          - What is the topic about?
          - Why is it relevant today (social, economic, or political context)?
          - Mention causes or factors contributing to the issue.
      - **Paragraph 2**: Analyze implications or provide a balanced discussion.
          - Pros and cons, challenges, or key opportunities.
          - Government policies, societal roles, or technological interventions.
      - **Paragraph 3 (if needed)**: Discuss potential solutions.
          - Propose actionable steps by individuals, governments, or institutions.
          - Include examples or case studies.

    - **Conclusion (50-70 words)**:
      - Summarize the essay in 1-2 sentences.
      - End with a forward-looking statement, famous quote, or call to action.

    **Additional Guidelines**:
    - Use transition words like *however*, *moreover*, *therefore*, etc., for cohesion.
    - Avoid repetition, and ensure precision in every statement.
    - Make the essay engaging while maintaining an exam-appropriate tone.

    **Essay Topic**:
    {question}

    **Final Expected Output**:
    Write the essay strictly in the format specified above, adhering to the word limit and addressing all the focus areas for maximum marks.With proper paragraph structure and format.
    """
    # Request to Groq API
    response = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    try:
        result = {
            "50 Marks SSC Essay": response.choices[0].message.content.strip()
        }
        return result
    except Exception as e:
        return {"Error": str(e)}, 500


question = "Write an essay on 'Importance of education in present time'. (250 words)"
print(generate_essay_answer(question))