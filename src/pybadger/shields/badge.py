from typing import Literal as _Literal, NamedTuple as _NamedTuple
import base64 as _base64
from pathlib import Path as _Path
import pylinks as _pylinks

from pybadger import Badge as _Badge, ThemedBadge as _ThemedBadge, BadgeSettings as _BadgeSettings


class ShieldsSettings(_NamedTuple):
    """Common settings for Shields.io badges."""
    style: _Literal["flat", "flat-square", "plastic", "for-the-badge", "social"] | None = None
    logo: str | _Path | _pylinks.url.URL | tuple[
        str, str | bytes | _Path | _pylinks.url.URL
    ] | None = None
    logo_color: str | None = None
    logo_size: _Literal["auto"] | None = None
    logo_width: int | None = None
    label: str | None = None
    label_color: str | None = None
    color: str | None = None
    logo_dark: str | _Path | _pylinks.url.URL | tuple[
        str, str | bytes | _Path | _pylinks.url.URL
    ] | None = None
    logo_color_dark: str | None = None
    label_color_dark: str | None = None
    color_dark: str | None = None
    cache_seconds: int | None = None

    def __add__(self, other):
        if other is None:
            return self
        if not isinstance(other, ShieldsSettings):
            raise TypeError("Only ShieldsSettings objects can be added together.")
        kwargs = {}
        for param in self._fields:
            arg_self = getattr(self, param)
            kwargs[param] = arg_self if arg_self is not None else getattr(other, param)
        return ShieldsSettings(**kwargs)

    def __radd__(self, other):
        if other is None:
            return self
        raise TypeError("Only ShieldsSettings objects can be added together.")


shields_settings_default = ShieldsSettings()


def create(
    path: str,
    queries: dict[str, str | bytes | bool | None] | None = None,
    shields_settings: ShieldsSettings | None = None,
    badge_settings: _BadgeSettings | None = None,
):
    _url = _pylinks.url.create("https://img.shields.io") / path
    shields_settings = shields_settings + shields_settings_default
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
    for key, val in (
        ("color", shields_settings.color),
        ("labelColor", shields_settings.label_color),
        ("logo", _process_logo(shields_settings.logo) if shields_settings.logo else None),
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
        ("logo", _process_logo(shields_settings.logo_dark) if shields_settings.logo_dark else None),
        ("logoColor", shields_settings.logo_color_dark),
    ):
        if val is not None:
            _url_dark.queries[key] = val
    return _ThemedBadge(url=_url, url_dark=_url_dark, settings=badge_settings)


def _process_logo(logo: str | _Path | _pylinks.url.URL | tuple[str, str | bytes | _Path | _pylinks.url.URL]):

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

    if isinstance(logo, tuple):
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

    # if not isinstance(value, dict):
    #     raise ValueError(f"`logo` expects either a string or a dict, but got {type(value)}.")
    # for key, val in value.items():
    #     if key == "width":
    #         self._logo["width"] = val
    #     elif key == "color":
    #         if isinstance(val, str):
    #             self._logo["color"] = {"dark": val, "light": val}
    #         elif isinstance(val, dict):
    #             for key2, val2 in val.items():
    #                 if key2 not in ("dark", "light"):
    #                     raise ValueError()
    #                 self._logo["color"][key2] = val2
    #         else:
    #             raise ValueError()
    #     elif key == "simple_icons":
    #         self._logo["data"] = val
    #     elif key == "url":
    #         content = _pylinks.http.request(url=val, response_type="bytes")
    #         self._logo["data"] = encode_logo(content)
    #     elif key == "local":
    #         with open(val["value"], "rb") as f:
    #             content = f.read()
    #             self._logo = encode_logo(content)
    #     elif key == "bytes":
    #         self._logo = encode_logo(content)
    #     elif key == "github":
    #         content = _pylinks.http.request(
    #             url=_pylinks.github.user(val["user"])
    #             .repo(val["repo"])
    #             .branch(val["branch"])
    #             .file(val["path"], raw=True),
    #             response_type="bytes",
    #         )
    #         self._logo["data"] = encode_logo(content)
    #     else:
    #         raise ValueError(f"Key '{key}' in logo spec. {value} is not recognized.")
    # return


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




# class ShieldsBadge(Badge):
#     """SHIELDS.IO Badge"""
#
#     def __init__(
#         self,
#         path: str,
#         style: Literal["plastic", "flat", "flat-square", "for-the-badge", "social"] = None,
#         text: str | dict[Literal["left", "right"], str] = None,
#         logo: str | tuple[str, str] = None,
#         color: str | dict[str, str | dict[str, str]] = None,
#         cache_time: int = None,
#         alt: str = None,
#         title: str = None,
#         width: str = None,
#         height: str = None,
#         align: str = None,
#         link: str | URL = None,
#         default_theme: Literal["light", "dark"] = "light",
#         html_syntax: str | dict[Literal["tag_seperator", "content_indent"], str] = None,
#     ):
#         """
#         Parameters
#         ----------
#         path : pylinks.URL
#             Clean URL (without additional queries) of the badge image.
#         style : {'plastic', 'flat', 'flat-square', 'for-the-badge', 'social'}
#             Style of the badge.
#         left_text : str
#             Text on the left-hand side of the badge. Pass an empty string to omit the left side.
#         right_text : str
#             Text on the right-hand side of the badge. This can only be set for static badges.
#             When `left_text` is set to empty string, this will be the only text shown.
#         logo : str
#             Logo on the badge. Two forms of input are accepted:
#             1. A SimpleIcons icon name (see: https://simpleicons.org/), e.g. 'github',
#                 or one of the following names: 'bitcoin', 'dependabot', 'gitlab', 'npm', 'paypal',
#                 'serverfault', 'stackexchange', 'superuser', 'telegram', 'travis'.
#             2. A filepath to an image file; this must be inputted as a tuple, where the first
#                element is the file extension, and the second element is the full path to the image file,
#                e.g. `('png', '/home/pictures/my_logo.png')`.
#         logo_width : float
#             Horizontal space occupied by the logo.
#         logo_color_light : str
#             Color of the logo. This and other color inputs can be in one of the following forms:
#             hex, rgb, rgba, hsl, hsla and css named colors.
#         left_color_light : str
#             Color of the left side. See `logo_color` for more detail.
#         right_color_dark : str
#             Color of the right side. See `logo_color` for more detail.
#         cache_time : int
#             HTTP cache lifetime in seconds.
#         """
#
#         self._url: URL = url("https://img.shields.io") / path
#         self.style: Literal["plastic", "flat", "flat-square", "for-the-badge", "social"] = style
#
#         self._text = self._init_text()
#         self.text = text
#
#         self._logo = self._init_logo()
#         self.logo = logo
#
#         self._color = self._init_color()
#         self.color = color
#
#         self.cache_time: int = cache_time
#
#         if alt is not False:
#             alt = alt or self.text["left"] or self.text["right"]
#         super().__init__(
#             alt=alt,
#             title=title,
#             width=width,
#             height=height,
#             align=align,
#             link=link,
#             default_theme=default_theme,
#             html_syntax=html_syntax,
#         )
#         return
#
#     def url(self, mode: Literal["light", "dark", "clean"] = "dark") -> URL:
#         """
#         URL of the badge image.
#
#         Parameters
#         ----------
#         mode : {'dark', 'light', 'clean'}
#             'dark' and 'light' provide the URL of the badge image customized for dark and light themes,
#             respectively, while 'clean' gives the URL of the badge image without any customization.
#
#         Returns
#         -------
#         url : pylinks.url.URL
#             A URL object, which among others, has a __str__ method to output the URL as a string.
#         """
#         url = self._url.copy()
#         if mode == "clean":
#             return url
#         for key, val in (
#             ("label", self.text["left"]),
#             ("message", self.text["right"]),
#             ("style", self.style),
#             ("labelColor", self.color["left"][mode]),
#             ("color", self.color["right"][mode]),
#             ("logo", self.logo["data"]),
#             ("logoColor", self.logo["color"][mode]),
#             ("logoWidth", self.logo["width"]),
#             ("cacheSeconds", self.cache_time),
#         ):
#             if val is not None:
#                 url.queries[key] = val
#         return url
#
#     @property
#     def color(self):
#         return copy.deepcopy(self._color)
#
#     @color.setter
#     def color(self, value):
#         if value is None:
#             self._color = self._init_color()
#             return
#         if isinstance(value, str):
#             new_colors = {"dark": value, "light": value}
#             if self._is_static and not self.text["left"]:
#                 self._color["right"] = new_colors
#                 return
#             self._color["left"] = new_colors
#             return
#         if not isinstance(value, dict):
#             return ValueError()
#         for key, val in value.items():
#             if key not in ("left", "right", "dark", "light"):
#                 raise ValueError()
#             if isinstance(val, str):
#                 if key in ("left", "right"):
#                     self._color[key] = {"dark": val, "light": val}
#                 else:
#                     side = "right" if self._is_static and not self.text["left"] else "left"
#                     self._color[side][key] = val
#             elif isinstance(val, dict):
#                 for key2, val2 in val.items():
#                     if key2 not in ("left", "right", "dark", "light"):
#                         raise ValueError()
#                     if key2 in ("dark", "light"):
#                         if key in ("dark", "light"):
#                             raise ValueError()
#                         self._color[key][key2] = val2
#                     else:
#                         if key in ("left", "right"):
#                             raise ValueError()
#                         self._color[key2][key] = val2
#             else:
#                 raise ValueError()
#         return
#
#     @property
#     def text(self):
#         return copy.deepcopy(self._text)
#
#     @text.setter
#     def text(self, value):
#         if value is None:
#             self._text = self._init_text()
#             return
#         if isinstance(value, str):
#             if self._is_static:
#                 self._text = {"left": "", "right": value}
#                 return
#             self._text["left"] = value
#             return
#         if not isinstance(value, dict):
#             raise ValueError()
#         for key, val in value.items():
#             if key not in ("left", "right"):
#                 raise ValueError()
#             if key == "right" and not self._is_static:
#                 raise ValueError()
#             self._text[key] = val
#         return
#
#     @property
#     def _is_static(self):
#         return str(self._url).startswith("https://img.shields.io/static/")
#
#     @staticmethod
#     def _init_text():
#         return {"left": None, "right": None}
#
#     @staticmethod
#     def _init_color():
#         return {"left": {"dark": None, "light": None}, "right": {"dark": None, "light": None}}
#
#     @staticmethod
#     def _init_logo():
#         return {"data": None, "width": None, "color": {"dark": None, "light": None}}
