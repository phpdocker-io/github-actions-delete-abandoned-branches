from src import github


def run_action(ignore_branches: list, last_commit_age_days: int, dry_run: bool) -> list:
    print(f'ignore_branches: {ignore_branches}, last_commit_age_days: {last_commit_age_days}, dry_run: {dry_run}')

    deleted_branches: list = ['foo']
    github.get_open_prs()

    return deleted_branches
