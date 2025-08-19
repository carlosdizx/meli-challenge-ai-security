from fastapi import APIRouter
from dto.log_entry import LogEntry

router = APIRouter()


@router.post("/")
def analyze(logs: list[LogEntry]):
    return {
        "received": len(logs),
        "threat_detected": False,
        "scores": [],
        "suggested_action": "allow",
    }
