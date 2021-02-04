import requests
from requests.models import Response


def get(url: str, force_debug: bool = False, headers: dict = None) -> Response:
    return request(method='get', url=url, headers=headers, force_debug=force_debug)


def request(method: str, url: str, json: dict = None, headers: dict = None, force_debug: bool = False) -> Response:
    try:
        response = requests.request(method=method, url=url, json=json, headers=headers)
        if force_debug:
            debug_request(url, method, response, json, headers)

        return response
    except Exception as ex:
        debug_request(url, method, None, json, headers)
        raise ex


def debug_request(
        url: str,
        method: str,
        response: Response = None,
        payload: dict = None,
        headers: dict = None,
) -> None:
    print('#########################')
    print(f'Debugging request to {url}')
    print(f'Method: {method}')
    print(f'Payload: {payload}')
    print(f'Headers: {headers}')
    if response is not None:
        print(f'Response: {response}')
        print(response.json())
    print('#########################')
