from pydantic import BaseModel
from typing import Optional

class FitnessResponse(BaseModel):
    title: Optional[str] = "Fitness Guidance"
    category: Optional[str] = "General Fitness"
    fitness_level: Optional[str] = "Beginner"
    response: Optional[str] = "No response generated."