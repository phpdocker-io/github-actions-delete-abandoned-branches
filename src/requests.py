from os import environ as env

import requests
from requests.models import Response


def post(url: str, json: dict = None, headers: dict = None, force_debug: bool = False) -> Response:
    return request(method='post', url=url, json=json, headers=headers, force_debug=force_debug)


def patch(url: str, json: dict = None, headers: dict = None, force_debug: bool = False) -> Response:
    return request(method='patch', url=url, json=json, headers=headers, force_debug=force_debug)


def get(url: str, force_debug: bool = False, headers: dict = None) -> Response:
    return request(method='get', url=url, headers=headers, force_debug=force_debug)


def request(method: str, url: str, json: dict = None, headers: dict = None, force_debug: bool = False) -> Response:
    try:
        response = requests.request(method=method, url=url, json=json, headers=headers)
        debug_request(url, method, response, json, headers, force_debug)

        return response
    except Exception as ex:
        debug_request(url, method, None, json, headers, force_debug)
        raise ex


def debug_request(
        url: str,
        method: str,
        response: Response = None,
        payload: dict = None,
        headers: dict = None,
        force: bool = False
) -> None:
    """
    Set CI_DEBUG env var to anything if you want to debug requests made. Otherwise unset.
    """
    if force or env.get('CI_DEBUG') is not None:
        print('#########################')
        print(f'Debugging request to {url}')
        print(f'Method: {method}')
        print(f'Payload: {payload}')
        print(f'Headers: {headers}')
        if response is not None:
            print(f'Response: {response}')
            print(response.json())
        print('#########################')
