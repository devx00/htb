#!/usr/bin/env python3
"""
Just a manual test for now. 
Will have to come up with a better solution later.
"""
import os
from dotenv import load_dotenv

from pprint import pprint
# Suppress only the single warning from urllib3 needed.
import htbapi
from htbapi import profiles
from htbapi import HTBChallenge
htbapi.session.proxies = {"https": "https://localhost:8080"}
htbapi.client.disablesslwarnings()
htbapi.session.verify = False

sessionfile = "tests/.session"
def login():
    load_dotenv()

    EMAIL = os.getenv("EMAIL")
    PASSWORD = os.getenv("PASSWORD")
    otp = input("otp> ")

    try:
        if EMAIL is None or PASSWORD is None:
            return
        token, refresh = htbapi.initialize(EMAIL, PASSWORD, otp)
        with open(sessionfile, 'w') as f:
            f.write(f"{token}\n{refresh}")

    except htbapi.exceptions.HTBRequestException as e:
        print(e, e.response.url)

def loadsession():
    with open(sessionfile, 'r') as f:
        lines = [l.strip() for l in f.readlines()]
        if len(lines) == 2:
            htbapi.restoresession(lines[0], lines[1])
            return True
    return False

if not loadsession():
    login()


# testinfo = htbapi.session.get("/user/info")
# users = profiles.findprofiles("parad")
c = HTBChallenge({"id": 5})
print(c.name)
# p = profiles.findprofile("3nt3r")
# pprint(p.__dict__)
# pprint(p.user_owns)
# p.load()
# pprint(p.__dict__)