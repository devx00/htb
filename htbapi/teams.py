"""Methods pertaining to teams on HTB.

This module contains classes and methods for working with teams
on HTB.
"""


from . import session
from .models import HTBObject
from typing import List, Optional
import json


class HTBTeam(HTBObject):
    """A team on HTB
    
    Attributes:
        id (int): The teams ID.
        name (str): The teams name.
        motto (str): The teams motto.
        respected (bool): Whether the current user respects this team or not.
        ranking (int): The teams global ranking.
        avatar (str): The path to the teams avatar image.
    """
    pass

def findteams(name: str) -> List[HTBTeam]:
    """Searches for teams matching :name.

    Searches HTB for any teams matching the name :name.
    
    Args:
        name: A partial or full name to search for.
    Returns:
        A list of matching teams.
    """
    resp = session.get(
        "/search/fetch", 
        params={"query": name, "tags": json.dumps(["teams"])})
    results = resp.json()
    searchresults = results["teams"] if "teams" in results else []
    matches = [HTBTeam(res) for res in searchresults]
    return matches

def findteam(name: str) -> Optional[HTBTeam]:
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
