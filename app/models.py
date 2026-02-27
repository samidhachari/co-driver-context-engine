from pydantic import BaseModel, Field
from typing import List


class ContextRequest(BaseModel):
    user_text: str = Field(
        ..., json_schema_extra={"example": "I feel very sleepy"}
    )
    battery: int = Field(
        ..., ge=0, le=100, json_schema_extra={"example": 15}
    )
    time: str = Field(
        ..., json_schema_extra={"example": "23:30"}
    )
    location: str = Field(
        ..., json_schema_extra={"example": "highway"}
    )


class ContextResponse(BaseModel):
    driver_state: str
    battery_status: str
    time_of_day: str
    location: str
    risk_level: str
    priority: str
    recommended_action: str
    rules_triggered: List[str]
    explanation: List[str]
    ml_prediction: str
    confidence_score: float
    decision_source: str