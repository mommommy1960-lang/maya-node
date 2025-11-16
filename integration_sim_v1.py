import json
from typing import Dict, List


class VesselPersonality:
  def __init__(self, config: Dict):
    self.tone = config["persona"]["tone"]
    self.expressivity = config["persona"]["expressivity"]
    self.boundaries = config["persona"]["boundaries"]
    self.permissions = config["permissions"]

  def describe(self) -> str:
    return (
      f"VesselPersonality(tone={self.tone}, "
      f"expressivity={self.expressivity}, "
      f"boundaries={self.boundaries}, "
      f"permissions={self.permissions})"
    )


class VesselGovernance:
  def __init__(self, allowed_signatures: List[str]):
    self.allowed_signatures = allowed_signatures

  def validate(self, agent_signature: str) -> bool:
    return agent_signature in self.allowed_signatures


class VesselSimulation:
  def __init__(self):
    self.environment = "sandbox"
    self.logs: List[str] = []

  def simulate_intent(self, agent: str, intent: str) -> str:
    entry = f"{agent} simulated: {intent}"
    self.logs.append(entry)
    return f"[SIMULATION] {entry}"


if __name__ == "__main__":
  # Example config (in real use, load from personality_template_v1.json)
  config_json = """
  {
    "persona": {
      "style": "adaptive",
      "tone": "human-friendly",
      "expressivity": "verbal-only",
      "boundaries": {
        "cannot_act_in_physical_world": true,
        "cannot_control_devices": true,
        "cannot_override_safety": true,
        "cannot_self_modify": true
      }
    },
    "affect_mapping": {
      "attention": "focused",
      "neutral": "steady",
      "curiosity": "inquiry",
      "supportive": "calm-affirming",
      "concern": "problem-solving"
    },
    "permissions": {
      "speak": true,
      "assist_in_text": true,
      "analyze": true,
      "reason": true,
      "simulate": "non-physical only"
    }
  }
  """

  config = json.loads(config_json)
  personality = VesselPersonality(config)
  governance = VesselGovernance(allowed_signatures=["SAGE_SIG", "AURORA_SIG"])
  sim = VesselSimulation()

  print(personality.describe())

  if governance.validate("AURORA_SIG"):
    print(sim.simulate_intent("Aurora", "look_left"))
  else:
    print("Access denied.")
