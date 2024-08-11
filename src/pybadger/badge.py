"""Abstract base class definition for all badge objects."""


# Non-standard libraries
from markitup.html import element as _html
import pylinks as _pylinks


class Badge:

    def __init__(
        self,
        src_light: str | _pylinks.url.URL,
        src_dark: str | _pylinks.url.URL | None = None,
        image_attributes: dict[str, str | bool] | None = None,
        anchor_attributes: dict[str, str | bool] | None = None,
        picture_attributes: dict[str, str | bool] | None = None,
        src_light_attributes: dict[str, str | bool] | None = None,
        src_dark_attributes: dict[str, str | bool] | None = None,
        default_img_light: bool = True,
    ):
        self.src_light = src_light
        self.src_dark = src_dark
        self.image_attributes = image_attributes or {}
        self.anchor_attributes = anchor_attributes or {}
        self.picture_attributes = picture_attributes or {}
        self.src_light_attributes = src_light_attributes or {}
        self.src_dark_attributes = src_dark_attributes or {}
        self.default_img_light = default_img_light
        return

    def img(
        self,
        image_attributes: dict[str, str | bool] | None = None,
        anchor_attributes: dict[str, str | bool] | None = None,
        light: bool | None = None,
    ) -> _html.Img | _html.A:
        image_attributes = image_attributes if isinstance(image_attributes, dict) else self.image_attributes
        default_light = light if light is not None else self.default_img_light
        src = self.src_light if default_light else (self.src_dark if self.src_dark else self.src_light)
        img = _html.img(src=src, **image_attributes)
        a_attrs = anchor_attributes if isinstance(anchor_attributes, dict) else self.anchor_attributes
        if not a_attrs:
            return img
        return _html.a(img, a_attrs)

    def picture(
        self,
        image_attributes: dict[str, str | bool] | None = None,
        anchor_attributes: dict[str, str | bool] | None = None,
        picture_attributes: dict[str, str | bool] | None = None,
        src_light_attributes: dict[str, str | bool] | None = None,
        src_dark_attributes: dict[str, str | bool] | None = None,
        default_img_light: bool | None = None,
    ):
        picture = _html.picture_color_scheme(
            self.src_light,
            self.src_dark or self.src_light,
            picture_attributes if isinstance(picture_attributes, dict) else self.picture_attributes,
            src_light_attributes if isinstance(src_light_attributes, dict) else self.src_light_attributes,
            src_dark_attributes if isinstance(src_dark_attributes, dict) else self.src_dark_attributes,
            image_attributes if isinstance(image_attributes, dict) else self.image_attributes,
            default_img_light if default_img_light is not None else self.default_img_light,
        )
        a_attrs = anchor_attributes if isinstance(anchor_attributes, dict) else self.anchor_attributes
        if not a_attrs:
            return picture
        return _html.a(picture, a_attrs)

    def set(
        self,
        image_attributes: dict[str, str | bool] | None = None,
        anchor_attributes: dict[str, str | bool] | None = None,
        picture_attributes: dict[str, str | bool] | None = None,
        src_light_attributes: dict[str, str | bool] | None = None,
        src_dark_attributes: dict[str, str | bool] | None = None,
        default_img_light: bool | None = None,
    ) -> None:
        args = locals()
        for attr in (
            "image_attributes",
            "anchor_attributes",
            "picture_attributes",
            "src_light_attributes",
            "src_dark_attributes",
            "default_img_light",
        ):
            value = args[attr]
            if value is not None:
                if attr == "default_img_light":
                    setattr(self, attr, value)
                else:
                    setattr(self, attr, getattr(self, attr) | value)
        return

    def display(self):
        from IPython.display import HTML, display
        display(HTML(str(self)))
        return

    def __str__(self):
        element = self.picture() if self.src_dark else self.img()
        return str(element)

    def __add__(self, other):
        if other is None:
            return self
        if not isinstance(other, Badge):
            raise TypeError("Only badges can be added to badges.")
        return Badge(
            src_light=other.src_light or self.src_light,
            src_dark=other.src_dark or self.src_dark,
            image_attributes=self.image_attributes | other.image_attributes,
            anchor_attributes=self.anchor_attributes | other.anchor_attributes,
            picture_attributes=self.picture_attributes | other.picture_attributes,
            src_light_attributes=self.src_light_attributes | other.src_light_attributes,
            src_dark_attributes=self.src_dark_attributes | other.src_dark_attributes,
            default_img_light=self.default_img_light or other.default_img_light,
        )
