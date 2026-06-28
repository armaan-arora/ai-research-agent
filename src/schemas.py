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

class EvaluatorOutput(BaseModel):
    coverage: int = Field(description="Score 1-10 how well the topic is covered")
    citations: int = Field(description="Score 1-10 how well sources are cited")
    clarity: int = Field(description="Score 1-10 how clear and structured the report is")
    depth: int = Field(description="Score 1-10 how deep and detailed the report is")
    overall: int = Field(description="Overall score 1-10")
    feedback: str = Field(description="One sentence feedback on how to improve the report")
        