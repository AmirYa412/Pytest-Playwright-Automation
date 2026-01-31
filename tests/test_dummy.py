def test_browser_opens_saucedemo(pages):
    """Verify browser opens saucedemo."""
    pages._page.goto(pages._env.base_url)
    assert "Swag Labs" in pages._page.title()
    print(f"\n✅ Opened: {pages._env.base_url}")