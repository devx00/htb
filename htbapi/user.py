"""Contains methods for interacting with the logged in user's account.

This module provides methods for accessing and modifying the user's account
details, including profile info, connection packs, etc.
"""

from .models import HTBObject


class HTBUser(HTBObject):
    """A HTB User Account.
    
    Since this class is for accessing the current user's account it is meant to
    be a singleton class and not manually instantiated. 
    """

    objectendpoint = "/user/info"
    objectkey = "info"


