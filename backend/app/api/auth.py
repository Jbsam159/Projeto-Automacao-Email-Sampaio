from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse
from app.core.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
  user = db.query(User).filter(User.email == data.email).first()

  if not user or not verify_password(data.password, user.password_hash):
    raise HTTPException(status_code=401, detail="Credenciais inválidas")

  token = create_access_token({"sub": str(user.id)})

  return {"access_token": token}
