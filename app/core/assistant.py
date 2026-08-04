class Charles:

    def start(self):
        print("=" * 34)
        print("       CHARLES AI ASSISTANT")
        print("=" * 34)

        while True:
            command = input("\nYou: ")

            if command.lower() == "exit":
                print("Charles: Goodbye!")
                break

            print(f"Charles: I heard -> {command}")