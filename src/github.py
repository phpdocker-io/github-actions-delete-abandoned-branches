import requests


def get_open_prs():
    print(requests.get('https://google.com').raw)
