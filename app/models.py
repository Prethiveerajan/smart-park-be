from pydantic import BaseModel

class BookingRequest(BaseModel):
    parking_id: int
    user_name: str
    contact: str
    user_id: str
    

# models.py
# from pydantic import BaseModel

# class BookingRequest(BaseModel):
#     parking_id: int
#     user_name: str
#     contact: str
#     user_mail: str  # Changed from user_mail to user_email
#     user_id: str
