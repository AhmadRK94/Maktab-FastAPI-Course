from fastapi import FastAPI, status, HTTPException, Path
import random
from schemas import ExpenseCreateSchema, ExpenseResponseSchema

app = FastAPI()
expenses = []


@app.get(
    "/expenses",
    status_code=status.HTTP_200_OK,
    response_model=list[ExpenseResponseSchema],
)
def get_all_expenses():
    return expenses


@app.get(
    "/expenses/{id}",
    status_code=status.HTTP_200_OK,
    response_model=ExpenseResponseSchema,
)
def get_expense_by_id(id: int = Path()):
    for expense in expenses:
        if expense["id"] == id:
            return expense
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"item with id = {id} doesn't exist.",
    )


@app.post("/expenses", status_code=status.HTTP_201_CREATED)
def add_expense(expense: ExpenseCreateSchema):
    expenses.append({"id": random.randint(0, 1000000000), **expense.model_dump()})


@app.put("/expenses/{id}", status_code=status.HTTP_200_OK)
def update_expense(expense: ExpenseCreateSchema, id: int = Path()):
    for item in expenses:
        if item["id"] == id:
            item["description"] = expense.description
            item["amount"] = expense.amount
            return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"item with id = {id} doesn't exist.",
    )


@app.delete("/expenses/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(id: int = Path()):
    for i, expense in enumerate(expenses):
        if expense["id"] == id:
            expenses.pop(i)
            return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"item with id = {id} doesn't exist.",
    )
