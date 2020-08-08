"""Contains methods for interacting with the logged in user's account.

This module provides methods for accessing and modifying the user's account
details, including profile info, connection packs, etc.
"""

from .models import HTBObject


class HTBUser(HTBObject):
    """A HTB User Account.
    
    Since this class is for accessing the current user's account it is meant to
    be a singleton class and not manually instantiated. 

    Attributes:
        id (int): The user's ID.
        name (str): The user's username.
        email (str): The user's email.
        timezone (str): The user's timezone.
        isVip (bool): Whether the user is a VIP member or not.
        canAccessVIP (bool): Whether the user has access to the VIP servers.
        isServerVIP (bool): Whether the user's current server is a VIP server.
        server_id (int): The ID of the user's current VPN server.
        avatar (str): The path to the user's avatar image.
        profile (HTBProfile): The user's profile.
    """

    objectendpoint = "/user/info"
    objectkey = "info"


