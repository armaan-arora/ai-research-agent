from pydantic import BaseModel, Field
from typing import List

class PlannerOutput(BaseModel):
    sub_queries: List[str] = Field(
        description="List of 3 focused search queries to research the topic"
    )

class ReflectorOutput(BaseModel):
    verdict: str = Field(
        description="SUFFICIENT if enough info exists, INSUFFICIENT if more research needed"
    )
    gaps: str = Field(
        description="What key information is missing, or 'None' if sufficient"
    )
    new_queries: List[str] = Field(
        description="2 new search queries to fill gaps, or empty list if sufficient"
    )