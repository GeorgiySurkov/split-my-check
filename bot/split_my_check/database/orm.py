from uuid import uuid4, UUID
from datetime import datetime
import typing as t

from sqlalchemy import TIMESTAMP, BigInteger, String, ForeignKey, SmallInteger
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

from split_my_check.utils import now

uuidpk = t.Annotated[UUID, mapped_column(primary_key=True, default=uuid4)]


class Base(DeclarativeBase):
    type_annotation_map = {
        datetime: TIMESTAMP(timezone=True),
    }


class User(Base):
    __tablename__ = "user"

    id: Mapped[uuidpk]
    created_at: Mapped[datetime] = mapped_column(default=now)


class TelegramUser(Base):
    __tablename__ = "telegram_user"

    id: Mapped[uuidpk]
    user_id: Mapped[UUID] = mapped_column(ForeignKey(User.id), unique=True)

    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    username: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(default=now)
    first_name: Mapped[str] = mapped_column(String(64))
    last_name: Mapped[str] = mapped_column(String(64))


class ExpenseGroup(Base):
    __tablename__ = "expense_group"

    id: Mapped[str] = mapped_column(String(20), primary_key=True)
    owner_id: Mapped[UUID] = mapped_column(ForeignKey(User.id))
    name: Mapped[str] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(default=now)
    updated_at: Mapped[datetime] = mapped_column(default=now, onupdate=now)


class ExpenseGroupParticipant(Base):
    __tablename__ = "expense_group_participant"

    expense_group_id: Mapped[str] = mapped_column(
        ForeignKey(ExpenseGroup.id),
        primary_key=True,
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey(User.id), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=now)


class Expense(Base):
    __tablename__ = "expense"

    id: Mapped[uuidpk]
    expense_group_id: Mapped[str] = mapped_column(ForeignKey(ExpenseGroup.id))
    payer_id: Mapped[UUID] = mapped_column(ForeignKey(User.id))
    name: Mapped[str] = mapped_column(String(128))
    amount: Mapped[int] = mapped_column(BigInteger)

    created_at: Mapped[datetime] = mapped_column(default=now)
    updated_at: Mapped[datetime] = mapped_column(default=now, onupdate=now)


class ExpenseParticipant(Base):
    __tablename__ = "expense_participant"

    expense_id: Mapped[UUID] = mapped_column(ForeignKey(Expense.id), primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey(User.id), primary_key=True)
    fraction: Mapped[int | None] = mapped_column(SmallInteger)
    explicit_part: Mapped[int | None] = mapped_column(BigInteger)
