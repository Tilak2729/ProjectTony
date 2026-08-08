from core.constants import WAKE_WORD
from agent.validator import ResponseValidator
from agent.tool_executor import ToolExecutor


class Agent:

    def __init__(self, listener, speaker, gemini, registry):

        self.listener = listener
        self.speaker = speaker
        self.gemini = gemini

        self.tool_executor = ToolExecutor(registry)

    def run(self):

        self.speaker.speak("Tony is ready.")

        while True:

            text = self.listener.listen()

            if not text:
                continue

            print(f"\nYou: {text}")

            if text.lower() == "exit":

                self.speaker.speak("Goodbye.")

                break

            if not text.lower().startswith(WAKE_WORD):

                continue

            command = text[len(WAKE_WORD):].strip(" ,")

            if not command:

                self.speaker.speak("Yes?")

                continue

            self.process_command(command)

    def process_command(self, command):

        try:

            print("\n🧠 Thinking...")

            result = self.gemini.ask(command)

            if not ResponseValidator.validate(result):

                self.speaker.speak(
                    "I received an invalid response from my AI engine."
                )

                return

            if result["type"] == "conversation":

                self.speaker.speak(
                    result["response"]
                )

                return

            if result["type"] == "tool_call":

                tool_name = result["tool"]

                print(
                    f"\n🛠 Executing: {tool_name}"
                )

                tool_result = self.tool_executor.execute(
                    tool_name,
                    result["arguments"]
                )

                self.speaker.speak(
                    tool_result["message"]
                )

        except Exception as e:

            print(f"\n❌ ERROR: {e}")

            self.speaker.speak(
                "Sorry, something went wrong while processing your request."
            )