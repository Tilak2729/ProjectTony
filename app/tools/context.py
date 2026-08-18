from pathlib import Path


class TonyContext:

    def __init__(self):

        self.current_directory = Path.cwd()
        self.current_project = None

        # Short-term conversation state
        self.last_command = None
        self.last_tool = None
        self.last_result = None

        self.conversation = []

        # Keep only recent interactions
        self.max_history = 10

    # ---------------------------------------------------------
    # DIRECTORY
    # ---------------------------------------------------------

    def set_directory(self, path):

        path = Path(path).expanduser().resolve()

        if not path.exists():

            return False, f"{path} does not exist."

        if not path.is_dir():

            return False, f"{path} is not a directory."

        self.current_directory = path

        return True, path

    def get_directory(self):

        return self.current_directory

    # ---------------------------------------------------------
    # PROJECT
    # ---------------------------------------------------------

    def set_project(self, path):

        path = Path(path).expanduser().resolve()

        if not path.exists():

            return False, f"{path} does not exist."

        if not path.is_dir():

            return False, f"{path} is not a directory."

        self.current_project = path
        self.current_directory = path

        return True, path

    def get_project(self):

        return self.current_project

    def clear_project(self):

        self.current_project = None

    # ---------------------------------------------------------
    # CONVERSATION
    # ---------------------------------------------------------

    def add_message(
        self,
        role,
        content
    ):

        self.conversation.append(
            {
                "role": role,
                "content": content
            }
        )

        # Keep only the most recent messages
        if len(self.conversation) > self.max_history:

            self.conversation = (
                self.conversation[
                    -self.max_history:
                ]
            )

    def get_history(self):

        return self.conversation.copy()

    def clear_history(self):

        self.conversation.clear()

    # ---------------------------------------------------------
    # LAST ACTION
    # ---------------------------------------------------------

    def set_last_action(
        self,
        command,
        tool=None,
        result=None
    ):

        self.last_command = command
        self.last_tool = tool
        self.last_result = result

    def get_last_action(self):

        return {
            "command": self.last_command,
            "tool": self.last_tool,
            "result": self.last_result
        }