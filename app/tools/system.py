import platform
import psutil

from registry.decorators import tool
from tools.tool_result import ToolResult


@tool(
    name="system_info",
    description="""
Get information about the user's computer.

Actions:
- system: Get operating system and computer information.
- cpu: Get CPU usage.
- memory: Get RAM usage.
- battery: Get battery level and charging status.

Parameters:
action (string)
"""
)
def system_info(action: str) -> ToolResult:

    try:

        if action == "system":

            system = platform.system()
            release = platform.release()
            version = platform.version()
            machine = platform.machine()
            processor = platform.processor()

            message = (
                f"Operating system: {system} {release}. "
                f"Version: {version}. "
                f"Architecture: {machine}. "
                f"Processor: {processor}."
            )

            return ToolResult(
                True,
                message
            )

        if action == "cpu":

            cpu_usage = psutil.cpu_percent(
                interval=1
            )

            return ToolResult(
                True,
                f"CPU usage is {cpu_usage} percent."
            )

        if action == "memory":

            memory = psutil.virtual_memory()

            used_gb = memory.used / (
                1024 ** 3
            )

            total_gb = memory.total / (
                1024 ** 3
            )

            percentage = memory.percent

            message = (
                f"RAM usage is {percentage} percent. "
                f"{used_gb:.1f} GB of "
                f"{total_gb:.1f} GB is currently being used."
            )

            return ToolResult(
                True,
                message
            )

        if action == "battery":

            battery = psutil.sensors_battery()

            if battery is None:

                return ToolResult(
                    False,
                    "Battery information is not available."
                )

            percentage = battery.percent

            if battery.power_plugged:

                status = "charging."

            else:

                status = "not charging."

            return ToolResult(
                True,
                f"Battery is at {percentage} percent and is {status}"
            )

        return ToolResult(
            False,
            "Unsupported system information action."
        )

    except Exception as e:

        print(f"System information error: {e}")

        return ToolResult(
            False,
            "I could not retrieve the system information."
        )