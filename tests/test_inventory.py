import pytest
from playwright.sync_api import expect


@pytest.mark.inventory
class TestInventoryPage:
    """Test inventory page functionality."""

    @pytest.fixture(autouse=True)
    def setup(self, pages):
        """Authenticate and navigate to inventory page."""
        pages.authenticate(user="standard_user")
        pages.inventory.navigate()

    @pytest.mark.regression
    def test_all_products_have_required_elements(self, pages, data):
        """Verify each product has title, image, description, price, and add to cart button."""
        expected_products = [data["inventory"][key] for key in data["inventory"]]
        product_count = pages.inventory.get_product_count()
        assert product_count == 6, f"Expected 6 products, found {product_count}"

        inventory = pages.inventory
        for product_name in expected_products:
            product_card = inventory.get_product_card(product_name)

            expect(product_card.locator(inventory.item_name)).to_have_text(product_name)
            expect(product_card.locator(inventory.item_img)).to_be_visible()
            expect(product_card.locator(inventory.item_desc)).not_to_be_empty()
            expect(product_card.locator(inventory.item_price)).to_contain_text("$")
            expect(product_card.locator(inventory.add_to_cart_btn)).to_be_enabled()


    def test_add_and_remove_item_updates_cart_badge(self, pages, data):
        """Verify adding and removing item updates the cart badge."""
        header = pages.inventory.header
        inventory = pages.inventory

        expect(header.shopping_cart_badge).not_to_be_visible()

        product_name = data["inventory"]["item_1"]
        product_card = inventory.get_product_card(product_name)
        product_card.locator(inventory.add_to_cart_btn).click()

        expect(header.shopping_cart_badge).to_be_visible()
        expect(header.shopping_cart_badge).to_have_text("1")

        product_card.locator(inventory.remove_btn).click()
        expect(header.shopping_cart_badge).not_to_be_visible()
