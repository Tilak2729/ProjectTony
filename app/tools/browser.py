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
- type: Type text into an interactive element by ID.
- press: Press a keyboard key on an interactive element by ID.
- close: Close the browser.

Parameters:
action (string)
url (string, optional)
query (string, optional)
element_id (integer, optional)
text (string, optional)
key (string, optional)
"""
)
def browser(
    action: str,
    url: str = None,
    query: str = None,
    element_id: int = None,
    text: str = None,
    key: str = None
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

            page_text = (
                browser_manager
                .get_page_text()
            )

            if not page_text:

                return ToolResult(
                    False,
                    "The page does not contain readable text."
                )

            return ToolResult(
                True,
                page_text[:12000]
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

        if action == "type":

            if element_id is None:

                return ToolResult(
                    False,
                    "No element ID was provided."
                )

            if text is None:

                return ToolResult(
                    False,
                    "No text was provided."
                )

            browser_manager.type_text(
                element_id,
                text
            )

            return ToolResult(
                True,
                f"Typed text into element {element_id}."
            )

        if action == "press":

            if element_id is None:

                return ToolResult(
                    False,
                    "No element ID was provided."
                )

            if not key:

                return ToolResult(
                    False,
                    "No key was provided."
                )

            browser_manager.press_key(
                element_id,
                key
            )

            return ToolResult(
                True,
                f"Pressed {key} on element {element_id}."
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