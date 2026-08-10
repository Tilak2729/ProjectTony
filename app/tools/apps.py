import subprocess

from registry.decorators import tool
from tools.tool_result import ToolResult


APPLICATIONS = {
    "notepad": "notepad.exe",
    "calculator": "CalculatorApp.exe",
    "paint": "mspaint.exe",
}


@tool(
    name="open_application",
    description="""
Open an installed desktop application.

Supported applications:
- notepad
- calculator
- paint

Parameters:
application (string)
"""
)
def open_application(application: str) -> ToolResult:

    application = application.lower().strip()

    if application not in APPLICATIONS:

        return ToolResult(
            success=False,
            message=(
                f"{application} is not supported. "
                "I can currently open Notepad, "
                "Calculator, or Paint."
            )
        )

    try:

        subprocess.Popen(
            APPLICATIONS[application]
        )

        return ToolResult(
            success=True,
            message=(
                f"{application.title()} "
                "opened successfully."
            )
        )

    except Exception as e:

        return ToolResult(
            success=False,
            message=str(e)
        )


@tool(
    name="close_application",
    description="""
Close a desktop application.

Supported applications:
- notepad
- calculator
- paint

Parameters:
application (string)
"""
)
def close_application(application: str) -> ToolResult:

    application = application.lower().strip()

    if application not in APPLICATIONS:

        return ToolResult(
            success=False,
            message=(
                f"{application} is not supported."
            )
        )

    process_name = APPLICATIONS[application]

    try:

        result = subprocess.run(
            [
                "taskkill",
                "/IM",
                process_name,
                "/F"
            ],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:

            return ToolResult(
                success=False,
                message=(
                    f"{application.title()} "
                    "does not appear to be running."
                )
            )

        return ToolResult(
            success=True,
            message=(
                f"{application.title()} "
                "closed successfully."
            )
        )

    except Exception as e:

        return ToolResult(
            success=False,
            message=str(e)
        )


@tool(
    name="list_applications",
    description="""
List the desktop applications Tony currently supports.
"""
)
def list_applications() -> ToolResult:

    applications = ", ".join(
        name.title()
        for name in APPLICATIONS
    )

    return ToolResult(
        success=True,
        message=(
            f"Supported applications: "
            f"{applications}."
        )
    )