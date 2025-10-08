from fastapi import APIRouter, status, HTTPException, Path, Depends
from app.core.db import Session, get_db
from app.expenses.schemas import ExpenseCreateSchema, ExpenseResponseSchema
from app.expenses.models import ExpenseModel
from app.users.models import UserModel
from app.auth.dependency import get_current_user

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[ExpenseResponseSchema],
)
def get_all_expenses(
    current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)
):
    user_id = current_user.id
    user = db.query(UserModel).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {user_id} does'nt exist.",
        )
    expenses = db.query(ExpenseModel).filter_by(user_id=user_id).all()
    return expenses


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=ExpenseResponseSchema,
)
def get_expense_by_id(
    id: int = Path(),
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_id = current_user.id
    user = db.query(UserModel).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {user_id} does'nt exist.",
        )
    expense = db.query(ExpenseModel).filter_by(id=id).first()
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"item with id = {id} doesn't exist.",
        )
    return expense


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_expense(
    create_expense: ExpenseCreateSchema,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_id = current_user.id
    user = db.query(UserModel).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {user_id} does'nt exist.",
        )
    create_expense_dict = create_expense.model_dump()
    create_expense_dict["user_id"] = user_id
    new_expense = ExpenseModel(**create_expense_dict)
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)


@router.put("/{id}", status_code=status.HTTP_200_OK)
def update_expense(
    update_expense: ExpenseCreateSchema,
    id: int = Path(),
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_id = current_user.id
    user = db.query(UserModel).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {user_id} does'nt exist.",
        )
    expense_object = db.query(ExpenseModel).filter_by(id=id).first()
    if not expense_object:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"item with id = {id} doesn't exist.",
        )
    for key, value in update_expense.model_dump().items():
        setattr(expense_object, key, value)

    db.commit()
    db.refresh(expense_object)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    id: int = Path(),
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_id = current_user.id
    user = db.query(UserModel).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {user_id} does'nt exist.",
        )
    expense_object = db.query(ExpenseModel).filter_by(id=id).first()
    if not expense_object:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"item with id = {id} doesn't exist.",
        )
    db.delete(expense_object)
    db.commit()
