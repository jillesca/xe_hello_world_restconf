import json
import urllib3
import requests
from requests.auth import HTTPBasicAuth

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

PROTOCOL = "https://"
BASE_URL = "sandbox-iosxe-latest-1.cisco.com"
USERNAME = "admin"
PASSWORD = "C1sco12345"


API_ENDPOINTS = [
    "/restconf/data/Cisco-IOS-XE-native:native/version",
    "/restconf/data/Cisco-IOS-XE-native:native/hostname",
]


def create_restconf_session() -> requests.Session:
    session = requests.session()
    session.auth = HTTPBasicAuth(USERNAME, PASSWORD)
    session.headers.update({"Accept": "application/yang-data+json"})
    session.verify = False
    return session


def fetch_data(session: requests.Session, endpoint: str) -> str:
    try:
        response = session.get(PROTOCOL + BASE_URL + endpoint)
        response.raise_for_status()
        return response.text
    except requests.exceptions.HTTPError as err:
        print(f"Http Error: {err=}")
        exit()
    except requests.exceptions.ConnectionError as err:
        print(f"Error Connecting: {err=}")
        exit()
    except requests.exceptions.Timeout as err:
        print(f"Timeout Error: {err=}")
        exit()
    except requests.exceptions.RequestException as err:
        print(f"An unexpected error happened: {err=}")
        exit()


def parse_json(data: str) -> dict:
    return json.loads(data)


def classify_results(data_parsed: dict) -> dict:
    if "Cisco-IOS-XE-native:hostname" in data_parsed:
        return {"iosxe_hostname": data_parsed["Cisco-IOS-XE-native:hostname"]}
    if "Cisco-IOS-XE-native:version" in data_parsed:
        return {"iosxe_version": data_parsed["Cisco-IOS-XE-native:version"]}


def print_results(results: dict) -> None:
    iosxe_hostname = results.get("iosxe_hostname", "FAILED_TO_GET_HOSTNAME")
    iosxe_version = results.get("iosxe_version", "FAILED_TO_GET_VERSION")

    msg = f"Reviewed {BASE_URL}\n"
    msg += f"Hostname found: {iosxe_hostname}\n"
    msg += f"IOS XE Version found: {iosxe_version}\n"
    print(msg)


def main() -> None:
    session = create_restconf_session()
    responses = [fetch_data(session, endpoint) for endpoint in API_ENDPOINTS]

    parsed_responses = [parse_json(response) for response in responses]

    combined_results: dict = {}
    for parsed_response in parsed_responses:
        combined_results.update(classify_results(parsed_response))

    print_results(combined_results)


if __name__ == "__main__":
    main()
