"""The main module for sending requests to the API.

The Client class is the main Session object that is used
to communicate with the API.
It is recommended not to use this class directly.
Instead one sheould use the methods provided in the module
respective to what object you are working with.

ie. Use the htb.machines module when working with a Machine

TODO: Improve exception handling. 
TODO: Make more specific Exception types and messages.
"""
from typing import Optional
import requests
from requests import Session, Request, Response
from requests.models import PreparedRequest
from urllib3.exceptions import InsecureRequestWarning
import json


from .exceptions import HTBException
from .exceptions import HTBRequestException
from .exceptions import HTBFurtherAuthRequired

BASEURL = "https://www.hackthebox.eu/api/v4"
def disablesslwarnings():
    """This is just for debugging purposes so I could use Burp"""
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning) # pylint: disable=no-member

class Client(Session):
    @staticmethod
    def url(endpoint: str) -> str:
        """
        Takes an endpoint and returns the full URL.

        Args:
            endpoint: The relative path to convert.
        Returns:
            The full URL for the endpoint
        """
        if endpoint[0] != "/":
            endpoint = "/" + endpoint
        return BASEURL + endpoint

    @property
    def needsOTP(self) -> bool:
        """
        Checks to see if 2fa is enabled and if it is checks 
        whether or not the session token is already authorized with one or not.

        Returns:
            Whether an OTP is required to complete authentication.
        """
        return self.is2faEnabled and not self.tokenHas2FA

    @property
    def isAuthenticated(self) -> bool:
        """
        Checks that session has an access token and that an OTP is not
        required to proceed.

        Returns:
            Whether session is fully authenticated including 2fa if enabled.
        """
        return self.accesstoken is not None \
            and not self.needsOTP

    @property
    def accesstoken(self) -> Optional[str]:
        """The current access token for authentication"""
        return self._accesstoken

    @accesstoken.setter
    def accesstoken(self, new: Optional[str]):
        """
        The setter for accesstoken. Makes sure to change
        the Authorization header when a new value is specified

        Args:
            new: The new access token to use for auth.
        """
        self._accesstoken = new
        if new is not None:
            self.headers["Authorization"] = f"Bearer {new}"
        elif "Authorization" in self.headers:
            del self.headers["Authorization"]

    def __init__(self):
        """
        Initializes a client object. If persist is True then the session token
        and refresh token are stored with the storage module.
        Note: The storage module also needs to be configured for this to
        properly store the session.
        """
        super().__init__()
        self.headers['User-Agent'] = "Python HTB API"
        self.headers['Accept'] = "application/json, text/plain, */*"
        self.accesstoken = None
        self.refreshtoken = None
        self.is2faEnabled = False
        self.tokenHas2FA = False

    def send(self, request: PreparedRequest, store=True, **kwargs) -> Response:
        """
        Sends the prepared request that is stored in self._request
        and stores the response in self._response.

        Args:
            request: The prepared Request to send.
            store: Whether to store the Request for future retry.
        Returns:
            The Response object.
        Raises:
            HTBRequestException: If the request fails.
        """
        if store:
            self._request = request
        self._response = super().send(request, **kwargs)
        self.checkresponse()
        return self._response

    def get(self, endpoint: str, **kwargs) -> Response:
        """
        Issue a GET request to the endpoint with the query params specified
        using the shared session.

        Args:
            endpoint: The api endpoint to send request to (ie /user/info).
        Returns:
            The Response object.
        Raises:
            HTBRequestException: If the request fails.
        """
        req = self.prepare_request(
            Request("GET", Client.url(endpoint), **kwargs))
        return self.send(req)

    def post(self, endpoint: str, **kwargs) -> Response:
        """
        Issue a POST request to the endpoint with the JSON data specified
        and the query params specified using the shared session.

        Args:
            endpoint: The api endpoint to send request to (ie /user/info).
        Returns:
            The Response object.
        Raises:
            HTBRequestException: If the request fails.
        """
        req = self.prepare_request(
            Request("POST", Client.url(endpoint), **kwargs))
        return self.send(req)

    def login(self, email: str, password: str, ignore2fa=False):
        """
        Login to the HTB API with the given username and password.
        If the user requires 2fa then a HTBFurtherAuthRequired exception
        will be raised unless ignore2fa=True. In that case the user must
        check client.needsOTP and then call submit2fa manually if required.

        Args:
            email: The user's email to login with.
            password: The user's password.
            ignore2fa: Whether to suppress HTBFurtherAuthRequired.
        Raises:
            HTBFurtherAuthRequired: If 2FA is enabled and ignore2fa=False.
            HTBRequestException: If the request fails.
        """
        url = Client.url("/login")
        req = self.prepare_request(
            Request("POST",
                    url,
                    json={
                        "email": email,
                        "password": password,
                        "remember": True
                    }))
        resp = self.send(req, False)
        body = resp.json()
        msg = body["message"]
        self.accesstoken = msg["access_token"]
        self.refreshtoken = msg["refresh_token"]
        self.is2faEnabled = msg["is2FAEnabled"]
        self.tokenHas2FA = False
        if not ignore2fa and self.needsOTP:
            raise HTBFurtherAuthRequired()

    def submit2fa(self, code: str):
        """
        Submits the 2fa code, or backup code, if the user requires it.
        If the code is 6 digits long it is assumed to be a normal code,
        if it is 20 characters it is assumed to be a backup code.

        Args:
            code: The OTP generated by authenticator app, or a backup code.
        Raises:
            HTBException: If the code is invalid.
            HTBRequestException: If the request fails.
        """
        if len(code) == 6:
            url = Client.url("/2fa/login")
            data = {"one_time_password": code}
        elif len(code) == 20:
            url = Client.url("/2fa/login/bypass")
            data = {"backup_code": code}
        else:
            raise HTBException("Invalid Two Factor Authorization Code")

        req = self.prepare_request(Request("POST", url, json=data))
        resp = super().send(req)
        if resp.status_code == 200:
            self.tokenHas2FA = True

    def refreshsession(self, ignore2fa=False):
        """
        Attempts to refresh the current session using the provided
        token or a previously cached token.
        If the user requires 2fa then a HTBFurtherAuthRequired exception
        will be raised unless ignore2fa=True. In that case the user must
        check client.needsOTP and then call submit2fa manually if required.
        
        Args:
            ignore2fa: Whether to suppress HTBFurtherAuthRequired.
        Raises:
            HTBFurtherAuthRequired: If 2FA is enabled and ignore2fa=False. 
        """
        url = Client.url("/login/refresh")
        req = self.prepare_request(
            Request("POST", url, json={"refresh_token": self.refreshtoken}))
        self.refreshtoken = None
        resp = self.send(req, False)
        body = resp.json()
        msg = body["message"]
        self.accesstoken = msg["access_token"]
        self.refreshtoken = msg["refresh_token"]
        if self.needsOTP:
            raise HTBFurtherAuthRequired()

    def logout(self):
        """
        Logs the current session out and removes all tokens.

        Raises:
            HTBRequestException: If the request fails.
        """
        self.post("/logout")
        self.accesstoken = None
        self.refreshtoken = None

    def checkresponse(self):
        """
        Checks the response for errors and raises an Exception
        when one is found.

        Raises:
            HTBRequestException: If the request contains errors.
        """
        if self._response is not None:
            if self._response.status_code > 400:
                exception = HTBRequestException(self._response)
                if (exception.code == 401 and self.refreshtoken is not None):
                    self.refreshsession()
                    self.retry()
                else:
                    raise exception
            try:
                r = self._response.json()
                if "error" in r:
                    raise HTBException(r["error"])
            except json.decoder.JSONDecodeError:
                pass
        else:
            raise HTBRequestException(None)

    def retry(self):
        """
        Retries the last request if possible.

        Raises:
            HTBRequestException: If the request fails.
        """
        if self._request is not None:
            return self.send(self._request)


session = Client()
