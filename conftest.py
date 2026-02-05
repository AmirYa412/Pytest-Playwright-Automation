import re
import json
import pytest
import base64
from pathlib import Path
from factories.pages import PageFactory
from support.environment import Environment


PROJECT_ROOT = Path(__file__).parent.resolve()

def pytest_addoption(parser):
    """Add custom CLI options (only --env, pytest-playwright handles browser)."""
    parser.addoption("--env", action="store", default=None, help="Environment [qa, ci, dev, production, www]")


@pytest.fixture(scope="session", autouse=True)
def configure_playwright(playwright):
    # Sauce demo website uses data-test and not data-testid
    playwright.selectors.set_test_id_attribute("data-test")


@pytest.fixture(scope="session")
def env(request):
    """Get environment from CLI - REQUIRED."""
    env_prefix = request.config.getoption("--env")
    if not env_prefix:
        raise EnvironmentError("--env is required. Supports: --env=qa|ci|dev|www")
    return Environment(env_prefix)


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """
    Override pytest-playwright's browser launch arguments.
    These apply to ALL browsers (chromium, firefox, webkit).
    """
    return {
        **browser_type_launch_args,
        # Common automation args
        "args": [
            "--disable-blink-features=AutomationControlled",  # Hide automation flags
            "--disable-dev-shm-usage",  # Overcome limited resource problems in CI
            "--no-sandbox",  # Required for running as root in Docker
        ],
        # Slow down operations for debugging (0 = normal speed)
        "slow_mo": 0
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    Override viewport and other context-level settings globally.
    This is cleaner than a JSON config because it applies natively.
    """
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
    }


@pytest.fixture(scope="session")
def auth_state_cache():
    """Session-scoped auth state cache."""
    return {}


@pytest.fixture
def pages(page, env, auth_state_cache):
    """
    Main fixture - tests only need this.
    Uses pytest-playwright's page fixture under the hood.
    """
    return PageFactory(page, env, auth_state_cache)


@pytest.fixture(scope="session")
def data(env):
    hardcoded_filename = "production.json"
    if env.is_ci:
        hardcoded_filename = "ci.json"
    file_path = Path(PROJECT_ROOT) / "hardcoded_data" / hardcoded_filename
    with open(file_path, 'r') as f:
        return json.load(f)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call':
        page = item.funcargs.get("page")
        if report.failed and page:
            screenshot_bytes = page.screenshot()
            screenshot_base64 = base64.b64encode(screenshot_bytes).decode('utf-8')
            extra.append(pytest_html.extras.image(screenshot_base64))
            slug = re.sub(r'[^a-zA-Z0-9]', '-', item.nodeid)
            test_slug = re.sub(r'-+', '-', slug).lower().strip('-')

            # 2. Define the path relative to report.html
            # Structure: reports/report.html -> reports/test-results/test-slug/video.webm
            video_rel_path = f"test-results/{test_slug}/video.webm"

            # 3. Add as a simple clickable link
            # 'extra.url' creates a standard link in the 'Extra' column
            extra.append(pytest_html.extras.url(video_rel_path, name="🔴 Video Recording"))

    report.extra = extra