import datetime

from sqlalchemy.orm import Mapped, mapped_column

from droidapi.db import Base


class StaticToken(Base):
    __tablename__ = "tokens"
    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(unique=True)
    issued_at: Mapped[datetime.datetime]
    expires_at: Mapped[datetime.datetime]

    def to_dict(self):
        return dict(issued_at=self.issued_at.isoformat(), expires_at=self.expires_at.isoformat())