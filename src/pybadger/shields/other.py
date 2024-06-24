from pybadger import BadgeSettings as _BadgeSettings, Badge as _Badge
from pybadger import shields as _shields


def chat_discord(
    server_id: str,
    shields_settings: _shields.ShieldsSettings | None = None,
    badge_settings: _BadgeSettings | None = None,
) -> _Badge:
    """Number of online users in Discord server.

    Parameters
    ----------
    server_id : str
        Server ID of the Discord server (e.g., `102860784329052160`),
        which can be located in the url of the channel.
    shields_settings : pybadger.shields.ShieldsSettings, optional
            Settings for the Shields.io badge to override the default global settings.
    badge_settings : pybadger.BadgeSettings, optional
        Settings for the badge to override the default global settings.

    Notes
    -----
    A Discord server admin must enable the widget setting on the server for this badge to work.
    This can be done in the Discord app: Server Setting > Widget > Enable Server Widget

    References
    ----------
    [Shields.io API - Discord](https://shields.io/badges/discord)
    """
    return _shields.create(
        path=f"discord/{server_id}",
        shields_settings=shields_settings + _shields.ShieldsSettings(label="Discord"),
        badge_settings=badge_settings + _BadgeSettings(
            title="Number of online users in Discord server.",
            alt="Discord Users",
            link=f"https://discordapp.com/channel/{server_id}",
        ),
    )
