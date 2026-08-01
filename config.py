# ==========================
# JARVIS Configuration File
# ==========================

# Which voice engine to use.
# Options: "edge" (free, current default), "openai", "elevenlabs", "piper", "coqui"
VOICE_ENGINE = "edge"

# Voice settings for Edge TTS
EDGE_VOICE = "en-GB-RyanNeural"

# General voice tuning (used across engines where supported)
VOICE_SPEED = 1.0      # 1.0 = normal speed, 1.2 = 20% faster, 0.8 = 20% slower
VOICE_PITCH = 0        # 0 = normal pitch, in Hz adjustment (e.g. -20, +20)
VOICE_VOLUME = 1.0     # 1.0 = normal volume, 0.5 = half volume

# JARVIS identity
ASSISTANT_NAME = "JARVIS"
GREETING = "Good morning. All systems are operational. How may I assist you today?"