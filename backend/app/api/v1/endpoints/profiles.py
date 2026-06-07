"""
FastAPI endpoints untuk operasi profiles.
CRUD operations untuk tabel profiles.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from typing import List
import uuid

from app.core.database import get_db
from app.models.user import Profile
from app.schemas.user import ProfileCreate, ProfileUpdate, ProfileResponse
from app.core.security import get_current_user_from_token
from fastapi import Header


router = APIRouter(prefix="/profiles", tags=["Profiles"])


async def get_current_user_id(authorization: str = Header(None)) -> uuid.UUID:
    """
    Dependency untuk mendapatkan user ID dari token.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token tidak valid"
        )
    
    token = authorization.replace("Bearer ", "")
    user_id = get_current_user_from_token(token)
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token tidak valid atau kadaluarsa"
        )
    
    try:
        return uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Format user ID tidak valid"
        )


@router.get("/", response_model=List[ProfileResponse])
async def get_all_profiles(
    db: AsyncSession = Depends(get_db),
    current_user_id: uuid.UUID = Depends(get_current_user_id)
):
    """
    Dapatkan semua profiles (hanya untuk admin/development).
    """
    result = await db.execute(select(Profile))
    profiles = result.scalars().all()
    return profiles


@router.get("/me", response_model=ProfileResponse)
async def get_my_profile(
    db: AsyncSession = Depends(get_db),
    current_user_id: uuid.UUID = Depends(get_current_user_id)
):
    """
    Dapatkan profile pengguna yang sedang login.
    """
    result = await db.execute(select(Profile).where(Profile.id == current_user_id))
    profile = result.scalar_one_or_none()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile tidak ditemukan"
        )
    
    return profile


@router.post("/", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_profile(
    profile_data: ProfileCreate,
    db: AsyncSession = Depends(get_db),
    current_user_id: uuid.UUID = Depends(get_current_user_id)
):
    """
    Buat profile baru untuk pengguna.
    """
    # Cek apakah profile sudah ada
    result = await db.execute(select(Profile).where(Profile.id == current_user_id))
    existing_profile = result.scalar_one_or_none()
    
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Profile sudah ada untuk user ini"
        )
    
    # Buat profile baru
    new_profile = Profile(
        id=current_user_id,
        **profile_data.model_dump(exclude={'id'}),
        data_cv=profile_data.data_cv.model_dump() if profile_data.data_cv else {}
    )
    
    db.add(new_profile)
    await db.commit()
    await db.refresh(new_profile)
    
    return new_profile


@router.patch("/me", response_model=ProfileResponse)
async def update_my_profile(
    profile_data: ProfileUpdate,
    db: AsyncSession = Depends(get_db),
    current_user_id: uuid.UUID = Depends(get_current_user_id)
):
    """
    Update profile pengguna yang sedang login.
    """
    # Cek apakah profile ada
    result = await db.execute(select(Profile).where(Profile.id == current_user_id))
    profile = result.scalar_one_or_none()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile tidak ditemukan"
        )
    
    # Update field yang disediakan
    update_data = profile_data.model_dump(exclude_unset=True)
    
    # Convert data_cv ke dict jika ada
    if 'data_cv' in update_data and update_data['data_cv']:
        update_data['data_cv'] = update_data['data_cv'].model_dump()
    
    for key, value in update_data.items():
        setattr(profile, key, value)
    
    await db.commit()
    await db.refresh(profile)
    
    return profile


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_my_profile(
    db: AsyncSession = Depends(get_db),
    current_user_id: uuid.UUID = Depends(get_current_user_id)
):
    """
    Hapus profile pengguna yang sedang login.
    """
    result = await db.execute(select(Profile).where(Profile.id == current_user_id))
    profile = result.scalar_one_or_none()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile tidak ditemukan"
        )
    
    await db.delete(profile)
    await db.commit()
    
    return None