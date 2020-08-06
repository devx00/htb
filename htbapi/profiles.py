"""Methods pertaining to user profiles on HTB.

This module contains classes and methods for working with user profiles
on HTB.
"""

from . import session
from typing import List, Optional
from .models import HTBObject
import json

class HTBProfile(HTBObject):
    """A HTB user's profile."""

    objectendpoint = "/user/profile/basic/"
    objectkey = "profile"


def findprofiles(username: str) -> List[HTBProfile]:
    """Searches for profiles matchine :username:.

    Searches HTB for any user profiles matching the username :username.
    
    Args:
        username: A partial or full username to search for.
    Returns:
        A list of matching profiles.
    """

    resp = session.get(
        "/search/fetch", 
        params={"query": username, "tags": json.dumps(["users"])})
    results = resp.json()
    searchresults = results["users"] if "users" in results else []
    matches = [HTBProfile(prof) for prof in searchresults]
    return matches

def findprofile(username: str) -> Optional[HTBProfile]:
    """Finds a specific profile by username.

    Searches HTB for a specific user profile matching the specified username
    and returns it if one is found. Otherwise returns None.

    Args:
        username: An exact username to lookup.
    Returns:
        A HTBProfile matching the requested username.
    """
    profiles = findprofiles(username)
    for profile in profiles:
        if profile.name == username:
            return profile
