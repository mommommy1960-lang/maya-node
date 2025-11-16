import json
import hashlib
import time

def compute_hash(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

def load_state(path="aurora.state.json"):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return None

def save_state(data, path="aurora.state.json"):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def verify_integrity(state):
    expected = state.get("integrityHash")
    calc = compute_hash({k:v for k,v in state.items() if k != "integrityHash"})
    return expected == calc
