from typing import Literal as _Literal
from dataclasses import dataclass as _dataclass, asdict as _asdict
import base64 as _base64
from pathlib import Path as _Path
import pylinks as _pylinks

from pybadger import Badge as _Badge


@_dataclass
class ShieldsSettings:
    """Common settings for Shields.io badges."""
    style: _Literal["flat", "flat-square", "plastic", "for-the-badge", "social"] | None = None
    color: str | None = None
    label: str | None = None
    label_color: str | None = None
    logo: str | _Path | _pylinks.url.URL | tuple[
        str, str | bytes | _Path | _pylinks.url.URL
    ] | None = None
    logo_color: str | None = None
    logo_size: _Literal["auto"] | None = None
    logo_width: int | None = None
    cache_seconds: int | None = None

    def __call__(self):
        return _asdict(self)

    def __add__(self, other):
        if other is None:
            return self
        if not isinstance(other, ShieldsSettings):
            raise TypeError("Only ShieldsSettings objects can be added together.")
        kwargs_new = self() | other()
        return ShieldsSettings(**kwargs_new)

    def __radd__(self, other):
        if other is None:
            return self
        raise TypeError("Only ShieldsSettings objects can be added together.")



class ShieldsBadge:
    def __init__(
        self,
        url: _pylinks.url.URL,
        params_light: dict | None = None,
        params_dark: dict | None = None,
        attrs_img: dict[str, str | bool] | None = None,
        attrs_a: dict[str, str | bool] | None = None,
        attrs_picture: dict[str, str | bool] | None = None,
        attrs_source_light: dict[str, str | bool] | None = None,
        attrs_source_dark: dict[str, str | bool] | None = None,
    ):
        self.url = url
        self.params_light = params_light or {}
        self.params_dark = params_dark or {}
        self.attrs_img = attrs_img or {}
        self.attrs_a = attrs_a or {}
        self.attrs_picture = attrs_picture or {}
        self.attrs_source_light = attrs_source_light or {}
        self.attrs_source_dark = attrs_source_dark or {}
        return

    @staticmethod
    def _process_logo(
        logo: str | bytes | _Path | _pylinks.url.URL
    ):

        mime_type = {
            "apng": "image/apng",
            "avif": "image/avif",
            "bmp": "image/bmp",
            "gif": "image/gif",
            "ico": "image/x-icon",
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "png": "image/png",
            "svg": "image/svg+xml",
            "tif": "image/tiff",
            "tiff": "image/tiff",
            "webp": "image/webp",
        }

        def encode_logo(content, mime_type: str = "png"):
            return f'data:{mime_type};base64,{_base64.b64encode(content).decode()}'

        if isinstance(logo, (tuple, list)):
            if len(logo) != 2:
                raise ValueError()
            extension = logo[0]
            data = logo[1]
            if extension not in mime_type:
                raise ValueError(f"Logo extension '{extension}' is not recognized.")
        else:
            extension = None
            data = logo

        if isinstance(data, str):
            if data.startswith(("http://", "https://")):
                content = _pylinks.http.request(url=data, response_type="bytes")
                extension = extension or logo.rsplit(".", 1)[-1]
                if extension not in mime_type:
                    raise ValueError(f"Logo extension '{extension}' is not recognized.")
                return encode_logo(content, mime_type=mime_type[extension])
            return data

        if isinstance(data, bytes):
            if extension is None:
                raise ValueError()
            return encode_logo(data, mime_type=mime_type[extension])

        if isinstance(data, _Path):
            content = data.read_bytes()
            extension = extension or logo.suffix[1:]
            if extension not in mime_type:
                raise ValueError(f"Logo extension '{extension}' is not recognized.")
            return encode_logo(content, mime_type=mime_type[extension])

        if isinstance(data, _pylinks.url.URL):
            content = _pylinks.http.request(url=data, response_type="bytes")
            extension = extension or str(data).rsplit(".", 1)[-1]
            if extension not in mime_type:
                raise ValueError(f"Logo extension '{extension}' is not recognized.")
            return encode_logo(content, mime_type=mime_type[extension])

        raise ValueError(f"Logo type '{type(logo)}' is not recognized.")



def create(
    path: str,
    queries: dict[str, str | bytes | bool | None] | None = None,
    light_settings: ShieldsSettings | None = None,
    dark_settings: ShieldsSettings | None = None,
):
    if l

    url_light = _pylinks.url.create("https://img.shields.io") / path
    url_dark = url_light.copy()

    common_queries = {
        "style": shields_settings.style,
        "logoSize": shields_settings.logo_size,
        "logoWidth": shields_settings.logo_width,
        "label": shields_settings.label,
        "cacheSeconds": shields_settings.cache_seconds,
    } | (queries or {})
    for key, val in common_queries.items():
        if val is not None:
            _url.queries[key] = val
    _url_dark = _url.copy()
    logo_light = _process_logo(shields_settings.logo) if shields_settings.logo else None
    for key, val in (
        ("color", shields_settings.color),
        ("labelColor", shields_settings.label_color),
        ("logo", logo_light),
        ("logoColor", shields_settings.logo_color),
    ):
        if val is not None:
            _url.queries[key] = val
    if not (
        shields_settings.logo_dark
        or shields_settings.logo_color_dark
        or shields_settings.color_dark
        or shields_settings.label_color_dark
    ):
        return _Badge(url=_url, settings=badge_settings)
    for key, val in (
        ("color", shields_settings.color_dark),
        ("labelColor", shields_settings.label_color_dark),
        ("logo", _process_logo(shields_settings.logo_dark) if shields_settings.logo_dark else logo_light),
        ("logoColor", shields_settings.logo_color_dark),
    ):
        if val is not None:
            _url_dark.queries[key] = val
    return _ThemedBadge(url=_url, src_dark=_url_dark, settings=badge_settings)





class ShieldsBadger:
    """Shields.io badge creator."""

    def __init__(
        self,
        endpoint_start: str,
        endpoint_key: str | None = None,
        default_shields_settings: ShieldsSettings | None = None,
        default_badge_settings: _BadgeSettings | None = None,
    ):
        """
        Parameters
        ----------
        default_shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default global settings.
            These will be used as default values for all badges,
            unless the same argument is also provided to the method when creating a specific badge.
        default_badge_settings : pybadger.BadgeSettings, optional
            Settings for the badge to override the default global settings.
            These will be used as default values for all badges,
            unless the same argument is also provided to the method when creating a specific badge.
        """
        self.endpoint_start = endpoint_start
        self.endpoint_key = endpoint_key
        self.default_badge_settings = default_badge_settings
        self.default_shields_settings = default_shields_settings
        return

    def _create_path(self, before: list[str], after: list[str]) -> str:
        """Create the path for the badge."""
        mid = f"/{self.endpoint_key}/" if self.endpoint_key else "/"
        return f"{self.endpoint_start}/{'/'.join(before)}{mid}{'/'.join(after)}"

    def _shields_settings(self, setings: ShieldsSettings | None) -> ShieldsSettings | None:
        """Get the shields settings to use for the badge."""
        return setings + self.default_shields_settings if setings else self.default_shields_settings

    def _badge_settings(self, settings: _BadgeSettings | None) -> _BadgeSettings | None:
        """Get the badge settings to use for the badge."""
        return settings + self.default_badge_settings if settings else self.default_badge_settings
