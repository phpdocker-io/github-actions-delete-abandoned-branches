import sys
from typing import List


def parse_input() -> (list, int):
    args: List[str] = sys.argv

    if len(args) != 4:
        input_string = ' '.join(args)
        expected_string = f'{args[0]} ignore_branches last_commit_age_days dry_run_yes_no'
        raise RuntimeError(f'Incorrect input: {input_string}. Expected: {expected_string}')

    branches_raw: str = args[1]
    branches_parsed = branches_raw.split(',')
    if branches_parsed == ['']:
        branches_parsed = []

    branch_last_commit = int(args[2])

    # Dry run can only be either `true` or `false`, as strings due to github actions input limitations
    is_dry_run = False if args[3] == 'no' else True

    return branches_parsed, branch_last_commit, is_dry_run


def format_output(deleted_branches: list) -> None:
    print(f'::set-output deleted_branches={deleted_branches}')
