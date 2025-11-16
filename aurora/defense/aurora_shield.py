def detect_malware_pattern(text):
    bad_signals = ["rm -rf", "DROP TABLE", "token=", "curl http"]
    return any(sig in text for sig in bad_signals)

def block_if_unsafe(text):
    if detect_malware_pattern(text):
        return False
    return True
