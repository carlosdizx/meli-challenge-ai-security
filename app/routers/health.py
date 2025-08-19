from fastapi import APIRouter
from app.services.model_service import model_service

router = APIRouter()


@router.get("/")
def health():
    return {
        "status": "ok",
        "model_loaded": model_service.is_loaded(),
        "feature_columns_count": len(model_service.feature_cols),
    }
