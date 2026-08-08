import os
import json
import time
from google.genai.errors import ServerError

from dotenv import load_dotenv
from google import genai
from registry.registry import registry

load_dotenv()


class GeminiClient:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY not found.")

        self.client = genai.Client(api_key=api_key)

    def ask(self, prompt: str):

        with open("app/prompts/system_prompt.txt", "r", encoding="utf-8") as file:
            system_prompt = file.read()

        full_prompt = f"""
    {system_prompt}

    {registry.tool_prompt()}

    User Request:

    {prompt}
    """

        max_retries = 3

        for attempt in range(max_retries):

            try:

                response = self.client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=full_prompt
                )

                text = response.text.strip()

                try:
                    return json.loads(text)

                except json.JSONDecodeError:

                    print("⚠️ Gemini returned invalid JSON.")

                    return {
                        "type": "conversation",
                        "response": "I couldn't understand the response from my AI engine."
                    }

            except ServerError:

                if attempt == max_retries - 1:
                    raise

                print(f"⚠️ Gemini unavailable. Retrying ({attempt + 1}/{max_retries})...")

                time.sleep(2)