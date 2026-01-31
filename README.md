# Playwright Test Automation Framework

A professional-grade test automation framework built with **Playwright** and **pytest**, demonstrating industry best practices for scalable, maintainable end-to-end testing.

---

## 🏗️ Framework Architecture

This framework follows a **layered architecture** with clear separation of concerns:
```
Pytest-Playwright-Automation/
├── components/          # Reusable UI components (Header, Sidebar, etc.)
├── config/             # Environment-specific configuration files
├── factories/          # Factory pattern for lazy-loading page objects
├── pages/              # Page Object Model implementation
├── support/            # Core framework infrastructure (Environment)
├── tests/              # Test suites organized by feature
├── users/              # User credentials management
├── utilities/          # Helper utilities (AuthHelper, etc.)
└── conftest.py         # Pytest configuration and fixtures
```

### **Key Design Patterns**

✅ **Page Object Model (POM)** - Clean separation of page structure from test logic  
✅ **Factory Pattern** - Lazy-loading page objects for better memory management  
✅ **Component Pattern** - Reusable UI components (Header, Sidebar) across pages  
✅ **Environment Abstraction** - Multi-environment support (qa, ci, dev, production)  
✅ **Smart Authentication** - Cookie injection to bypass UI login for faster test execution  

---

## 🚀 Quick Start

### **Prerequisites**

- Python 3.12+
- pip (Python package manager)

### **Installation**

1. **Clone the repository**
```bash
git clone <repository-url>
cd Pytest-Playwright-Automation
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
playwright install  # Install browser binaries
```

4. **Configure environment variables**

Create a `.env` file in the root directory:
```env
PROD_SAUCEDEMO_USER_PASSWORD=secret_sauce
CI_SAUCEDEMO_USER_PASSWORD=secret_sauce
```

> **⚠️ Important:** For security, `.env` files should **NEVER** be committed to version control. Always add `.env` to `.gitignore` and use secure secret management solutions.

---

## 🎯 Running Tests

### **Basic Execution**
```bash
# Run all tests (requires --env flag)
pytest --env=production

# Run specific test file
pytest tests/test_login.py --env=www

# Run with headed browser (see the browser)
pytest --env=production --headed

# Run with specific browser
pytest --env=production --browser=firefox
pytest --env=production --browser=webkit
```

### **Advanced Options**
```bash
# Parallel execution
pytest --env=www -n 4

# Generate HTML report
pytest --env=www --html=reports/report.html

# Run specific markers
pytest -m login --env=www

# Different environments
pytest --env=qa          # qa.saucedemo.com
pytest --env=ci          # ci.saucedemo.com
pytest --env=production  # saucedemo.com
```

---

## 📁 Framework Structure

### **Pages**

Page objects encapsulate page-specific logic with Playwright's native locators:
```python
class LoginPage(BasePage):
    PATH = "/"
    TITLE = None
    
    def __init__(self, page, env):
        super().__init__(page, env)
        
        # Locators defined in __init__ using Playwright best practices
        self.username_input = page.get_by_test_id("username")
        self.password_input = page.get_by_test_id("password")
        self.login_button = page.get_by_test_id("login-button")
    
    def perform_login(self, user: str):
        """Perform full UI login."""
        # Implementation...
```

### **Components**

Reusable UI components used across multiple pages:
```python
class Header:
    """Header component - appears on all authenticated pages."""
    
    def __init__(self, page: Page):
        self.logo = page.get_by_text("Swag Labs")
        self.shopping_cart_button = page.get_by_test_id("shopping-cart-link")
        self.sidebar_menu_button = page.get_by_role("button", name="Open Menu")
```

### **Factories**

Page factory for lazy-loading and encapsulation:
```python
class PageFactory:
    """Factory for lazy-loading page objects."""
    
    @property
    def login(self) -> LoginPage:
        if 'login' not in self._pages_cache:
            self._pages_cache['login'] = LoginPage(self._page, self._env)
        return self._pages_cache['login']
```

### **Authentication**

Smart cookie injection to bypass UI login:
```python
# In tests - fast authentication via cookie
pages.authenticate(user="standard_user")
pages.inventory.navigate()

# OR - full UI login for testing login functionality
pages.login.perform_login(user="standard_user")
```

---

## 🧪 Writing Tests

Tests use a single `pages` fixture for clean, maintainable code:
```python
class TestInventoryPage:
    def test_add_item_to_cart(self, pages):
        """Test adding item to shopping cart."""
        # Authenticate via cookie (fast)
        pages.authenticate(user="standard_user")
        
        # Navigate and interact
        pages.inventory.navigate()
        pages.inventory.add_item_to_cart("Sauce Labs Backpack")
        
        # Assertions using Playwright's expect
        assert pages.inventory.header.get_cart_item_count() == 1
```

---

## ⚙️ Configuration

### **Environment Config** (`config/`)
```json
{
  "timeout": 30000,
  "viewport": {
    "width": 1920,
    "height": 1080
  },
  "screenshots_on_failure": true
}
```

### **Environment URLs**

URLs are dynamically built based on environment prefix:

- `--env=production` → `https://saucedemo.com`
- `--env=qa` → `https://qa.saucedemo.com`
- `--env=ci` → `https://ci.saucedemo.com`
- `--env=dev` → `https://dev.saucedemo.com`

---

## 🎨 Key Features

### **Playwright Best Practices**

✅ **Native locators** - `get_by_role()`, `get_by_test_id()`, `get_by_label()`  
✅ **Auto-waiting** - No manual waits, Playwright handles synchronization  
✅ **Expect assertions** - Built-in retry mechanism for stable tests  
✅ **Multi-browser** - Chromium, Firefox, WebKit support out of the box  

### **Framework Features**

✅ **Smart Authentication** - Cookie injection for 10x faster test execution  
✅ **Component Reusability** - DRY principle with reusable UI components  
✅ **Environment Flexibility** - Easy switching between qa/ci/dev/prod  
✅ **Parallel Execution** - pytest-xdist support for faster CI/CD  
✅ **HTML Reports** - Beautiful test reports with screenshots on failure  
✅ **Type Safety** - Type hints throughout for better IDE support  

---

## 📊 Test Reports

HTML reports with screenshots are automatically generated on failure:
```bash
pytest --env=www --html=reports/report.html --self-contained-html
```

Reports include:
- Test execution summary
- Screenshots on failure
- Execution time metrics
- Browser/environment metadata

---

## 🔧 Troubleshooting

### **Common Issues**

**Issue:** `--env is required` error  
**Solution:** Always specify environment: `pytest --env=production`

**Issue:** Browser not found  
**Solution:** Run `playwright install`

**Issue:** Authentication fails  
**Solution:** Verify `.env` file has correct credentials

**Issue:** Tests fail with timeout  
**Solution:** Increase timeout in config files or run with `--headed` to debug

---

## 📝 Best Practices

1. **Always use `get_by_test_id()` or `get_by_role()`** for locators (avoid CSS/XPath)
2. **Use `pages.authenticate()` for non-login tests** (faster execution)
3. **Use `pages.login.perform_login()` only for login-specific tests** (full UI flow)
4. **Keep page objects focused** - One page class per page
5. **Use components for shared UI** - Header, Sidebar, Modals, etc.
6. **Run tests in parallel** - Use `-n auto` for CI/CD
7. **Never commit `.env` files** - Use secret management in production

---

## 🛠️ Tech Stack

- **Python** 3.12+
- **Playwright** 1.58.0 - Modern browser automation
- **pytest** 9.0.2 - Test framework
- **pytest-playwright** 0.7.2 - Playwright integration
- **pytest-html** 4.2.0 - HTML reporting
- **pytest-xdist** 3.8.0 - Parallel execution
- **python-dotenv** 1.2.1 - Environment variable management

---

## 📚 Project Structure Details
```
├── components/            # Reusable UI components
│   ├── header.py           # Header component (logo, cart, menu)
│   └── sidebar_menu.py     # Sidebar navigation
│
├── config/                  # Environment configurations
│   ├── ci_config.json      # CI/QA/Dev settings
│   └── production_config.json
│
├── factories/               # Object factories
│   └── pages.py            # Page factory for lazy-loading
│
├── pages/                   # Page Object Models
│   ├── base_page.py        # Base page with common methods
│   ├── login_page.py       # Login page object
│   └── inventory_page.py   # Inventory page object
│
├── support/                 # Core infrastructure
│   └── environment.py      # Environment configuration class
│
├── tests/                   # Test suites
│   ├── test_login.py       # Login functionality tests
│   └── test_inventory.py   # Inventory page tests
│
├── users/                   # User management
│   └── users.py            # User credentials
│
├── utilities/               # Helper utilities
│   └── auth_helper.py      # Authentication helper
│
├── conftest.py             # pytest fixtures and configuration
├── pytest.ini              # pytest settings
├── requirements.txt        # Python dependencies
└── .env                    # Environment variables (NOT in repo!)
```

---

## 📄 License

This project is for demonstration and educational purposes.

---
