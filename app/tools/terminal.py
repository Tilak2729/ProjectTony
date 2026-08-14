import subprocess

from registry.decorators import tool
from tools.tool_result import ToolResult


# Commands Tony can execute without confirmation.
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
    "dir",
    "ls",
}


# Commands/patterns that should never be executed automatically.
BLOCKED_PATTERNS = [
    "format ",
    "format-",
    "remove-partition",
    "clear-disk",
    "diskpart",
    "shutdown",
    "restart-computer",
    "stop-computer",
    "remove-item c:\\",
    "remove-item *",
    "del c:\\",
    "rd c:\\",
]


def classify_command(command: str) -> str:

    command_lower = command.lower().strip()

    # Completely blocked commands
    for pattern in BLOCKED_PATTERNS:

        if pattern in command_lower:

            return "blocked"

    # Explicitly safe commands
    if command_lower in SAFE_COMMANDS:

        return "safe"

    # Everything else requires confirmation
    return "confirmation"


@tool(
    name="terminal",
    description="""
Execute a PowerShell command on the Windows computer.

The terminal can:
- Check Python, Node, npm and Git versions.
- Run Git commands.
- Run directory and system information commands.
- Execute other development commands after confirmation.

Parameters:
command (string)
working_directory (string, optional)
"""
)
def terminal(
    command: str,
    working_directory: str = None,
    confirmed: bool = False
) -> ToolResult:

    if not command:

        return ToolResult(
            False,
            "No terminal command was provided."
        )

    command = command.strip()

    classification = classify_command(command)

    # ---------------------------------------------------------
    # BLOCKED
    # ---------------------------------------------------------

    if classification == "blocked":

        return ToolResult(
            False,
            "I cannot execute that terminal command."
        )

    # ---------------------------------------------------------
    # CONFIRMATION
    # ---------------------------------------------------------

    if (
        classification == "confirmation"
        and not confirmed
    ):

        return ToolResult(
            False,
            "This terminal command requires confirmation."
        )

    # ---------------------------------------------------------
    # EXECUTION
    # ---------------------------------------------------------

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
            timeout=60
        )

        output = (
            result.stdout.strip()
            or result.stderr.strip()
        )

        if not output:

            output = "Command completed successfully."

        # Prevent extremely large responses from being
        # sent back to Tony's voice system.
        if len(output) > 4000:

            output = (
                output[:4000]
                + "\nOutput truncated."
            )

        return ToolResult(
            result.returncode == 0,
            output
        )

    except subprocess.TimeoutExpired:

        return ToolResult(
            False,
            "The command timed out after 60 seconds."
        )

    except FileNotFoundError:

        return ToolResult(
            False,
            "The specified working directory does not exist."
        )

    except Exception as e:

        print(
            f"Terminal error: {e}"
        )

        return ToolResult(
            False,
            "I could not execute the terminal command."
        )