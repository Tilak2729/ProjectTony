from tools.browser_manager import BrowserManager


browser = BrowserManager()

browser.open_url("https://www.google.com")

input("Press Enter to close...")

browser.close()