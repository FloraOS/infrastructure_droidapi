import datetime

from sqlalchemy.orm import Mapped, mapped_column

from droidapi.db import BaseModel


class Update(BaseModel):
    __tablename__ = "updates"
    id: Mapped[int] = mapped_column(primary_key=True)
    file_name: Mapped[str]
    timestamp: Mapped[datetime.datetime]
    file_id: Mapped[str]
    build_id: Mapped[str]
    device: Mapped[str]
    buildtype: Mapped[str]
    size: Mapped[int]
    url: Mapped[str]
    base_version: Mapped[str]

    def to_dict(self):
        return dict(
            datetime=int(self.timestamp.timestamp()),
            filename=self.file_name,
            romtype=self.buildtype,
            size=self.size,
            url=self.url,
            version=self.base_version,
            id=self.build_id,
        )