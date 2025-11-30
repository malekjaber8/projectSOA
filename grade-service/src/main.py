from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Grade Service")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client.gradeDB
grades_collection = db.grades

# JWT Secret
JWT_SECRET = os.getenv("JWT_SECRET", "ton_super_secret_jwt_pour_les_tests")

# Middleware JWT
def verify_token(authorization: str = None):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token manquant")
    
    token = authorization.split(" ")[1]
    
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Token expiré")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Token invalide")


@app.get("/health")
async def health_check():
    return {"status": " Grade Service is running!", "timestamp": datetime.now()}


@app.post("/grades/")
async def create_grade(
    grade_data: dict,
    authorization: str = Header(None, alias="Authorization")
):
    user = verify_token(authorization)
    
    required_fields = ["student_id", "course_id", "valeur", "semestre"]
    for field in required_fields:
        if field not in grade_data:
            raise HTTPException(status_code=400, detail=f"Champ {field} manquant")
    
    grade = {
        "student_id": grade_data["student_id"],
        "course_id": grade_data["course_id"],
        "valeur": float(grade_data["valeur"]),
        "semestre": grade_data["semestre"],
        "date_notation": datetime.now(),
        "created_by": user.get("email", "unknown")
    }
    
    # Validation note entre 0 et 20
    if grade["valeur"] < 0 or grade["valeur"] > 20:
        raise HTTPException(status_code=400, detail="La note doit être entre 0 et 20")
    
    result = grades_collection.insert_one(grade)
    
    return {
        "success": True,
        "message": "Note ajoutée avec succès",
        "grade_id": str(result.inserted_id)
    }

# READ - Lister les notes d'un étudiant + calcul moyenne
@app.get("/grades/student/{student_id}")
async def get_student_grades(student_id: str, authorization: str = Header(None, alias="Authorization")):
    user = verify_token(authorization)
    
    student_grades = list(grades_collection.find({"student_id": student_id}))
    
    # Convert ObjectId to string
    for grade in student_grades:
        grade["_id"] = str(grade["_id"])
        grade["date_notation"] = grade["date_notation"].isoformat()
    
    # Calcul moyenne
    notes = [g["valeur"] for g in student_grades]
    moyenne = sum(notes) / len(notes) if notes else 0
    
    return {
        "success": True,
        "student_id": student_id,
        "grades": student_grades,
        "moyenne": round(moyenne, 2),
        "count": len(student_grades)
    }

# READ - Toutes les notes
@app.get("/grades/")
async def get_all_grades(authorization: str = Header(None, alias="Authorization")):
    user = verify_token(authorization)
    
    all_grades = list(grades_collection.find())
    for grade in all_grades:
        grade["_id"] = str(grade["_id"])
        grade["date_notation"] = grade["date_notation"].isoformat()
    
    return {
        "success": True,
        "count": len(all_grades),
        "grades": all_grades
    }

# UPDATE - Modifier une note
@app.put("/grades/{grade_id}")
async def update_grade(grade_id: str, grade_data: dict, authorization: str = Header(None, alias="Authorization")):
    user = verify_token(authorization)
    
    # Vérifier si la note existe
    existing_grade = grades_collection.find_one({"_id": ObjectId(grade_id)})
    if not existing_grade:
        raise HTTPException(status_code=404, detail="Note non trouvée")
    
    # Mettre à jour seulement les champs fournis
    update_data = {}
    if "valeur" in grade_data:
        valeur = float(grade_data["valeur"])
        if valeur < 0 or valeur > 20:
            raise HTTPException(status_code=400, detail="La note doit être entre 0 et 20")
        update_data["valeur"] = valeur
    
    if "semestre" in grade_data:
        update_data["semestre"] = grade_data["semestre"]
    
    if "student_id" in grade_data:
        update_data["student_id"] = grade_data["student_id"]
    
    if "course_id" in grade_data:
        update_data["course_id"] = grade_data["course_id"]
    
    # Si aucun champ à mettre à jour
    if not update_data:
        raise HTTPException(status_code=400, detail="Aucun champ à mettre à jour")
    
    update_data["updated_at"] = datetime.now()
    
    result = grades_collection.update_one(
        {"_id": ObjectId(grade_id)},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Aucune modification effectuée")
    
    return {
        "success": True,
        "message": "Note modifiée avec succès"
    }

# DELETE - Supprimer une note
@app.delete("/grades/{grade_id}")
async def delete_grade(grade_id: str, authorization: str = Header(None, alias="Authorization")):
    user = verify_token(authorization)
    
    result = grades_collection.delete_one({"_id": ObjectId(grade_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Note non trouvée")
    
    return {
        "success": True,
        "message": "Note supprimée avec succès"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=3003, reload=True)