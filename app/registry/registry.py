import inspect
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

        signature = inspect.signature(function)

        parameters = []

        for parameter in signature.parameters.values():

            parameters.append(
                {
                    "name": parameter.name,
                    "type": str(parameter.annotation).replace("<class '", "").replace("'>", "")
                }
            )

        self._tools[name] = {
            "name": name,
            "description": description,
            "function": function,
            "parameters": parameters
        }

    def get(self, name: str):
        return self._tools.get(name)

    def list_tools(self):
        return list(self._tools.values())

    def tool_prompt(self):

        prompt = "Available Functions:\n\n"

        for tool in self._tools.values():

            prompt += f"""
Function Name:
{tool['name']}

Description:
{tool['description']}

Parameters:
"""

            for parameter in tool["parameters"]:

                prompt += f"- {parameter['name']} ({parameter['type']})\n"

            prompt += "\n-------------------------\n"

        return prompt


registry = ToolRegistry()