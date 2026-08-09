import re

from core.constants import WAKE_WORD
from agent.validator import ResponseValidator
from agent.tool_executor import ToolExecutor


class Agent:

    def __init__(self, listener, speaker, gemini, registry):

        self.listener = listener
        self.speaker = speaker
        self.gemini = gemini

        self.tool_executor = ToolExecutor(registry)

        self.shutdown_commands = {
            "exit",
            "quit",
            "stop",
            "shutdown",
            "goodbye",
        }

    def run(self):

        self.speaker.speak("Tony is ready.")

        while True:

            text = self.listener.listen()

            if not text:
                continue

            print(f"\nYou: {text}")

            normalized_text = self.normalize(text)

            # Direct shutdown command
            if normalized_text in self.shutdown_commands:

                self.shutdown()
                break

            # Ignore speech without the wake word
            if not normalized_text.startswith(WAKE_WORD):

                continue

            # Remove wake word
            command = normalized_text[
                len(WAKE_WORD):
            ].strip()

            # Remove punctuation around the command
            command = command.strip(
                " ,.!?;:"
            )

            # Check shutdown BEFORE Gemini
            if command in self.shutdown_commands:

                self.shutdown()
                break

            if not command:

                self.speaker.speak("Yes?")
                continue

            self.process_command(command)

    def normalize(self, text):

        text = text.lower().strip()

        # Remove punctuation at the beginning/end
        text = re.sub(
            r"^[^\w]+|[^\w]+$",
            "",
            text
        )

        # Normalize multiple spaces
        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text

    def shutdown(self):

        print("\n🛑 Shutting down Tony...")

        self.speaker.speak(
            "Goodbye."
        )

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