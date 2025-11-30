from fastapi import HTTPException
import jwt
import os

def verify_jwt_token(token: str):
    JWT_SECRET = os.getenv("JWT_SECRET", "ton_super_secret_jwt_pour_les_tests")
    
    if not token:
        raise HTTPException(status_code=401, detail="Token manquant")
    
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Token expiré")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Token invalide")