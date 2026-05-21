from utils.model import llm
from utils.prompt import prompt
from utils.parser import FitnessResponse

from langchain_core.output_parsers import PydanticOutputParser

parser = PydanticOutputParser(
    pydantic_object=FitnessResponse
)

chain = prompt | llm | parser


def generate_fitness_response(question, fitness_level):

    result = chain.invoke({
        "question": question,
        "fitness_level": fitness_level,
        "format_instructions": parser.get_format_instructions()
    })

    return result