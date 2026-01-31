from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page object for the Login Page."""

    PATH = "/"
    TITLE = None

    def __init__(self, page, env):
        super().__init__(page, env)

        # Locators as attributes - direct, native, clear
        self.username_input = page.get_by_test_id("username")
        self.password_input = page.get_by_test_id("password")
        self.login_button = page.get_by_test_id("login-button")
        self.error_message = page.get_by_test_id("error")

    def perform_login(self, user: str):
        """
        Perform full UI login flow (ALWAYS uses UI, never cached cookies).
        For testing login functionality.

        Args:
            user: User key from environment
        """
        try:
            user_credentials = self._env.users[user]
        except KeyError:
            raise KeyError(
                f"User '{user}' not found. "
                f"Available: {list(self._env.users.keys())}"
            )

        # Navigate to login page
        self.navigate()

        # Use locator attributes directly
        self.username_input.fill(user_credentials["username"])
        self.password_input.fill(user_credentials["password"])
        self.login_button.click()

        # Wait for redirect to inventory
        self._page.wait_for_url("**/inventory.html", timeout=self.timeout)

    def is_err_msg_displayed(self) -> bool:
        """Check if error message is displayed."""
        return self.error_message.is_visible()

    def get_error_message_text(self) -> str:
        """Get error message text."""
        return self.error_message.text_content()