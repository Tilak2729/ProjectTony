import re

from core.constants import WAKE_WORD
from agent.validator import ResponseValidator
from agent.tool_executor import ToolExecutor


class Agent:

    def __init__(self, listener, speaker, gemini, registry):

        self.listener = listener
        self.speaker = speaker
        self.gemini = gemini

        self.tool_executor = ToolExecutor(registry)

        self.shutdown_commands = {
            "exit",
            "quit",
            "stop",
            "shutdown",
            "goodbye",
        }

        # Stores an action waiting for user confirmation.
        self.pending_action = None

    def run(self):

        self.speaker.speak("Tony is ready.")

        while True:

            text = self.listener.listen()

            if not text:
                continue

            print(f"\nYou: {text}")

            normalized_text = self.normalize(text)

            # -------------------------------------------------
            # HANDLE PENDING CONFIRMATION FIRST
            # -------------------------------------------------

            if self.pending_action:

                confirmation = self.check_confirmation(
                    normalized_text
                )

                if confirmation == "yes":

                    self.execute_pending_action()
                    continue

                if confirmation == "no":

                    self.pending_action = None

                    self.speaker.speak(
                        "Okay, I cancelled that action."
                    )

                    continue

            # -------------------------------------------------
            # DIRECT SHUTDOWN
            # -------------------------------------------------

            if normalized_text in self.shutdown_commands:

                self.shutdown()
                break

            # -------------------------------------------------
            # WAKE WORD
            # -------------------------------------------------

            wake_word = WAKE_WORD.lower()

            if wake_word not in normalized_text:

                continue

            # Remove Tony wherever it appears.
            command = re.sub(
                rf"\b{re.escape(wake_word)}\b",
                "",
                normalized_text,
                count=1
            ).strip()

            command = command.strip(
                " ,.!?;:"
            )

            # -------------------------------------------------
            # SHUTDOWN AFTER WAKE WORD
            # -------------------------------------------------

            if command in self.shutdown_commands:

                self.shutdown()
                break

            if not command:

                self.speaker.speak("Yes?")
                continue

            self.process_command(command)

    # ---------------------------------------------------------
    # NORMALIZATION
    # ---------------------------------------------------------

    def normalize(self, text):

        text = text.lower().strip()

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text

    # ---------------------------------------------------------
    # CONFIRMATION DETECTION
    # ---------------------------------------------------------

    def check_confirmation(self, text):

        yes_phrases = {
            "yes",
            "yeah",
            "yep",
            "yes please",
            "yeah please",
            "do it",
            "do that",
            "go ahead",
            "continue",
            "confirmed",
            "confirm",
            "i confirm",
            "i give you confirmation",
            "you have my confirmation",
            "you have my permission",
            "proceed",
        }

        no_phrases = {
            "no",
            "nope",
            "cancel",
            "cancel it",
            "don't",
            "do not",
            "stop",
            "never mind",
            "never mind it",
        }

        # Exact matches first.
        if text in yes_phrases:

            return "yes"

        if text in no_phrases:

            return "no"

        # Handle natural confirmation sentences.
        confirmation_keywords = [
            "yes",
            "confirm",
            "confirmation",
            "permission",
            "go ahead",
            "proceed",
            "do it",
        ]

        for phrase in confirmation_keywords:

            if phrase in text:

                return "yes"

        cancellation_keywords = [
            "cancel",
            "don't do it",
            "do not do it",
            "never mind",
        ]

        for phrase in cancellation_keywords:

            if phrase in text:

                return "no"

        return None

    # ---------------------------------------------------------
    # PENDING ACTION
    # ---------------------------------------------------------

    def request_confirmation(
        self,
        tool_name,
        arguments,
        message
    ):

        self.pending_action = {
            "tool": tool_name,
            "arguments": arguments
        }

        self.speaker.speak(message)

    # ---------------------------------------------------------
    # EXECUTE CONFIRMED ACTION
    # ---------------------------------------------------------

    def execute_pending_action(self):

        action = self.pending_action

        self.pending_action = None

        tool_name = action["tool"]
        arguments = action["arguments"]

        print(
            f"\n🛡 Confirmed action: {tool_name}"
        )

        # Tell the file manager that this action
        # has passed Tony's confirmation layer.
        arguments = dict(arguments)

        arguments["confirmed"] = True

        tool_result = self.tool_executor.execute(
            tool_name,
            arguments
        )

        self.speaker.speak(
            tool_result["message"]
        )

    # ---------------------------------------------------------
    # SHUTDOWN
    # ---------------------------------------------------------

    def shutdown(self):

        print("\n🛑 Shutting down Tony...")

        self.speaker.speak(
            "Goodbye."
        )

    # ---------------------------------------------------------
    # COMMAND PROCESSING
    # ---------------------------------------------------------

    def process_command(self, command):

        try:

            print("\n🧠 Thinking...")

            result = self.gemini.ask(command)

            if not ResponseValidator.validate(result):

                self.speaker.speak(
                    "I received an invalid response from my AI engine."
                )

                return

            if result["type"] == "conversation":

                self.speaker.speak(
                    result["response"]
                )

                return

            if result["type"] == "tool_call":

                tool_name = result["tool"]
                arguments = result["arguments"]

                # -------------------------------------------------
                # DESTRUCTIVE ACTION CHECK
                # -------------------------------------------------

                if (
                    tool_name == "file_manager"
                    and arguments.get("action") == "delete"
                ):

                    path = arguments.get(
                        "path",
                        "the selected item"
                    )

                    try:

                        from tools.files import resolve_path

                        resolved_path = resolve_path(path)

                        display_path = str(
                            resolved_path
                        )

                    except Exception:

                        display_path = path

                    self.request_confirmation(
                        tool_name,
                        arguments,
                        (
                            f"This will permanently delete "
                            f"{display_path}. "
                            f"Do you want me to continue?"
                        )
                    )

                    return


                if tool_name == "terminal":

                    command = arguments.get(
                        "command",
                        ""
                    )

                    try:

                        from tools.terminal import classify_command

                        classification = classify_command(
                            command
                        )

                    except Exception:

                        classification = "confirmation"

                    if classification == "blocked":

                        self.speaker.speak(
                            "I cannot execute that terminal command."
                        )

                        return

                    if classification == "confirmation":

                        working_directory = arguments.get(
                            "working_directory"
                        )

                        confirmation_message = (
                            f"I need your confirmation before "
                            f"I execute this terminal command: "
                            f"{command}"
                        )

                        if working_directory:

                            confirmation_message += (
                                f" in {working_directory}"
                            )

                        confirmation_message += ". Do you want me to continue?"

                        self.request_confirmation(
                            tool_name,
                            arguments,
                            confirmation_message
                        )

                        return

                # -------------------------------------------------
                # NORMAL TOOL EXECUTION
                # -------------------------------------------------

                print(
                    f"\n🛠 Executing: {tool_name}"
                )

                tool_result = self.tool_executor.execute(
                    tool_name,
                    arguments
                )

                self.speaker.speak(
                    tool_result["message"]
                )

        except Exception as e:

            print(
                f"\n❌ ERROR: {e}"
            )

            self.speaker.speak(
                "Sorry, something went wrong while processing your request."
            )