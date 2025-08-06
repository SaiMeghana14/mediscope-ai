import json
from pathlib import Path

def save_feedback(data):
    path = Path("data/feedbacks.json")
    feedbacks = []
    if path.exists():
        feedbacks = json.loads(path.read_text())
    feedbacks.append(data)
    path.write_text(json.dumps(feedbacks, indent=2))
