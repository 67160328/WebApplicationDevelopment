from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.db.models.user import User
from app.schemas.user_schema import UserResponse, UserUpdateRequest, UsernameCheckResponse
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["User Management"])

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """GET /me - Get current logged-in user profile."""
    return current_user

@router.get("/check-username/{name}", response_model=UsernameCheckResponse)
async def check_username(name: str, db: Session = Depends(get_db)):
    """GET /check-username/{name} - Check if a username is available."""
    user = db.query(User).filter(User.username == name).first()
    return UsernameCheckResponse(
        username=name,
        is_available=user is None
    )

@router.get("", response_model=List[UserResponse])
async def get_all_users(
    skip: int = Query(0, ge=0, description="Pagination skip offset"),
    limit: int = Query(10, ge=1, le=100, description="Pagination limit size"),
    db: Session = Depends(get_db)
):
    """GET /users - Fetch all users with pagination."""
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.get("/{id}", response_model=UserResponse)
async def get_user_by_id(id: int, db: Session = Depends(get_db)):
    """GET /users/{id} - Get user profile by ID."""
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.put("/{id}", response_model=UserResponse)
async def update_user(
    id: int, 
    payload: UserUpdateRequest, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """PUT /users/{id} - Update user profile information."""
    if current_user.id != id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Cannot edit another user's profile"
        )
    
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if payload.email is not None:
        user.email = payload.email
    if payload.full_name is not None:
        user.full_name = payload.full_name
        
    db.commit()
    db.refresh(user)
    return user

@router.delete("/{id}")
async def delete_user(
    id: int, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """DELETE /users/{id} - Delete user profile."""
    if current_user.id != id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Cannot delete another user's account"
        )
        
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
    db.delete(user)
    db.commit()
    return {"message": f"User ID {id} has been deleted"}
