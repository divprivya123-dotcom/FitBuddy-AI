from pydantic import BaseModel, Field, field_validator


ALLOWED_GOALS = {"Weight Loss", "Muscle Gain", "General Wellness", "Flexibility"}
ALLOWED_INTENSITIES = {"Low", "Medium", "High"}


class UserInput(BaseModel):
    username: str = Field(min_length=2, max_length=100)
    user_id: str = Field(min_length=2, max_length=50)
    age: int = Field(ge=13, le=100)
    weight: float = Field(gt=20, le=500)
    goal: str
    intensity: str

    @field_validator("goal")
    @classmethod
    def validate_goal(cls, value):
        if value not in ALLOWED_GOALS:
            raise ValueError("Please select a valid fitness goal")
        return value

    @field_validator("intensity")
    @classmethod
    def validate_intensity(cls, value):
        if value not in ALLOWED_INTENSITIES:
            raise ValueError("Please select a valid workout intensity")
        return value


class FeedbackRequest(BaseModel):
    user_id: str = Field(min_length=2, max_length=50)
    feedback: str = Field(min_length=3, max_length=1000)