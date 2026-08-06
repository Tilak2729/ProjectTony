import tempfile
import os

import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write

from faster_whisper import WhisperModel
from silero_vad import load_silero_vad, get_speech_timestamps


class Listener:

    def __init__(self):

        print("Loading Whisper model...")

        self.whisper = WhisperModel(
            "small",
            device="cpu",
            compute_type="int8"
        )

        print("Loading Silero VAD...")

        self.vad = load_silero_vad()

        self.sample_rate = 16000

        print("Voice system ready.")

    def listen(self):

        print("\n🎤 Speak... (max 10 seconds)")

        audio = sd.rec(
            int(10 * self.sample_rate),
            samplerate=self.sample_rate,
            channels=1,
            dtype="float32"
        )

        sd.wait()

        audio = audio.flatten()

        speech = get_speech_timestamps(
            audio,
            self.vad,
            sampling_rate=self.sample_rate
        )

        if not speech:
            return ""

        start = speech[0]["start"]
        end = speech[-1]["end"]

        audio = audio[start:end]

        with tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        ) as temp:

            write(
                temp.name,
                self.sample_rate,
                (audio * 32767).astype(np.int16)
            )

            temp_path = temp.name

        try:

            segments, _ = self.whisper.transcribe(temp_path)

            text = ""

            for segment in segments:
                text += segment.text

            return text.strip()

        finally:

            if os.path.exists(temp_path):
                os.remove(temp_path)