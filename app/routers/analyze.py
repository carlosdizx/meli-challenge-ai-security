from fastapi import APIRouter
from typing import List, Dict, Any

router = APIRouter()


@router.post("/")
def analyze(batch: List[Dict[str, Any]]):
    return {
        "received": len(batch),
        "threat_detected": False,
        "scores": [],
        "suggested_action": "allow",
        "note": "stub - conectaremos el modelo en el siguiente paso"
    }
