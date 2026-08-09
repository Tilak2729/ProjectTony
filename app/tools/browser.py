from tools.browser_manager import BrowserManager
from registry.decorators import tool
from tools.tool_result import ToolResult


browser_manager = BrowserManager()


@tool(
    name="browser",
    description="""
Control Tony's web browser.

Actions:
- open_url: Open a website or URL.
- search: Search Google.
- close: Close the browser.

Parameters:
action (string)
url (string, optional)
query (string, optional)
"""
)
def browser(
    action: str,
    url: str = None,
    query: str = None
) -> ToolResult:

    try:

        if action == "open_url":

            if not url:

                return ToolResult(
                    False,
                    "No URL was provided."
                )

            if not url.startswith(
                ("http://", "https://")
            ):

                url = "https://" + url

            browser_manager.open_url(url)

            return ToolResult(
                True,
                f"Opened {url}."
            )

        if action == "search":

            if not query:

                return ToolResult(
                    False,
                    "No search query was provided."
                )

            browser_manager.search(query)

            return ToolResult(
                True,
                f"Searching for {query}."
            )

        if action == "close":

            browser_manager.close()

            return ToolResult(
                True,
                "Browser closed."
            )

        return ToolResult(
            False,
            "Unsupported browser action."
        )

    except Exception as e:

        print(f"Browser error: {e}")

        return ToolResult(
            False,
            "I could not complete the browser action."
        )