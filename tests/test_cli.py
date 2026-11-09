"""
Unit tests for CLI utilities and dynamic username resolution.
"""

import os
import unittest
from unittest.mock import patch
from drago.cli import resolve_username

class TestUsernameResolution(unittest.TestCase):
    def setUp(self):
        self.orig_env = os.environ.copy()

    def tearDown(self):
        os.environ.clear()
        os.environ.update(self.orig_env)

    def test_explicit_cli_argument(self):
        user, src = resolve_username(args_username="AnuragTummapudi", config_username="Deepak-Kambala")
        self.assertEqual(user, "AnuragTummapudi")
        self.assertIn("CLI argument", src)

    def test_target_user_env_var(self):
        os.environ["TARGET_USER"] = "AnuragTummapudi"
        user, src = resolve_username(args_username="", config_username="")
        self.assertEqual(user, "AnuragTummapudi")
        self.assertIn("TARGET_USER", src)

    def test_github_repository_owner_env_var(self):
        os.environ.pop("TARGET_USER", None)
        os.environ["GITHUB_REPOSITORY_OWNER"] = "AnuragTummapudi"
        user, src = resolve_username(args_username="", config_username="")
        self.assertEqual(user, "AnuragTummapudi")
        self.assertIn("GITHUB_REPOSITORY_OWNER", src)

    def test_github_repository_env_var(self):
        os.environ.pop("TARGET_USER", None)
        os.environ.pop("GITHUB_REPOSITORY_OWNER", None)
        os.environ["GITHUB_REPOSITORY"] = "AnuragTummapudi/drago"
        user, src = resolve_username(args_username="", config_username="")
        self.assertEqual(user, "AnuragTummapudi")
        self.assertIn("GITHUB_REPOSITORY", src)

    def test_config_username_valid(self):
        os.environ.pop("TARGET_USER", None)
        os.environ.pop("GITHUB_REPOSITORY_OWNER", None)
        os.environ.pop("GITHUB_REPOSITORY", None)
        user, src = resolve_username(args_username=None, config_username="custom-dev")
        self.assertEqual(user, "custom-dev")
        self.assertIn("drago.config.json", src)

    def test_config_username_ignores_placeholders(self):
        os.environ.pop("TARGET_USER", None)
        os.environ.pop("GITHUB_REPOSITORY_OWNER", None)
        os.environ.pop("GITHUB_REPOSITORY", None)
        # Should ignore octocat, your_username, placeholder, empty string
        for placeholder in ["octocat", "your_username", "placeholder", ""]:
            with patch("subprocess.check_output", side_effect=Exception("no git")):
                user, _ = resolve_username(args_username="", config_username=placeholder)
                self.assertIsNone(user)

    def test_git_remote_fallback(self):
        os.environ.pop("TARGET_USER", None)
        os.environ.pop("GITHUB_REPOSITORY_OWNER", None)
        os.environ.pop("GITHUB_REPOSITORY", None)
        with patch("subprocess.check_output", return_value="https://github.com/TestOwner/drago.git\n"):
            user, src = resolve_username(args_username="", config_username="")
            self.assertEqual(user, "TestOwner")
            self.assertIn("git remote origin URL", src)

if __name__ == "__main__":
    unittest.main()

