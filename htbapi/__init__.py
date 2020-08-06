"""An unofficial library for working with HackTheBox's API.

This library provides an easy way to work with the HackTheBox API.
It supports querying machine info, challenge info, user info, and more.
"""
import logging
from . import client
from . import exceptions
from .client import Client
from .client import session
from .challenges import HTBChallenge
from .machines import HTBMachine
from .profiles import HTBProfile
from .teams import HTBTeam
from typing import Optional, Tuple

from .__version__ import __title__, __description__, __url__, __version__
from .__version__ import __build__, __author__, __author_email__, __license__
from .__version__ import __copyright__


def initialize(email: str, password: str, otp: str=None) -> Tuple[Optional[str], Optional[str]]:
    """Initialize the API Client.

    Initialize the client with credentials and optional otp if 2fa is enabled.
    If 2fa is enabled but an otp is not provided, all requests will fail until
    an otp is manually submitted through the client.

    Args:
        email: The email to authenticate with.
        password: The password to authenticate with.
        otp: The 2fa OTP to use is 2fa is enabled.
    Returns:
        A tuple containing the access token and refresh token for the session.
    """
    session.login(email, password, otp is not None)
    if session.needsOTP and otp is not None:
        session.submit2fa(otp)
    return (session.accesstoken, session.refreshtoken)


def restoresession(accesstoken: str, refreshtoken: str):
    """Restores a session with existing accesstoken and refreshtoken.
    
    Args:
        accesstoken: The access token from a previous session.
        refreshtoken: The refresh token from a previous session.
    """
    session.accesstoken = accesstoken
    session.refreshtoken = refreshtoken

