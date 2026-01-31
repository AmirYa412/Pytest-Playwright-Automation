from playwright.sync_api import Page

class SidebarMenu:
    """Sidebar navigation menu component."""

    def __init__(self, page: Page):
        self._page = page

        # Using get_by_test_id (configured to data-test) or get_by_role
        self.all_items_link = page.get_by_test_id("inventory-sidebar-link")
        self.about_link = page.get_by_test_id("about-sidebar-link")
        self.logout_link = page.get_by_test_id("logout-sidebar-link")
        self.reset_app_link = page.get_by_test_id("reset-sidebar-link")
        self.close_menu_button = page.get_by_role("button", name="Close Menu")

    def click_all_items(self):
        self.all_items_link.click()

    def click_about(self):
        self.about_link.click()

    def click_logout(self):
        self.logout_link.click()

    def click_reset_app(self):
        self.reset_app_link.click()

    def close_menu(self):
        self.close_menu_button.click()