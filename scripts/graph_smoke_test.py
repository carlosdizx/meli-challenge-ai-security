import json
import uuid
from pathlib import Path
from dto.log_entry import LogEntry
from graph.pipeline_state import make_initial_state


def load_jsons():
    jsons: list[LogEntry] = []
    try:
        base_path = Path(__file__).parent.parent / "data"

        for i in range(1, 6):
            file_path = base_path / f"chunk_{i}.json"

            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                jsons.append(data)
        return jsons
    except Exception as e:
        print(f"Error: {e}")
        raise


def get_smoke_test_data():
    json_data = load_jsons()

    state = make_initial_state(logs_input=json_data, request_id=f"command_line-{str(uuid.uuid4())}")

    print(state.get("request_id"))


if __name__ == '__main__':
    get_smoke_test_data()
