from utils.model import llm
from utils.parser import FitnessResponse
from utils.prompt import prompt, lf_prompt

from langchain_core.output_parsers import PydanticOutputParser
from langfuse.langchain import CallbackHandler

parser = PydanticOutputParser(
    pydantic_object=FitnessResponse
)

chain = prompt | llm | parser

langfuse_callback = CallbackHandler()


def generate_fitness_response(question, fitness_level):

    metadata = {
        "project": "AI Fitness Guidance Chatbot",
        "fitness_level": fitness_level
    }

    if lf_prompt is not None:
        metadata["prompt_name"] = lf_prompt.name
        metadata["prompt_version"] = str(lf_prompt.version)
    else:
        metadata["prompt_name"] = "fallback-local-prompt"
        metadata["prompt_version"] = "local"

    result = chain.invoke(
        {
            "question": question,
            "fitness_level": fitness_level,
            "format_instructions": parser.get_format_instructions()
        },
        config={
            "callbacks": [langfuse_callback],
            "tags": ["ai-fitness-guidance-chatbot"],
            "metadata": metadata
        }
    )

    return result