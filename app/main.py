from core.constants import WAKE_WORD

from llm.gemini import GeminiClient
from registry.registry import registry

from voice.listener import Listener
from voice.speaker import Speaker

import tools.apps
import tools.volume
from agent.validator import ResponseValidator

def main():

    print("=" * 50)
    print("       tony AI ASSISTANT")
    print("=" * 50)

    listener = Listener()
    speaker = Speaker()
    gemini = GeminiClient()

    speaker.speak("tony is ready.")

    while True:

        text = listener.listen()

        if not text:
            continue

        print(f"\nYou: {text}")

        if text.lower() == "exit":
            speaker.speak("Goodbye.")
            break

        if not text.lower().startswith(WAKE_WORD):
            continue

        command = text[len(WAKE_WORD):].strip(" ,")

        if not command:
            speaker.speak("Yes?")
            continue

        try:

            print("\n🧠 Thinking...")

            result = gemini.ask(command)
            if not ResponseValidator.validate(result):

                speaker.speak(
                    "I received an invalid response from my AI engine."
                )

                continue

            if result["type"] == "conversation":

                speaker.speak(result["response"])

            elif result["type"] == "tool_call":

                tool = registry.get(result["tool"])

                if tool is None:

                    speaker.speak("I don't know how to do that yet.")
                    continue

                print(f"\n🛠 Executing: {result['tool']}")

                tool_result = tool["function"](**result["arguments"])

                speaker.speak(tool_result.message)

        except Exception as e:

            print(f"\n❌ ERROR: {e}")

            speaker.speak(
                "Sorry, something went wrong while processing your request."
            )

if __name__ == "__main__":
    main()