"""Dynamically create badges using the PePy API.

References
----------
- [PePy Website](https://pepy.tech/)
- [PePy Repository](https://github.com/psincraian/pepy)
"""


# Standard libraries
from typing import Literal as _Literal, NamedTuple as _NamedTuple
# Non-standard libraries
import pylinks as _pylinks

from pybadger import BadgeSettings as _BadgeSettings, Badge as _Badge, ThemedBadge as _ThemedBadge


_BASE_URL = _pylinks.url.create("https://static.pepy.tech")


class PepySettings(_NamedTuple):
    """Settings for the PePy badge.

    Attributes
    ----------
    left_text : str, optional
        Text to display on the left side of the badge.
    units : {'international_system', 'abbreviation', 'none'}, default: 'international_system'
        Unit of numbers shown on the right side of the badge.
    left_color : str, optional
        Color of the left side of the badge, e.g., `black`, `blue`, etc.
    right_color : str, optional
        Color of the right side of the badge, e.g., `black`, `blue`, etc.
    left_color_dark : str, optional
        Dark-mode color of the left side of the badge, e.g., `black`, `blue`, etc.
    right_color_dark : str, optional
        Dark-mode color of the right side of the badge, e.g., `black`, `blue`, etc.
    """

    left_text: str | None = None
    units: _Literal["international_system", "abbreviation", "none"] = "international_system"
    left_color: str | None = None
    right_color: str | None = None
    left_color_dark: str | None = None
    right_color_dark: str | None = None

    def __add__(self, other):
        if other is None:
            return self
        if not isinstance(other, PepySettings):
            raise TypeError("Only PepySettings objects can be added together.")
        kwargs = {}
        for param in self._fields:
            arg_self = getattr(self, param)
            kwargs[param] = arg_self if arg_self is not None else getattr(other, param)
        return PepySettings(**kwargs)

    def __radd__(self, other):
        if other is None:
            return self
        raise TypeError("Only PepySettings objects can be added together.")


pepy_settings_default = PepySettings()


def pypi_downloads(
    package: str,
    period: _Literal["total", "month", "week"] = "total",
    pepy_settings: PepySettings | None = None,
    badge_settings: _BadgeSettings | None = None,
) -> _Badge:
    """
    Number of downloads for a PyPI package.

    Parameters
    ----------
    package : str
        Package name.
    period : {'total', 'month', 'week'}, default: 'total'
        Time period to query.
    pepy_settings : pybadger.pepy.PepySettings, optional
        Settings for the PePy badge.
    badge_settings : pybadger.BadgeSettings, optional
        Settings for the badge.

    References
    ----------
    - [PePy Source Code](https://github.com/psincraian/pepy/blob/master/pepy/application/badge_service.py)
    """
    _url = _BASE_URL / "personalized-badge" / package
    pepy_settings = pepy_settings + pepy_settings_default + PepySettings(
        left_text="Total Downloads" if period == "total" else f"Downloads/{period.capitalize()}"
    )
    badge_settings = badge_settings + _BadgeSettings(
        title="",
        link=f"https://pepy.tech/project/{package}",
    )
    common_queries = {
        "left_text": pepy_settings.left_text, "units": pepy_settings.units, "period": period
    }
    for key, val in common_queries.items():
        if val is not None:
            _url.queries[key] = val
    _url_dark = _url.copy()
    for key, val in (
        ("left_color", pepy_settings.left_color),
        ("right_color", pepy_settings.right_color),
    ):
        if val is not None:
            _url.queries[key] = val
    if not (pepy_settings.left_color_dark or pepy_settings.right_color_dark):
        return _Badge(url=_url, settings=badge_settings)
    for key, val in (
        ("left_color", pepy_settings.left_color_dark),
        ("right_color", pepy_settings.right_color_dark),
    ):
        if val is not None:
            _url_dark.queries[key] = val
    return _ThemedBadge(url=_url, url_dark=_url_dark, settings=badge_settings)
