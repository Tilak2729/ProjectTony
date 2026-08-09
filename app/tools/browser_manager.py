from playwright.sync_api import sync_playwright


class BrowserManager:

    def __init__(self):

        self.playwright = None
        self.browser = None
        self.page = None

    def start(self):

        if self.browser:
            return

        print("🌐 Starting Tony browser...")

        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=False
        )

        self.page = self.browser.new_page()

    def open_url(self, url):

        self.start()

        self.page.goto(url)

    def search(self, query):

        self.start()

        self.page.goto(
            "https://www.google.com/search?q="
            + query.replace(" ", "+")
        )

    def get_page_text(self):

        self.start()

        return self.page.locator(
            "body"
        ).inner_text()

    def get_interactive_elements(self):

        self.start()

        elements = []

        locator = self.page.locator(
            "a, button, input, textarea, select"
        )

        count = locator.count()

        for i in range(count):

            element = locator.nth(i)

            try:

                if not element.is_visible():

                    continue

                tag = element.evaluate(
                    "(el) => el.tagName"
                )

                text = element.inner_text(
                    timeout=500
                ).strip()

                placeholder = element.get_attribute(
                    "placeholder"
                )

                aria_label = element.get_attribute(
                    "aria-label"
                )

                value = (
                    text
                    or placeholder
                    or aria_label
                    or "(no text)"
                )

                elements.append(
                    {
                        "id": len(elements),
                        "tag": tag,
                        "text": value
                    }
                )

            except Exception:

                continue

        return elements

    def _get_visible_elements(self):

        self.start()

        locator = self.page.locator(
            "a, button, input, textarea, select"
        )

        visible_elements = []

        count = locator.count()

        for i in range(count):

            element = locator.nth(i)

            try:

                if element.is_visible():

                    visible_elements.append(
                        element
                    )

            except Exception:

                continue

        return visible_elements

    def click_element(self, element_id):

        visible_elements = (
            self._get_visible_elements()
        )

        if (
            element_id < 0
            or element_id >= len(visible_elements)
        ):

            raise ValueError(
                "Invalid element ID."
            )

        visible_elements[
            element_id
        ].click()

    def type_text(
        self,
        element_id,
        text
    ):

        visible_elements = (
            self._get_visible_elements()
        )

        if (
            element_id < 0
            or element_id >= len(visible_elements)
        ):

            raise ValueError(
                "Invalid element ID."
            )

        element = visible_elements[
            element_id
        ]

        element.fill(text)

    def press_key(
        self,
        element_id,
        key
    ):

        visible_elements = (
            self._get_visible_elements()
        )

        if (
            element_id < 0
            or element_id >= len(visible_elements)
        ):

            raise ValueError(
                "Invalid element ID."
            )

        element = visible_elements[
            element_id
        ]

        element.press(key)

    def close(self):

        if self.browser:

            self.browser.close()

            self.browser = None

        if self.playwright:

            self.playwright.stop()

            self.playwright = None

            self.page = None