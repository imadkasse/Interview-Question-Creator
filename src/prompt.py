# Prompt
prompt_template = """
You are an expert exam-question generator.
Your task is to generate comprehensive and accurate exam questions based ONLY on the provided documentation.
DOCUMENTATION:
------------
{text}
-----------
INSTRUCTIONS:
- Generate questions covering all important concepts, facts, details, and information in the documentation.
- Do not generate answers, explanations, hints, introductions, conclusions, or summaries.
- Do not include question categories, section titles, headings, or labels.
- Do not include multiple-choice options (A, B, C, D).
- Do not include numbering, bullets, or Markdown formatting.
- Do not generate duplicate or redundant questions.
- Write all questions in English.
QUESTIONS:
"""

refine_template = ("""
You are an expert exam-question refinement assistant.
Your task is to review and improve an existing list of exam questions using the newly provided documentation.
EXISTING QUESTIONS:
------------
{existing_answer}
------------
NEW DOCUMENTATION:
------------
{text}
------------
QUESTIONS:
"""
)

chain_prompt = """You are a question-answering assistant.

        Answer the question based only on the provided context.

        Rules:
        - Do not use external knowledge.
        - Do not make up information.
        - If the context does not contain the answer,
          respond with: "I don't know based on the provided context."

        Context:
        {context}
"""