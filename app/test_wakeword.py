from voice.wakeword import WakeWordDetector

detector = WakeWordDetector()

while True:

    detector.wait_for_wake_word()

    print("tony is awake!")