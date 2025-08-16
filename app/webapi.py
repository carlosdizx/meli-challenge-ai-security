from fastapi import FastAPI
from dto.log_entry import LogEntry

app = FastAPI()


@app.post("/analyze")
def analyze(logs: list[LogEntry]):
    result = {"message": "Registros procesados exitosamente", "total_entries": len(logs)}
    return result
