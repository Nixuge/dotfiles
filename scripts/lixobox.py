#!/bin/python3

from collections import namedtuple
from getpass import getpass
from time import sleep
from typing import Any, Literal, Optional

import requests
import json


IP_CHECKER_ENDPOINT = "https://api.ipify.org"
ROUTER_ENDPOINT = "http://livebox/ws"

hardcoded_pass = ""
print_ip = True


LoginData = namedtuple("LoginData", "username token groups")


def main(*args: str) -> int:
    SESSION = requests.session()

    print("Lixobox")

    def find_argument(name: str) -> Optional[str]:
        if any(x.lower().startswith(f"{name}=") for x in args):
            return [x.replace(f"{name}=", "") for x in args if x.lower().startswith(f"{name}=")][-1]
        else:
            return None

    username = find_argument("user") or "admin"
    password = find_argument("pass") or hardcoded_pass

    if not password:
        password = getpass(f"Password ({username}@livebox): ")

    token = login(SESSION, username, password).token

    if not token:
        print("Authentication failed, token was null")
        exit(1)

    print("Logged in!", token)

    if print_ip:
        print("Initial IP: ", requests.get(IP_CHECKER_ENDPOINT).text, "\n")

    set_dhcp_value(SESSION, 0)
    print("DHCP disabled")

    sleep(1.5)
    set_dhcp_value(SESSION, 1)
    print("DHCP enabled, pinging...")

    NEW_IP = None

    while not NEW_IP:
        sleep(1.5)
        try:
            NEW_IP = requests.get(IP_CHECKER_ENDPOINT, timeout=1).text
        except:
            print("...")
    if print_ip:
        print(f"New IP: {NEW_IP}")

    return 0


def generate_headers(session: requests.Session = None):
    data = {
        "Authorization": "X-Sah-Login",
        "Content-Type": "application/x-sah-ws-4-call+json"
    }

    if not session:
        return data

    token = session.cookies.get("sah/contextId")

    return {
        **data,
        "Authorization": f"X-Sah {token}",
        "X-Context": token
    }


def generate_outbound_payload(service: Literal[
        "sah.Device.Information",  # login
        "NeMo.Intf.data",  # network monitor
    ],
    method: str,**params: Any) -> str:
    return json.dumps({"service": service, "method": method, "parameters": {**params}})


def login(session: requests.Session, username: str, password: str) -> LoginData:
    print(f"Logging in as {username} on {ROUTER_ENDPOINT}...")

    token = None
    groups = []

    payload = generate_outbound_payload("sah.Device.Information","createContext",
        applicationName="webui", username=username, password=password
    )

    try:
        response = session.post(
            ROUTER_ENDPOINT,
            headers=generate_headers(),
            data=payload,
            verify=False
        )

        if response.status_code != 200:
            raise Exception(
                f"Status code was not 200 ({response.status_code})")

        json = response.json()

        status = json.get("status", 1)
        if json.get("status", 1) != 0:
            raise Exception(f"Login status was not 0 ({status})")

        received_username = json.get("data", {}).get("username", None)
        if received_username != username:
            raise Exception(f"Received username did not match ({received_username} != {username})")

        token = json.get("data", {}).get("contextID")
        session.cookies.set("sah/contextId", token)
    except Exception as ex:
        print("Got an exception:", ex)
        pass

    return LoginData(username, token, groups)


def set_dhcp_value(session: requests.Session, value: Literal[0, 1]) -> bool:
    success = False

    payload = generate_outbound_payload(
        "NeMo.Intf.data",
        "setFirstParameter",
        name="Enable",
        value=value,
        flag="dhcp",
        traverse="down"
    )

    try:
        response = session.post(
            ROUTER_ENDPOINT,
            headers=generate_headers(session),
            data=payload,
            verify=False
        )

        json = response.json()
        errors = json.get("errors", None)

        if response.status_code != 200:
            raise Exception(
                f"Status code was not 200 ({response.status_code}, {errors or 'no additional info'})"
            )

        if errors:
            raise Exception(f"Got errors: {errors}")

        success = True
    except Exception as ex:
        print("Got an exception:", ex)
        pass

    return success


if __name__ == "__main__":
    import traceback
    import sys

    exit_code = 1

    try:
        exit_code = main(*sys.argv[1:])

    except KeyboardInterrupt:
        print("\n\nEnding execution due to user interaction.")

    except Exception as err:
        print()
        print("An error occured!")
        print(err)
        traceback.print_tb(err.__traceback__)

    finally:
        print()
        exit(exit_code)
