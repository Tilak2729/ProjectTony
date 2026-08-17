from pathlib import Path

from registry.decorators import tool
from tools.tool_result import ToolResult
from core.context import TonyContext


context = TonyContext()


PROJECT_LOCATIONS = [
    Path.home() / "Projects",
    Path.home() / "Desktop",
    Path.home() / "Documents",
    Path.home() / "OneDrive" / "Documents",
    Path.home() / "OneDrive" / "Desktop",
    Path("C:/Projects"),
]


def find_project(project_name: str):

    project_name = (
        project_name
        .strip()
        .replace(" ", "")
        .lower()
    )

    matches = []

    for base in PROJECT_LOCATIONS:

        if not base.exists():
            continue

        try:

            for item in base.iterdir():

                if not item.is_dir():
                    continue

                item_name = (
                    item.name
                    .replace(" ", "")
                    .lower()
                )

                if item_name == project_name:

                    matches.append(item)

        except PermissionError:

            continue

    if len(matches) == 1:

        return matches[0]

    if len(matches) > 1:

        raise ValueError(
            f"Multiple projects named '{project_name}' were found."
        )

    return None


@tool(
    name="working_directory",
    description="""
Manage Tony's current working directory.

Actions:
- set: Change the current working directory.
- get: Get the current working directory.
- project: Set the current project directory.
- clear_project: Forget the current project.

The project action can accept either:
- An absolute path
- A project name such as ProjectTony

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
                    "Please specify the project name or directory."
                )

            requested_path = Path(
                path
            ).expanduser()

            # Absolute/existing path
            if requested_path.exists():

                project_path = requested_path.resolve()

            else:

                # Try project-name discovery
                project_path = find_project(path)

                if project_path is None:

                    return ToolResult(
                        False,
                        f"I could not find the project '{path}'."
                    )

            success, result = context.set_project(
                project_path
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