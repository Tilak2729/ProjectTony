import subprocess

from registry.decorators import tool
from tools.tool_result import ToolResult


# Commands that are safe for Tony to execute automatically.
SAFE_COMMANDS = {
    "python --version",
    "python -V",
    "node --version",
    "node -v",
    "npm --version",
    "npm -v",
    "git --version",
    "git status",
    "git branch",
    "git log",
    "where python",
    "where node",
    "where git",
    "pwd",
    "whoami",
    "hostname",
}


@tool(
    name="terminal",
    description="""
Execute a PowerShell command on the Windows computer.

Safe commands can execute automatically.

Actions:
- run: Execute a PowerShell command.

Parameters:
command (string)
working_directory (string, optional)
"""
)
def terminal(
    command: str,
    working_directory: str = None
) -> ToolResult:

    if not command:

        return ToolResult(
            False,
            "No terminal command was provided."
        )

    command = command.strip()

    # ---------------------------------------------------------
    # SAFETY CHECK
    # ---------------------------------------------------------

    normalized_command = command.lower().strip()

    if normalized_command not in SAFE_COMMANDS:

        return ToolResult(
            False,
            (
                "This terminal command requires "
                "confirmation before execution."
            )
        )

    try:

        result = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                command
            ],
            cwd=working_directory,
            capture_output=True,
            text=True,
            timeout=30
        )

        output = (
            result.stdout.strip()
            or result.stderr.strip()
        )

        if not output:

            output = "Command completed successfully."

        return ToolResult(
            result.returncode == 0,
            output
        )

    except subprocess.TimeoutExpired:

        return ToolResult(
            False,
            "The command timed out."
        )

    except Exception as e:

        print(f"Terminal error: {e}")

        return ToolResult(
            False,
            "I could not execute the terminal command."
        )