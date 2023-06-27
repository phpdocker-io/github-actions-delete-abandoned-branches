import sys
from os import getenv
from typing import List


def parse_input() -> (list, int, list, bool, str, str, str):
    args: List[str] = sys.argv

    num_args = len(args)

    if num_args < 4 or num_args > 7:
        input_string = ' '.join(args)
        expected_string = f'{args[0]} ignore_branches last_commit_age_days prefixes dry_run_yes_no github_token github_repo github_base_url'
        raise RuntimeError(f'Incorrect input: {input_string}. Expected: {expected_string}')

    branches_raw: str = args[1]
    ignore_branches = branches_raw.split(',')
    if ignore_branches == ['']:
        ignore_branches = []

    last_commit_age_days = int(args[2])

    prefixes_raw: str = args[3]
    prefixes = prefixes_raw.split(',')
    if prefixes == ['']:
        prefixes = []

    # Dry run can only be either `true` or `false`, as strings due to github actions input limitations
    dry_run = False if args[4] == 'no' else True

    github_token = args[5]

    github_repo = getenv('GITHUB_REPOSITORY')

    github_base_url = args[6] if num_args >= 7 else 'https://api.github.com'

    return ignore_branches, last_commit_age_days, prefixes, dry_run, github_token, github_repo, github_base_url


def format_output(output_strings: dict) -> None:
    file_path = getenv('GITHUB_OUTPUT')

    with open(file_path, "a") as gh_output:
        for name, value in output_strings.items():
            gh_output.write(f'{name}={value}\n')
