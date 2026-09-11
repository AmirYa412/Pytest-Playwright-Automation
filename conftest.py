import os
import json
import pytest
from pathlib import Path
from factories.pages import PageFactory
from logger import LoggerFactory
from support.environment import Environment
from support.trace_report import build_trace_summary_html


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


@pytest.fixture(scope="session", autouse=True)
def logger():
    """Session-scoped logger."""
    return LoggerFactory(project="gui")


@pytest.fixture(scope="function", autouse=True)
def log_test_execution(request, logger):
    """Log test start and end automatically."""
    test_name = request.node.name
    logger.info(f"*** TEST {test_name} STARTING")
    yield  # Test runs here
    logger.info(f"*** TEST {test_name} ENDED")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extras', [])
    # .absolute() (not .resolve()) to match how pytest-playwright's own output_path
    # fixture normalizes --output - keeps both paths comparable if either lives under a
    # symlink (e.g. macOS /tmp -> /private/tmp).
    report_dir = Path(item.config.getoption("--html")).absolute().parent

    if report.when == 'call':
        page = item.funcargs.get("page")
        output_path = item.funcargs.get("output_path")
        if report.failed and page and output_path:
            test_results_dir = Path(output_path)
            screenshot_path = test_results_dir / "screenshot.png"
            page.screenshot(path=str(screenshot_path))  # creates test_results_dir if needed
            rel_dir = os.path.relpath(test_results_dir, report_dir)
            # File path, not base64: keeps pytest-html's normal image viewer/styling and
            # avoids window.open(data:...), which browsers block as a top-level navigation.
            extra.append(pytest_html.extras.image(f"{rel_dir}/screenshot.png"))

    if report.when == 'teardown':
        # video/trace are only written to disk during fixture teardown; output_path is
        # pytest-playwright's own fixture for that artifact directory.
        output_path = item.funcargs.get("output_path")
        if output_path:
            test_results_dir = Path(output_path)
            rel_dir = os.path.relpath(test_results_dir, report_dir)

            video_path = test_results_dir / "video.webm"
            if video_path.exists():
                extra.append(pytest_html.extras.url(f"{rel_dir}/video.webm", name="🔴 Video Recording"))

            # rep_call, stashed by pytest-playwright, holds the test's real pass/fail outcome.
            test_failed = getattr(item, "rep_call", None) is not None and item.rep_call.failed
            trace_path = test_results_dir / "trace.zip"
            if test_failed and trace_path.exists():
                try:
                    extra.append(pytest_html.extras.html(build_trace_summary_html(trace_path)))
                except Exception as e:
                    print(f"Error parsing trace.zip for report: {e}")

    report.extras = extra
