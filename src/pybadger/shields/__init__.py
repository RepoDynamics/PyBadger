"""Dynamically create badges using the shields.io API.

References
----------
* https://shields.io/
* https://github.com/badges/shields
"""

from pybadger.shields.badge import create, ShieldsSettings, shields_settings_default
from pybadger.shields import core, binder, codecov, conda, github, lib_io, other, pypi, rtd

