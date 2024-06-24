import pylinks as _pylinks

from pybadger import BadgeSettings as _BadgeSettings, Badge as _Badge
from pybadger import shields as _shields
from pybadger.shields.badge import ShieldsBadger as _ShieldsBadger


class ReadTheDocsBadge(_ShieldsBadger):
    """Shields.io Read The Docs badges."""

    def __init__(
        self,
        package_name: str,
        default_shields_settings: _shields.ShieldsSettings | None = None,
        default_badge_settings: _BadgeSettings | None = None,
    ):
        """
        Parameters
        ----------
        package_name : str
            The name of the package on Read The Docs.
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
            endpoint_start="readthedocs",
            endpoint_key=package_name,
            default_shields_settings=default_shields_settings,
            default_badge_settings=default_badge_settings,
        )
        self.package_name = package_name
        self._link = _pylinks.site.readthedocs.project(name=package_name)
        return

    def build_status(
        self,
        version: str | None = None,
        shields_settings: _shields.ShieldsSettings | None = None,
        badge_settings: _BadgeSettings | None = None,
    ) -> _Badge:
        """Build status of the website.

        Parameters
        ----------
        version : str, optional
            A specific version of the website to query.
            If not provided, the latest version will be queried.
        shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default instance settings.
        badge_settings : pybadger.BadgeSettings, optional
            Settings for the badge to override the default instance settings.

        """
        return _shields.create(
            path=self._create_path([], [version] if version else []),
            shields_settings=self._shields_settings(shields_settings) + _shields.ShieldsSettings(
                label="Website", logo="readthedocs",
            ),
            badge_settings=self._badge_settings(badge_settings) + _BadgeSettings(
                title="Website build status. Click to see more details on the ReadTheDocs platform.",
                alt="Website Build Status",
                link=self._link.build_status
            ),
        )
