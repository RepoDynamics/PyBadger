from typing import Literal as _Literal
import pylinks as _pylinks

from pybadger import BadgeSettings as _BadgeSettings, Badge as _Badge
from pybadger import shields as _shields
from pybadger.shields.badge import ShieldsBadger as _ShieldsBadger


class LibrariesIO(_ShieldsBadger):
    """Shields.io Libraries.io badges.

    References
    ----------
    - [Libraries.io](https://libraries.io/)
    """

    def __init__(
        self,
        platform: str,
        package: str,
        scope: str | None = None,
        default_shields_settings: _shields.ShieldsSettings | None = None,
        default_badge_settings: _BadgeSettings | None = None,
    ):
        """
        Parameters
        ----------
        platform : str, default: 'pypi'
            Name of the platform where the package is distributed, e.g. 'pypi', 'npm', etc.
        package : str
            Name of the package.
        scope : str, optional
            The scope of the npm package, e.g., `@babel`.
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
            endpoint_start="librariesio",
            endpoint_key=f"{platform}/{scope}/{package}" if scope else f"{platform}/{package}",
            default_shields_settings=default_shields_settings,
            default_badge_settings=default_badge_settings,
        )
        self._link = _pylinks.site.lib_io.package(platform=platform, package=package)
        return

    def dependency_status(
        self,
        version: str | None = None,
        shields_settings: _shields.ShieldsSettings | None = None,
        badge_settings: _BadgeSettings | None = None,
    ) -> _Badge:
        """Dependency status.

        Paramaters
        ----------
        version : str, optional
            A specific version to query.
        shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default instance settings.
        badge_settings : pybadger.BadgeSettings, optional
            Settings for the badge to override the default instance settings.

        Notes
        -----
        - The right-hand text shows either 'up to date', or '{number} out of date'.

        References
        ----------
        - [Shields.io API - Libraries.io dependency status for latest release](https://shields.io/badges/libraries-io-dependency-status-for-latest-release)
        - [Shields.io API - Libraries.io dependency status for specific release](https://shields.io/badges/libraries-io-dependency-status-for-specific-release)
        """
        return _shields.create(
            path=self._create_path(["release"], [version] if version else []),
            shields_settings=self._shields_settings(shields_settings) + _shields.ShieldsSettings(
                label="Dependencies",
            ),
            badge_settings=self._badge_settings(badge_settings) + _BadgeSettings(
                title="Status of the project's dependencies.",
                alt="Dependency Status",
                link=self._link.dependencies(version=version) if version else self._link.homepage,
            ),
        )

    def dependents(
        self,
        repo: bool = False,
        shields_settings: _shields.ShieldsSettings | None = None,
        badge_settings: _BadgeSettings | None = None,
    ) -> _Badge:
        """
        Number of packages or repositories that depend on this package.

        Parameters
        ----------
        repo : bool, default: False
            Whether to query repositories (True) or packages (False).
        shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default instance settings.
        badge_settings : pybadger.BadgeSettings, optional
            Settings for the badge to override the default instance settings.

        References
        ----------
        - [Shields.io API - Dependent repos (via Libraries.io)](https://shields.io/badges/dependent-repos-via-libraries-io)
        - [Shields.io API - Dependent repos (via Libraries.io), scoped npm package](https://shields.io/badges/dependent-repos-via-libraries-io-scoped-npm-package)
        - [Shields.io API - Dependents (via Libraries.io)](https://shields.io/badges/dependents-via-libraries-io)
        - [Shields.io API - Dependents (via Libraries.io), scoped npm package](https://shields.io/badges/dependents-via-libraries-io-scoped-npm-package)
        """
        return _shields.create(
            path=self._create_path(["dependent-repos" if repo else "dependents"], []),
            shields_settings=self._shields_settings(shields_settings) + _shields.ShieldsSettings(
                label="Dependents",
            ),
            badge_settings=self._badge_settings(badge_settings) + _BadgeSettings(
                title=f"Number of {'repositories' if repo else 'packages'} that depend on us.",
                alt="Dependents",
                link=self._link.homepage,
            ),
        )

    def source_rank(
        self,
        shields_settings: _shields.ShieldsSettings | None = None,
        badge_settings: _BadgeSettings | None = None,
    ) -> _Badge:
        """SourceRank ranking of the package.

        Parameters
        ----------
        shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default instance settings.
        badge_settings : pybadger.BadgeSettings, optional
            Settings for the badge to override the default instance settings.

        References
        ----------
        - [Shields.io API - Libraries.io SourceRank](https://shields.io/badges/libraries-io-source-rank)
        """
        return _shields.create(
            path=self._create_path(["sourcerank"], []),
            shields_settings=self._shields_settings(shields_settings) + _shields.ShieldsSettings(
                label="SourceRank",
            ),
            badge_settings=self._badge_settings(badge_settings) + _BadgeSettings(
                title=(
                    "Ranking of the source code according to libraries.io SourceRank algorithm. "
                    "Click to see more details on libraries.io website."
                ),
                alt="SourceRank",
                link=self._link.source_rank,
            ),
        )
