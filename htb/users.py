from .search import search


def find(username, exact=False):
    """
    Searches HTB for for the supplied search term
    and returns any matching User objects.
    If exact == True this will return the user
    with the matching username if one exists, else None.
    """
    searchresults = search(username, tags=["users"])
    matches = searchresults["users"] if "users" in searchresults else []
    if not exact:
        return matches
    else:
        for user in matches:
            if user.name == username:
                return user
