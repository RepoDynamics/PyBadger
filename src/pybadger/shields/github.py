from typing import Literal

import pylinks as _pylinks

from pybadger import BadgeSettings as _BadgeSettings, Badge as _Badge
from pybadger import shields as _shields
from pybadger.shields.badge import ShieldsBadger as _ShieldsBadger


class GitHubRepositoryBadger(_ShieldsBadger):
    """Shields.io GitHub badges."""

    def __init__(
        self,
        user: str,
        repo: str,
        branch: str | None = None,
        default_shields_settings: _shields.ShieldsSettings | None = None,
        default_badge_settings: _BadgeSettings | None = None,
    ):
        """
        Parameters
        ----------
        user : str
            GitHub username.
        repo : str
            GitHub repository name.
        branch : str, optional
            Repository branch name to use as default for branch-specific endpoints.
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
            endpoint_start="github",
            endpoint_key=f"{user}/{repo}",
            default_shields_settings=default_shields_settings,
            default_badge_settings=default_badge_settings
        )
        self.user = user
        self.repo = repo
        self.branch = branch
        self._repo_link = _pylinks.site.github.user(user).repo(repo)
        return

    def _branch(self, branch: str | None = None) -> str | None:
        """Get the branch to use for the badge."""
        if branch == "":
            return
        if branch:
            return branch
        if self.branch:
            return self.branch
        return

    def commit_activity(
        self,
        interval: Literal["t", "y", "m", "w"] = "t",
        author_filter: str | None = None,
        branch: str | None = None,
        shields_settings: _shields.ShieldsSettings | None = None,
        badge_settings: _BadgeSettings | None = None,
    ) -> _Badge:
        """Number of commits in a branch.

        Parameters
        ----------
        interval : {'t', 'y', 'm', 'w'}, default: 't'
            Interval of time to calculate the number of commits.
            - 't': total
            - 'y': last year
            - 'm': last month
            - 'w': last week
        author_filter : str, optional
            A GitHub username to only count commits by that user.
        branch: str, optional
            A specific branch to count commits in.
            If not provided, the default (i.e., main) branch of the repository is used.
            If the branch is not provided here but a default value is set
            in the `branch` attribute of this instance, that branch will be used.
            To use the default repository branch regardless of whether a default value is set or not,
            set this argument to an empty string.
        shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default instance settings.
        badge_settings : pybadger.BadgeSettings, optional
            Settings for the badge to override the default instance settings.

        References
        ----------
        - [Shields.io API - GitHub commit activity](https://shields.io/badges/git-hub-commit-activity)
        - [Shields.io API - GitHub commit activity (branch)](https://shields.io/badges/git-hub-commit-activity-branch)
        """
        before = ["commit-activity", interval]
        branch = self._branch(branch)
        after = [branch] if branch else []
        interval_text = {"y": "year", "m": "month", "w": "week"}
        title = (
            f"{'Total number' if interval == 't' else 'Number'} of commits "
            f"""{f"in branch '{branch}' " if branch else ''}"""
            f"{f'in the last {interval_text[interval]}' if interval != 't' else ''}. "
            "Click to see the full list of commits."
        )
        alt = "Commit activity"
        link = self._repo_link.branch(branch).commits if branch else self._repo_link.commits
        return _shields.create(
            path=self._create_path(before, after),
            queries={"authorFilter": author_filter},
            shields_settings=self._shields_settings(shields_settings) + _shields.ShieldsSettings(label="Commits"),
            badge_settings=self._badge_settings(badge_settings) + _BadgeSettings(title=title, alt=alt, link=link),
        )

    def commits_difference(
        self,
        base: str,
        head: str,
        shields_settings: _shields.ShieldsSettings | None = None,
        badge_settings: _BadgeSettings | None = None
    ) -> _Badge:
        """Number of commits between two references, i.e., branches, tags, or hashes.

        Parameters
        ----------
        base : str
            The base reference.
        head : str
            The head reference.
        shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default instance settings.
        badge_settings : pybadger.BadgeSettings, optional
            Settings for the badge to override the default instance settings.

        References
        ----------
        - [Shields.io API - GitHub commits difference between two branches/tags/commits](https://shields.io/badges/git-hub-commits-difference-between-two-branches-tags-commits)
        """
        title = f"Number of commits between '{base}' and '{head}'. Click to see the full list of commits."
        alt = "Commits difference"
        link = self._repo_link.compare(base, head)
        return _shields.create(
            path=self._create_path(["commits-difference"], []),
            queries={"base": base, "head": head},
            shields_settings=self._shields_settings(shields_settings) + _shields.ShieldsSettings(label="Commits Difference"),
            badge_settings=self._badge_settings(badge_settings) + _BadgeSettings(title=title, alt=alt, link=link),
        )

    def commits_since_latest_release(
        self,
        include_prereleases: bool = True,
        sort: Literal["date", "semver"] = "semver",
        filter: str | None = None,
        branch: str | None = None,
        shields_settings: _shields.ShieldsSettings | None = None,
        badge_settings: _BadgeSettings | None = None
    ) -> _Badge:
        """Number of commits since the latest release.

        Parameters
        ----------
        include_prereleases : bool, default: True
            Whether to include prereleases.
        sort : {'date', 'semver'}, default: 'semver'
            Sort the releases by date or by Semantic Versioning.
        filter : str, optional
            Filter the tags/release names before selecting the latest from the list.
            Two constructs are available:
            - `*` is a wildcard matching zero or more characters.
            - `!` negates the whole pattern.
        branch: str, optional
            A specific branch to look for releases.
            If not provided, the default (i.e., main) branch of the repository is used.
            If the branch is not provided here but a default value is set
            in the `branch` attribute of this instance, that branch will be used.
            To use the default repository branch regardless of whether a default value is set or not,
            set this argument to an empty string.
        shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default instance settings.
        badge_settings : pybadger.BadgeSettings, optional
            Settings for the badge to override the default instance settings.

        References
        ----------
        - [Shields.io API - GitHub commits since latest release](https://shields.io/badges/git-hub-commits-since-latest-release)
        - [Shields.io API - GitHub commits since latest release (branch)](https://shields.io/badges/git-hub-commits-since-latest-release-branch)
        """
        after = ["latest"]
        branch = self._branch(branch)
        if branch:
            after.append(branch)
        title = (
            f"Number of commits since the latest release{' on branch ' + branch if branch else ''}. "
            "Click to see the full list of commits."
        )
        alt = "Commits since latest release"
        link = self._repo_link.branch(branch).commits if branch else self._repo_link.commits
        return _shields.create(
            path=self._create_path(["commits-since"], after),
            queries={"include_prereleases": include_prereleases, "sort": sort, "filter": filter},
            shields_settings=self._shields_settings(shields_settings) + _shields.ShieldsSettings(label="Commits Since Latest Release"),
            badge_settings=self._badge_settings(badge_settings) + _BadgeSettings(title=title, alt=alt, link=link),
        )

    def commits_since_tag(
        self,
        tag: str,
        branch: str | None = None,
        shields_settings: _shields.ShieldsSettings | None = None,
        badge_settings: _BadgeSettings | None = None
    ) -> _Badge:
        """Number of commits since a specific tag.

        Parameters
        ----------
        tag : str
            The tag.
        branch: str, optional
            A specific branch to look for the tagged version.
            If not provided, the default (i.e., main) branch of the repository is used.
            If the branch is not provided here but a default value is set
            in the `branch` attribute of this instance, that branch will be used.
            To use the default repository branch regardless of whether a default value is set or not,
            set this argument to an empty string.
        shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default instance settings.
        badge_settings : pybadger.BadgeSettings, optional
            Settings for the badge to override the default instance settings.

        References
        ----------
        - [Shields.io API - GitHub commits since tagged version](https://shields.io/badges/git-hub-commits-since-tagged-version)
        - [Shields.io API - GitHub commits since tagged version (branch)](https://shields.io/badges/git-hub-commits-since-tagged-version-branch)
        """
        after = [tag]
        branch = self._branch(branch)
        if branch:
            after.append(branch)
        title = (
            f"Number of commits since tag '{tag}'{' on branch ' + branch if branch else ''}. "
            "Click to see the full list of commits."
        )
        alt = "Commits since version"
        link = self._repo_link.branch(branch).commits if branch else self._repo_link.commits
        return _shields.create(
            path=self._create_path(["commits-since"], after),
            shields_settings=self._shields_settings(shields_settings) + _shields.ShieldsSettings(label=f"Commits Since {tag}"),
            badge_settings=self._badge_settings(badge_settings) + _BadgeSettings(title=title, alt=alt, link=link),
        )

    def created_at(
        self,
        shields_settings: _shields.ShieldsSettings | None = None,
        badge_settings: _BadgeSettings | None = None
    ) -> _Badge:
        """Date of repository creation.

        Parameters
        ----------
        shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default instance settings.
        badge_settings : pybadger.BadgeSettings, optional
            Settings for the badge to override the default instance settings.

        References
        ----------
        - [Shields.io API - GitHub created at](https://shields.io/badges/git-hub-created-at)
        """
        return _shields.create(
            path=self._create_path(["created-at"], []),
            shields_settings=self._shields_settings(shields_settings) + _shields.ShieldsSettings(label="Created"),
            badge_settings=self._badge_settings(badge_settings) + _BadgeSettings(title="Repository creation date", alt="Repository creation date"),
        )

    def last_commit(
        self,
        path: str | None = None,
        display_timestamp: Literal["author", "committer"] = "author",
        branch: str | None = None,
        shields_settings: _shields.ShieldsSettings | None = None,
        badge_settings: _BadgeSettings | None = None
    ) -> _Badge:
        """Time of the last commit (of a file) in a branch.

        Parameters
        ----------
        path : str, optional
            A specific path in the repository to check for the last commit.
            If not provided, the last commit of the branch is selected.
        display_timestamp : {'author', 'committer'}, default: 'author'
            Whether to display the author's timestamp or the committer's timestamp.
        branch: str, optional
            A specific branch to look for the last commit.
            If not provided, the default (i.e., main) branch of the repository is used.
            If the branch is not provided here but a default value is set
            in the `branch` attribute of this instance, that branch will be used.
            To use the default repository branch regardless of whether a default value is set or not,
            set this argument to an empty string.
        shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default instance settings.
        badge_settings : pybadger.BadgeSettings, optional
            Settings for the badge to override the default instance settings.

        References
        ----------
        - [Shields.io API - GitHub last commit](https://shields.io/badges/git-hub-last-commit)
        - [Shields.io API - GitHub last commit (branch)](https://shields.io/badges/git-hub-last-commit-branch)
        """
        branch = self._branch(branch)
        after = [branch] if branch else []
        title = (
            f"Time of the last commit{' on branch ' + branch if branch else ''}. "
            "Click to see the full list of commits."
        )
        alt = "Last commit"
        link = self._repo_link.branch(branch).commits if branch else self._repo_link.commits
        return _shields.create(
            path=self._create_path(["last-commit"], after),
            queries={"path": path, "display_timestamp": display_timestamp},
            shields_settings=self._shields_settings(shields_settings) + _shields.ShieldsSettings(label="Last Commit"),
            badge_settings=self._badge_settings(badge_settings) + _BadgeSettings(title=title, alt=alt, link=link),
        )

    def release_date(
        self,
        include_prereleases: bool = True,
        display_date: Literal["created_at", "published_at"] = "created_at",
        shields_settings: _shields.ShieldsSettings | None = None,
        badge_settings: _BadgeSettings | None = None
    ) -> _Badge:
        """Date of the latest release.

        Parameters
        ----------
        include_prereleases : bool, default: True
            Whether to include prereleases.
        display_date : {'created_at', 'published_at'}, default: 'created_at'
            Whether to display the creation date of the release or the publication date.
        shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default instance settings.
        badge_settings : pybadger.BadgeSettings, optional
            Settings for the badge to override the default instance settings.

        References
        ----------
        - [Shields.io API - GitHub release date](https://shields.io/badges/git-hub-release-date)
        """
        return _shields.create(
            path=self._create_path(["release-date-pre" if include_prereleases else "release-date"], []),
            queries={"display_date": display_date},
            shields_settings=self._shields_settings(shields_settings) + _shields.ShieldsSettings(label="Latest Release"),
            badge_settings=self._badge_settings(badge_settings) + _BadgeSettings(title="Latest release date. Click to see more details in the Releases section of the repository.", alt="Latest release date", link=self._repo_link.releases(tag="latest")),
        )

    def language_count(
        self,
        shields_settings: _shields.ShieldsSettings | None = None,
        badge_settings: _BadgeSettings | None = None
    ) -> _Badge:
        """Number of programming languages used in the repository.

        Parameters
        ----------
        shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default instance settings.
        badge_settings : pybadger.BadgeSettings, optional
            Settings for the badge to override the default instance settings.

        References
        ----------
        - [Shields.io API - GitHub language count](https://shields.io/badges/git-hub-language-count)
        """
        return _shields.create(
            path=self._create_path(["languages", "count"], []),
            shields_settings=self._shields_settings(shields_settings) + _shields.ShieldsSettings(label="Languages"),
            badge_settings=self._badge_settings(badge_settings) + _BadgeSettings(title="Number of programming languages used in the project.", alt="Programming Languages"),
        )

    def search_hits(
        self,
        query: str,
        shields_settings: _shields.ShieldsSettings | None = None,
        badge_settings: _BadgeSettings | None = None
    ) -> _Badge:
        """Number of search hits in the repository.

        Parameters
        ----------
        query : str
            The search query.
        shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default instance settings.
        badge_settings : pybadger.BadgeSettings, optional
            Settings for the badge to override the default instance settings.

        References
        ----------
        - [Shields.io API - GitHub search hit counter](https://shields.io/badges/git-hub-search-hit-counter)
        """
        return _shields.create(
            path=self._create_path(["search"], [query]),
            shields_settings=self._shields_settings(shields_settings) + _shields.ShieldsSettings(label=query),
            badge_settings=self._badge_settings(badge_settings) + _BadgeSettings(title=f"Number of search hits for query '{query}' in the repository.", alt=f"Search Hits ({query})"),
        )

    def top_language(
        self,
        shields_settings: _shields.ShieldsSettings | None = None,
        badge_settings: _BadgeSettings | None = None
    ) -> _Badge:
        """The top language in the repository, and its share in percent.

        Parameters
        ----------
        shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default instance settings.
        badge_settings : pybadger.BadgeSettings, optional
            Settings for the badge to override the default instance settings.

        References
        ----------
        - [Shields.io API - GitHub top language](https://shields.io/badges/git-hub-top-language)
        """
        return _shields.create(
            path=self._create_path(["languages", "top"], []),
            shields_settings=self._shields_settings(shields_settings),
            badge_settings=self._badge_settings(badge_settings) + _BadgeSettings(title="Percentage of the most used programming language in the repository.", alt="Top Programming Language"),
        )

    def actions_workflow_status(
        self,
        workflow: str,
        branch: str | None = None,
        event: str | None = None,
        shields_settings: _shields.ShieldsSettings | None = None,
        badge_settings: _BadgeSettings | None = None
    ) -> _Badge:
        """Status of a GitHub Actions workflow.

        Parameters
        ----------
        workflow : str
            The name of the workflow file, e.g., 'ci.yaml'.
        branch : str, optional
            The branch to check the workflow status for.
            If not provided, the default (i.e., main) branch of the repository is used.
            If the branch is not provided here but a default value is set
            in the `branch` attribute of this instance, that branch will be used.
            To use the default repository branch regardless of whether a default value is set or not,
            set this argument to an empty string.
        event : str, optional
            The event that triggered the workflow.
        shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default instance settings.
        badge_settings : pybadger.BadgeSettings, optional
            Settings for the badge to override the default instance settings.

        References
        ----------
        - [Shields.io API - GitHub workflow status](https://shields.io/badges/git-hub-workflow-status)
        """
        branch = self._branch(branch)
        title = (
            f"Status of the GitHub Actions workflow '{workflow}'"
            f"{f' on branch {branch}' if branch else ''}"
            f"{f' for event {event}' if event else ''}."
            "Click to see more details in the Actions section of the repository."
        )
        alt = "Workflow Status"
        link = self._repo_link.branch(branch).workflow(workflow) if branch else self._repo_link.workflow(workflow)
        return _shields.create(
            path=self._create_path(["actions", "workflow", "status"], [workflow]),
            queries={"branch": branch, "event": event},
            shields_settings=self._shields_settings(shields_settings) + _shields.ShieldsSettings(label="Workflow"),
            badge_settings=self._badge_settings(badge_settings) + _BadgeSettings(title=title, alt=alt, link=link),
        )

    def branch_check_runs(
        self,
        branch: str,
        name_filter: str | None = None,
        shields_settings: _shields.ShieldsSettings | None = None,
        badge_settings: _BadgeSettings | None = None
    ) -> _Badge:
        """Status of GitHub Actions check-runs for a branch.

        Parameters
        ----------
        branch : str
            Branch name.
        name_filter : str, optional
            Name of a specific check-run.
        shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default instance settings.
        badge_settings : pybadger.BadgeSettings, optional
            Settings for the badge to override the default instance settings.

        References
        ----------
        - [Shields.io API - GitHub branch check runs](https://shields.io/badges/git-hub-branch-check-runs)
        """
        title = (
            f"Status of GitHub Actions check-runs on branch '{branch}'"
            f"{f' for check-run {name_filter}' if name_filter else ''}."
        )
        alt = "Check-Runs Status"
        return _shields.create(
            path=self._create_path(["check-runs"], [branch]),
            queries={"nameFilter": name_filter},
            shields_settings=self._shields_settings(shields_settings) + _shields.ShieldsSettings(label="Check Runs"),
            badge_settings=self._badge_settings(badge_settings) + _BadgeSettings(title=title, alt=alt),
        )

    def dependency_status(
        self,
        shields_settings: _shields.ShieldsSettings | None = None,
        badge_settings: _BadgeSettings | None = None,
    ) -> _Badge:
        """Dependency status for the package, according to Libraries.io.

        Parameters
        ----------
        shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default instance settings.
        badge_settings : pybadger.BadgeSettings, optional
            Settings for the badge to override the default instance settings.

        References
        ----------
        - [Shields.io API - Libraries.io dependency status for GitHub repo](https://shields.io/badges/libraries-io-dependency-status-for-git-hub-repo)
        """
        return _shields.create(
            path=f"librariesio/github/{self.user}/{self.repo}",
            shields_settings=self._shields_settings(shields_settings) + _shields.ShieldsSettings(
                label="Dependencies",
            ),
            badge_settings=self._badge_settings(badge_settings) + _BadgeSettings(
                title="Status of the project's dependencies.",
                alt="Dependency Status",
            ),
        )

    def downloads_all_releases(
        self,
        asset: str | None = None,
        shields_settings: _shields.ShieldsSettings | None = None,
        badge_settings: _BadgeSettings | None = None,
    ) -> _Badge:
        """Number of downloads of all releases.

        Parameters
        ----------
        asset : str, optional
            Name of a specific asset to query.
        shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default instance settings.
        badge_settings : pybadger.BadgeSettings, optional
            Settings for the badge to override the default instance settings.

        References
        ----------
        - [Shields.io API - GitHub Downloads (all assets, all releases)](https://shields.io/badges/git-hub-downloads-all-assets-all-releases)
        - [Shields.io API - GitHub Downloads (specific asset, all releases)](https://shields.io/badges/git-hub-downloads-specific-asset-all-releases)
        """
        return _shields.create(
            path=self._create_path(["downloads"], [asset if asset else "total"]),
            shields_settings=self._shields_settings(shields_settings) + _shields.ShieldsSettings(label="Downloads", logo="github"),
            badge_settings=self._badge_settings(badge_settings) + _BadgeSettings(
                title="Number of downloads of all releases from GitHub.",
                alt="GitHub Downloads",
                link=self._repo_link.releases(),
            ),
        )

    def downloads_release(
        self,
        asset: str | None = None,
        tag: str | Literal["latest"] = "latest",
        include_prereleases: bool = True,
        sort: Literal["date", "semver"] = "date",
        shields_settings: _shields.ShieldsSettings | None = None,
        badge_settings: _BadgeSettings | None = None,
    ) -> _Badge:
        """
        Number of downloads of a GitHub release.

        Parameters
        ----------
        asset : str, optional
            Name of a specific asset to query.
        tag : str, default: "latest"
            Release tag to query. Setting to 'latest' will query the latest release.
        include_prereleases : bool, default: True
            Whether to include pre-releases.
        sort : {'date', 'semver'}, default: 'date'
            Sort the releases by date or by Semantic Versioning.
            Only applicable if `tag` is set to 'latest'.
        shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default instance settings.
        badge_settings : pybadger.BadgeSettings, optional
            Settings for the badge to override the default instance settings.

        References
        ----------
        - [Shields.io API - GitHub Downloads (all assets, latest release)](https://shields.io/badges/git-hub-downloads-all-assets-latest-release)
        - [Shields.io API - GitHub Downloads (all assets, specific tag)](https://shields.io/badges/git-hub-downloads-all-assets-specific-tag)
        - [Shields.io API - GitHub Downloads (specific asset, latest release)](https://shields.io/badges/git-hub-downloads-specific-asset-latest-release)
        - [Shields.io API - GitHub Downloads (specific asset, specific tag)](https://shields.io/badges/git-hub-downloads-specific-asset-specific-tag)
        """
        return _shields.create(
            path=self._create_path(
                ["downloads-pre" if tag == "latest" and include_prereleases else "downloads"],
                [tag, asset if asset else "total"]
            ),
            queries={"sort": sort} if tag == "latest" else None,
            shields_settings=self._shields_settings(shields_settings) + _shields.ShieldsSettings(
                label="Downloads", logo="github"),
            badge_settings=self._badge_settings(badge_settings) + _BadgeSettings(
                title=f"Number of downloads from GitHub for the {'latest release' if tag == 'latest' else f'release tag {tag}'}. Click to see more details in the 'Releases' section of the repository.",
                alt="GitHub Downloads",
                link=self._repo_link.releases(tag=tag),
            ),
        )

    def issue_search_hits(
        self,
        query: str,
        shields_settings: _shields.ShieldsSettings | None = None,
        badge_settings: _BadgeSettings | None = None,
    ) -> _Badge:
        """Number of search hits for a query in issues/pull requests.

        Parameters
        ----------
        query : str
            The search query.
            For example, `type:issue is:closed label:bug`.
            For a full list of available filters and allowed values,
            see GitHub's documentation on [Searching issues and pull requests](https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests).
        shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default instance settings.
        badge_settings : pybadger.BadgeSettings, optional
            Settings for the badge to override the default instance settings.

        References
        ----------
        - [Shields.io API - GitHub issue custom search in repo](https://shields.io/badges/git-hub-issue-custom-search-in-repo)
        """
        return _shields.create(
            path=self._create_path(["issues-search"], []),
            queries={"query": query},
            shields_settings=self._shields_settings(shields_settings) + _shields.ShieldsSettings(label=query),
            badge_settings=self._badge_settings(badge_settings) + _BadgeSettings(
                title=f"Number of search hits for query '{query}' in repository issues/pulls.",
                alt=f"Search Hits ({query})",
            ),
        )

    def issue_details(
        self,
        kind: Literal["issues", "pulls"],
        number: int,
        property: Literal["state", "title", "author", "label", "comments", "age", "last-update", "milestone"],
        shields_settings: _shields.ShieldsSettings | None = None,
        badge_settings: _BadgeSettings | None = None,
    ) -> _Badge:
        """Details of an issue or pull request.

        Parameters
        ----------
        kind : {'issues', 'pulls'}
            Whether to query issues or pull requests.
        number : int
            The issue or pull request number.
        property : {'state', 'title', 'author', 'label', 'comments', 'age', 'last-update', 'milestone'}
            The property to display.
        shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default instance settings.
        badge_settings : pybadger.BadgeSettings, optional
            Settings for the badge to override the default instance settings.

        References
        ----------
        - [Shields.io API - GitHub issue/pull reqyest detail](https://shields.io/badges/git-hub-issue-pull-request-detail)
        """
        return _shields.create(
            path=self._create_path([kind, "detail", property], [str(number)]),
            shields_settings=self._shields_settings(shields_settings) + _shields.ShieldsSettings(label=f"{property.capitalize()} (#{number})"),
            badge_settings=self._badge_settings(badge_settings) + _BadgeSettings(
                title=f"{property.capitalize()} of the issue/pull number {number}.",
                alt=f"Issue Details",
            ),
        )

    def issue_count(
        self,
        kind: Literal["issues", "pulls"],
        state: Literal["open", "closed"] = "open",
        label: str | None = None,
        show_state: bool = True,
        shields_settings: _shields.ShieldsSettings | None = None,
        badge_settings: _BadgeSettings | None = None,
    ):
        """Number of open/closed issues or pull requests.

        Parameters
        ----------
        kind : {'issues', 'pulls'}
            Whether to query issues or pull requests.
        state : {'open', 'closed'}, default: 'open'
            Whether to query open or closed issues/pull requests.
        label : str, optional
            A specific GitHub label to filter issues/pulls.
        show_state : bool, default: True
            Whether to display the queried state on the right-hand side of the badge.
        shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default instance settings.
        badge_settings : pybadger.BadgeSettings, optional
            Settings for the badge to override the default instance settings.
        """
        variant = {
            ("issues", "open", True): "issues",
            ("issues", "open", False): "issues-raw",
            ("issues", "closed", True): "issues-closed",
            ("issues", "closed", False): "issues-closed-raw",
            ("pulls", "open", True): "issues-pr",
            ("pulls", "open", False): "issues-pr-raw",
            ("pulls", "closed", True): "issues-pr-closed",
            ("pulls", "closed", False): "issues-pr-closed-raw",
        }
        return _shields.create(
            path=self._create_path([variant[(kind, state, show_state)]], [label] if label else []),
            shields_settings=self._shields_settings(shields_settings) + _shields.ShieldsSettings(
                label=f"{kind.capitalize() if show_state else f'{state.capitalize()} {kind.capitalize()}'}{f' ({label})' if label else ''}",
            ),
            badge_settings=self._badge_settings(badge_settings) + _BadgeSettings(
                title=f"Number of {state} {kind}{f' with label {label}' if label else ''}.",
                alt=f"{state.capitalize()} {kind.capitalize()} Count",
            ),
        )

    def license(
        self,
        filename: str = "LICENSE",
        branch: str = "main",
        shields_settings: _shields.ShieldsSettings | None = None,
        badge_settings: _BadgeSettings | None = None,
    ) -> _Badge:
        """License of the GitHub repository.

        Parameters
        ----------
        filename : str, default: 'LICENSE'
            Name of the license file in the GitHub branch.
            This is used to create a link to the license.
        branch : str, default: 'main'
            The branch to look for the license file.
            This is used to create a link to the license.
        shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default instance settings.
        badge_settings : pybadger.BadgeSettings, optional
            Settings for the badge to override the default instance settings.

        References
        ----------
        - [Shields.io API - GitHub license](https://shields.io/badges/git-hub-license)
        """
        return _shields.create(
            path=self._create_path(["license"], []),
            shields_settings=self._shields_settings(shields_settings) + _shields.ShieldsSettings(label="License"),
            badge_settings=self._badge_settings(badge_settings) + _BadgeSettings(
                title=f"Project license. Click to read the complete license.",
                alt="License",
                link=self._repo_link.branch(branch).file(filename)
            ),
        )

    def deployment_status(
        self,
        environment: str,
        shields_settings: _shields.ShieldsSettings | None = None,
        badge_settings: _BadgeSettings | None = None,
    ) -> _Badge:
        """Deployment status of a GitHub environment.

        Parameters
        ----------
        environment : str
            The name of the deployment environment.
        shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default instance settings.
        badge_settings : pybadger.BadgeSettings, optional
            Settings for the badge to override the default instance settings.

        References
        ----------
        - [Shields.io API - GitHub deployments](https://shields.io/badges/git-hub-deployments)
        """
        return _shields.create(
            path=self._create_path(["deployments"], [environment]),
            shields_settings=self._shields_settings(shields_settings) + _shields.ShieldsSettings(label=f"Deployment ({environment})"),
            badge_settings=self._badge_settings(badge_settings) + _BadgeSettings(
                title=f"Deployment status for '{environment}' environment.",
                alt="Deployment Status",
            ),
        )

    def discussion_count(
        self,
        shields_settings: _shields.ShieldsSettings | None = None,
        badge_settings: _BadgeSettings | None = None,
    ) -> _Badge:
        """Number of discussions in the GitHub repository.

        Parameters
        ----------
        shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default instance settings.
        badge_settings : pybadger.BadgeSettings, optional
            Settings for the badge to override the default instance settings.

        References
        ----------
        - [Shields.io API - GitHub discussions](https://shields.io/badges/git-hub-discussions)
        """
        return _shields.create(
            path=self._create_path(["discussions"], []),
            shields_settings=self._shields_settings(shields_settings) + _shields.ShieldsSettings(
                label="Discussions"),
            badge_settings=self._badge_settings(badge_settings) + _BadgeSettings(
                title=f"Number of discussions. Click to open the Discussions section of the repository.",
                alt="Discussion Count",
                link=self._repo_link.discussions(),
            ),
        )

    def discussion_search_hits(
        self,
        query: str,
        shields_settings: _shields.ShieldsSettings | None = None,
        badge_settings: _BadgeSettings | None = None,
    ) -> _Badge:
        """Number of search hits for a query in discussions.

        Parameters
        ----------
        query : str
            The search query.
            For example, `is:answered answered-by:someUsername`.
            For a full list of available filters and allowed values,
            see GitHub's documentation on [Searching discussions](https://docs.github.com/en/search-github/searching-on-github/searching-discussions).
        shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default instance settings.
        badge_settings : pybadger.BadgeSettings, optional
            Settings for the badge to override the default instance settings.

        References
        ----------
        - [Shields.io API - GitHub discussions custom search in repo](https://shields.io/badges/git-hub-discussions-custom-search-in-repo)
        """
        return _shields.create(
            path=self._create_path(["discussions-search"], []),
            queries={"query": query},
            shields_settings=self._shields_settings(shields_settings) + _shields.ShieldsSettings(label=query),
            badge_settings=self._badge_settings(badge_settings) + _BadgeSettings(
                title=f"Number of search hits for query '{query}' in repository discussions.",
                alt=f"Discussions Search Hits ({query})",
            ),
        )

    def python_versions(
        self,
        pyproject_path: str,
        branch: str = "main",
        shields_settings: _shields.ShieldsSettings | None = None,
        badge_settings: _BadgeSettings | None = None,
    ) -> _Badge:
        """Supported Python versions read from `pyproject.toml` file.

        Parameters
        ----------
        pyproject_path : str, optional
            Path to the `pyproject.toml` file to read the supported Python versions from,
            e.g., `src/pyproject.toml`.
        branch : str, default: 'main'
            The branch to look for the `pyproject.toml` file.
        shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default instance settings.
        badge_settings : pybadger.BadgeSettings, optional
            Settings for the badge to override the default instance settings.

        References
        ----------
        - [Shields.io API - Python Version from PEP 621 TOML](https://shields.io/badges/python-version-from-pep-621-toml)
        """
        return _shields.create(
            path="python/required-version-toml",
            queries={"tomlFilePath": str(self._repo_link.branch(branch).file(pyproject_path, raw=True))},
            shields_settings=self._shields_settings(shields_settings) + _shields.ShieldsSettings(
                label="Supports Python",
            ),
            badge_settings=self._badge_settings(badge_settings) + _BadgeSettings(
                title="Supported Python versions",
                alt="Supported Python Versions",
            ),
        )

    def code_size(
        self,
        shields_settings: _shields.ShieldsSettings | None = None,
        badge_settings: _BadgeSettings | None = None,
    ) -> _Badge:
        """Code size in bytes.

        Parameters
        ----------
        shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default instance settings.
        badge_settings : pybadger.BadgeSettings, optional
            Settings for the badge to override the default instance settings.

        References
        ----------
        - [Shields.io API - GitHub code size in bytes](https://shields.io/badges/git-hub-code-size-in-bytes)
        """
        return _shields.create(
            path=self._create_path(["languages", "code-size"], []),
            shields_settings=self._shields_settings(shields_settings) + _shields.ShieldsSettings(
                label="Code Size",
            ),
            badge_settings=self._badge_settings(badge_settings) + _BadgeSettings(
                title="Code size",
                alt="Code Size",
            ),
        )

    def dir_count(
        self,
        path: str | None = None,
        typ: Literal["file", "dir"] | None = None,
        extension: str | None = None,
        shields_settings: _shields.ShieldsSettings | None = None,
        badge_settings: _BadgeSettings | None = None,
    ) -> _Badge:
        """Number of files/subdirectories directly in a directory (not recursive).

        Parameters
        ----------
        path : str, optional
            A path to count the files/directories in.
            If not provided, the count is for the root directory.
        typ : {'file', 'dir'}, optional
            Whether to count files or directories.
            If not provided, both files and directories are counted.
            Note that due to GitHub API's limit, if a directory contains more than 1000 files,
            the badge will show an inaccurate count.
        extension : str, optional
            Count only files with a specific extension.
            Specify the extension without a leading dot.
            Only applicable if `typ` is `file`.
        shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default instance settings.
        badge_settings : pybadger.BadgeSettings, optional
            Settings for the badge to override the default instance settings.

        References
        ----------
        - [Shields.io API - GitHub repo file or directory count](https://shields.io/badges/git-hub-repo-file-or-directory-count)
        - [Shields.io API - GitHub repo file or directory count (in path)](https://shields.io/badges/git-hub-repo-file-or-directory-count-in-path)
        """
        things = (
            "files and directories" if not typ else (
                "directories" if typ == "dir" else f"{f'{extension.upper()} ' if extension else ''}files"
            )
        )
        return _shields.create(
            path=self._create_path(["directory-file-count"], [path] if path else []),
            queries={"type": typ, "extension": extension},
            shields_settings=self._shields_settings(shields_settings) + _shields.ShieldsSettings(
                label="Files",
            ),
            badge_settings=self._badge_settings(badge_settings) + _BadgeSettings(
                title=f"Number of {things} in the {path if path else 'root'} directory",
                alt="File Count",
            ),
        )

    def repo_size(
        self,
        shields_settings: _shields.ShieldsSettings | None = None,
        badge_settings: _BadgeSettings | None = None,
    ) -> _Badge:
        """Total size of the repository in bytes.

        Parameters
        ----------
        shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default instance settings.
        badge_settings : pybadger.BadgeSettings, optional
            Settings for the badge to override the default instance settings.

        References
        ----------
        - [Shields.io API - GitHub repo size](https://shields.io/badges/git-hub-repo-size)
        """
        return _shields.create(
            path=self._create_path(["repo-size"], []),
            shields_settings=self._shields_settings(shields_settings) + _shields.ShieldsSettings(
                label="Repo Size",
            ),
            badge_settings=self._badge_settings(badge_settings) + _BadgeSettings(
                title=f"Total size of the repository.",
                alt="Repository Size",
            ),
        )

    def forks(
        self,
        shields_settings: _shields.ShieldsSettings | None = None,
        badge_settings: _BadgeSettings | None = None,
    ) -> _Badge:
        """Number of repository forks.

        Parameters
        ----------
        shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default instance settings.
        badge_settings : pybadger.BadgeSettings, optional
            Settings for the badge to override the default instance settings.

        References
        ----------
        - [Shields.io API - GitHub forks](https://shields.io/badges/git-hub-forks)
        """
        return _shields.create(
            path=self._create_path(["forks"], []),
            shields_settings=self._shields_settings(shields_settings) + _shields.ShieldsSettings(
                label="Forks",
            ),
            badge_settings=self._badge_settings(badge_settings) + _BadgeSettings(
                title=f"Number of repository forks",
                alt="Forks",
            ),
        )

    def stars(
        self,
        shields_settings: _shields.ShieldsSettings | None = None,
        badge_settings: _BadgeSettings | None = None,
    ) -> _Badge:
        """Number of repository stars.

        Parameters
        ----------
        shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default instance settings.
        badge_settings : pybadger.BadgeSettings, optional
            Settings for the badge to override the default instance settings.

        References
        ----------
        - [Shields.io API - GitHub Repo stars](https://shields.io/badges/git-hub-repo-stars)
        """
        return _shields.create(
            path=self._create_path(["stars"], []),
            shields_settings=self._shields_settings(shields_settings) + _shields.ShieldsSettings(
                label="Stars",
            ),
            badge_settings=self._badge_settings(badge_settings) + _BadgeSettings(
                title=f"Number of repository stars",
                alt="Stars",
            ),
        )

    def watchers(
        self,
        shields_settings: _shields.ShieldsSettings | None = None,
        badge_settings: _BadgeSettings | None = None,
    ) -> _Badge:
        """Number of repository watchers.

        Parameters
        ----------
        shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default instance settings.
        badge_settings : pybadger.BadgeSettings, optional
            Settings for the badge to override the default instance settings.

        References
        ----------
        - [Shields.io API - GitHub watchers](https://shields.io/badges/git-hub-watchers)
        """
        return _shields.create(
            path=self._create_path(["watchers"], []),
            shields_settings=self._shields_settings(shields_settings) + _shields.ShieldsSettings(
                label="Watchers",
            ),
            badge_settings=self._badge_settings(badge_settings) + _BadgeSettings(
                title=f"Number of repository watchers",
                alt="Watchers",
            ),
        )

    def version(
        self,
        source: Literal["tag", "release"] = "release",
        display_name: Literal["tag", "release"] | None = "release",
        sort: Literal["date", "semver"] = "date",
        filter: str | None = None,
        include_prereleases: bool = True,
        shields_settings: _shields.ShieldsSettings | None = None,
        badge_settings: _BadgeSettings | None = None,
    ) -> _Badge:
        """Latest version of the software.

        Parameters
        ----------
        source : {'tag', 'release'}, default: 'release'
            Whether to get the latest version from tags or releases.
        display_name : {'tag', 'release'}, default: 'release'
            Whether to display the tag name or release name.
            Only applicable if `source` is set to 'release'.
        sort : {'date', 'semver'}, default: 'date'
            Sort the releases by date or by Semantic Versioning.
        filter : str, optional
            Filter the tags/release names before selecting the latest from the list.
            Two constructs are available:
            - `*` is a wildcard matching zero or more characters.
            - `!` negates the whole pattern.
        include_prereleases : bool, default: True
            Whether to include pre-releases.
        shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default instance settings.
        badge_settings : pybadger.BadgeSettings, optional
            Settings for the badge to override the default instance settings.

        References
        ----------
        - [Shields.io API - GitHub Release](https://shields.io/badges/git-hub-release)
        - [Shields.io API - GitHub Tag](https://shields.io/badges/git-hub-tag)
        """
        queries = {"sort": sort, "filter": filter, "include_prereleases": include_prereleases}
        if source == "release":
            queries["display_name"] = display_name
        return _shields.create(
            path=self._create_path(["v", source], []),
            queries=queries,
            shields_settings=self._shields_settings(shields_settings) + _shields.ShieldsSettings(
                label="Latest Version",
            ),
            badge_settings=self._badge_settings(badge_settings) + _BadgeSettings(
                title=f"Latest version of the package. Click to see more details in the 'Releases' section of the repository.",
                alt="Latest Version",
                link=self._repo_link.releases(tag="latest"),
            ),
        )

    def milestone_count(
        self,
        state: Literal["open", "closed", "all"] = "all",
        shields_settings: _shields.ShieldsSettings | None = None,
        badge_settings: _BadgeSettings | None = None,
    ) -> _Badge:
        """Number of milestones in the repository.

        Parameters
        ----------
        state : {'open', 'closed', 'all'}, default: 'all'
            Whether to count open, closed, or all milestones.
        shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default instance settings.
        badge_settings : pybadger.BadgeSettings, optional
            Settings for the badge to override the default instance settings.

        References
        ----------
        - [Shields.io API - GitHub number of milestones](https://shields.io/badges/git-hub-number-of-milestones)
        """
        return _shields.create(
            path=self._create_path(["milestones", state], []),
            shields_settings=self._shields_settings(shields_settings) + _shields.ShieldsSettings(
                label=f"{state.upper()} Milestones",
            ),
            badge_settings=self._badge_settings(badge_settings) + _BadgeSettings(
                title=f"Number of {state} milestones. Click to see more details in the Milestones section of the repository.",
                alt="Milestone Count",
                link=self._repo_link.milestones(state=state if state == "closed" else "open"),
            ),
        )
