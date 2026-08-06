from voice.listener import Listener

listener = Listener()

while True:

    text = listener.listen()

    if text:

        print()

        print("You:", text)

        print("-" * 50)