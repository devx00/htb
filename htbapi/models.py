"""Contains the base data models used for casting values returned from the API.

This module contains various classes and methods for working with HTB data.
"""

from htbapi.exceptions import HTBException
import htbapi

class HTBObjectLoadFailed(HTBException):
    pass

class HTBObject:
    """A basic HTB data object."""

    """The endpoint where this object can be loaded from."""
    objectendpoint: str = None

    """The key to access the object with when loading."""
    objectkey: str = None

    isloaded = False

    def __init__(self, obj: dict):
        """Initializes the object with a dict of values."""
        self.id = None
        if "value" in obj and not "name" in obj:
            # Search returns object names as the "value" property.
            obj["name"] = obj["value"]
        self.__dict__.update(obj)

    def load(self, force=False):
        """Loads this objects properties from the API.

        Loads all missing properties from the API. 
        Object id must already be set at the very minimum.

        Args:
            force: Whether to force load from the API even if already loaded.
        Raises:
            HTBObjectLoadFailed: If the object can't be loaded.
        """
        if self.objectendpoint is None and self.objectkey is None:
            msg = (f"Couldn't load {self.__class__.__name__}. "
                   f"{self.__class__.__name__} is not configured.")
            raise HTBObjectLoadFailed(msg)
        if not self.isloaded or force:
            endpoint = self.objectendpoint + str(self.id)
            resp = htbapi.session.get(endpoint)
            result = resp.json()
            obj = result[self.objectkey]
            self.__dict__.update(obj)
            self.isloaded = True


class HTBProfile(HTBObject):
    """A HTB user's profile."""

    objectendpoint = "/user/profile/basic/"
    objectkey = "profile"


class HTBMachine(HTBObject):
    """A machine on HTB"""
    
    objectendpoint = "/machine/profile/"
    objectkey = "info"


class HTBTeam(HTBObject):
    """A team on HTB"""
    pass


class HTBChallenge(HTBObject):
    """A challenge on HTB"""
    pass