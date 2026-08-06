from pycaw.pycaw import (
    AudioUtilities,
)

from registry.decorators import tool
from tools.tool_result import ToolResult


@tool(
    name="change_volume",
    description="""
Control the system volume.

Actions:
- increase
- decrease
- mute
- unmute
- set

Parameter:
action (string)
level (integer, only used with 'set')
"""
)
def change_volume(
    action: str,
    level: int = None
) -> ToolResult:

    device = AudioUtilities.GetSpeakers()

    volume = device.EndpointVolume

    current = volume.GetMasterVolumeLevelScalar()

    if action == "increase":

        current = min(current + 0.1, 1.0)

        volume.SetMasterVolumeLevelScalar(current, None)

        return ToolResult(
            True,
            "Volume increased."
        )

    elif action == "decrease":

        current = max(current - 0.1, 0.0)

        volume.SetMasterVolumeLevelScalar(current, None)

        return ToolResult(
            True,
            "Volume decreased."
        )

    elif action == "mute":

        volume.SetMute(1, None)

        return ToolResult(
            True,
            "Volume muted."
        )

    elif action == "unmute":

        volume.SetMute(0, None)

        return ToolResult(
            True,
            "Volume unmuted."
        )

    elif action == "set":

        if level is None:

            return ToolResult(
                False,
                "Please provide a volume level."
            )

        level = max(0, min(level, 100))

        volume.SetMasterVolumeLevelScalar(
            level / 100,
            None
        )

        return ToolResult(
            True,
            f"Volume set to {level} percent."
        )

    return ToolResult(
        False,
        "Unknown volume action."
    )