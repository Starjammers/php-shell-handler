from re import compile, match
from time import sleep
import requests

MAX_RETRIES = 5


def connection_check(url, headers=None):
    print("[*] - TESTING CONNECTION...")
    try:
        make_request(url, headers)
    except ConnectionError:
        print(f"[-] - CONNECTION FAILED... CANNOT CONNECT OUT TO URL: {url}")
        return False
    
    print("[+] - CONNECTION SUCCEEDED!")
    return True


def validate_url(url):
    url_regex = compile("https?://([0-9a-zA-Z]*.)+(/[\w&?=]+)?")

    if not url.startswith('http'):
        url = "http://" + url

    if not match(url_regex, url):
        raise InvalidUrlError(f"'{url}' does not seem to be a valid URL")

    return url


def make_request(url, headers=None, method="GET", post_data={}, timeout=5, retries=0):
    if method.upper() == "POST":
        if not post_data:
            raise InvalidRequestError("No data was provided to post")
        elif not isinstance(post_data, dict):
            raise InvalidRequestError("invalid data was provided to post")
        try:
            resp = requests.post(url, headers=headers, data=post_data, timeout=timeout)
        except Exception:
            if retries > MAX_RETRIES:
                raise ConnectionError(f"[-] - '{url}' cannot be connected to")
            else:
                sleep(1)
                return make_request(url, headers=headers, method=method, data=post_data, retries=retries+1)
    else:
        try:
            resp = requests.get(url, headers=headers, timeout=timeout, verify=False)
        except Exception:
            if retries > MAX_RETRIES:
                raise ConnectionError(f"[-] - '{url}' cannot be connected to")
            else:
                sleep(1)
                return make_request(url, headers=headers, retries=retries+1)

    # maybe further validation of response?

    return resp


class InvalidRequestError(Exception):
    pass
