from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt

from database import get_db
import models
import schemas
import auth

app = FastAPI(title="Car Pooling API")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"}
)

async def get_current_user(token: str =Depends(oauth2_scheme), db: Session = Depends(get_db)):   
    
    try:
        # Decoding to safely compare the email?
        payload = jwt.decode(token, auth.API_KEY, algorithms=[auth.ALGORITHM])
        email: str = payload.get('sub')
        
        if email is None:
            # Yes, Indeed.
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
        
    except JWTError:
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user



@app.post("/users/", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    
    if db_user:
        raise HTTPException(status_code=400,
                            detail="Email is already registered")
    
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(
                           email=user.email, 
                           password_hash=hashed_password,
                           created_on=datetime.now()
                           )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@app.post("/token", response_model=schemas.Token) #Question: Why Depends Section Empty? #Ans: Because It runs callable functions like OAuth and formats the incoming data appropriately
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    
    if not user or not auth.verify_password(form_data.password, user.password_hash):
        raise credentials_exception
    
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer"
        }

@app.get("/users/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

@app.get("/drivers/me", response_model=schemas.DriverResponse)
def read_drivers_me(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    current_driver_user = db.query(models.Driver).filter(models.Driver.user_id == current_user.id).first()
    
    if current_driver_user is None:
        raise credentials_exception
    
    return current_driver_user

@app.get("/passengers/me", response_model = schemas.PassengerResponse)
def read_passengers_me(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    current_passenger_user = db.query(models.Passenger).filter(models.Passenger.user_id == current_user.id).first()
    
    if current_passenger_user is None:
        raise credentials_exception
        
    return current_passenger_user

@app.get("/bookings/drivers/me", response_model=schemas.DriverBookingResponse)
def read_driver_bookings_me(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    current_driver_user = db.query(models.Driver).filter(models.Driver.user_id == current_user.id).first()
    
    if current_driver_user is None:
        raise credentials_exception
    
    current_driver_bookings = db.query(models.Booking).filter(models.Booking.driver_id == current_driver_user.id).first()
    
    if current_driver_bookings is None:
        raise credentials_exception
    
    return current_driver_bookings

@app.get("/bookings/passengers/me", response_model=schemas.PassengerBookingResponse)
def read_driver_bookings_me(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    current_passenger_user = db.query(models.Passenger).filter(models.Passenger.user_id == current_user.id).first()
    
    if current_passenger_user is None:
        raise credentials_exception
    
    current_driver_bookings = db.query(models.Booking).filter(models.Booking.passenger_id == current_passenger_user.id).first()
    
    if current_driver_bookings is None:
        raise credentials_exception
    
    return current_driver_bookings


@app.get("/passengers/profile/me", response_model=schemas.PassengerProfileResponse)
def read_passenger_profile(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    current_passenger_user = db.query(models.Passenger).filter(models.Passenger.user_id == current_user.id).first()
    
    if current_passenger_user is None:
        raise credentials_exception
    
    passenger_profile = db.query(models.PassengerProfile).filter(models.PassengerProfile.passenger_id == current_passenger_user.id).first()
    
    if passenger_profile is None:
        raise credentials_exception
    
    return passenger_profile

@app.get("/drivers/profile/me", response_model=schemas.DriverProfileResponse)
def read_passenger_profile(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    current_driver_user = db.query(models.Driver).filter(models.Driver.user_id == current_user.id).first()
    
    if current_driver_user is None:
        raise credentials_exception
    
    driver_profile = db.query(models.DriverProfile).filter(models.DriverProfile.driver_id == current_driver_user.id).first()
    
    if driver_profile is None:
        raise credentials_exception
    
    return driver_profile