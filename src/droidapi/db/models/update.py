from sqlalchemy import DateTime, String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from droidapi.db import BaseModel


class Update(BaseModel):
    id: Mapped[int] = mapped_column(primary_key=True, auto_increment=True)
    file_name: String
    timestamp: DateTime
    file_id: String
    build_id: String
    device: String
    buildtype: String
    size: Integer
    url: String
    base_version: String

    def to_dict(self):
        return dict(
            datetime=self.timestamp,
            filename=self.file_name,
            romtype=self.buildtype,
            size=self.size,
            url=self.url,
            version=self.base_version,
        )