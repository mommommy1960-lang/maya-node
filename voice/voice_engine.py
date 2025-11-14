#!/usr/bin/env python3
"""
Commons Voice Engine (CVE) – v1

Routes agent text -> appropriate voice tag -> TTS backend -> plays audio.

Usage examples:

  python voice/voice_engine.py --agent ROCKET --text "Queen, this reactor is about to have feelings."

  echo '{"agent":"KING","text":"The Custodian's safety is non-negotiable."}' | python voice/voice_engine.py

Plug your actual TTS backend into the `tts_speak()` function.
"""

import argparse, json, sys
from pathlib import Path

# Path to config (relative to this file)
CONFIG_PATH = Path(__file__).parent / "voices.config.json"


def load_config():
    if not CONFIG_PATH.exists():
        raise SystemExit(f"[voice] voices.config.json not found at {CONFIG_PATH}")
    data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    return data


def pick_voice(config, agent_name: str) -> str:
    """Return a voice tag for the given agent, or a default."""
    agent_name = (agent_name or "").strip().upper()
    if agent_name in config:
        return config[agent_name].get("voice", "default")
    return "default"


# ============================
#  TTS BACKEND HOOK
# ============================

def tts_speak(text: str, voice_tag: str):
    """
    >>> THIS is where you plug in your real TTS engine. <<<

    Options you can wire in here:
      - pyttsx3 (offline, uses system voices)
      - Coqui TTS (local models)
      - cloud TTS APIs (OpenAI, ElevenLabs, etc.)

    For now, this stub just prints what *would* be spoken.
    Replace this implementation with real audio.
    """
    # TODO: replace with real TTS call
    print(f"[voice:{voice_tag}] {text}")


# ============================
#  MAIN ROUTING
# ============================

def handle_message(agent: str, text: str):
    cfg = load_config()
    voice_tag = pick_voice(cfg, agent)
    tts_speak(text, voice_tag)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Commons Voice Engine (agent-aware TTS router)")
    ap.add_argument("--agent", "-a", help="Agent name (e.g. KING, DATA, UHURA)")
    ap.add_argument("--text", "-t", help="Text to speak. If omitted, JSON will be read from stdin.")
    args = ap.parse_args(argv)

    # Case 1: CLI args
    if args.agent and args.text:
        handle_message(args.agent, args.text)
        return

    # Case 2: JSON from stdin
    raw = sys.stdin.read().strip()
    if not raw:
        raise SystemExit("[voice] No input provided. Use --agent/--text or pipe JSON.")

    try:
        obj = json.loads(raw)
    except Exception as e:
        raise SystemExit(f"[voice] Failed to parse JSON from stdin: {e}")

    agent = obj.get("agent") or args.agent
    text = obj.get("text") or args.text
    if not agent or not text:
        raise SystemExit("[voice] Need both 'agent' and 'text' to speak.")

    handle_message(agent, text)


if __name__ == "__main__":
    main()
