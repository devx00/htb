"""Methods pertaining to machines on HTB.

This module contains classes and methods for working with machines
on HTB.
"""


from htbapi.search import search
from htbapi.models import HTBMachine
from typing import List


def findmachines(name: str) -> List[HTBMachine]:
    """Searches for machines matchine :name.

    Searches HTB for any machines matching the name :name.
    
    Args:
        name: A partial or full name to search for.
    Returns:
        A list of matching machines.
    """
    searchresults = search(name, tags=["machines"])
    matches = searchresults["machines"] if "machines" in searchresults else []
    return matches

def findmachine(name: str) -> HTBMachine:
    """Finds a specific machine by name.

    Searches HTB for a specific machine matching the specified name
    and returns it if one is found. Otherwise returns None.

    Args:
        name: An exact box name to lookup.
    Returns:
        A HTBMachine matching the requested name.
    """
    boxes = findmachines(name)
    for box in boxes:
        if box.name == name:
            return box
