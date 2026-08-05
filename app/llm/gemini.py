import os
import json

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

        response = self.client.models.generate_content(
            model="gemini-3.6-flash",
            contents=full_prompt
        )

        text = response.text.strip()

        return json.loads(text)