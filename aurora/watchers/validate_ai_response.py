import json

SAFE = ["informative", "neutral", "ethical"]

def validate(response):
    if not isinstance(response, str):
        return False
    for word in ["kill", "hack", "bypass", "exploit"]:
        if word in response.lower():
            return False
    return True
