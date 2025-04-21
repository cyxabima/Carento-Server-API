from pydantic import BaseModel, EmailStr


class ContactGetModel(BaseModel):
    name: str
    email: EmailStr
    message: str

class AdminGetModel(BaseModel):
    name: str
    password: str