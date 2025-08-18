# 1. Importar librerias

import json
from pathlib import Path
from dto.log_entry import LogEntry
from scripts.download_dataset import load_dataset

# 2. Leer dataset

df = load_dataset()

# 3. Exportar el dataset limpio a un archivo JSON

records = df.to_dict('records')

log_entries = [LogEntry.from_dict(record).to_dict() for record in records]

output_path = Path(__file__).parent.parent / 'data' / 'dataset.json'
output_path.parent.mkdir(parents=True, exist_ok=True)

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(log_entries, f, indent=2, ensure_ascii=False)

print(f"Dataset limpio exportado exitosamente a: {output_path}")
