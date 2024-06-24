from typing import Literal as _Literal

from pybadger import BadgeSettings as _BadgeSettings, Badge as _Badge
from pybadger import shields as _shields
from pybadger.shields.badge import ShieldsBadger as _ShieldsBadger


class CodeCov(_ShieldsBadger):
    """Shields.io CodeCov badges."""

    def __init__(
        self,
        vcs_name: _Literal["github", "gh", "gitlab", "gl", "bitbucket", "bb"],
        user: str,
        repo: str,
        token: str | None = None,
        default_shields_settings: _shields.ShieldsSettings | None = None,
        default_badge_settings: _BadgeSettings | None = None,
    ):
        """
        Parameters
        ----------
        vcs_name : {'github', 'gh', 'gitlab', 'gl', 'bitbucket', 'bb'}
            The name of the version control system hosting the repository.
        user : str
            The username of the repository owner.
        repo : str
            The name of the repository.
        token : str, optional
            The token to authenticate with the CodeCov API for private repositories.
            You can find the token under the badge section of your project settings page at:
            https://codecov.io/[vcsName]/[user]/[repo]/settings/badge.
        default_shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default global settings.
            These will be used as default values for all badges,
            unless the same argument is also provided to the method when creating a specific badge.
        default_badge_settings : pybadger.BadgeSettings, optional
            Settings for the badge to override the default global settings.
            These will be used as default values for all badges,
            unless the same argument is also provided to the method when creating a specific badge.
        """
        super().__init__(
            endpoint_start="codecov/c",
            endpoint_key=f"{vcs_name}/{user}/{repo}",
            default_shields_settings=default_shields_settings,
            default_badge_settings=default_badge_settings,
        )
        self.vcs_name = vcs_name
        self.user = user
        self.repo = repo
        self.token = token
        abbr = {"github": "gh", "gitlab": "gl", "bitbucket": "bb"}
        self._link = f"https://codecov.io/{abbr[vcs_name]}/{user}/{repo}"
        return

    def coverage(
        self,
        flag: str | None = None,
        branch: str | None = None,
        shields_settings: _shields.ShieldsSettings | None = None,
        badge_settings: _BadgeSettings | None = None,
    ) -> _Badge:
        """Code coverage.

        Parameters
        ----------
        flag : str, optional
            A specific flag to query.
        branch : str, optional
            Name of a specific branch to query.
        shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default instance settings.
        badge_settings : pybadger.BadgeSettings, optional
            Settings for the badge to override the default instance settings.

        References
        ----------
        [Shields.io API - Codecov](https://shields.io/badges/codecov)
        [Shields.io API - Codecov (with branch)](https://shields.io/badges/codecov-with-branch)
        """
        return _shields.create(
            path=self._create_path([], [branch] if branch else []),
            queries={"token": self.token, "flag": flag},
            shields_settings=self._shields_settings(shields_settings) + _shields.ShieldsSettings(
                label="Test Coverage", logo="codecov",
            ),
            badge_settings=self._badge_settings(badge_settings) + _BadgeSettings(
                title="Source code coverage by the test suite. Click to see more details on codecov.io.",
                alt="Test Coverage",
                link=self._link + f"/branch/{branch}" if branch else ''
            ),
        )
