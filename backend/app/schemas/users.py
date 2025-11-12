from pydantic import BaseModel, EmailStr
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None
class UserOut(BaseModel):
    id: str
    name: str
    email: EmailStr
    phone: str | None = None
