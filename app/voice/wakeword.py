import numpy as np
import sounddevice as sd
from openwakeword.model import Model


class WakeWordDetector:

    def __init__(self):

        print("Loading Wake Word model...")

        self.model = Model(
            wakeword_models=[]
        )

        self.sample_rate = 16000
        self.chunk_size = 1280

        print("Wake Word model loaded.")

    def wait_for_wake_word(self):

        print("\n🟢 Waiting for 'tony'...")

        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype="int16",
            blocksize=self.chunk_size
        ) as stream:

            while True:

                audio, _ = stream.read(self.chunk_size)

                audio = audio.flatten().astype(np.int16)

                prediction = self.model.predict(audio)

                for score in prediction.values():

                    if score > 0.5:

                        print("\n👂 Wake word detected!")

                        return