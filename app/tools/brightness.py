import screen_brightness_control as sbc

from registry.decorators import tool
from tools.tool_result import ToolResult


@tool(
    name="brightness",
    description="""
Control the screen brightness.

Actions:
- increase: Increase brightness by 10 percent.
- decrease: Decrease brightness by 10 percent.
- set: Set brightness to a specific percentage.
- get: Get the current brightness.

Parameters:
action (string)
level (integer, optional)
"""
)
def brightness(
    action: str,
    level: int = None
) -> ToolResult:

    try:

        current = sbc.get_brightness()

        if isinstance(current, list):
            current = current[0]

        current = int(current)

        if action == "get":

            return ToolResult(
                True,
                f"Brightness is currently {current} percent."
            )

        if action == "increase":

            new_level = min(
                current + 10,
                100
            )

            sbc.set_brightness(new_level)

            return ToolResult(
                True,
                f"Brightness increased to {new_level} percent."
            )

        if action == "decrease":

            new_level = max(
                current - 10,
                0
            )

            sbc.set_brightness(new_level)

            return ToolResult(
                True,
                f"Brightness decreased to {new_level} percent."
            )

        if action == "set":

            if level is None:

                return ToolResult(
                    False,
                    "No brightness level was provided."
                )

            level = max(
                0,
                min(level, 100)
            )

            sbc.set_brightness(level)

            return ToolResult(
                True,
                f"Brightness set to {level} percent."
            )

        return ToolResult(
            False,
            "Unsupported brightness action."
        )

    except Exception as e:

        print(f"Brightness error: {e}")

        return ToolResult(
            False,
            "I could not change the screen brightness."
        )