from src import github


def run_action(ignore_branches: list, last_commit_age_days: int) -> bool:
    print(f'ignore_branches: {ignore_branches}, last_commit_age_days: {last_commit_age_days}')

    deleted_branches: list = ['foo']
    github.get_open_prs()

    format_output(deleted_branches)
    return True


def format_output(deleted_branches: list) -> None:
    print(f'::set-output deleted_branches={deleted_branches}')
