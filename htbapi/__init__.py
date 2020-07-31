"""Initializes the package and provides some helper methods.

This module initializes the htbapi package and provides some helper methods for
authenticating and restoring sessions, as well as other setup and config tasks.
"""

from typing import Tuple
from .client import Client

session = Client()


def initialize(email: str, password: str, otp: str=None) -> Tuple[str, str]:
    """Initialize the API Client.

    Initialize the client with credentials and optional otp if 2fa is enabled.
    If 2fa is enabled but an otp is not provided, all requests will fail until
    an otp is manually submitted through the client.

    Args:
        email: The email to authenticate with.
        password: The password to authenticate with.
        otp: Optional; The 2fa OTP to use is 2fa is enabled.
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

