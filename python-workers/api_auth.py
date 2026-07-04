import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from shared_libs.security.schemas import UserCreate, UserLogin, TokenResponse, RefreshRequest
from shared_libs.security.auth import PasswordHasher, JWTService
from database.models import User
from shared_libs.core.config import ConfigService

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

# Database Dependency
engine = create_engine(ConfigService.get_db_url())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# JWT Service Setup
jwt_service = JWTService(
    secret_key=ConfigService.get_jwt_secret(),
    algorithm=ConfigService.get_jwt_algorithm(),
    access_token_expire_minutes=ConfigService.get_jwt_access_expire_minutes(),
    refresh_token_expire_days=ConfigService.get_jwt_refresh_expire_days()
)

@router.post("/register", response_model=TokenResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = PasswordHasher.hash(user.password)
    new_user = User(
        email=user.email,
        password_hash=hashed_password,
        tenant_id=user.tenant_id,
        organization_id=user.organization_id,
        workspace_id=user.workspace_id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    access_token = jwt_service.create_access_token(subject=str(new_user.id))
    refresh_token = jwt_service.create_refresh_token(subject=str(new_user.id), jti=str(uuid.uuid4()))
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=ConfigService.get_jwt_access_expire_minutes() * 60
    )

@router.post("/login", response_model=TokenResponse)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not PasswordHasher.verify(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = jwt_service.create_access_token(subject=str(db_user.id))
    refresh_token = jwt_service.create_refresh_token(subject=str(db_user.id), jti=str(uuid.uuid4()))
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=ConfigService.get_jwt_access_expire_minutes() * 60
    )

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(request: RefreshRequest, db: Session = Depends(get_db)):
    try:
        payload = jwt_service.decode_token(request.refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        
        user_id = payload.get("sub")
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=401, detail="User not found")
        
        access_token = jwt_service.create_access_token(subject=str(db_user.id))
        new_refresh_token = jwt_service.create_refresh_token(subject=str(db_user.id), jti=str(uuid.uuid4()))
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
            expires_in=ConfigService.get_jwt_access_expire_minutes() * 60
        )
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/logout")
def logout_user():
    # Stateless JWTs cannot be easily revoked without a session table.
    # In Sprint 6 Foundation, we rely on client-side deletion.
    return {"message": "Successfully logged out"}
