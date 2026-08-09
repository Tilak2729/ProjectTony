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

    def close(self):

        if self.browser:

            self.browser.close()

            self.browser = None

        if self.playwright:

            self.playwright.stop()

            self.playwright = None

            self.page = None