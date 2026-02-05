import json
from pathlib import Path
from users.users import CI_USERS, PRODUCTION_USERS


class Environment:
    """
    Environment configuration based on prefix (qa, ci, dev, production).
    Dynamically builds URLs based on env_prefix.

    Args:
        env_prefix: Environment prefix ('qa', 'ci', 'dev',, 'production')
        domain: Base domain (default: 'saucedemo.com')
    """

    def __init__(self, env_prefix: str, domain: str = "saucedemo.com"):
        self.prefix = env_prefix.lower()
        self.protocol = "https://"
        self.domain = f"{env_prefix}.{domain}"
        self.is_ci = self._is_ci_environment()
        self.base_url = self.set_base_url()
        self.users = self._get_automation_users()

    def _is_ci_environment(self) -> bool:
        """Check if environment is CI (qa, dev, ci)."""
        return self.prefix in ("qa", "dev", "ci")

    def _get_automation_users(self) -> dict:
        """Get users for current environment with validation."""
        users = CI_USERS if self.is_ci else PRODUCTION_USERS

        for user_key, user_data in users.items():
            if user_data.get("password") is None:
                raise ValueError(f"User '{user_key}' has None password. Check .env file and users/users.py")
        return users

    def set_base_url(self) -> str:
        """Build base URL dynamically based on env_prefix."""
        return f"{self.protocol}{self.domain}"

    @property
    def screenshots_on_failure(self) -> bool:
        """Check if screenshots on failure are enabled."""
        return self._config.get("screenshots_on_failure", True)



