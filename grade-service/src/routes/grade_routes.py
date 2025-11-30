from fastapi import APIRouter, HTTPException, Depends
from typing import List
from models.grade_model import Grade, GradeCreate, GradeResponse
from middleware.auth_middleware import verify_jwt_token

router = APIRouter()

# Cette version utilise les routes séparées
# Mais dans notre cas, on a tout dans main.py pour simplifier

@router.post("/", response_model=GradeResponse)
async def create_grade(grade: GradeCreate, token: str = Depends(verify_jwt_token)):
    # Implémentation similaire à celle dans main.py
    pass

@router.get("/student/{student_id}")
async def get_student_grades(student_id: str, token: str = Depends(verify_jwt_token)):
    # Implémentation similaire à celle dans main.py
    pass