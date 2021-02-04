from src import requests

GH_BASE_URL = "https://api.github.com"


class Github:
    def __init__(self, github_repo: str, github_token: str):
        self.github_token = github_token
        self.github_repo = github_repo

    def make_headers(self) -> dict:
        return {'authorization': f'Bearer: {self.github_token}'}

    def get_deletable_branches(self) -> list:
        url = f'{GH_BASE_URL}/repos/{self.github_repo}/branches'
        headers = self.make_headers()

        response = requests.get(url=url, headers=headers, force_debug=True)
        print(response.json())

        return []
