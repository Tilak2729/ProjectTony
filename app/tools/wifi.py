import subprocess

from registry.decorators import tool
from tools.tool_result import ToolResult


WIFI_ADAPTER = "Wi-Fi"


def get_wifi_status():

    result = subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-Command",
            f"Get-NetAdapter -Name '{WIFI_ADAPTER}' "
            "| Select-Object -ExpandProperty Status"
        ],
        capture_output=True,
        text=True
    )

    return result.stdout.strip()


@tool(
    name="wifi",
    description="""
Control the Wi-Fi adapter.

Actions:
- status: Check whether Wi-Fi is enabled.
- on: Enable Wi-Fi.
- off: Disable Wi-Fi.

Parameters:
action (string)
"""
)
def wifi(action: str) -> ToolResult:

    try:

        if action == "status":

            status = get_wifi_status()

            if status == "Up":

                return ToolResult(
                    True,
                    "Wi-Fi is currently on."
                )

            if status == "Disabled":

                return ToolResult(
                    True,
                    "Wi-Fi is currently off."
                )

            return ToolResult(
                True,
                f"Wi-Fi status is {status}."
            )

        if action == "on":

            subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-Command",
                    f"Enable-NetAdapter "
                    f"-Name '{WIFI_ADAPTER}' "
                    f"-Confirm:$false"
                ],
                check=True
            )

            return ToolResult(
                True,
                "Wi-Fi has been turned on."
            )

        if action == "off":

            subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-Command",
                    f"Disable-NetAdapter "
                    f"-Name '{WIFI_ADAPTER}' "
                    f"-Confirm:$false"
                ],
                check=True
            )

            return ToolResult(
                True,
                "Wi-Fi has been turned off."
            )

        return ToolResult(
            False,
            "Unsupported Wi-Fi action."
        )

    except subprocess.CalledProcessError:

        return ToolResult(
            False,
            "Windows did not allow me to change the Wi-Fi adapter."
        )

    except Exception as e:

        print(f"Wi-Fi error: {e}")

        return ToolResult(
            False,
            "I could not control the Wi-Fi adapter."
        )