from voice.listener import Listener
from agent.voice_agent import VoiceAgent

listener = Listener()

agent = VoiceAgent(listener)

while True:

    agent.wait_for_wake_word()

    print("\nWAKE WORD DETECTED\n")