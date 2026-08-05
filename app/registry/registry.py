from typing import Callable


class ToolRegistry:

    def __init__(self):
        self._tools = {}

    def register(
        self,
        name: str,
        description: str,
        function: Callable
    ):

        self._tools[name] = {
            "name": name,
            "description": description,
            "function": function
        }

    def get(self, name: str):

        return self._tools.get(name)

    def list_tools(self):

        return list(self._tools.values())


registry = ToolRegistry()