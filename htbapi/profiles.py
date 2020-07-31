"""Methods pertaining to user profiles on HTB.

This module contains classes and methods for working with user profiles
on HTB.
"""

from typing import List
from htbapi.models import HTBProfile
from htbapi.search import search




def findprofiles(username: str) -> List[HTBProfile]:
    """Searches for profiles matchine :username:.

    Searches HTB for any user profiles matching the username :username.
    
    Args:
        username: A partial or full username to search for.
    Returns:
        A list of matching profiles.
    """
    searchresults = search(username, tags=["users"])
    matches = searchresults["users"] if "users" in searchresults else []
    return matches

def findprofile(username: str) -> HTBProfile:
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
