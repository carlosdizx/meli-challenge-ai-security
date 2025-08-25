from fastapi import APIRouter
from services.model_service import model_service

router = APIRouter()


@router.get("/")
def health():
    return {
        "status": "ok",
        "model_loaded": model_service.is_loaded(),
    }
