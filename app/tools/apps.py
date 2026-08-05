import subprocess

from registry.decorators import tool
from tools.tool_result import ToolResult


@tool(
    name="open_application",
    description="Open an installed desktop application."
)
def open_application(application: str) -> ToolResult:

    applications = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "paint": "mspaint.exe"
    }

    application = application.lower()

    if application not in applications:

        return ToolResult(
            success=False,
            message=f"{application} is not supported."
        )

    try:

        subprocess.Popen(applications[application])

        return ToolResult(
            success=True,
            message=f"{application.title()} opened successfully."
        )

    except Exception as e:

        return ToolResult(
            success=False,
            message=str(e)
        )