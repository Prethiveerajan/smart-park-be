# from pydantic import BaseModel

# class BookingRequest(BaseModel):
#     parking_id: int
#     user_name: str
#     contact: str
#     user_id: str
    



from pydantic import BaseModel, EmailStr

class BookingRequest(BaseModel):
    parking_id: int
    user_name: str
    contact: str
    email: EmailStr  # New field for email
    user_id: str
