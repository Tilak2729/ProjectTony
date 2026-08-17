from pathlib import Path

from registry.decorators import tool
from tools.tool_result import ToolResult
from core.context import TonyContext


context = TonyContext()


@tool(
    name="working_directory",
    description="""
Manage Tony's current working directory.

Actions:
- set: Change the current working directory.
- get: Get the current working directory.
- project: Set the current project directory.
- clear_project: Forget the current project.

Parameters:
action (string)
path (string, optional)
"""
)
def working_directory(
    action: str,
    path: str = None
) -> ToolResult:

    try:

        if action == "get":

            return ToolResult(
                True,
                f"Current directory is {context.get_directory()}."
            )

        if action == "set":

            if not path:

                return ToolResult(
                    False,
                    "Please specify the directory."
                )

            success, result = context.set_directory(
                path
            )

            if not success:

                return ToolResult(
                    False,
                    result
                )

            return ToolResult(
                True,
                f"Working directory changed to {result}."
            )

        if action == "project":

            if not path:

                return ToolResult(
                    False,
                    "Please specify the project directory."
                )

            success, result = context.set_project(
                path
            )

            if not success:

                return ToolResult(
                    False,
                    result
                )

            return ToolResult(
                True,
                f"Current project is now {result}."
            )

        if action == "clear_project":

            context.clear_project()

            return ToolResult(
                True,
                "Current project cleared."
            )

        return ToolResult(
            False,
            "Unsupported working directory action."
        )

    except Exception as e:

        print(
            f"Context error: {e}"
        )

        return ToolResult(
            False,
            "I could not change the working directory."
        )