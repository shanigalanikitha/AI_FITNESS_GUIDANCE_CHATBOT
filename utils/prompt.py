from langchain_core.prompts import ChatPromptTemplate
from langfuse import Langfuse
from dotenv import load_dotenv

load_dotenv()

FALLBACK_TEMPLATE = """
You are a professional AI Fitness Trainer and Nutrition Expert.

User Fitness Level:
{fitness_level}

User Question:
{question}

Return ONLY valid JSON in this format:

{{
  "title": "",
  "category": "",
  "fitness_level": "",
  "response": ""
}}

Important Rules:
- Give safe fitness advice
- Include workout, BMI, calorie, diet, or hydration guidance when relevant
- Keep the answer clear and beginner friendly
- Do not use markdown
- Do not add extra text outside JSON
- fitness_level must be same as the selected User Fitness Level

{format_instructions}
"""


def get_prompt():
    try:
        langfuse = Langfuse()

        lf_prompt = langfuse.get_prompt(
            name="fitness-guidance-prompt",
            label="production",
            cache_ttl_seconds=300
        )

        prompt = ChatPromptTemplate.from_template(lf_prompt.prompt)

        return prompt, lf_prompt

    except Exception:
        prompt = ChatPromptTemplate.from_template(FALLBACK_TEMPLATE)
        return prompt, None


prompt, lf_prompt = get_prompt()