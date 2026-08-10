from llm.gemini import GeminiClient
from registry.registry import registry

from voice.listener import Listener
from voice.speaker import Speaker

from agent.agent import Agent

import tools.apps
import tools.volume
import tools.browser
import tools.system


def main():

    print("=" * 50)
    print("       TONY AI ASSISTANT")
    print("=" * 50)

    listener = Listener()
    speaker = Speaker()
    gemini = GeminiClient()

    agent = Agent(
        listener=listener,
        speaker=speaker,
        gemini=gemini,
        registry=registry
    )

    agent.run()


if __name__ == "__main__":
    main()