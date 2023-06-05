"""
Dynamically create badges using the shields.io API

References
----------
* https://shields.io/
* https://github.com/badges/shields
"""

# Standard libraries
from typing import Optional, Sequence, Literal
import base64
# Non-standard libraries
import pylinks
from pylinks import url
from pylinks.url import URL
# Self
from pybadgeit import _badge


_BASE_URL = url('https://img.shields.io')


class ShieldsBadge(_badge.Badge):
    """SHIELDS.IO Badge"""

    def __init__(
            self,
            path: str,
            style: Literal['plastic', 'flat', 'flat-square', 'for-the-badge', 'social'] = None,
            left_text: str = None,
            right_text: str = None,
            logo: str | tuple[str, str] = None,
            logo_width: float = None,
            logo_color_light: str = None,
            logo_color_dark: str = None,
            left_color_light: str = None,
            left_color_dark: str = None,
            right_color_light: str = None,
            right_color_dark: str = None,
            cache_time: int = None,
            alt: str = None,
            title: str = None,
            width: str = None,
            height: str = None,
            align: str = None,
            link: str | URL = None,
            default_theme: Literal['light', 'dark'] = 'dark',
    ):
        """
        Parameters
        ----------
        path : pylinks.URL
            Clean URL (without additional queries) of the badge image.
        style : {'plastic', 'flat', 'flat-square', 'for-the-badge', 'social'}
            Style of the badge.
        left_text : str
            Text on the left-hand side of the badge. Pass an empty string to omit the left side.
        right_text : str
            Text on the right-hand side of the badge. This can only be set for static badges.
            When `left_text` is set to empty string, this will be the only text shown.
        logo : str
            Logo on the badge. Two forms of input are accepted:
            1. A SimpleIcons icon name (see: https://simpleicons.org/), e.g. 'github',
                or one of the following names: 'bitcoin', 'dependabot', 'gitlab', 'npm', 'paypal',
                'serverfault', 'stackexchange', 'superuser', 'telegram', 'travis'.
            2. A filepath to an image file; this must be inputted as a tuple, where the first
               element is the file extension, and the second element is the full path to the image file,
               e.g. `('png', '/home/pictures/my_logo.png')`.
        logo_width : float
            Horizontal space occupied by the logo.
        logo_color_light : str
            Color of the logo. This and other color inputs can be in one of the following forms:
            hex, rgb, rgba, hsl, hsla and css named colors.
        left_color_light : str
            Color of the left side. See `logo_color` for more detail.
        right_color_dark : str
            Color of the right side. See `logo_color` for more detail.
        cache_time : int
            HTTP cache lifetime in seconds.
        """
        super().__init__(
            alt=alt, title=title, width=width, height=height, align=align, link=link, default_theme=default_theme
        )
        self._url: URL = url(str(path))
        self.style: Literal['plastic', 'flat', 'flat-square', 'for-the-badge', 'social'] = style
        self.left_text: str = left_text
        self.right_text: str = right_text
        self.logo = logo
        self.logo_width: float = logo_width
        self.logo_color_light: str = logo_color_light
        self.logo_color_dark: str = logo_color_dark
        self.left_color_light: str = left_color_light
        self.left_color_dark: str = left_color_dark
        self.right_color_light: str = right_color_light
        self.right_color_dark: str = right_color_dark
        self.cache_time: int = cache_time
        return

    def url(self, mode: Literal['light', 'dark', 'clean'] = 'dark') -> URL:
        """
        URL of the badge image.

        Parameters
        ----------
        mode : {'dark', 'light', 'clean'}
            'dark' and 'light' provide the URL of the badge image customized for dark and light themes,
            respectively, while 'clean' gives the URL of the badge image without any customization.

        Returns
        -------
        url : pylinks.url.URL
            A URL object, which among others, has a __str__ method to output the URL as a string.
        """
        url = self._url.copy()
        if mode == 'clean':
            return url
        for key, val in (
                ('label', self.left_text),
                ('message', self.right_text),
                ('style', self.style),
                ('labelColor', self.left_color_dark if mode == 'dark' else self.left_color_light),
                ('color', self.right_color_dark if mode == 'dark' else self.right_color_light),
                ('logo', self.logo),
                ('logoColor', self.logo_color_dark if mode == 'dark' else self.logo_color_light),
                ('logoWidth', self.logo_width),
                ('cacheSeconds', self.cache_time),
        ):
            if val is not None:
                url.queries[key] = val
        return url

    @property
    def logo(self):
        return self._logo

    @logo.setter
    def logo(self, value):
        if value is None or isinstance(value, str):
            self._logo = value
        elif isinstance(value, Sequence):
            with open(value[1], 'rb') as img_file:
                self._logo = f'data:image/{value[0].lower()};base64,{base64.b64encode(img_file.read()).decode()}'
                # self._logo = bytes(
                #     f'data:image/{value[0].lower()};base64,{base64.b64encode(img_file.read()).decode()}',
                #     'utf8'
                # )
        else:
            raise ValueError("`logo` expects either a string or a sequence of two strings.")
        return


def static(right_text: str, left_text: Optional[str] = "") -> ShieldsBadge:
    """Static badge with custom text on the right-hand side.

    Parameters
    ----------
    right_text : str
        The text on the right-hand side of the badge.
    left_text : str, default: ''
        Text on the left-hand side of the badge. An empty string (default) will omit the left side.
    """
    return ShieldsBadge(path=_BASE_URL/'static/v1', right_text=right_text, left_text=left_text, alt=right_text)


class GitHub:
    """GitHub Badges."""

    def __init__(
            self,
            username: str,
            repo_name: str,
            logo: Optional[str] = 'github',
            logo_color_light: Optional[str] = 'FFF',
            logo_color_dark: Optional[str] = 'FFF',
    ):
        """
        Parameters
        ----------
        username : str
            GitHub username.
        repo_name : str
            GitHub repository name.
        """
        self.username = username
        self.repo_name = repo_name
        self.logo = logo
        self.logo_color_light = logo_color_light
        self.logo_color_dark = logo_color_dark
        self._url = _BASE_URL / 'github'
        self._address = f'{username}/{repo_name}'
        self._repo_link = pylinks.github.user(username).repo(repo_name)
        return

    @property
    def _logo_config(self):
        return {'logo': self.logo, 'logo_color_dark': self.logo_color_dark, 'logo_color_light': self.logo_color_light}

    def workflow_status(
            self,
            filename: str,
            branch: Optional[str] = None,
            description: Optional[str] = None,
            left_text: Optional[str] = None,
            alt: Optional[str] = None,

    ) -> ShieldsBadge:
        """Status (failing/passing) of a GitHub workflow.

        Parameters
        ----------
        filename : str
            Full filename of the workflow, e.g. 'ci.yaml'.
        branch : str, optional
            Name of specific branch to query.
        description : str, optional
            A description for the workflow.
            This will be used for the 'title' attribute of the badge's 'img' element.
        """
        path = self._url / 'actions/workflow/status' / self._address / filename
        link = self._repo_link.workflow(filename)
        if branch:
            path.queries['branch'] = branch
            link = self._repo_link.branch(branch).workflow(filename)
        title = (
            f"""Status of the GitHub Actions workflow '{filename}'{f"on branch '{branch}'" if branch else ''}. """
            f"""{f"{description.strip().rstrip('.')}. " if description else ""}"""
            'Click to see more details in the Actions section of the repository.'
        )
        return ShieldsBadge(
            path=path,
            link=link,
            left_text=left_text,
            alt=alt if alt else (left_text if alt is None else None),
            title=title,
            **self._logo_config
        )

    def pr_issue(
            self,
            pr: bool = True,
            closed: bool = False,
            label: Optional[str] = None,
            raw: bool = False,
    ) -> ShieldsBadge:
        """Number of pull requests or issues on GitHub.

        Parameters
        ----------
        pr : bool, default: True
            Whether to query pull requests (True, default) or issues (False).
        closed : bool, default: False
            Whether to query closed (True) or open (False, default) issues/pull requests.
        label : str, optional
            A specific GitHub label to query.
        raw : bool, default: False
            Display 'open'/'close' after the number (False) or only display the number (True).
        """
        path = self._url / (
            f"issues{'-pr' if pr else ''}{'-closed' if closed else ''}"
            f"{'-raw' if raw else ''}/{self._address}{f'/{label}' if label else ''}"
        )
        link = self._repo_link.pr_issues(pr=pr, closed=closed, label=label)
        return ShieldsBadge(path=path, link=link, **self._logo_config)

    def top_language(self) -> ShieldsBadge:
        """The top language in the repository, and its frequency."""
        return ShieldsBadge(path=self._url/'languages/top'/self._address)

    def language_count(self) -> ShieldsBadge:
        """Number of programming languages used in the repository."""
        return ShieldsBadge(path=self._url/'languages/count/'/self._address)

    def downloads(
            self,
            tag: Optional[str | Literal['latest']] = None,
            asset: Optional[str] = None,
            include_pre_release: bool = True,
            sort_by_semver: bool = False,
    ) -> ShieldsBadge:
        """
        Number of downloads of a GitHub release.

        Parameters
        ----------
        tag : str, default: None
            A specific release tag to query. If set to None (default), number of total downloads is displayed.
            Additionally, the keyword 'latest' can be provided to query the latest release.
        asset : str, optional
            An optional asset to query.
        include_pre_release : bool, default: True
            Whether to include pre-releases in the count.
        sort_by_semver : bool, default: False
            If tag is set to 'latest', whether to choose the latest release according
            to the Semantic Versioning (True), or according to date (False).
        """
        path = self._url / f"downloads{'-pre' if include_pre_release else ''}/{self._address}"
        if not tag:
            path /= 'total'
        else:
            path /= f'{tag}/{asset if asset else "total"}'
            if sort_by_semver:
                path.queries['sort'] = 'semver'
        return ShieldsBadge(path=path, link=self._repo_link.releases(tag=tag if tag else 'latest'))

    def license(
            self,
            branch: str = "main",
            filename: str = "LICENSE"
    ) -> ShieldsBadge:
        """License of the GitHub repository.

        Parameters
        ----------
        branch : str, default: 'main'
            Name of the GitHub branch containing the license file.
            This is used to create a link to the license.
        filename : str, default: 'LICENSE'
            Name of the license file in the GitHub branch.
            This is used to create a link to the license.
        """
        return ShieldsBadge(path=self._url/'license'/self._address, link=self._repo_link.branch(branch).file(filename))

    def commit_activity(self, interval: Literal['y', 'm', 'w'] = 'm', branch: Optional[str] = None) -> ShieldsBadge:
        path = self._url / 'commit-activity' / interval / self._address
        link = self._repo_link.commits
        if branch:
            path /= branch
            link = self._repo_link.branch(branch).commits
        return ShieldsBadge(path=path, link=link)

    def commits_since(
            self, version: str | Literal['latest'],
            branch: Optional[str] = None,
            include_pre_release: bool = True,
            sort_by_semver: bool = False,
    ):
        path = self._url / 'commits-since' / self._address / version
        link = self._repo_link.commits
        if branch:
            path /= branch
            link = self._repo_link.branch(branch).commits
        if include_pre_release:
            path.queries['include_prereleases'] = None
        if sort_by_semver:
            path.queries['sort'] = 'semver'
        return ShieldsBadge(path=path, link=link)

    def last_commit(self, branch: Optional[str] = None):
        path = self._url / 'last-commit' / self._address
        link = self._repo_link.commits
        if branch:
            path /= branch
            link = self._repo_link.branch(branch).commits
        return ShieldsBadge(path=path, link=link)

    def release_date(self, pre_release: bool = True, publish_date: bool = False):
        path = self._url / ('release-date-pre' if pre_release else 'release-date') / self._address
        if publish_date:
            path.queries['display_date'] = 'published_at'
        return ShieldsBadge(path=path, link=self._repo_link.releases(tag='latest'))

    def release_version(
            self,
            display_name: Optional[Literal['tag', 'release']] = None,
            include_pre_release: bool = True,
            sort_by_semver: bool = False,
    ):
        path = self._url / 'v/release' / self._address
        if display_name:
            path.queries['display_name'] = display_name
        if include_pre_release:
            path.queries['include_prereleases'] = None
        if sort_by_semver:
            path.queries['sort'] = 'semver'
        return ShieldsBadge(path=path, link=self._repo_link.releases(tag='latest'))

    def code_size(self):
        return ShieldsBadge(path=self._url/'languages/code-size'/self._address)

    def dir_file_count(
            self, path: Optional[str] = None,
            file_or_dir: Optional[Literal['file', 'dir']] = None,
            file_extension: Optional[str] = None
    ):
        img_path = self._url / 'directory-file-count' / self._address
        if path:
            img_path /= path
        if file_or_dir:
            img_path.queries['type'] = file_or_dir
        if file_extension:
            img_path.queries['extension'] = file_extension
        return ShieldsBadge(img_path)

    def repo_size(self):
        return ShieldsBadge(self._url / 'repo-size' / self._address)

    def milestones(self, state: Literal['open', 'closed', 'all'] = 'all'):
        link = self._repo_link.milestones(state=state if state == 'closed' else 'open')
        return ShieldsBadge(self._url/'milestones'/state/self._address, link=link)

    def discussions(self) -> ShieldsBadge:
        return ShieldsBadge(path=self._url/'discussions'/self._address, link=self._repo_link.discussions())

    def dependency_status(self) -> ShieldsBadge:
        return ShieldsBadge(_BASE_URL/'librariesio/github'/self._address)


class PyPI:

    def __init__(self, package_name: str):
        self.package_name = package_name
        self._url = _BASE_URL / 'pypi'
        self._link = pylinks.pypi.project(package_name)
        return

    def downloads(self, period: Literal['dd', 'dw', 'dm'] = 'dm'):
        return ShieldsBadge(self._url/period/self.package_name, link=self._link.home)

    def format(self):
        return ShieldsBadge(self._url/'format'/self.package_name, link=self._link.home)

    def development_status(self):
        return ShieldsBadge(self._url/'status'/self.package_name)

    def supported_python_versions(self):
        return ShieldsBadge(self._url/'pyversions'/self.package_name, link=self._link.home)

    def version(self):
        return ShieldsBadge(self._url/'v'/self.package_name, link=self._link.home)


class Conda:

    def __init__(self, package_name: str, channel: str = 'conda-forge'):
        """
        Parameters
        ----------
        package_name : str
            Package name.
        channel : str, default: 'conda-forge'
            Channel name.
        """
        self.package_name = package_name
        self._channel = channel
        self._url = _BASE_URL / 'conda'
        self._address = f'{channel}/{package_name}'
        self._link = pylinks.conda.project(name=package_name, channel=channel)
        return

    def downloads(self):
        """Number of total downloads."""
        return ShieldsBadge(self._url/'dn'/self._address, link=self._link.home)

    def supported_platforms(self):
        return ShieldsBadge(self._url/'pn'/self._address, link=self._link.home)

    def version(self):
        return ShieldsBadge(self._url/'v'/self._address, link=self._link.home)


def build_read_the_docs(
        project: str,
        version: Optional[str] = None,
        left_text: Optional[str] = 'Website',
        alt: Optional[str] = 'Website Build Status',
        title: Optional[str] = 'Website build status. Click to see more details on the ReadTheDocs platform.',
        logo: Optional[str] = 'readthedocs',
        logo_color_light: str = 'FFF',
        logo_color_dark: str = 'FFF',
) -> ShieldsBadge:
    """Build status of a ReadTheDocs project.

    Parameters
    ----------
    project : str
        ReadTheDocs project name.
    version : str, optional
        Specific ReadTheDocs version of the documentation to query.
        https://img.shields.io/readthedocs/opencadd?logo=readthedocs&logoColor=%238CA1AF
    left_text : str, default = 'Website'
        Text on the left-hand side of the badge. If set to None, the shields.io default ('docs') will be selected.

    """
    return ShieldsBadge(
        path=_BASE_URL/'readthedocs'/f"{project}{f'/{version}' if version else ''}",
        link=pylinks.readthedocs.project(project).build_status,
        left_text=left_text,
        alt=alt,
        title=title,
        logo=logo,
        logo_color_dark=logo_color_dark,
        logo_color_light=logo_color_light,
    )


def coverage_codecov(
        user: str,
        repo: str,
        branch: Optional[str] = None,
        left_text: Optional[str] = 'Code Coverage',
        alt: Optional[str] = 'Code Coverage',
        title: Optional[str] = 'Source code coverage by the test suite. Click to see more details on codecov.io.',
        logo: Optional[str] = 'codecov',
        logo_color_light: str = 'FFF',
        logo_color_dark: str = 'FFF',
) -> ShieldsBadge:
    """Code coverage calculated by codecov.io.

    Parameters
    ----------
    user : str
        GitHub username
    repo : str
        GitHub repository name.
    branch : str, optional
        Name of specific branch to query.
    """
    return ShieldsBadge(
        path=_BASE_URL/f"codecov/c/github/{user}/{repo}{f'/{branch}' if branch else ''}",
        link=f"https://codecov.io/gh/{user}/{repo}{f'/branch/{branch}' if branch else ''}",  #TODO: use PyLinks
        left_text=left_text,
        alt=alt,
        title=title,
        logo=logo,
        logo_color_light=logo_color_light,
        logo_color_dark=logo_color_dark,
    )


def chat_discord(
    server_id: str
):
    """Number of online users in Discord server.

    Parameters
    ----------
    server_id : str
        Server ID of the Discord server.
        It can be located in the url of the channel.

    Notes
    -----
    A Discord server admin must enable the widget setting on the server for this badge to work.
    """
    return ShieldsBadge(path=_BASE_URL/'discord'/server_id)


def binder():
    logo = (
        'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFkAAABZCAMAAABi1XidAAAB8lBMVEX///9XmsrmZYH1'
        'olJXmsr1olJXmsrmZYH1olJXmsr1olJXmsrmZYH1olL1olJXmsr1olJXmsrmZYH1olL1olJXmsrmZYH1olJXmsr1ol'
        'L1olJXmsrmZYH1olL1olJXmsrmZYH1olL1olL0nFf1olJXmsrmZYH1olJXmsq8dZb1olJXmsrmZYH1olJXmspXmspX'
        'msr1olL1olJXmsrmZYH1olJXmsr1olL1olJXmsrmZYH1olL1olLeaIVXmsrmZYH1olL1olL1olJXmsrmZYH1olLna3'
        '1Xmsr1olJXmsr1olJXmsrmZYH1olLqoVr1olJXmsr1olJXmsrmZYH1olL1olKkfaPobXvviGabgadXmsqThKuofKHm'
        'Z4Dobnr1olJXmsr1olJXmspXmsr1olJXmsrfZ4TuhWn1olL1olJXmsqBi7X1olJXmspZmslbmMhbmsdemsVfl8Zgms'
        'Nim8Jpk8F0m7R4m7F5nLB6jbh7jbiDirOEibOGnKaMhq+PnaCVg6qWg6qegKaff6WhnpKofKGtnomxeZy3noG6dZi+'
        'n3vCcpPDcpPGn3bLb4/Mb47UbIrVa4rYoGjdaIbeaIXhoWHmZYHobXvpcHjqdHXreHLroVrsfG/uhGnuh2bwj2Hxk1'
        '7yl1vzmljzm1j0nlX1olL3AJXWAAAAbXRSTlMAEBAQHx8gICAuLjAwMDw9PUBAQEpQUFBXV1hgYGBkcHBwcXl8gICA'
        'goiIkJCQlJicnJ2goKCmqK+wsLC4usDAwMjP0NDQ1NbW3Nzg4ODi5+3v8PDw8/T09PX29vb39/f5+fr7+/z8/Pz9/v'
        '7+zczCxgAABC5JREFUeAHN1ul3k0UUBvCb1CTVpmpaitAGSLSpSuKCLWpbTKNJFGlcSMAFF63iUmRccNG6gLbuxkXU'
        '66JAUef/9LSpmXnyLr3T5AO/rzl5zj137p136BISy44fKJXuGN/d19PUfYeO67Znqtf2KH33Id1psXoFdW30sPZ1sM'
        'vs2D060AHqws4FHeJojLZqnw53cmfvg+XR8mC0OEjuxrXEkX5ydeVJLVIlV0e10PXk5k7dYeHu7Cj1j+49uKg7uLU6'
        '1tGLw1lq27ugQYlclHC4bgv7VQ+TAyj5Zc/UjsPvs1sd5cWryWObtvWT2EPa4rtnWW3JkpjggEpbOsPr7F7EyNewtp'
        'BIslA7p43HCsnwooXTEc3UmPmCNn5lrqTJxy6nRmcavGZVt/3Da2pD5NHvsOHJCrdc1G2r3DITpU7yic7w/7Rxnjc0'
        'kt5GC4djiv2Sz3Fb2iEZg41/ddsFDoyuYrIkmFehz0HR2thPgQqMyQYb2OtB0WxsZ3BeG3+wpRb1vzl2UYBog8FfGh'
        'ttFKjtAclnZYrRo9ryG9uG/FZQU4AEg8ZE9LjGMzTmqKXPLnlWVnIlQQTvxJf8ip7VgjZjyVPrjw1te5otM7RmP7xm'
        '+sK2Gv9I8Gi++BRbEkR9EBw8zRUcKxwp73xkaLiqQb+kGduJTNHG72zcW9LoJgqQxpP3/Tj//c3yB0tqzaml05/+or'
        'HLksVO+95kX7/7qgJvnjlrfr2Ggsyx0eoy9uPzN5SPd86aXggOsEKW2Prz7du3VID3/tzs/sSRs2w7ovVHKtjrX2pd'
        '7ZMlTxAYfBAL9jiDwfLkq55Tm7ifhMlTGPyCAs7RFRhn47JnlcB9RM5T97ASuZXIcVNuUDIndpDbdsfrqsOppeXl5Y'
        '+XVKdjFCTh+zGaVuj0d9zy05PPK3QzBamxdwtTCrzyg/2Rvf2EstUjordGwa/kx9mSJLr8mLLtCW8HHGJc2R5hS219'
        'IiF6PnTusOqcMl57gm0Z8kanKMAQg0qSyuZfn7zItsbGyO9QlnxY0eCuD1XL2ys/MsrQhltE7Ug0uFOzufJFE2PxBo'
        '/YAx8XPPdDwWN0MrDRYIZF0mSMKCNHgaIVFoBbNoLJ7tEQDKxGF0kcLQimojCZopv0OkNOyWCCg9XMVAi7ARJzQdM2'
        'QUh0gmBozjc3Skg6dSBRqDGYSUOu66Zg+I2fNZs/M3/f/Grl/XnyF1Gw3VKCez0PN5IUfFLqvgUN4C0qNqYs5YhPL+'
        'aVZYDE4IpUk57oSFnJm4FyCqqOE0jhY2SMyLFoo56zyo6becOS5UVDdj7Vih0zp+tcMhwRpBeLyqtIjlJKAIZSbI8S'
        'GSF3k0pA3mR5tHuwPFoa7N7reoq2bqCsAk1HqCu5uvI1n6JuRXI+S1Mco54YmYTwcn6Aeic+kssXi8XpXC4V3t7/AD'
        'uTNKaQJdScAAAAAElFTkSuQmCC'
    )
    badge = static(right_text='binder', left_text='launch')
    badge.logo = logo
    badge.right_color_dark = badge.right_color_light = '579aca'
    badge.link = ''  # TODO
    return badge


class LibrariesIO:
    """Shields badges provided by Libraries.io."""

    def __init__(self, package_name: str, platform: str = 'pypi'):
        """
        Parameters
        ----------
        package_name : str
            Name of the package.
        platform : str, default: 'pypi'
            The platform where the package is distributed, e.g. 'pypi', 'conda' etc.
        """
        self.platform = platform
        self.package_name = package_name
        self._url = _BASE_URL / 'librariesio'
        self._address = f'{platform}/{package_name}'
        self._link = URL(f'https://libraries.io/{platform}/{package_name}')
        return

    def dependency_status(self, version: Optional[str] = None) -> ShieldsBadge:
        """
        Dependency status of a package distributed on a package manager platform,
        obtained using Libraries.io.
        The right-hand text shows either 'up to date', or '{number} out of date'.

        Parameters
        ----------
        platform : str
            Name of a supported package manager, e.g. 'pypi', 'conda'.
        package_name : str
            Name of the package.
        version : str, optional
            A specific version to query.

        References
        ----------
        * https://libraries.io/
        """
        path = self._url / 'release' / self._address
        link = self._link
        if version:
            path /= version
            link /= f'{version}/tree'
        else:
            link /= 'tree'
        return ShieldsBadge(path, link=link)

    def dependents(
            self,
            repo: bool = False
    ) -> ShieldsBadge:
        """
        Number of packages or repositories that depend on this package.

        Parameters
        ----------
        repo : bool, default: False
            Whether to query repositories (True) or packages (False).
        """
        path = self._url / ('dependent-repos' if repo else 'dependents') / self._address
        return ShieldsBadge(path, link=self._link)

    def source_rank(self) -> ShieldsBadge:
        """SourceRank ranking of the package."""
        return ShieldsBadge(self._url/'sourcerank'/self._address, link=self._link/'sourcerank')
