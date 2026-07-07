from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    email: str
    class Config:
        from_attributes = True
        
class DriverResponse(BaseModel):
    id: int
    name:str
    aadhaar_no: str
    car_no_plate: str
    
    class Config:
        from_attributes = True

class PassengerResponse(BaseModel):
    id: int
    name: str
    aadhaar_no: str
    
    class Config:
        from_attributes = True

class DriverBookingResponse(BaseModel):
    id: int
    pickup_point: str
    destination: str
    booking_progress: str
  
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None