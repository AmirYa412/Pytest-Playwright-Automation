import pytest
from factories.pages import PageFactory
from support.environment import Environment


def pytest_addoption(parser):
    """Add custom CLI options (only --env, pytest-playwright handles browser)."""
    parser.addoption(
        "--env", action="store", default=None, help="Environment [qa, ci, dev, production, www]")


@pytest.fixture(scope="session")
def env(request):
    """Get environment from CLI - REQUIRED."""
    env_prefix = request.config.getoption("--env")
    if not env_prefix:
        raise EnvironmentError("--env is required. Supports: --env=qa|ci|dev|production|www")
    return Environment(env_prefix)


@pytest.fixture(scope="session")
def browser_context_args(env):
    """
    Override pytest-playwright's browser_context_args.
    This applies our viewport and other context settings if needed.
    """
    return {
        "viewport": env.viewport,
        "ignore_https_errors": True,
    }


@pytest.fixture(scope="session")
def auth_state_cache():
    """Session-scoped auth state cache."""
    return {}


@pytest.fixture
def pages(page, env, auth_state_cache) -> PageFactory:
    """
    Main fixture - tests only need this.
    Uses pytest-playwright's page fixture under the hood.
    """
    return PageFactory(page, env, auth_state_cache)