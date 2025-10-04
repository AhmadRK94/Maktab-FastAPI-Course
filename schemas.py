from pydantic import BaseModel, Field


class ExpenseCreateSchema(BaseModel):
    description: str = Field(..., max_length=64)
    amount: float = Field(..., gt=0)


class ExpenseResponseSchema(ExpenseCreateSchema):
    id: int = Field(...)
