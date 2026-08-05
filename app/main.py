from llm.gemini import GeminiClient


def main():

    gemini = GeminiClient()

    while True:

        user_input = input("\nYou: ")

        if user_input.lower() == "exit":
            break

        response = gemini.ask(user_input)

        print(f"\nCharles: {response}")


if __name__ == "__main__":
    main()