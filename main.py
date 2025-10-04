from fastapi import FastAPI, status, HTTPException, Body, Path
import random

app = FastAPI()
expenses = []


@app.get("/expenses", status_code=status.HTTP_200_OK)
def get_all_expenses():
    return expenses


@app.get("/expenses/{id}", status_code=status.HTTP_200_OK)
def get_expense_by_id(id: int = Path()):
    for expense in expenses:
        if expense["id"] == id:
            return expense
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"item with id = {id} doesn't exist.",
    )


@app.post("/expenses", status_code=status.HTTP_201_CREATED)
def add_expense(description: str = Body(), amount: float = Body()):
    expenses.append(
        {
            "id": random.randint(0, 1000000000),
            "description": description,
            "amount": amount,
        }
    )


@app.put("/expenses/{id}", status_code=status.HTTP_200_OK)
def update_expense(id: int = Path(), description: str = Body(), amount: float = Body()):
    for expense in expenses:
        if expense["id"] == id:
            expense["description"] = description
            expense["amount"] = amount
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
