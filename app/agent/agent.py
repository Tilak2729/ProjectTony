from core.constants import WAKE_WORD
from core.logger import logger

from agent.validator import ResponseValidator


class Agent:

    def __init__(self, listener, speaker, gemini, registry):

        self.listener = listener
        self.speaker = speaker
        self.gemini = gemini
        self.registry = registry

    def run(self):

        logger.info("Tony agent started.")

        self.speaker.speak("Tony is ready.")

        while True:

            text = self.listener.listen()

            if not text:
                continue

            print(f"\nYou: {text}")

            logger.info(f"Transcript: {text}")

            if text.lower() == "exit":

                self.speaker.speak("Goodbye.")

                logger.info("Tony stopped.")

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

            logger.info(f"Command: {command}")

            result = self.gemini.ask(command)

            if not ResponseValidator.validate(result):

                logger.error(f"Invalid AI response: {result}")

                self.speaker.speak(
                    "I received an invalid response from my AI engine."
                )

                return

            if result["type"] == "conversation":

                self.speaker.speak(result["response"])

                return

            if result["type"] == "tool_call":

                tool_name = result["tool"]

                tool = self.registry.get(tool_name)

                if tool is None:

                    logger.error(f"Unknown tool requested: {tool_name}")

                    self.speaker.speak(
                        "I don't know how to do that yet."
                    )

                    return

                print(f"\n🛠 Executing: {tool_name}")

                logger.info(f"Executing tool: {tool_name}")

                tool_result = tool["function"](
                    **result["arguments"]
                )

                logger.info(
                    f"Tool result: {tool_result.message}"
                )

                self.speaker.speak(
                    tool_result.message
                )

        except Exception as e:

            logger.exception("Agent processing error")

            print(f"\n❌ ERROR: {e}")

            self.speaker.speak(
                "Sorry, something went wrong while processing your request."
            )