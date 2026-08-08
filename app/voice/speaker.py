import wave
import winsound

from piper import PiperVoice


class Speaker:

    def __init__(self):

        self.model = "voices/en_US-lessac-medium.onnx"

        print("Loading Piper voice...")

        self.voice = PiperVoice.load(self.model)

        print("Piper voice ready.")

    def speak(self, text: str):

        print(f"\ntony: {text}")

        output_path = "voices/response.wav"

        with wave.open(output_path, "wb") as wav_file:

            self.voice.synthesize_wav(
                text,
                wav_file
            )

        winsound.PlaySound(
            output_path,
            winsound.SND_FILENAME
        )