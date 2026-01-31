from playwright.sync_api import Page


class Header:
    """Header component - appears on all authenticated pages."""

    def __init__(self, page: Page):
        self._page = page

        self.logo = page.get_by_text("Swag Labs")
        self.page_title = page.get_by_test_id("title")
        self.shopping_cart_button = page.get_by_test_id("shopping-cart-link")
        self.shopping_cart_badge = page.get_by_test_id("shopping-cart-badge")
        self.sidebar_menu_button = page.get_by_role("button", name="Open Menu")


    def is_logo_displayed(self) -> bool:
        return self.logo.is_visible()

    def click_shopping_cart(self):
        self.shopping_cart_button.click()

    def click_sidebar_menu(self):
        self.sidebar_menu_button.click()

    def get_header_title_text(self) -> str:
        return self.page_title.text_content()

    def get_cart_item_count(self) -> int:
        # Check if badge exists first to avoid timeout if cart is empty
        if self.shopping_cart_badge.is_visible():
            return int(self.shopping_cart_badge.text_content())
        return 0