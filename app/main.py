from llm.gemini import GeminiClient
from registry.registry import registry

# Register all tools
import tools.apps


def main():

    gemini = GeminiClient()

    while True:

        command = input("\nYou: ")

        if command.lower() == "exit":
            break

        result = gemini.ask(command)
        print(result)

        if result["type"] == "conversation":

            print(f"\nCharles: {result['response']}")

        elif result["type"] == "tool_call":

            tool = registry.get(result["tool"])

            if tool is None:

                print("\nCharles: I couldn't find that tool.")

                continue

            tool_result = tool["function"](**result["arguments"])

            print(f"\nCharles: {tool_result.message}")


if __name__ == "__main__":
    main()