import argparse
from os import getenv

DEFAULT_GITHUB_API_URL = 'https://api.github.com'


class Options:
    def __init__(
            self,
            ignore_branches: list[str],
            last_commit_age_days: int,
            allowed_prefixes: list[str],
            github_token: str,
            github_repo: str,
            dry_run: bool = True,
            github_base_url: str = DEFAULT_GITHUB_API_URL
    ):
        self.ignore_branches = ignore_branches
        self.last_commit_age_days = last_commit_age_days
        self.allowed_prefixes = allowed_prefixes
        self.github_token = github_token
        self.github_repo = github_repo
        self.dry_run = dry_run
        self.github_base_url = github_base_url


class InputParser:
    @staticmethod
    def get_args() -> argparse.Namespace:
        parser = argparse.ArgumentParser('Github Actions Delete Old Branches')

        parser.add_argument("--ignore-branches", help="Comma-separated list of branches to ignore")

        parser.add_argument(
            "--allowed-prefixes",
            help="Comma-separated list of prefixes a branch must match to be deleted"
        )

        parser.add_argument("--github-token", required=True)

        parser.add_argument(
            "--github-base-url",
            default=DEFAULT_GITHUB_API_URL,
            help="The API base url to be used in requests to GitHub Enterprise"
        )

        # Not setting `type=int` to avoid issues when it's passed as a quoted string
        parser.add_argument(
            "--last-commit-age-days",
            help="How old in days must be the last commit into the branch for the branch to be deleted",
            default=60,
        )

        parser.add_argument(
            "--dry-run",
            choices=["yes", "no"],
            default="yes",
            help="Whether to delete branches at all. Defaults to 'yes'. Possible values: yes, no (case sensitive)"
        )

        return parser.parse_args()

    def parse_input(self) -> Options:
        args = self.get_args()

        branches_raw: str = "" if args.ignore_branches is None else args.ignore_branches
        ignore_branches = branches_raw.split(',')
        if ignore_branches == ['']:
            ignore_branches = []

        allowed_prefixes_raw: str = "" if args.allowed_prefixes is None else args.allowed_prefixes
        allowed_prefixes = allowed_prefixes_raw.split(',')
        if allowed_prefixes == ['']:
            allowed_prefixes = []

        # Dry run can only be either `true` or `false`, as strings due to github actions input limitations
        dry_run = False if args.dry_run == 'no' else True

        return Options(
            ignore_branches=ignore_branches,
            last_commit_age_days=int(args.last_commit_age_days),
            allowed_prefixes=allowed_prefixes,
            dry_run=dry_run,
            github_token=args.github_token,
            github_repo=getenv('GITHUB_REPOSITORY'),
            github_base_url=args.github_base_url
        )


def format_output(output_strings: dict) -> None:
    file_path = getenv('GITHUB_OUTPUT')

    with open(file_path, "a") as gh_output:
        for name, value in output_strings.items():
            gh_output.write(f'{name}={value}\n')
