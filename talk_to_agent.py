"""
talk_to_agent.py
----------------
The "flex" step. This lets you TALK to your agent out loud, from your own
computer's microphone and speakers, straight from the terminal — no phone needed.

This is optional. The easiest way to talk to your agent is the "Test AI agent"
button in the ElevenLabs dashboard (no code at all). Use THIS script once you
want to say in an interview: "I ran the agent locally through the Python SDK."

The code below is the official ElevenLabs pattern, lightly commented.

SETUP (one time):
  1) pip install "elevenlabs[pyaudio]" python-dotenv
       - macOS: you may first need:   brew install portaudio
       - Ubuntu/Debian: you may first need:
         sudo apt-get install libportaudio2 portaudio19-dev -y
  2) Copy .env.example to .env and fill in your AGENT_ID and ELEVENLABS_API_KEY.

RUN:
  python talk_to_agent.py
  ...then just start speaking. Press Ctrl+C to end the call.
"""

import os
import signal

from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface

# Load AGENT_ID and ELEVENLABS_API_KEY from your .env file
load_dotenv()

agent_id = os.getenv("AGENT_ID")
api_key = os.getenv("ELEVENLABS_API_KEY")

if not agent_id:
    raise SystemExit("Missing AGENT_ID. Add it to your .env file (see .env.example).")

# Create the ElevenLabs client. The API key is only required if your agent is
# private (authentication enabled). For a public test agent you can leave it out.
elevenlabs = ElevenLabs(api_key=api_key)

# Set up the live conversation. DefaultAudioInterface uses your computer's
# default mic + speakers. The callbacks just print the conversation so you can
# read along in the terminal while you talk.
conversation = Conversation(
    elevenlabs,
    agent_id,
    requires_auth=bool(api_key),
    audio_interface=DefaultAudioInterface(),
    callback_agent_response=lambda response: print(f"Agent: {response}"),
    callback_user_transcript=lambda transcript: print(f"You:   {transcript}"),
)

# Let Ctrl+C cleanly hang up the call.
signal.signal(signal.SIGINT, lambda sig, frame: conversation.end_session())

print("Starting the call — say hello! (Press Ctrl+C to hang up.)")
conversation.start_session()

# Wait until the call ends, then print the conversation ID. You can paste that
# ID into the dashboard later to review the transcript and what the agent did.
conversation_id = conversation.wait_for_session_end()
print(f"Conversation ID: {conversation_id}")
