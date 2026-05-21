from typing import Union, List, Optional 
from pydantic import BaseModel

class FitnessResponse(BaseModel):
    title: Optional[str] = "Fitness Guidance"

    category: Optional[str] = "General Fitness"
    
    response: Optional[Union[str, List[str]]] = (
        "No response generated."

    )    
