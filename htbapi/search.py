"""Contains methods for searching HTB.

This module contains methods for searching HTB for various types of elements,
including Users, Machines, Challenges, and Teams.
"""
import json
from htbapi.models import HTBTeam
from htbapi.models import HTBMachine
from htbapi.models import HTBChallenge
from htbapi.models import HTBProfile
from htbapi.models import HTBObject
from typing import Dict, List
from htbapi import session

searchtags = ["users", "machines", "challenges", "teams"]
objectclasses = {
    "users": HTBProfile,
    "machines": HTBMachine,
    "challenges": HTBChallenge,
    "teams": HTBTeam
}
def search(term: str, tags=searchtags) -> Dict[str, List[HTBObject]]:
    """Searches HTB for objects matching certain criteria.
    
    Searches HTB for objects matching :term: that are of a type 
    that is in :tags:.
    i.e. search("player", ["machines", "challenges"]) would return all machines
    and challenges that have "player" in its name.

    Note: Known issue when searching for certain terms we are
    receiving error "Failed to parse tags."

    Args:
        term: The search term to query HTB with.
        tags: A list of object types to search for. 
            Available types: users, machines, challenges, teams
    Returns:
        A dict containing object type names as keys, and a list of 
        matching objects of the respective types as the values.
    Raises:
        HTBRequestException: If a request fails.
    """
    resp = session.get("/search/fetch", params={"query": term, "tags": json.dumps(tags)})
    results = resp.json()
    # Map the results onto the proper classes according to the name of the keys.
    parsed = {objkey: [objectclasses[objkey](obj) for obj in results[objkey]] for objkey in results}
    return parsed
