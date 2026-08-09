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
- read_page: Read visible webpage text.
- get_elements: Get numbered interactive webpage elements.
- click: Click an interactive webpage element by ID.
- close: Close the browser.

Parameters:
action (string)
url (string, optional)
query (string, optional)
element_id (integer, optional)
"""
)
def browser(
    action: str,
    url: str = None,
    query: str = None,
    element_id: int = None
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

        if action == "read_page":

            text = browser_manager.get_page_text()

            if not text:

                return ToolResult(
                    False,
                    "The page does not contain readable text."
                )

            return ToolResult(
                True,
                text[:12000]
            )

        if action == "get_elements":

            elements = (
                browser_manager
                .get_interactive_elements()
            )

            if not elements:

                return ToolResult(
                    False,
                    "No interactive elements were found."
                )

            formatted = "\n".join(
                f"[{item['id']}] "
                f"{item['tag']}: "
                f"{item['text']}"
                for item in elements[:100]
            )

            return ToolResult(
                True,
                formatted
            )

        if action == "click":

            if element_id is None:

                return ToolResult(
                    False,
                    "No element ID was provided."
                )

            browser_manager.click_element(
                element_id
            )

            return ToolResult(
                True,
                f"Clicked element {element_id}."
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