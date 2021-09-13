from datetime import datetime

from src import requests

GH_BASE_URL = "https://api.github.com"


class Github:
    def __init__(self, github_repo: str, github_token: str):
        self.github_token = github_token
        self.github_repo = github_repo

    def make_headers(self) -> dict:
        return {
            'authorization': f'Bearer {self.github_token}',
            'content-type': 'application/vnd.github.v3+json',
        }

    def get_paginated_branches_url(self, page: int = 0) -> str:
        return f'{GH_BASE_URL}/repos/{self.github_repo}/branches?protected=false&per_page=30&page={page}'

    def get_deletable_branches(self, last_commit_age_days: int, ignore_branches: list) -> list:
        # Default branch might not be protected
        default_branch = self.get_default_branch()

        url = self.get_paginated_branches_url()
        headers = self.make_headers()

        response = requests.get(url=url, headers=headers)
        if response.status_code != 200:
            raise RuntimeError(f'Failed to make request to {url}. {response} {response.json()}')

        deletable_branches = []
        branch: dict
        branches: list = response.json()
        current_page = 1

        while len(branches) > 0:
            for branch in branches:
                branch_name = branch.get('name')

                commit_hash = branch.get('commit', {}).get('sha')
                commit_url = branch.get('commit', {}).get('url')

                print(f'Analyzing branch `{branch_name}`...')

                # Immediately discard protected branches, default branch and ignored branches
                if branch_name == default_branch:
                    print(f'Ignoring `{branch_name}` because it is the default branch')
                    continue

                # We're already retrieving non-protected branches from the API, but it pays being careful when dealing
                # with third party apis
                if branch.get('protected') is True:
                    print(f'Ignoring `{branch_name}` because it is protected')
                    continue

                if branch_name in ignore_branches:
                    print(f'Ignoring `{branch_name}` because it is on the list of ignored branches')
                    continue

                # Move on if commit is in an open pull request
                if self.has_open_pulls(commit_hash=commit_hash):
                    print(f'Ignoring `{branch_name}` because it has open pulls')
                    continue

                # Delete if it's part of a pull request that's merged
                if self.pull_was_merged(commit_hash=commit_hash):
                    print(f'Branch `{branch_name}` meets the criteria for deletion')
                    deletable_branches.append(branch_name)
                    continue

                # Move on if branch is base for a pull request
                if self.is_pull_request_base(branch=branch_name):
                    print(f'Ignoring `{branch_name}` because it is the base for a pull request of another branch')
                    continue

                # Move on if last commit is newer than last_commit_age_days
                if self.is_commit_older_than(commit_url=commit_url, older_than_days=last_commit_age_days) is False:
                    print(f'Ignoring `{branch_name}` because last commit is newer than {last_commit_age_days} days')
                    continue

                print(f'Branch `{branch_name}` meets the criteria for deletion')
                deletable_branches.append(branch_name)

            # Re-request next page
            current_page += 1

            response = requests.get(url=self.get_paginated_branches_url(page=current_page), headers=headers)
            if response.status_code != 200:
                raise RuntimeError(f'Failed to make request to {url}. {response} {response.json()}')

            branches: list = response.json()

        return deletable_branches

    def delete_branches(self, branches: list) -> None:
        for branch in branches:
            print(f'Deleting branch `{branch}`...')
            url = f'{GH_BASE_URL}/repos/{self.github_repo}/git/refs/heads/{branch}'

            response = requests.request(method='DELETE', url=url, headers=self.make_headers())
            if response.status_code != 204:
                print(f'Failed to delete branch `{branch}`')
                raise RuntimeError(f'Failed to make DELETE request to {url}. {response} {response.json()}')

            print(f'Branch `{branch}` DELETED!')

    def get_default_branch(self) -> str:
        url = f'{GH_BASE_URL}/repos/{self.github_repo}'
        headers = self.make_headers()

        response = requests.get(url=url, headers=headers)

        if response.status_code != 200:
            raise RuntimeError('Error: could not determine default branch. This is a big one.')

        return response.json().get('default_branch')

    def pull_was_merged(self, commit_hash: str) -> bool:
        """
        Returns true if commit is part of a merged pull request
        """
        url = f'{GH_BASE_URL}/repos/{self.github_repo}/commits/{commit_hash}/pulls'
        headers = self.make_headers()
        headers['accept'] = 'application/vnd.github.groot-preview+json'

        response = requests.get(url=url, headers=headers)
        if response.status_code != 200:
            raise RuntimeError(f'Failed to make request to {url}. {response} {response.json()}')

        pull_request: dict
        for pull_request in response.json():
            if pull_request.get('state') == 'closed' and 'merged_at' in pull_request:
                return True

        return False

    def has_open_pulls(self, commit_hash: str) -> bool:
        """
        Returns true if commit is part of an open pull request or the branch is the base for a pull request
        """
        url = f'{GH_BASE_URL}/repos/{self.github_repo}/commits/{commit_hash}/pulls'
        headers = self.make_headers()
        headers['accept'] = 'application/vnd.github.groot-preview+json'

        response = requests.get(url=url, headers=headers)
        if response.status_code != 200:
            raise RuntimeError(f'Failed to make request to {url}. {response} {response.json()}')

        pull_request: dict
        for pull_request in response.json():
            if pull_request.get('state') == 'open':
                return True

        return False

    def is_pull_request_base(self, branch: str) -> bool:
        """
        Returns true if the given branch is base for another pull request.
        """
        url = f'{GH_BASE_URL}/repos/{self.github_repo}/pulls?base={branch}'
        headers = self.make_headers()
        headers['accept'] = 'application/vnd.github.groot-preview+json'

        response = requests.get(url=url, headers=headers)
        if response.status_code != 200:
            raise RuntimeError(f'Failed to make request to {url}. {response} {response.json()}')

        return len(response.json()) > 0

    def is_commit_older_than(self, commit_url: str, older_than_days: int):
        response = requests.get(url=commit_url, headers=self.make_headers())
        if response.status_code != 200:
            raise RuntimeError(f'Failed to make request to {commit_url}. {response} {response.json()}')

        commit: dict = response.json().get('commit', {})
        committer: dict = commit.get('committer', {})
        author: dict = commit.get('author', {})

        # Get date of the committer (instead of the author) as the last commit could be old but just applied
        # for instance coming from a merge where the committer is bringing in commits from other authors
        # Fall back to author's commit date if none found for whatever bizarre reason
        commit_date_raw = committer.get('date', author.get('date'))
        if commit_date_raw is None:
            print(f"Warning: could not determine commit date for {commit_url}. Assuming it's not old enough to delete")
            return False

        # Dates are formatted like so: '2021-02-04T10:52:40Z'
        commit_date = datetime.strptime(commit_date_raw, "%Y-%m-%dT%H:%M:%SZ")

        delta = datetime.now() - commit_date
        print(f'Last commit was on {commit_date_raw} ({delta.days} days ago)')

        return delta.days > older_than_days
