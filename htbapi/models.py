"""Contains the base data models used for casting values returned from the API.

This module contains various classes and methods for working with HTB data.
"""

import logging
from typing import Any, Optional
from .exceptions import HTBException
import htbapi

class HTBObjectLoadFailed(HTBException):
    pass

class DifficultyChart:
    """An object representing a difficulty chart.

    A wrapper class for the data representing a difficulty chart for a
    machine or challenge.
    """
    pass

class HTBObject:
    """A basic HTB data object."""

    objectendpoint: Optional[str] = None
    """The endpoint where this object can be loaded from."""

    objectkey: Optional[str] = None
    """The key to access the object with when loading."""

    def __init__(self, obj: dict):
        """Initializes the object with a dict of values."""

        self.id = None
        self.isloaded = False
        if "value" in obj and not "name" in obj:
            # Search returns object names as the "value" property.
            obj["name"] = obj["value"]
        self.__dict__.update(obj)

    def __getattr__(self, name: str) -> Any:
        """Attempts to load the object if the requested key is not found.

        Args:
            name: The requested key.
        Raises:
            AttributeError: If the requested key is still missing after a load
                            or if an object can't be loaded.
        """

        if self.objectendpoint is not None and not self.isloaded:
            try:
                logging.debug(
                    f"Loading [{self.__class__.__name__}]: {self.id}")
                self.load()
            except AttributeError:
                """Fail silently. 
                An AttributeError will be raised by __getattribute__.
                """

                pass
        
        return self.__getattribute__(name)

    @classmethod
    def fromname(cls, name):
        """Loads a {cls} object by name.

        This method should be overridden by any subclesses that support
        finding an object by name.

        Args:
            cls: The class of the object being loaded.
            name: The name of the object to load.
        Returns:
            A {cls} object.
        Raises:
            NotImplementedError: If {cls} does not support this method.
        """

        raise NotImplementedError()

    def load(self, force=False):
        """Loads this objects properties from the API.

        Loads all missing properties from the API if not already loaded.
        If force=True then it will reload from the API even if isloaded=True.
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
            logging.debug(f"After loading: {self.__dict__}")
