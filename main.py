import sys
from typing import List

import src.actions


def parse_input() -> (list, int):
    args: List[str] = sys.argv

    if len(args) != 3:
        input_string = ' '.join(args)
        expected_string = f'{args[0]} ignore_branches last_commit_age_days'
        raise RuntimeError(f'Incorrect input: {input_string}. Expected: {expected_string}')

    branches_raw: str = args[1]
    branches_parsed = branches_raw.split(',')
    if branches_parsed == ['']:
        branches_parsed = []

    branch_last_commit = int(args[2])

    return branches_parsed, branch_last_commit


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    branches, last_commit_age_days = parse_input()

    src.actions.run_action(ignore_branches=branches, last_commit_age_days=last_commit_age_days)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
