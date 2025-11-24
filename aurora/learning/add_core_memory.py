import json
from datetime import date

STATE_PATH = "aurora.state.json"
LOG_PATH = "aurora/learning/memory_log.md"

def add_core_memory(summary: str, memory_id: str | None = None):
    if memory_id is None:
        memory_id = f"{date.today()}-{summary[:12].replace(' ', '-') }"

    with open(STATE_PATH, "r", encoding="utf-8") as f:
        state = json.load(f)

    state.setdefault("important_memories", []).append({
        "id": memory_id,
        "timestamp": str(date.today()),
        "summary": summary
    })

    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

    line = f"{date.today()} – {summary}\n"
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line)

    print("Memory added:", memory_id)
