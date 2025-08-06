import json
from pathlib import Path
from datetime import datetime

def save_history(input_text, output):
    path = Path("data/history.json")
    history = []
    if path.exists():
        history = json.loads(path.read_text())
    history.append({
        "input": input_text,
        "output": output,
        "timestamp": datetime.now().isoformat()
    })
    path.write_text(json.dumps(history, indent=2))
