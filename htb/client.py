from requests import Session, Request
from . import storage
from . import exceptions


BASEURL = "https://www.hackthebox.eu/api/v4"


class Client(Session):

    @property
    def sessiontoken(self):
        """
        Returns the current session token or loads one if using
        persistent sessions and one has previously been stored.
        """
        if self._sessiontoken is None and self.persist:
            self._sessiontoken = storage.loadkey("SESSION_TOKEN")
        return self._sessiontoken

    @sessiontoken.setter
    def sessiontoken(self, token):
        """
        Sets the session's auth bearer header with the value of the
        new token.
        """
        self._sessiontoken = token
        if token is None:
            del self.headers['Authorization']
        else:
            self.headers['Authorization'] = f"Bearer {token}"
        if self.persist:
            storage.setkey("SESSION_TOKEN", token)

    @sessiontoken.deleter
    def sessiontoken(self):
        """
        Deletes the current session token.
        """
        self._sessiontoken = None
        del self.headers['Authorization']
        if self.persist:
            storage.delkey("SESSION_TOKEN")

    @property
    def refreshtoken(self):
        """
        Returns the current refresh token or loads one if using
        persistent sessions and one has previously been stored.
        """
        if self._refreshtoken is None and self.persist:
            self._refreshtoken = storage.loadkey("REFRESH_TOKEN")
        return self._refreshtoken

    @refreshtoken.setter
    def refreshtoken(self, token):
        """
        Sets a new refresh token.
        """
        self._refreshtoken = token
        if self.persist:
            storage.setkey("REFRESH_TOKEN", token)

    @refreshtoken.deleter
    def refreshtoken(self):
        """
        Deletes the current refresh token.
        """
        self._refreshtoken = None
        if self.persist:
            storage.delkey("REFRESH_TOKEN")

    @staticmethod
    def url(endpoint):
        """
        Takes an endpoint and returns the full URL.
        """
        if endpoint[0] != "/":
            endpoint = "/" + endpoint
        return f"{BASEURL}{endpoint}"

    def __init__(self, persist=True):
        """
        Initializes a client object. If persist is True then the session token
        and refresh token are stored with the storage module.
        Note: The storage module also needs to be configured for this to
        properly store the session.
        """
        self.persist = persist
        super().__init__(self)
        self.headers['User-Agent'] = "Python HTB API"
        self.headers['Accept'] = "application/json, text/plain, */*"

    def send(self, request, store=True, **kwargs):
        """
        Sends the prepared request that is stored in self._request
        and stores the response in self._response.
        """
        if store:
            self._request = request
        self._response = super().send(request, kwargs)
        self.checkresponse()
        return self._response

    def get(self, endpoint, **kwargs):
        """
        Issue a GET request to the endpoint with the query params specified
        using the shared session.
        """
        req = self.prepare_request(
            Request("GET", Client.url(endpoint), kwargs))
        return self.send(req)

    def post(self, endpoint, **kwargs):
        """
        Issue a POST request to the endpoint with the JSON data specified
        and the query params specified using the shared session.
        """
        req = self.prepare_request(
            Request("POST", Client.url(endpoint), kwargs))
        return self.send(req)

    def login(self, email, password, ignore2fa=False):
        """
        Login to the HTB API with the given username and password.
        If the user requires 2fa this method raises
        the AuthRequires2fa Exception unless ignore2fa is True.
        """
        url = Client.url("/login")
        req = self.prepare_request(
            Request("POST", url, json={
                "email": email,
                "password": password,
                "remember": True
                }))
        resp = self.send(req, False)
        body = resp.json()
        msg = body["message"]
        self.sessiontoken = msg["access_token"]
        self.refreshtoken = msg["refresh_token"]
        is2faEnabled = msg["is2FAEnabled"]
        if is2faEnabled:
            raise exceptions.FurtherAuthRequired()

    def submit2fa(self, code):
        """
        Submits the 2fa code, or backup code, if the user requires it.
        If the code is 6 digits long it is assumed to be a normal code,
        if it is 20 characters it is assumed to be a backup code.
        """

    def refreshsession(self):
        """
        Attempts to refresh the current session using the provided
        token or a previously cached token.
        """
        token = self.refreshtoken
        del self.refreshtoken
        url = Client.url("/login/refresh")
        req = self.prepare_request(
            Request("POST", url, json={"refresh_token": token}))
        resp = self.send(req, False)
        body = resp.json()
        msg = body["message"]
        self.sessiontoken = msg["access_token"]
        self.refreshtoken = msg["refresh_token"]
        # TODO: Raise Exception When 2fa is raquired
        # tokenHas2fa = msg["tokenHas2FA"]
        # is2faEnabled = msg["is2FAEnabled"]

    def logout(self):
        """
        Logs the current session out and removes all tokens.
        """
        self.post("/logout")
        del self.sessiontoken
        del self.refreshtoken

    def checkresponse(self):
        """
        Checks the response for errors and raises an Exception
        when one is found.
        """
        if self._response is not None:
            exception = exceptions.httpcode_exception(
                self._response.status_code)
            if exception is not None:
                if (
                    type(exception) == exceptions.UnauthorizedException and
                    self.refreshtoken is not None
                ):
                    self.refreshsession()
                    self.retry()
                else:
                    raise exception

    def retry(self):
        """
        Retries the last request if possible.
        """
        if self._request is not None:
            return self.send()
