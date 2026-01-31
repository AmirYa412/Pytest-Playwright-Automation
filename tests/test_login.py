class TestLoginPage:

    def test_login_successful_(self, pages):
        pages.login.navigate()
        pages.login.perform_login(user="standard_user")
        pages.inventory.verify_on_page()

