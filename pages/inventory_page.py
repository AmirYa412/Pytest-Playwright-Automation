from pages.base_page import BasePage


class InventoryPage(BasePage):
    """SauceDemo inventory/home page."""

    PATH = "/inventory.html"
    TITLE = "Products"

    def __init__(self, page, env):
        super().__init__(page, env)

        # All use get_by_test_id - Playwright best practice!
        self.inventory_items = page.get_by_test_id("inventory-item")
        self.inventory_item_names = page.get_by_test_id("inventory-item-name")
        self.inventory_item_prices = page.get_by_test_id("inventory-item-price")
        self.sort_dropdown = page.get_by_test_id("product_sort_container")

        # Components (to be added later)
        # self.header = Header(page)
        # self.sidebar = SidebarMenu(page)

    def are_items_titles_displayed(self) -> bool:
        """Check if inventory item titles are displayed."""
        return self.inventory_item_names.first.is_visible()

    def add_item_to_cart(self, item_name: str):
        """
        Add an item to cart by its name.

        Args:
            item_name: Product name (e.g., "Sauce Labs Backpack")
        """
        # Normalize item name for data-test attribute
        normalized_name = item_name.lower().replace(' ', '-')
        data_test_value = f"add-to-cart-{normalized_name}"

        # Use get_by_test_id (configured to use data-test)
        add_button = self._page.get_by_test_id(data_test_value)
        add_button.click()

    def choose_option(self, sort_by: str):
        """
        Select sort option from dropdown.

        Args:
            sort_by: Sort option value ('az', 'za', 'lohi', 'hilo')
        """
        self.sort_dropdown.select_option(sort_by)

    def are_items_sorted_as_expected(self, sort_by: str) -> bool:
        """
        Verify items are sorted correctly.

        Args:
            sort_by: Sort option ('hilo' or 'lohi')

        Returns:
            True if sorted correctly, False otherwise
        """
        # Get all price elements
        price_elements = self.inventory_item_prices.all()

        # Extract prices as floats
        prices = []
        for element in price_elements:
            price_text = element.text_content()
            price = float(price_text.replace("$", ""))
            prices.append(price)

        # Verify sorting
        for i in range(len(prices) - 1):
            if sort_by == "hilo" and prices[i] < prices[i + 1]:
                return False
            elif sort_by == "lohi" and prices[i] > prices[i + 1]:
                return False

        return True