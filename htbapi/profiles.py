"""Methods pertaining to user profiles on HTB.

This module contains classes and methods for working with user profiles
on HTB.
"""

from . import session
from typing import List, Optional
from .models import HTBObject
import json

class HTBProfile(HTBObject):
    """A HTB user's profile.
    
    Attributes:
        id (int): The users ID.
        name (str): The user's username.
        timezone (str): The user's timezone.
        isVip (bool): Whether the user is a VIP member or not.
        avatar (str): The path to the user's avatar image.
        points (int): The number of points the user has.
        system_owns (int): The number of system owns the user has.
        user_owns (int): The number of user owns the user has.
        system_bloods (int): The number of system bloods the user has.
        user_bloods (int): The number of user bloods the user has.
        respects (int): The number of respects a user has.
        country_name (str): The country the user is from. Full name.
        country_code (str): The country the user is from. Abbreviation.
        team (HTBTeam): The user's team.
        university_name (str): The user's University.
        description (str): The user's profile description.
        github (str): A link to the user's github profile.
        linkedin (str): A link to the user's linkedin profile.
        twitter (str): A link to the user's twitter profile.
        website (str): A link to the user's website.
        isRespected (bool): Whether the authed user respects this user.
        isFollowed (bool): Whether the authed user follows this user.
        rank (str): The user's rank.
        rank_id (int): The rank ID of the user's rank.
        current_rank_progress (float): The percent progress to the next rank.
        next_rank (str): The next rank the user can level up to.
        next_rank_points (float): The total percent progress to the next rank.
        rank_ownership (str): The user's total completion percentage.
        rank_requirement (int): The percentage needed for the current rank.
        ranking (int): The user's global Hall of Fame ranking.
    """

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
