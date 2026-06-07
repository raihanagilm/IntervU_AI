"""
Security utilities untuk IntervU AI.
Menangani validasi JWT token dari Supabase authentication.
"""
from jose import jwt, JWTError
from typing import Optional, Dict, Any
from datetime import datetime
from app.core.config import settings


async def verify_supabase_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verifikasi JWT token dari Supabase.
    
    Args:
        token: JWT token dari header Authorization
        
    Returns:
        Payload token jika valid, None jika tidak valid
    """
    try:
        # Supabase menggunakan RS256 (asymmetric), jadi kita perlu public key
        # Untuk sekarang kita decode tanpa verifikasi signature (development only)
        # Production harus pakai JWK dari Supabase
        
        payload = jwt.decode(
            token,
            settings.supabase_anon_key,
            algorithms=["HS256", "RS256"],
            options={"verify_signature": False}  # TODO: Enable di production dengan proper JWK
        )
        
        return payload
    except JWTError as e:
        print(f"Token verification error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error during token verification: {e}")
        return None


def get_current_user_from_token(token: str) -> Optional[str]:
    """
    Extract user ID dari token.
    
    Args:
        token: JWT token
        
    Returns:
        User ID (UUID) jika valid, None jika tidak
    """
    payload = verify_supabase_token(token)
    if payload:
        # Supabase menyimpan user ID di field 'sub'
        return payload.get("sub")
    return None