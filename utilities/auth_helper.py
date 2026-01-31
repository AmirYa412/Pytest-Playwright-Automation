from datetime import datetime, timedelta
from playwright.sync_api import BrowserContext, Page
from support.environment import Environment


class AuthHelper:
    """Helper for managing authentication via direct cookie injection."""

    def __init__(self, page: Page, env: Environment, cookies_cache: dict):
        self._page = page
        self._env = env
        self._cookies_cache = cookies_cache

    def auth_with_cookie(self, user_key: str):
        """
        Inject authentication cookie for specified user to bypass UI login.

        Args:
            user_key: User key from environment.users (e.g., "standard_user")
        """
        try:
            user_data = self._env.users[user_key]
        except KeyError:
            raise KeyError(
                f"User '{user_key}' not found. "
                f"Available users: {list(self._env.users.keys())}"
            )

        # Navigate to domain (required to set cookies)
        self._page.goto(self._env.base_url)

        # Reuse cached cookie if available
        if user_key in self._cookies_cache:
            print(f"Using cached cookie for {user_key}")
            context = self._page.context
            context.add_cookies(self._cookies_cache[user_key])
        else:
            # Create new authentication cookie and cache it
            print(f"Creating authentication cookie for {user_key}")
            cookie = {
                'name': 'session-username',
                'value': user_data['username'],
                'url': self._env.base_url,
                'path': '/',
                'expires': int((datetime.now() + timedelta(days=1)).timestamp())
            }

            context = self._page.context
            context.add_cookies([cookie])
            self._cookies_cache[user_key] = [cookie]

    def is_authenticated(self) -> bool:
        """
        Check if page has valid authentication cookie.

        Returns:
            True if authenticated, False otherwise
        """
        cookies = self._page.context.cookies()
        return any(cookie['name'] == 'session-username' for cookie in cookies)

    def get_current_user(self) -> str | None:
        """
        Get currently authenticated username.

        Returns:
            Username string if authenticated, None otherwise
        """
        cookies = self._page.context.cookies()
        for cookie in cookies:
            if cookie['name'] == 'session-username':
                return cookie['value']
        return None

    def logout(self):
        """Clear authentication cookies."""
        context = self._page.context
        context.clear_cookies()
        self._page.reload()