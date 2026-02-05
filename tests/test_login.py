import pytest
from playwright.sync_api import expect


@pytest.mark.login
class TestLoginPage:
    """Test login page functionality."""

    @pytest.mark.regression
    def test_login_and_logout(self, pages):
        """Verify user is able to login and logout via UI"""
        pages.login.navigate()
        pages.login.perform_login(user="standard_user")

        pages.inventory.verify_on_page()
        pages.inventory.verify_page_title()
        expect(pages.inventory.header.logo).to_be_visible()
        expect(pages.inventory.header.sidebar_menu_button).to_be_visible()

        pages.inventory.header.click_sidebar_menu()
        pages.inventory.sidebar.click_logout()
        pages.login.verify_on_page()

    def test_login_error_message_for_locked_user(self, pages):
        pages.login.navigate()
        pages.login.perform_login(user="locked_out_user")
        expect(pages.login.error_message).to_have_text("Epic sadface: Sorry, this user has been locked out.")
