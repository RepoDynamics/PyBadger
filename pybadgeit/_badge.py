"""Abstract base class definition for all badge objects."""


# Standard libraries
from typing import Literal, Optional
from abc import ABC, abstractmethod
# Non-standard libraries
from pylinks.url import URL
from pyhtmlit import element as html


class Badge(ABC):
    """Abstract base class for badges."""

    @abstractmethod
    def url(self, mode: Literal['dark', 'light', 'clean'] = 'clean') -> str | URL:
        """

        Parameters
        ----------
        mode : {}
            clean: URL of the badge image without any customization.

        Returns
        -------

        """
        ...

    def __init__(
            self,
            alt: Optional[str],
            title: Optional[str],
            width: Optional[str],
            height: Optional[str],
            align: Optional[str],
            link: Optional[str | URL],
            default_theme: Literal['light', 'dark'],
    ):
        """
        Parameters
        ----------
        alt : str
            Alternative text to show if image doesn't load.
            Corresponds to the 'alt' attribute of the IMG element in HTML.
        title : str
            Description to show on mouse hover.
            Corresponds to the 'title' attribute of the IMG element in HTML.
        width : str
            Width of the image, e.g. '100px', '80%'.
            Corresponds to the 'width' attribute of the IMG element in HTML.
        height : str
            Height of the image, e.g. '100px', '80%'.
            Corresponds to the 'height' attribute of the IMG element in HTML.
        link : pylinks.URL
            Link URL, i.e. the URL that opens when clicking on the badge.
            Corresponds to the 'href' attribute of the A (anchor) element in HTML.
        """
        self.alt = alt
        self.title = title
        self.width = width
        self.height = height
        self.align = align
        self.link = link
        self.default_theme = default_theme
        return

    def as_html_picture(self, link: bool = True):
        picture = html.PICTURE(
            img=self.as_html_img(link=False),
            sources=[
                html.SOURCE(srcset=self.url('dark'), media="(prefers-color-scheme: dark)"),
                html.SOURCE(srcset=self.url('light'), media="(prefers-color-scheme: light)")
            ]
        )
        return html.A(href=self.link, content=[picture]) if link else picture

    def as_html_img(self, link: bool = True):
        img = html.IMG(
            src=self.url(self.default_theme),
            alt=self.alt,
            title=self.title,
            width=self.width,
            height=self.height,
            align=self.align,
        )
        if link and self.link:
            return html.A(href=self.link, content=[img])
        return img

    def __str__(self):
        return str(self.as_html_picture())

    @property
    def link(self) -> URL | None:
        """URL of the badge's anchor, i.e. where it links to."""
        return self._link

    @link.setter
    def link(self, value):
        self._link = None if not value else URL(str(value))
