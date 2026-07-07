from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DSN_URL = "postgresql://postgres:postgres@localhost/car_pooling"

engine = create_engine(DSN_URL)

# Guess: Makes a local session that is passed to all the
# DB handling funcions
SessionLocal = sessionmaker(autocommit=False, 
                            autoflush=False,
                            bind=engine
                            )

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: db.close()