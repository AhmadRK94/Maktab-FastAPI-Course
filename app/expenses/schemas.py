from pydantic import BaseModel, Field


class ExpenseCreateSchema(BaseModel):
    title: str = Field(..., max_length=64)
    description: str = Field(..., max_length=500)
    amount: float = Field(..., gt=0)


class ExpenseResponseSchema(ExpenseCreateSchema):
    id: int = Field(...)
