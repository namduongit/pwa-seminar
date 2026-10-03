from pydantic import BaseModel


class RegisterPoiOwner(BaseModel):
    full_name: str
    email: str
    password: str
    phone: str
    business_name: str
    business_address: str
    id_card: str

class Login(BaseModel):
    identifier: str
    password: str


class ChangePassword(BaseModel):
    current_password: str
    new_password: str
