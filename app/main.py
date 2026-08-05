from llm.gemini import GeminiClient
from registry.registry import registry
from voice.speaker import Speaker

import tools.apps


def main():

    speaker = Speaker()

    gemini = GeminiClient()

    speaker.speak("Hello. I am Charles.")

    while True:

        command = input("\nYou: ")

        if command.lower() == "exit":

            speaker.speak("Goodbye.")

            break

        result = gemini.ask(command)

        if result["type"] == "conversation":

            speaker.speak(result["response"])

        elif result["type"] == "tool_call":

            tool = registry.get(result["tool"])

            tool_result = tool["function"](**result["arguments"])

            speaker.speak(tool_result.message)


if __name__ == "__main__":
    main()