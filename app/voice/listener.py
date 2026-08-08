import tempfile
import os

import numpy as np
import sounddevice as sd
import torch
from scipy.io.wavfile import write

from faster_whisper import WhisperModel
from silero_vad import load_silero_vad


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

        self.chunk_duration = 512 / self.sample_rate

        self.chunk_size = 512

        self.max_recording_seconds = 15

        self.silence_duration = 0.8

        self.speech_threshold = 0.5

        print("Voice system ready.")

    def listen(self):

        print("\n🎤 Listening...")

        audio_chunks = []

        speech_detected = False
        silence_time = 0

        max_chunks = int(
            self.max_recording_seconds /
            self.chunk_duration
        )

        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype="float32",
            blocksize=self.chunk_size
        ) as stream:

            for _ in range(max_chunks):

                audio, _ = stream.read(
                    self.chunk_size
                )

                audio = audio.flatten()

                audio_tensor = torch.from_numpy(audio)

                speech_probability = self.vad(
                    audio_tensor,
                    self.sample_rate
                )

                is_speech = (
                    speech_probability.detach().item() >=
                    self.speech_threshold
                )

                if is_speech:

                    speech_detected = True
                    silence_time = 0

                    audio_chunks.append(audio)

                elif speech_detected:

                    audio_chunks.append(audio)

                    silence_time += self.chunk_duration

                    if silence_time >= self.silence_duration:

                        break

        if not speech_detected:

            return ""

        audio = np.concatenate(audio_chunks)

        return self._transcribe(audio)

    def _transcribe(self, audio):

        with tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        ) as temp:

            temp_path = temp.name

            write(
                temp_path,
                self.sample_rate,
                (audio * 32767).astype(np.int16)
            )

        try:

            segments, _ = self.whisper.transcribe(
                temp_path
            )

            text = ""

            for segment in segments:

                text += segment.text

            return text.strip()

        finally:

            if os.path.exists(temp_path):

                os.remove(temp_path)