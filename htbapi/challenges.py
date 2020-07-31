"""Methods pertaining to challenges on HTB.

This module contains classes and methods for working with challenges
on HTB.
"""


from htbapi.search import search
from htbapi.models import HTBChallenge
from typing import List


def findchallenges(name: str) -> List[HTBChallenge]:
    """Searches for challenges matching :name.

    Searches HTB for any challenges matching the name :name.
    
    Args:
        name: A partial or full name to search for.
    Returns:
        A list of matching challenges.
    """
    searchresults = search(name, tags=["challenges"])
    matches = searchresults["challenges"] if "challenges" in searchresults else []
    return matches

def findchallenge(name: str) -> HTBChallenge:
    """Finds a specific challenge by name.

    Searches HTB for a specific challenge matching the specified name
    and returns it if one is found. Otherwise returns None.

    Args:
        name: An exact challenge name to lookup.
    Returns:
        A HTBChallenge matching the requested name.
    """
    challenges = findchallenges(name)
    for challenge in challenges:
        if challenge.name == name:
            return challenge
