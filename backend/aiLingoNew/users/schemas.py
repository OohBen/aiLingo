from datetime import datetime
from ninja import Schema
from pydantic import EmailStr

class UserSchema(Schema):
    id: int
    email: EmailStr
    name: str
    profile_pic: str = None
    date_joined: datetime
    is_premium: bool
    home_language_id: int = None

class UserRegistrationSchema(Schema):
    email: EmailStr
    name: str
    password: str
    profile_pic: str = None
    home_language_id: int = None

class TokenSchema(Schema):
    token: str