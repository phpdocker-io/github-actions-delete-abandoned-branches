import sys
from os import getenv
from typing import List


class Options:
    def __init__(
            self,
            ignore_branches: list[str],
            last_commit_age_days: int,
            allowed_prefixes: list[str],
            dry_run: bool,
            github_token: str,
            github_repo: str,
            github_base_url: str = 'https://api.github.com'
    ):
        self.ignore_branches = ignore_branches
        self.last_commit_age_days = last_commit_age_days
        self.allowed_prefixes = allowed_prefixes
        self.dry_run = dry_run
        self.github_token = github_token
        self.github_repo = github_repo
        self.github_base_url = github_base_url

    def validate(self):
        errors = []
        if self.dry_run is None:
            errors.append("dry_run is undefined")

        if self.github_token is None:
            errors.append("github_token is undefined")

        if self.github_repo is None:
            errors.append("github_repo is undefined")

        if self.github_base_url is None:
            errors.append("github_base_url is undefined")

        if self.last_commit_age_days is None:
            errors.append("last_commit_age_days is undefined")

        if len(errors) > 0:
            raise RuntimeError(f"Errors found while parsing input options: {errors}")


def parse_input() -> Options:
    args: List[str] = sys.argv

    num_args = len(args)

    if num_args < 4 or num_args > 7:
        input_string = ' '.join(args)
        expected_string = f'{args[0]} ignore_branches last_commit_age_days allowed_prefixes dry_run_yes_no github_token github_repo github_base_url'
        raise RuntimeError(f'Incorrect input: {input_string}. Expected: {expected_string}')

    branches_raw: str = args[1]
    ignore_branches = branches_raw.split(',')
    if ignore_branches == ['']:
        ignore_branches = []

    last_commit_age_days = int(args[2])

    prefixes_raw: str = args[3]
    allowed_prefixes = prefixes_raw.split(',')
    if allowed_prefixes == ['']:
        allowed_prefixes = []

    # Dry run can only be either `true` or `false`, as strings due to github actions input limitations
    dry_run = False if args[4] == 'no' else True

    github_token = args[5]

    github_repo = getenv('GITHUB_REPOSITORY')

    github_base_url = args[6] if num_args >= 7 else 'https://api.github.com'

    options = Options(
        ignore_branches=ignore_branches,
        last_commit_age_days=last_commit_age_days,
        allowed_prefixes=allowed_prefixes,
        dry_run=dry_run,
        github_token=github_token,
        github_repo=github_repo,
        github_base_url=github_base_url
    )

    options.validate()

    return options


def format_output(output_strings: dict) -> None:
    file_path = getenv('GITHUB_OUTPUT')

    with open(file_path, "a") as gh_output:
        for name, value in output_strings.items():
            gh_output.write(f'{name}={value}\n')
