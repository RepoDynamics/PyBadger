from typing import Literal as _Literal
import pylinks as _pylinks

from pybadger import BadgeSettings as _BadgeSettings, Badge as _Badge
from pybadger import shields as _shields
from pybadger.shields.badge import ShieldsBadger as _ShieldsBadger


class PyPI(_ShieldsBadger):
    """Shields.io PyPI badges."""

    def __init__(
        self,
        package: str,
        pypi_base_url: str = "https://pypi.org",
        default_shields_settings: _shields.ShieldsSettings | None = None,
        default_badge_settings: _BadgeSettings | None = None,
    ):
        """
        Parameters
        ----------
        package : str
            Name of the package.
        pypi_base_url : str, default: 'https://pypi.org'
            Base URL of the PyPI website.
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
            endpoint_start="pypi",
            endpoint_key=package,
            default_shields_settings=default_shields_settings,
            default_badge_settings=default_badge_settings,
        )
        self.package = package
        self._pypi_base_url = pypi_base_url
        self._link = _pylinks.site.pypi.package(name=package)
        return

    def downloads(
        self,
        period: _Literal["t", "m", "w", "d"] = "t",
        shields_settings: _shields.ShieldsSettings | None = None,
        badge_settings: _BadgeSettings | None = None,
    ) -> _Badge:
        """Number of downloads.

        Parameters
        ----------
        period : {'t', 'm', 'w', 'd'}, default: 't'
            Period to display the number of downloads.
            - 't': Total
            - 'm': Monthly
            - 'w': Weekly
            - 'd': Daily
        shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default instance settings.
        badge_settings : pybadger.BadgeSettings, optional
            Settings for the badge to override the default instance settings.

        References
        ----------
        [Shields.io API - PyPI Downloads](https://shields.io/badges/py-pi-downloads)
        [Shields.io API - Pepy Total Downloads](https://shields.io/badges/pepy-total-downlods)
        """
        period_name = {"d": "day", "w": "week", "m": "month"}
        return _shields.create(
            path=f"pepy/dt/{self.package}" if period == "t" else self._create_path(before=[f"d{period}"], after=[]),
            shields_settings=self._shields_settings(shields_settings) + _shields.ShieldsSettings(
                label="Downloads", logo="pypi",
            ),
            badge_settings=self._badge_settings(badge_settings) + _BadgeSettings(
                title=(
                    f"{'Total number' if period == 't' else 'Number'} of downloads "
                    f"of all releases from PyPI{f', per {period_name[period]}' if period != 't' else ''}. "
                    f"Click to see more details on pypi.org."
                ),
                alt="PyPI Downloads",
                link=f"https://pepy.tech/projects/{self.package}",
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
        [Shields.io API - PyPI License](https://shields.io/badges/py-pi-license)
        """
        return _shields.create(
            path=self._create_path(["l"], []),
            queries={"pypiBaseUrl": self._pypi_base_url},
            shields_settings=self._shields_settings(shields_settings) + _shields.ShieldsSettings(
                label="License",
            ),
            badge_settings=self._badge_settings(badge_settings) + _BadgeSettings(
                title="Package license",
                alt="Package License",
                link=self._link.homepage
            ),
        )

    def distribution_format(
        self,
        shields_settings: _shields.ShieldsSettings | None = None,
        badge_settings: _BadgeSettings | None = None,
    ) -> _Badge:
        """Format of the distribution package.

        Parameters
        ----------
        shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default instance settings.
        badge_settings : pybadger.BadgeSettings, optional
            Settings for the badge to override the default instance settings.

        References
        ----------
        [Shields.io API - PyPI Format](https://shields.io/badges/py-pi-format)
        """
        return _shields.create(
            path=self._create_path(["format"], []),
            queries={"pypiBaseUrl": self._pypi_base_url},
            shields_settings=self._shields_settings(shields_settings) + _shields.ShieldsSettings(
                label="Distribution Format",
            ),
            badge_settings=self._badge_settings(badge_settings) + _BadgeSettings(
                title="Format of the distribution package",
                alt="Distribution Format",
                link=self._link.homepage
            ),
        )

    def development_status(
        self,
        shields_settings: _shields.ShieldsSettings | None = None,
        badge_settings: _BadgeSettings | None = None,
    ) -> _Badge:
        """Development status.

        Parameters
        ----------
        shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default instance settings.
        badge_settings : pybadger.BadgeSettings, optional
            Settings for the badge to override the default instance settings.

        References
        ----------
        [Shields.io API - PyPI Status](https://shields.io/badges/py-pi-status)
        """
        return _shields.create(
            path=self._create_path(["status"], []),
            queries={"pypiBaseUrl": self._pypi_base_url},
            shields_settings=self._shields_settings(shields_settings) + _shields.ShieldsSettings(
                label="Development Status",
            ),
            badge_settings=self._badge_settings(badge_settings) + _BadgeSettings(
                title="Development phase of the package.",
                alt="Development Status",
                link=self._link.homepage
            ),
        )

    def implementation(
        self,
        shields_settings: _shields.ShieldsSettings | None = None,
        badge_settings: _BadgeSettings | None = None,
    ) -> _Badge:
        """Python implementation used to build the package.

        Parameters
        ----------
        shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default instance settings.
        badge_settings : pybadger.BadgeSettings, optional
            Settings for the badge to override the default instance settings.

        References
        ----------
        - [Shields.io API - PyPI Implementation](https://shields.io/badges/py-pi-implementation)
        """
        return _shields.create(
            path=self._create_path(["implementation"], []),
            queries={"pypiBaseUrl": self._pypi_base_url},
            shields_settings=self._shields_settings(shields_settings) + _shields.ShieldsSettings(
                label="Python Implementation",
            ),
            badge_settings=self._badge_settings(badge_settings) + _BadgeSettings(
                title="Python implementation used to build the package",
                alt="Python Implementation",
                link=self._link.homepage
            ),
        )

    def python_versions(
        self,
        shields_settings: _shields.ShieldsSettings | None = None,
        badge_settings: _BadgeSettings | None = None,
    ) -> _Badge:
        """Supported Python versions read from trove classifiers.

        Parameters
        ----------
        shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default instance settings.
        badge_settings : pybadger.BadgeSettings, optional
            Settings for the badge to override the default instance settings.

        References
        ----------
        - [Shields.io API - Python Version](https://shields.io/badges/py-pi-python-version)
        """
        return _shields.create(
            path=self._create_path(["pyversions"], []),
            queries={"pypiBaseUrl": self._pypi_base_url},
            shields_settings=self._shields_settings(shields_settings) + _shields.ShieldsSettings(
                label="Supports Python",
            ),
            badge_settings=self._badge_settings(badge_settings) + _BadgeSettings(
                title="Supported Python versions of the latest release.",
                alt="Supported Python Versions",
                link=self._link.homepage
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
        - [Shields.io API - PyPI Version](https://shields.io/badges/py-pi-version)
        """
        return _shields.create(
            path=self._create_path(["v"], []),
            shields_settings=self._shields_settings(shields_settings) + _shields.ShieldsSettings(label="Latest Version"),
            badge_settings=self._badge_settings(badge_settings) + _BadgeSettings(
                title="Latest release version",
                alt="Latest Version",
                link=self._link.homepage,
            ),
        )
