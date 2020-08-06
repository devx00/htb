"""Methods pertaining to challenges on HTB.

This module contains classes and methods for working with challenges
on HTB.
"""


from . import session
from .models import HTBObject
from typing import List, Optional
import json

class HTBChallenge(HTBObject):
    """A challenge on HTB
    
    Attributes:
        id (int): The challenge ID.
        name (str): The name of the challenge.
        retired (bool): Whether the challenge is retired.
        difficulty (str): The challenge difficulty (Easy, Medium Hard, Insane)
        points (int): The number of points the challenge is worth.
        difficulty_chart (DifficultyChart): The difficulty chart data.
        solves (int): The number of solves the challenge has.
        authUserSolve (bool): Whether the current user has solved this.
        authUserSolveTime (str): The time from release when the user solved it.
        likes (int): The number of likes this challenge has.
        dislikes (int): The number of dislikes this challenge has.
        description (str): The challenge description.
        category_name (str): The category the challenge is in.
        first_blood_user (str): The username of the blood user.
        first_blood_user_id (int): The id of the blood user.
        first_blood_time (str): The time since release it took to get blood.
        first_blood_user_avatar (str): The blood user's avatar image path.
        creator_id (int): The creator's user id.
        creator_name (str): The creator's username.
        creator_avatar (str): The creator's avatar image path.
        isRespected (bool): Whether the creator is respected by the curr user.
        download (bool): Whether this challenge has files to download.
        sha256 (str): The sha256 checksum of the downloadable files.
        docker (bool): Whether this challenge has a docker instance.
        docker_port (int): The port of the challenges running docker instance.
        release_date (str): The date the challenge was released.
        likeByAuthUser (bool): Whether the user liked the challenge.
        dislikeByAuthUser (bool): Whether the user disliked the challenge.
        isTodo (bool): Whether this challenge is marked as todo.
        recommended (bool): Whether this challenge is recommended.
    """

    objectendpoint = "/challenge/info/"
    objectkey = "challenge"
    

def findchallenges(name: str) -> List[HTBChallenge]:
    """Searches for challenges matching :name.

    Searches HTB for any challenges matching the name :name.
    
    Args:
        name: A partial or full name to search for.
    Returns:
        A list of matching challenges.
    """

    resp = session.get(
        "/search/fetch", 
        params={"query": name, "tags": json.dumps(["challenges"])})
    results = resp.json()
    searchresults = results["challenges"] if "challenges" in results else []
    matches = [HTBChallenge(res) for res in searchresults]
    return matches

def findchallenge(name: str) -> Optional[HTBChallenge]:
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
