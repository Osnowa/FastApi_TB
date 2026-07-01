from pydantic import BaseModel, EmailStr

class SUserRegister(BaseModel):
    email: EmailStr
    password: str

class SUserLogin(BaseModel):
    email: EmailStr
    password: str

# Ответ — без пароля!
class SUserOut(BaseModel):
    id: int
    email: str
    model_config = {"from_attributes": True}  # работает с ORM-объектами

class SToken(BaseModel):
    access_token: str
    token_type: str = "bearer"