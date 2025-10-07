from sqlalchemy import String, Integer, Text, DateTime, func, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db import Base
from datetime import datetime


class ExpenseModel(Base):
    __tablename__ = "expenses"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(Text(500), nullable=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), server_onupdate=func.now()
    )
    user = relationship("UserModel", back_populates="expenses", uselist=False)
