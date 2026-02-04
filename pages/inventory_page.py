from pages.base_page import BasePage
from components.header import Header
from components.sidebar_menu import SidebarMenu


class InventoryPage(BasePage):
    """SauceDemo inventory/home page."""

    PATH = "/inventory.html"
    TITLE = "Products"

    def __init__(self, page, env):
        super().__init__(page, env)

        # Page elements
        self.inventory_items = page.get_by_test_id("inventory-item")
        self.inventory_item_names = page.get_by_test_id("inventory-item-name")
        self.inventory_item_prices = page.get_by_test_id("inventory-item-price")
        self.sort_dropdown = page.get_by_test_id("product_sort_container")

        self.item_name = page.get_by_test_id("inventory-item-name")
        self.item_desc = page.get_by_test_id("inventory-item-desc")
        self.item_price = page.get_by_test_id("inventory-item-price")
        self.item_img = page.locator("img.inventory_item_img")
        self.add_to_cart_btn = page.locator("button[id^='add-to-cart']")

        self.sort_dropdown = page.get_by_test_id("product_sort_container")
        self.header = Header(page)
        self.sidebar = SidebarMenu(page)

    def get_product_count(self) -> int:
        """Get total number of products displayed."""
        return self.inventory_items.count()

    def get_product_card(self, product_name):
        """
        Returns a Locator that represents the specific card for the given name.
        All subsequent calls on this returned locator will be scoped to this card.
        """
        return self.inventory_items.filter(
            has=self.item_name.get_by_text(product_name, exact=True)
        )

    def get_product_container_by_name(self, product_name: str):
        """Get product container by product name."""
        return self._page.locator(f'[data-test="inventory-item"]:has-text("{product_name}")')

    def get_product_title(self, product_name: str):
        """Get product title locator by product name."""
        container = self.get_product_container_by_name(product_name)
        return container.get_by_test_id("inventory-item-name")

    def get_product_image(self, product_name: str):
        """Get product image locator by product name."""
        container = self.get_product_container_by_name(product_name)
        return container.locator("img.inventory_item_img")

    def get_product_description(self, product_name: str):
        """Get product description locator by product name."""
        container = self.get_product_container_by_name(product_name)
        return container.get_by_test_id("inventory-item-desc")

    def get_product_price(self, product_name: str):
        """Get product price locator by product name."""
        container = self.get_product_container_by_name(product_name)
        return container.get_by_test_id("inventory-item-price")

    def get_product_add_to_cart_button(self, product_name: str):
        """Get add to cart button locator by product name."""
        container = self.get_product_container_by_name(product_name)
        return container.locator("button.btn_inventory")

    def are_items_titles_displayed(self) -> bool:
        """Check if inventory item titles are displayed."""
        return self.inventory_item_names.first.is_visible()

    def add_item_to_cart(self, product_name: str):
        """Add an item to cart by its name."""
        normalized_name = product_name.lower().replace(' ', '-')
        data_test_value = f"add-to-cart-{normalized_name}"
        add_button = self._page.get_by_test_id(data_test_value)
        add_button.click()

    def choose_option(self, sort_by: str):
        """Select sort option from dropdown."""
        self.sort_dropdown.select_option(sort_by)

    def are_items_sorted_as_expected(self, sort_by: str) -> bool:
        """Verify items are sorted correctly."""
        price_elements = self.inventory_item_prices.all()
        prices = []
        for element in price_elements:
            price_text = element.text_content()
            price = float(price_text.replace("$", ""))
            prices.append(price)

        for i in range(len(prices) - 1):
            if sort_by == "hilo" and prices[i] < prices[i + 1]:
                return False
            elif sort_by == "lohi" and prices[i] > prices[i + 1]:
                return False

        return True