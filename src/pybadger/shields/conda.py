from typing import Literal as _Literal

import pylinks as _pylinks

from pybadger import BadgeSettings as _BadgeSettings, Badge as _Badge
from pybadger import shields as _shields
from pybadger.shields.badge import ShieldsBadger as _ShieldsBadger


class Conda(_ShieldsBadger):
    """Shields.io Conda badges."""

    def __init__(
        self,
        package: str,
        channel: str = "conda-forge",
        default_shields_settings: _shields.ShieldsSettings | None = None,
        default_badge_settings: _BadgeSettings | None = None,
    ):
        """
        Parameters
        ----------
        package : str
            Package name.
        channel : str, default: 'conda-forge'
            Channel name.
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
            endpoint_start="conda",
            endpoint_key=f"{channel}/{package}",
            default_shields_settings=default_shields_settings,
            default_badge_settings=default_badge_settings,
        )
        self._link = _pylinks.site.conda.package(name=package, channel=channel)
        return

    def downloads(
        self,
        shields_settings: _shields.ShieldsSettings | None = None,
        badge_settings: _BadgeSettings | None = None,
    ) -> _Badge:
        """Number of total downloads.

        Parameters
        ----------
        shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default instance settings.
        badge_settings : pybadger.BadgeSettings, optional
            Settings for the badge to override the default instance settings.

        References
        ----------
        [Shields.io API - Conda Downloads](https://shields.io/badges/conda-downloads)
        """
        return _shields.create(
            path=self._create_path(["d"], []),
            shields_settings=self._shields_settings(shields_settings) + _shields.ShieldsSettings(
                label="Conda Downloads",
            ),
            badge_settings=self._badge_settings(badge_settings) + _BadgeSettings(
                title="Number of downloads for the Conda distribution.",
                alt="Conda Downloads",
                link=self._link.homepage,
            ),
        )

    def license(
        self,
        shields_settings: _shields.ShieldsSettings | None = None,
        badge_settings: _BadgeSettings | None = None,
    ) -> _Badge:
        """Package license.

        Parameters
        ----------
        shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default instance settings.
        badge_settings : pybadger.BadgeSettings, optional
            Settings for the badge to override the default instance settings.

        References
        ----------
        [Shields.io API - Conda License](https://shields.io/badges/conda-license)
        """
        return _shields.create(
            path=self._create_path(["l"], []),
            shields_settings=self._shields_settings(shields_settings) + _shields.ShieldsSettings(label="License"),
            badge_settings=self._badge_settings(badge_settings) + _BadgeSettings(
                title="Package license",
                alt="Package License",
                link=self._link.homepage,
            ),
        )

    def supported_platforms(
        self,
        shields_settings: _shields.ShieldsSettings | None = None,
        badge_settings: _BadgeSettings | None = None,
    ) -> _Badge:
        """Supported platforms.

        Parameters
        ----------
        shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default instance settings.
        badge_settings : pybadger.BadgeSettings, optional
            Settings for the badge to override the default instance settings.

        References
        ----------
        [Shields.io API - Conda Platform](https://shields.io/badges/conda-platform)
        """
        return _shields.create(
            path=self._create_path(["p"], []),
            shields_settings=self._shields_settings(shields_settings) + _shields.ShieldsSettings(
                label="Supported Platforms"),
            badge_settings=self._badge_settings(badge_settings) + _BadgeSettings(
                title="Supported platforms",
                alt="Supported Platforms",
                link=self._link.homepage,
            ),
        )

    def version(
        self,
        shields_settings: _shields.ShieldsSettings | None = None,
        badge_settings: _BadgeSettings | None = None,
    ) -> _Badge:
        """Package version.

        Parameters
        ----------
        shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default instance settings.
        badge_settings : pybadger.BadgeSettings, optional
            Settings for the badge to override the default instance settings.

        References
        ----------
        [Shields.io API - Conda Version](https://shields.io/badges/conda-version)
        """
        return _shields.create(
            path=self._create_path(["v"], []),
            shields_settings=self._shields_settings(shields_settings) + _shields.ShieldsSettings(label="Version"),
            badge_settings=self._badge_settings(badge_settings) + _BadgeSettings(
                title="Package version",
                alt="Package Version",
                link=self._link.homepage,
            ),
        )
