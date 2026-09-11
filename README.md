# 🎭 Playwright Test Automation Framework

A production-ready test automation framework built with **Playwright** and **pytest**, demonstrating modern QA engineering practices for enterprise-level web application testing.

**Target Application:** [SauceDemo](https://www.saucedemo.com) - E-commerce demo site  
**Framework Type:** Hybrid (UI + Component-based)  
**CI/CD:** Dockerized with GitHub Actions integration  
**Reporting:** HTML reports with screenshots and video recordings

---

## 📋 Table of Contents

- [Framework Architecture](#-framework-architecture)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [Running Tests](#-running-tests)
- [Docker Support](#-docker-support)
- [CI/CD Integration](#-cicd-integration)
- [Test Reports](#-test-reports)
- [Framework Features](#-framework-features)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [Best Practices](#-best-practices)

---

## 🗺️ Framework Architecture

This framework implements a **layered architecture** with clear separation of concerns:
```
pytest-playwright-automation/
├── components/          # Reusable UI components (Header, Sidebar)
├── factories/           # Factory pattern for lazy-loading page objects
├── hardcoded_data/      # Test data (environment-specific)
├── pages/               # Page Object Model (POM) implementation
├── support/             # Core framework infrastructure
├── tests/               # Test suites organized by feature
├── users/               # User credential management
├── utilities/           # Helper utilities (AuthHelper)
├── .github/workflows/   # CI/CD pipelines
├── conftest.py          # Pytest configuration and fixtures
├── pytest.ini           # Pytest settings
├── Dockerfile           # Docker containerization
└── requirements.txt     # Python dependencies
```

### Design Patterns

✅ **Page Object Model (POM)** - Encapsulates page structure and interactions  
✅ **Factory Pattern** - Lazy-loads page objects for optimal resource usage  
✅ **Component Pattern** - Reusable UI components (Header, Sidebar) across multiple pages  
✅ **Environment Abstraction** - Multi-environment support with dynamic URL building  
✅ **Smart Authentication** - Cookie injection bypasses UI login for 10x faster test execution

---

## 🛠 Tech Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.12+ | Core language |
| **Playwright** | 1.58.0 | Browser automation |
| **pytest** | 9.0.2 | Test framework |
| **pytest-playwright** | 0.7.2 | Playwright-pytest integration |
| **pytest-html** | 4.2.0 | HTML report generation |
| **pytest-xdist** | 3.8.0 | Parallel test execution |
| **python-dotenv** | 1.2.1 | Environment variable management |
| **Docker** | Latest | Containerization |
| **GitHub Actions** | N/A | CI/CD automation |

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.12+** installed
- **pip** package manager
- **Git** for version control
- **Docker** (optional, for containerized execution)

### Installation
```bash
# 1. Clone repository
git clone <repository-url>
cd pytest-playwright-automation

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install Playwright browsers
playwright install chromium firefox
```

### Environment Setup

Create a `.env` file in the project root:
```env
CI_SAUCEDEMO_USER_PASSWORD=secret_sauce
PROD_SAUCEDEMO_USER_PASSWORD=secret_sauce
```

---

## 🎯 Running Tests

### Local Execution
```bash
# Run all tests (requires --env flag)
pytest --env=www --browser=chromium

# Run specific test file
pytest tests/test_login.py --env=www --browser=chromium

# Run with headed browser (visible)
pytest --env=www --browser=chromium --headed

# Run with different browsers
pytest --env=www --browser=firefox
```

### Test Filtering with Markers
```bash
# Run regression tests only
pytest -m regression --env=www --browser=chromium

# Run login tests only
pytest -m login --env=www --browser=chromium

# Run inventory tests only
pytest -m inventory --env=www --browser=chromium


```

### Parallel Execution
```bash
# Run tests in parallel (4 workers)
pytest --env=www --browser=chromium -n 4

# Auto-detect CPU cores
pytest --env=www --browser=chromium -n auto
```

### Environment Options
```bash
pytest --env=www         # https://www.saucedemo.com (production)
pytest --env=qa          # https://qa.saucedemo.com (dummy)
pytest --env=ci          # https://ci.saucedemo.com (dummy)
pytest --env=dev         # https://dev.saucedemo.com (dummy)
```

---

## 🐳 Docker Support

### Build Docker Image
```bash
docker build -t pytest-playwright-automation:latest .
```

### Run Tests in Docker
```bash
# Basic run with environment file
docker run --rm \
  --env-file .env \
  -v $(pwd)/reports:/app/reports \
  pytest-playwright-automation:latest \
  pytest tests/ --env=www --browser=chromium -v

# Run specific marker
docker run --rm \
  --env-file .env \
  -v $(pwd)/reports:/app/reports \
  pytest-playwright-automation:latest \
  pytest tests/ --env=www --browser=chromium -m regression -v

# Run with parallel workers
docker run --rm \
  --env-file .env \
  -v $(pwd)/reports:/app/reports \
  pytest-playwright-automation:latest \
  pytest tests/ --env=www --browser=chromium -n 4 -v
```

### Dockerfile

The Docker image is based on Playwright's official Python image with all browser dependencies pre-installed:
```dockerfile
FROM mcr.microsoft.com/playwright/python:v1.58.0-jammy

WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["pytest"]
```

---

## 🔄 CI/CD Integration

### GitHub Actions Workflows

The framework includes two automated workflows:

#### 1. **On-Demand Test Runs** (`on-demand-test-runs.yml`)

Manually triggered workflow with configurable parameters:

- **Environment:** www, qa, ci, dev (only www is real, behaves as domain prefix)
- **Test Marker:** regression, login, inventory
- **Browser:** chromium (default)
- **Workers:** 1 (configurable)

**Trigger:** Manual via GitHub Actions UI

#### 2. **Regression Tests** (`cd.yml`)

Automated regression testing on code changes:

- **Environment:** www (production)
- **Browser:** chromium
- **Marker:** regression
- **Workers:** 1

**Trigger:** Push to `main` branch

### Reusable Workflow (`_test_logic.yml`)

Shared test execution logic used by both workflows:

- Docker image caching for faster builds
- Automated test execution
- Report generation and artifact upload
- GitHub Pages deployment
- Test result summary in workflow logs


Reports include:
- ✅ Test execution summary
- ✅ Screenshots (saved as PNG, linked for failed tests)
- ✅ Video recordings (linked for failed tests)
- ✅ Execution logs and metadata

---

## 📊 Test Reports

### HTML Reports

Test reports are automatically generated using `pytest-html` with the following features:

**Screenshots:**
- Captured automatically on test failure
- Saved to `reports/test-results/{test-name}/screenshot.png`
- Linked in HTML report for easy access

**Videos:**
- Recorded only for failed tests (`--video=retain-on-failure`)
- Saved to `reports/test-results/{test-name}/video.webm`
- Linked in HTML report for easy access
- Clickable "🔴 Video Recording" link in test results

**Traces:**
- Only appear if the run was launched with `--tracing=on` or `--tracing=retain-on-failure` (this is a plain pytest-playwright flag — nothing extra to configure), and only for tests that actually failed
- A failed test with a trace gets an expandable "🔍 Trace Summary" in the report: the failed Playwright action (if any) and its error, a compact action timeline, any console errors, and any failed (4xx/5xx) network requests
- The raw `trace.zip` is still saved to `reports/test-results/{test-name}/trace.zip` (not linked from the report) for a full timeline/DOM-snapshot/network deep-dive — open it with `playwright show-trace path/to/trace.zip`, or drag it into https://trace.playwright.dev (processes the file locally in your browser; it's not uploaded anywhere, worth knowing since traces can contain cookies/tokens from captured requests)

**Report Location:**
```
reports/
├── report.html              # Main HTML report
└── test-results/            # Screenshot/video/trace artifacts
    └── {test-name}/
        ├── screenshot.png
        ├── video.webm
        └── trace.zip
```

### Viewing Reports Locally
```bash
# After test execution
open reports/report.html
```

### CI/CD Reports

Reports are automatically deployed to GitHub Pages and accessible at:
```
https://<username>.github.io/<repo>/report.html
```

---

## ✨ Framework Features

### 1. **Page Object Model (POM)**

Clean separation of page structure from test logic:
```python
class LoginPage(BasePage):
    PATH = "/"
    
    def __init__(self, page, env):
        super().__init__(page, env)
        self.username_input = page.get_by_test_id("username")
        self.password_input = page.get_by_test_id("password")
        self.login_button = page.get_by_test_id("login-button")
    
    def perform_login(self, user: str):
        """Full UI login flow."""
        credentials = self._env.users[user]
        self.username_input.fill(credentials["username"])
        self.password_input.fill(credentials["password"])
        self.login_button.click()
```

### 2. **Factory Pattern**

Lazy-loading page objects for optimal memory management:
```python
class PageFactory:
    """Factory for lazy-loading page objects."""
    
    @property
    def login(self) -> LoginPage:
        if 'login' not in self._pages_cache:
            self._pages_cache['login'] = LoginPage(self._page, self._env)
        return self._pages_cache['login']
    
    @property
    def inventory(self) -> InventoryPage:
        if 'inventory' not in self._pages_cache:
            self._pages_cache['inventory'] = InventoryPage(self._page, self._env)
        return self._pages_cache['inventory']
```

**Benefits:**
- Pages created only when needed
- Single instance per test (caching)
- Clean test code with simple `pages.login` access

### 3. **Component Pattern**

Reusable UI components shared across multiple pages:
```python
class Header:
    """Header component - appears on all authenticated pages."""
    
    def __init__(self, page: Page):
        self.logo = page.get_by_text("Swag Labs")
        self.shopping_cart_button = page.get_by_test_id("shopping-cart-link")
        self.shopping_cart_badge = page.get_by_test_id("shopping-cart-badge")
        self.sidebar_menu_button = page.get_by_role("button", name="Open Menu")
    
    def get_cart_item_count(self) -> int:
        if self.shopping_cart_badge.is_visible():
            return int(self.shopping_cart_badge.text_content())
        return 0
```

**Components:**
- `Header` - Logo, cart, menu button (used across inventory, cart, checkout pages)
- `SidebarMenu` - Navigation menu (logout, about, reset app)

### 4. **Smart Authentication**

Cookie injection to bypass UI login for 10x faster test execution:
```python
# Fast authentication (cookie injection)
pages.authenticate(user="standard_user")
pages.inventory.navigate()

# Full UI login (for testing login functionality)
pages.login.navigate()
pages.login.perform_login(user="standard_user")
```

**How it works:**
1. First login creates session cookie
2. Cookie cached in memory (session-scoped)
3. Subsequent tests reuse cached cookie
4. No UI interaction needed

### 5. **Environment Management**

Dynamic URL construction based on environment:
```python
class Environment:
    def __init__(self, env_prefix: str, domain: str = "saucedemo.com"):
        self.prefix = env_prefix.lower()
        self.domain = f"{env_prefix}.{domain}"
        self.base_url = self.set_base_url()
        self.users = self._get_automation_users()
    
    def set_base_url(self) -> str:
        """Build base URL dynamically."""
        return f"{self.protocol}{self.domain}"
```

**Supported Environments:**
- `www` → `https://www.saucedemo.com`
- `qa` → `https://qa.saucedemo.com`
- `ci` → `https://ci.saucedemo.com`
- `dev` → `https://dev.saucedemo.com`

### 6. **Hardcoded Test Data**

Environment-specific test data loaded dynamically:

**Production Data** (`hardcoded_data/production.json`):
```json
{
  "inventory": {
    "item_1": "Sauce Labs Backpack",
    "item_2": "Sauce Labs Bike Light",
    "item_3": "Sauce Labs Bolt T-Shirt"
  }
}
```

**CI Data** (`hardcoded_data/ci.json`):
```json
{
  "inventory": {
    "item_1": "CI Fake Item",
    "item_2": "CI Fake Backpack"
  }
}
```

**Usage in tests:**
```python
def test_product_validation(self, pages, data):
    product_name = data["inventory"]["item_1"]
    # Use dynamic product name from environment-specific data
```

---

## 📁 Project Structure
```
pytest-playwright-automation/
│
├── .github/workflows/           # CI/CD pipelines
│   ├── on-demand-test-runs.yml  # Manual test execution
│   ├── cd.yml                   # Automated regression tests
│   └── _test_logic.yml          # Reusable workflow logic
│
├── components/                  # Reusable UI components
│   ├── header.py                # Header component (cart, menu, logo)
│   └── sidebar_menu.py          # Sidebar navigation component
│
├── factories/                   # Object factories
│   └── pages.py                 # PageFactory for lazy-loading
│
├── hardcoded_data/              # Test data (environment-specific)
│   ├── ci.json                  # CI environment test data
│   └── production.json          # Production environment test data
│
├── pages/                       # Page Object Model
│   ├── base_page.py             # Base page with common functionality
│   ├── login_page.py            # Login page object
│   └── inventory_page.py        # Inventory/products page object
│
├── support/                     # Core framework infrastructure
│   └── environment.py           # Environment configuration
│
├── tests/                       # Test suites
│   ├── test_login.py            # Login functionality tests
│   └── test_inventory.py        # Inventory page tests
│
├── users/                       # User credential management
│   └── users.py                 # User definitions (CI vs Production)
│
├── utilities/                   # Helper utilities
│   └── auth_helper.py           # Authentication via cookie injection
│
├── reports/                     # Generated test reports (gitignored)
│   ├── report.html              # HTML test report
│   └── test-results/            # Video recordings
│
├── .dockerignore                # Docker ignore patterns
├── .env                         # Environment variables (demo only!)
├── .gitignore                   # Git ignore patterns
├── conftest.py                  # Pytest fixtures and configuration
├── Dockerfile                   # Docker containerization
├── pytest.ini                   # Pytest settings
├── README.md                    # This file
└── requirements.txt             # Python dependencies
```

---

## ⚙️ Configuration

### pytest.ini
```ini
[pytest]
addopts =
    --html=reports/report.html
    --self-contained-html
    --capture=tee-sys
    --video=retain-on-failure
    --output=reports/test-results
    -v

markers =
    regression: Regression tests
    login: Login functionality tests
    inventory: Inventory page tests
```

### conftest.py

Key fixtures provided:

- `pages` - Main test fixture providing access to all page objects
- `env` - Environment configuration (URLs, users, settings)
- `data` - Hardcoded test data (environment-specific)
- `auth_state_cache` - Session-scoped authentication cache
- `browser_type_launch_args` - Custom browser launch arguments
- `browser_context_args` - Browser context configuration (viewport, etc.)

---

## 📝 Writing Tests

### Example Test
```python
import pytest
from playwright.sync_api import expect

@pytest.mark.inventory
class TestInventoryPage:
    
    @pytest.fixture(autouse=True)
    def setup(self, pages):
        """Authenticate and navigate before each test."""
        pages.authenticate(user="standard_user")
        pages.inventory.navigate()
    
    @pytest.mark.regression
    def test_all_products_have_required_elements(self, pages, data):
        """Verify each product has required elements."""
        expected_products = [data["inventory"][key] for key in data["inventory"]]
        product_count = pages.inventory.get_product_count()
        assert product_count == 6
        
        for product_name in expected_products:
            product_card = pages.inventory.get_product_card(product_name)
            expect(product_card.locator(pages.inventory.item_name)).to_have_text(product_name)
            expect(product_card.locator(pages.inventory.item_img)).to_be_visible()

```

### Test Organization

Tests are organized by feature:

- `test_login.py` - Login functionality (UI login, logout, error messages)
- `test_inventory.py` - Product catalog (product validation, cart operations)

### Available Markers
```python
@pytest.mark.regression  # Comprehensive regression suite
@pytest.mark.login       # Login-specific tests
@pytest.mark.inventory   # Inventory-specific tests
```

---

## 🎓 Best Practices

### Locator Strategy

✅ **Prefer:** `get_by_test_id()`, `get_by_role()`, `get_by_label()`  
❌ **Avoid:** CSS selectors, XPath (brittle, implementation-dependent)
```python
# Good
self.username = page.get_by_test_id("username")
self.submit = page.get_by_role("button", name="Submit")

# Bad
self.username = page.locator("#user-name")
self.submit = page.locator("//button[@id='login-button']")
```

### Authentication Strategy

✅ **Use `pages.authenticate()`** for non-login tests (10x faster)  
✅ **Use `pages.login.perform_login()`** only for testing login functionality
```python
# Fast (cookie injection) - for most tests
pages.authenticate(user="standard_user")
pages.inventory.navigate()

# Slow (UI login) - only for login tests
pages.login.navigate()
pages.login.perform_login(user="standard_user")
```

### Test Independence

✅ Each test should be independent and isolated  
✅ Use fixtures for setup/teardown  
✅ Don't rely on test execution order  
✅ Clean up test data after execution

### Parallel Execution

✅ Run tests in parallel for faster CI/CD: `pytest -n auto`  
✅ Ensure tests are thread-safe (no shared state)  
✅ Use session-scoped fixtures sparingly

### Hardcoded Data

✅ Use environment-specific test data from JSON files  
✅ Keep test data separate from test logic  
✅ Use descriptive keys: `data["inventory"]["item_1"]`

---

## 🔧 Troubleshooting

### Common Issues

**Error:** `--env is required`  
**Solution:** Always specify environment: `pytest --env=www --browser=chromium`

**Error:** Browser not found  
**Solution:** Install browsers: `playwright install chromium firefox`

**Error:** Authentication fails  
**Solution:** 
1. Check `.env` file has correct passwords
2. Ensure no quotes around passwords in `.env`
3. Verify user exists in `users/users.py`

**Error:** Tests timeout  
**Solution:** 
1. Run with `--headed` to debug visually
2. Check network connectivity
3. Verify target environment is accessible

**Error:** Docker tests fail but local tests pass  
**Solution:**
1. Verify `.env` file is passed correctly: `--env-file .env`
2. Check passwords don't have quotes in `.env`
3. Ensure Docker has network access

---


## 📄 License

This project is for educational and demonstration purposes.

---
