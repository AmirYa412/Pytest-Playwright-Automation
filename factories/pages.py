from playwright.sync_api import Page
from support.environment import Environment
from utilities.auth_helper import AuthHelper
from pages.login.login_page import LoginPage


class PageFactory:
    """Factory for lazy-loading page objects."""

    def __init__(self, page: Page, env: Environment, auth_cookies_cache: dict):
        self._page = page
        self._env = env
        self._pages_cache = {}
        self._auth_cookies_cache = auth_cookies_cache
        self.auth_helper = AuthHelper(page, env, auth_cookies_cache)

    def authenticate(self, user: str):
        """
        Authenticate user by injecting cookie (no UI interaction).
        For tests that don't test login functionality.

        Args:
            user: User key (e.g., 'standard_user')
        """
        self.auth_helper.auth_with_cookie(user)

    @property
    def login(self):
        """Get or create LoginPage instance."""
        if 'login' not in self._pages_cache:
            self._pages_cache['login'] = LoginPage(self._page, self._env)
        return self._pages_cache['login']

    # TODO: Add other page objects
    # @property
    # def inventory(self):
    #     if 'inventory' not in self._pages_cache:
    #         from pages.inventory.inventory_page import InventoryPage
    #         self._pages_cache['inventory'] = InventoryPage(self._page, self._env)
    #     return self._pages_cache['inventory']