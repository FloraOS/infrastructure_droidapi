from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from droidapi.db import BaseModel


class StaticToken(BaseModel):
    id: Mapped[int] = mapped_column(primary_key=True, auto_increment=True)
    token: Mapped[str] = mapped_column(unique=True)
    issued_at: DateTime
    expires_at: DateTime