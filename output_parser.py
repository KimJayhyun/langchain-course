from typing import Any, Dict, List

from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field


class Summary(BaseModel):
    summary: str = Field(description="summary of the given information")
    facts: List[str] = Field(
        description="interesting facts about the given information"
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "summary": self.summary,
            "facts": self.facts,
        }


summary_parser = PydanticOutputParser(pydantic_object=Summary)
