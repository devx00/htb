"""Methods pertaining to teams on HTB.

This module contains classes and methods for working with teams
on HTB.
"""


from htbapi.search import search
from htbapi.models import HTBTeam
from typing import List


def findteams(name: str) -> List[HTBTeam]:
    """Searches for teams matching :name.

    Searches HTB for any teams matching the name :name.
    
    Args:
        name: A partial or full name to search for.
    Returns:
        A list of matching teams.
    """
    searchresults = search(name, tags=["teams"])
    matches = searchresults["teams"] if "teams" in searchresults else []
    return matches

def findteam(name: str) -> HTBTeam:
    """Finds a specific team by name.

    Searches HTB for a specific team matching the specified name
    and returns it if one is found. Otherwise returns None.

    Args:
        name: An exact team name to lookup.
    Returns:
        A HTBTeam matching the requested name.
    """
    teams = findteams(name)
    for team in teams:
        if team.name == name:
            return team
