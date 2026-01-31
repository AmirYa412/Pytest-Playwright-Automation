from playwright.sync_api import Page, expect
from support.environment import Environment
import re


class BasePage:
    """Base page with common functionality for all page objects."""

    PATH = "/"
    TITLE = None

    def __init__(self, page: Page, env: Environment):
        self._page = page
        self._env = env
        self.timeout = self._env.timeout

    def navigate(self, path: str = None, verify_on_page: bool = True):
        """Navigate to page with optional validation."""
        target = path if path is not None else self.PATH
        self._page.goto(f"{self._env.base_url}{target}")

        if verify_on_page:
            self.verify_on_page()
            self.verify_page_title()

    def verify_on_page(self):
        """Verify URL contains expected PATH."""
        expect(self._page).to_have_url(re.compile(f"{self.PATH}"))

    def verify_page_title(self):
        """Verify page title matches TITLE attribute (if set)."""
        if self.TITLE and hasattr(self, 'header'):
            expect(self.header.page_title).to_have_text(self.TITLE)

    def get_current_page_title(self) -> str:
        """Get current page title."""
        return self._page.title()

    def refresh_page(self):
        """Refresh the current page."""
        self._page.reload()

    def get_page_source_code(self) -> str:
        """Get page HTML source."""
        return self._page.content()