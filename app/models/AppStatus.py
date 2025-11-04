from pydantic import BaseModel


class AppStatus(BaseModel):
    """Flag  -> base with users was downloaded and exist"""
    database: bool
