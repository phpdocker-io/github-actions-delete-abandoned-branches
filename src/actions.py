from src import github


def run_action() -> bool:
    deleted_branches: list = ['foo']
    github.get_open_prs()

    format_output(deleted_branches)
    return True


def format_output(deleted_branches: list) -> None:
    print(f'::set-output deleted_branches={deleted_branches}')
