"""Methods pertaining to machines on HTB.

This module contains classes and methods for working with machines
on HTB.
"""


from . import session
from .models import HTBObject
from typing import List, Optional
import json


class HTBMachine(HTBObject):
    """A machine on HTB
    
    Attributes:
        id (int): The machine ID.
        name (str): The name of the machine.
        os (str): The OS of the machine.
        active (bool): Whether the machine is active.
        retired (bool): Whether the machine is retired.
        points (int): The number of points the machine is currently worth.
        static_points (int): The number of points the machine was worth.
        release (str): The timestamp of when the machine was released.
        user_owns_count (int): The number of user owns.
        root_owns_count (int): The number of root owns.
        free (bool): Whether the machine is available to non-vip users.
        authUserInUserOwns (bool): Whether the user has owned user.
        authUserInRootOwns (bool): Whether the user has owned root.
        authUserHasReviewed (bool): Whether the user has left a review.
        stars (float): Number of stars (rating) the box has.
        difficulty (int): The machine difficulty.
        avatar (str): The path to the machines avatar image.
        feedbackForChart (DifficultyChart): The difficulty chart data.
        difficultyText (str): The difficulty (Easy, Medium, Hard, Insane).
        isCompleted (bool): Whether the user has completed the box.
        last_reset_time (str): Time since last reset.
        playInfo (LiveMachineInfo): The live info of the machine.
        maker (HTBProfile): The profile of the maker.
        maker2 (HTBProfile): The profile of the second maker.
        authUserFirstUserTime (str): The time it took the user to own user.
        authUserFirstRootTime (str): The time it took the user to own root.
        userBlood (MachineBlood): The blood object for user blood.
        userBloodAvatar (str): The user blood user's avatar.
        rootBlood (MachineBlood): The blood object for root blood.
        rootBloodAvatar (str): The root blood user's avatar.
        firstUserBloodTime (str): The time it took for user blood to fall.
        firstRootBloodTime (str): The time it took for root blood to fall.
        recommended (bool): Whether this machine is recommended.
    """
    
    objectendpoint = "/machine/profile/"
    objectkey = "info"

def findmachines(name: str) -> List[HTBMachine]:
    """Searches for machines matchine :name.

    Searches HTB for any machines matching the name :name.
    
    Args:
        name: A partial or full name to search for.
    Returns:
        A list of matching machines.
    """

    resp = session.get(
        "/search/fetch", 
        params={"query": name, "tags": json.dumps(["machines"])})
    results = resp.json()
    searchresults = results["machines"] if "machines" in results else []
    matches = [HTBMachine(res) for res in searchresults]
    return matches

def findmachine(name: str) -> Optional[HTBMachine]:
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
