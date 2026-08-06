from core.constants import WAKE_WORD


class VoiceAgent:

    def __init__(self, listener):

        self.listener = listener

    def wait_for_wake_word(self):

        print("🟢 Waiting for wake word...")

        while True:

            text = self.listener.listen()

            if not text:
                continue

            print(text)

            if WAKE_WORD in text.lower():

                return