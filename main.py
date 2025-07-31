from fastapi import FastAPI, BackgroundTasks, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
import time
import logging

app = FastAPI()

# In-memory 'database' for demo purposes
fake_user_db = set()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("welcome_email")

class UserCreate(BaseModel):
    username: str
    email: EmailStr


def send_welcome_email(email: str, username: str):
    # Simulate sending an email (real implementation would use smtplib/celery, etc.)
    logger.info(f"Preparing welcome email for {username} <{email}>")
    # Simulate email sending delay (but should not block request)
    time.sleep(0.1) # Very fast for demo; just a realistic simulation
    # Log success
    logger.info(f"Sent welcome email to {username} <{email}>")


@app.post("/register")
def register_user(user: UserCreate, background_tasks: BackgroundTasks):
    # Check for existing user (simulate uniqueness)
    if user.email in fake_user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered.")
    # Simulate user creation
    fake_user_db.add(user.email)
    # Schedule the background welcome email (does not block response)
    background_tasks.add_task(send_welcome_email, email=user.email, username=user.username)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "User registered! Check your email for a welcome message."})

# To test:
# 1. Run: uvicorn main:app --reload
# 2. POST to /register with username + email JSON
# 3. Check console logs for email sending
