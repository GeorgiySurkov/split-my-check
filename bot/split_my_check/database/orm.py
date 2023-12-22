import typing as t
from datetime import datetime
from uuid import uuid4, UUID

from sqlalchemy import TIMESTAMP, BigInteger, String, ForeignKey, SmallInteger
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

from split_my_check.utils import now, generate_expense_group_id

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

    # Data from telegram
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    username: Mapped[str] = mapped_column(String(32), index=True)
    first_name: Mapped[str] = mapped_column(String(64))
    last_name: Mapped[str | None] = mapped_column(String(64))
    language_code: Mapped[str | None] = mapped_column(
        String(35)
    )  # https://stackoverflow.com/a/17863380
    is_bot: Mapped[bool]
    is_premium: Mapped[bool | None]

    created_at: Mapped[datetime] = mapped_column(default=now)
    updated_at: Mapped[datetime] = mapped_column(default=now, onupdate=now)


class ExpenseGroup(Base):
    __tablename__ = "expense_group"

    id: Mapped[str] = mapped_column(
        String(20),
        primary_key=True,
        default=generate_expense_group_id,
    )

    owner_id: Mapped[UUID] = mapped_column(ForeignKey(User.id))
    name: Mapped[str | None] = mapped_column(String(256), default=None)

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
