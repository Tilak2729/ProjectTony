import subprocess
import tempfile
import os
import winsound


class Speaker:

    def __init__(self):

        self.model = "voices/en_US-lessac-medium.onnx"
        self.config = "voices/en_US-lessac-medium.onnx.json"

    def speak(self, text: str):

        print(f"\ntony: {text}")

        with tempfile.NamedTemporaryFile(
            suffix=".txt",
            delete=False,
            mode="w",
            encoding="utf-8"
        ) as input_file:

            input_file.write(text)

            input_path = input_file.name

        output_path = input_path.replace(".txt", ".wav")

        try:

            subprocess.run(
                [
                    "piper",
                    "--model",
                    self.model,
                    "--config",
                    self.config,
                    "--input-file",
                    input_path,
                    "--output-file",
                    output_path
                ],
                check=True,
                capture_output=True
            )

            winsound.PlaySound(output_path, winsound.SND_FILENAME)

        finally:

            if os.path.exists(input_path):
                os.remove(input_path)

            if os.path.exists(output_path):
                os.remove(output_path)