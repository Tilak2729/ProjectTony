from voice.speaker import Speaker


class Charles:

    def __init__(self):
        self.speaker = Speaker()

    def start(self):
        print("=" * 34)
        print("       CHARLES AI ASSISTANT")
        print("=" * 34)

        self.speaker.speak("Hello! I am Charles.")
        self.speaker.speak("Waiting for your command...")

        while True:
            command = input("\nYou: ")

            if command.lower() == "exit":
                self.speaker.speak("Goodbye!")
                break

            self.speaker.speak(f"I heard: {command}")