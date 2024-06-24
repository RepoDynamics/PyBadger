"""Custom static, dynamic, and endpoint badges."""

from typing import Literal as _Literal

from pybadger import BadgeSettings as _BadgeSettings, Badge as _Badge
from pybadger import shields as _shields


def static(
    message: str,
    shields_settings: _shields.ShieldsSettings | None = None,
    badge_settings: _BadgeSettings | None = None,
) -> _Badge:
    """Create a static badge with custom text.

    Parameters
    ----------
    message : str
        The text on the (right side of the) badge.
        When `ShieldsSettings.label` is not set in `shields_settings`,
        the badge will only have one side.
    shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default instance settings.
    badge_settings : pybadger.BadgeSettings, optional
        Settings for the badge to override the default instance settings.
    """
    # If `ShieldsSettings.label` is not set, Shields.io displays the text 'static' for the label.
    # To prevent this, set the label to an empty string when it is not provided.
    shields_settings_default = _shields.ShieldsSettings(label="")
    if shields_settings is not None:
        if not shields_settings.label:
            shields_settings = shields_settings_default + shields_settings
    else:
        shields_settings = shields_settings_default
    return _shields.create(
        path="static/v1",
        queries={"message": message},
        shields_settings=shields_settings,
        badge_settings=badge_settings,
    )


def dynamic(
    typ: _Literal["json", "toml", "xml", "yaml"],
    url: str,
    query: str,
    prefix: str | None = None,
    suffix: str | None = None,
    shields_settings: _shields.ShieldsSettings | None = None,
    badge_settings: _BadgeSettings | None = None,
) -> _Badge:
    """Create a dynamic badge with custom text extracted from a data file.

    Parameters
    ----------
    typ : {'json', 'toml', 'xml', 'yaml'}
        Type of the file.
    url : str
        URL of the file, e.g., `https://raw.githubusercontent.com/repodynamics/pybadger/main/pyproject.toml`
    query : str
        A [JSONPath](https://jsonpath.com/) expression (for JSON, TOML, and YAML files)
        or an [XPath](https://devhints.io/xpath) selector (for XML files)
        to query the file, e.g., `$.name`, `//slideshow/slide[1]/title`.
    prefix : str, optional
        Prefix to append to the extracted value.
    suffix : str, optional
        Suffix to append to the extracted value.
    shields_settings : pybadger.shields.ShieldsSettings, optional
        Settings for the Shields.io badge to override the default instance settings.
    badge_settings : pybadger.BadgeSettings, optional
        Settings for the badge to override the default instance settings.

    Notes
    -----
    - For XML documents that use a default namespace prefix,
    the local-name function must be used to construct the query.
    For example, `/*[local-name()='myelement']` rather than `/myelement`.
    - Useful resource for XPath selectors: [XPather](http://xpather.com/)

    References
    ----------
    - [Shields.io API - Dynamic JSON Badge](https://shields.io/badges/dynamic-json-badge)
    - [Shields.io API - Dynamic TOML Badge](https://shields.io/badges/dynamic-toml-badge)
    - [Shields.io API - Dynamic XML Badge](https://shields.io/badges/dynamic-xml-badge)
    - [Shields.io API - Dynamic YAML Badge](https://shields.io/badges/dynamic-yaml-badge)
    """
    return _shields.create(
        path=f"badge/dynamic/{typ}",
        queries={
            "url": url,
            "query": query,
            "prefix": prefix,
            "suffix": suffix,
        },
        shields_settings=shields_settings,
        badge_settings=badge_settings,
    )


def endpoint(
    url: str,
    shields_settings: _shields.ShieldsSettings | None = None,
    badge_settings: _BadgeSettings | None = None,
) -> _Badge:
    """Create a dynamic badge with custom text retrieved from a JSON endpoint.

    Parameters
    ----------
    url : str
        URL of the JSON endpoint. For the complete response schema, see References.
        Example response: `{ "schemaVersion": 1, "label": "hello", "message": "sweet world", "color": "orange" }`
    shields_settings : pybadger.shields.ShieldsSettings, optional
        Settings for the Shields.io badge to override the default instance settings.
    badge_settings : pybadger.BadgeSettings, optional
        Settings for the badge to override the default instance settings.

    References
    ----------
    - [Shields.io API - Endpoint Badge](https://shields.io/badges/endpoint-badge)
    """
    return _shields.create(
        path="endpoint",
        queries={"url": url},
        shields_settings=shields_settings,
        badge_settings=badge_settings,
   )