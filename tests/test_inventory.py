import pytest
from playwright.sync_api import expect


class TestInventoryPage:
    """Test inventory page functionality."""

    @pytest.fixture(autouse=True)
    def setup(self, pages):
        """Authenticate and navigate to inventory page."""
        pages.authenticate(user="standard_user")
        pages.inventory.navigate()

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
