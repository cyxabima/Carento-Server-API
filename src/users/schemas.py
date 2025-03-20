from pydantic import BaseModel


class UserCreateModel(BaseModel):
    pass


class UserGetModel(UserCreateModel):
    pass


class UserLoginModel(BaseModel):
    pass
