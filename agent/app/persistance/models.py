from datetime import datetime
from typing import List, Optional

from pydantic import BeforeValidator
from sqlmodel import Field, Relationship, SQLModel
from typing_extensions import Annotated


# === Validators ===
def validate_date(v):
    if isinstance(v, datetime):
        return v
    
    for f in ["%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%SZ"]:
        try:
            return datetime.strptime(v, f)
        except ValueError:
            pass
    
    raise ValueError("Invalid date format")

DateFormat = Annotated[datetime, BeforeValidator(validate_date)]

# ==== Models ===
class User(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    name: str
    phone: str = Field(unique=True)
    created_at: DateFormat = Field(default_factory=datetime.utcnow)
    updated_at: DateFormat = Field(default_factory=datetime.utcnow)
    
    tasks: List["Task"] = Relationship(back_populates="user")


class Task(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    title: str
    completed: bool = Field(default=False)
    user_id: str = Field(foreign_key="user.id")
    created_at: DateFormat = Field(default_factory=datetime.utcnow)
    updated_at: DateFormat = Field(default_factory=datetime.utcnow)
    
    user: Optional[User] = Relationship(back_populates="tasks")
