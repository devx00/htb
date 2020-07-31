"""Contains methods for interacting with the logged in user's account.

This module provides methods for accessing and modifying the user's account
details, including profile info, connection packs, etc.
"""

from htbapi.models import HTBObject


class HTBUser(HTBObject):
    """A HTB User Account."""

    objectendpoint = "/user/info"
    objectkey = "info"


