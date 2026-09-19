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
        self.sort_dropdown = page.get_by_test_id("product-sort-container")

        self.item_names = page.get_by_test_id("inventory-item-name")
        self.item_desc = page.get_by_test_id("inventory-item-desc")
        self.item_prices = page.get_by_test_id("inventory-item-price")
        self.item_img = page.locator("img.inventory_item_img")
        self.add_to_cart_btn = page.locator("button[id^='add-to-cart']")
        self.remove_btn = page.locator("button[id^='remove']")

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
            has=self.item_names.get_by_text(product_name, exact=True)
        )

    def get_product_title(self, product_name: str):
        """Get product title locator scoped to the given product's card."""
        return self.get_product_card(product_name).locator(self.item_names)

    def get_product_image(self, product_name: str):
        """Get product image locator scoped to the given product's card."""
        return self.get_product_card(product_name).locator(self.item_img)

    def get_product_description(self, product_name: str):
        """Get product description locator scoped to the given product's card."""
        return self.get_product_card(product_name).locator(self.item_desc)

    def get_product_price(self, product_name: str):
        """Get product price locator scoped to the given product's card."""
        return self.get_product_card(product_name).locator(self.item_prices)

    def get_product_add_to_cart_button(self, product_name: str):
        """Get add to cart button locator scoped to the given product's card."""
        return self.get_product_card(product_name).locator(self.add_to_cart_btn)

    def get_product_remove_button(self, product_name: str):
        """Get remove button locator scoped to the given product's card."""
        return self.get_product_card(product_name).locator(self.remove_btn)

    def are_items_titles_displayed(self) -> bool:
        """Check if inventory item titles are displayed."""
        return self.item_names.first.is_visible()

    def add_item_to_cart(self, product_name: str):
        """Add an item to cart by its name."""
        add_to_cart_button = self.get_product_add_to_cart_button(product_name)
        add_to_cart_button.click()

    def remove_item_from_cart(self, product_name: str):
        """Remove an item from the cart by its name."""
        remove_button = self.get_product_remove_button(product_name)
        remove_button.click()

    def choose_option(self, sort_by: str):
        """Select sort option from dropdown."""
        self.sort_dropdown.select_option(sort_by)

    def are_items_sorted_as_expected(self, sort_by: str) -> bool:
        """Verify items are sorted correctly.

        Supports all four SauceDemo sort options: name (az/za) and price
        (lohi/hilo). Raises for any other value instead of passing silently.
        """
        if sort_by in ("az", "za"):
            names = [element.text_content() for element in self.item_names.all()]
            return names == sorted(names, reverse=(sort_by == "za"))

        if sort_by in ("lohi", "hilo"):
            prices = [float(element.text_content().replace("$", "")) for element in self.item_prices.all()]
            return prices == sorted(prices, reverse=(sort_by == "hilo"))

        raise ValueError(f"Unsupported sort option: {sort_by!r}. Expected one of: az, za, lohi, hilo")