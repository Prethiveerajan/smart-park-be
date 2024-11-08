from pydantic import BaseModel, EmailStr
from pydantic.networks import EmailStr
class BookingRequest(BaseModel):
    parking_id: int
    user_name: str
    contact: str
    email: EmailStr  # New field for email
    user_id: str

class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str