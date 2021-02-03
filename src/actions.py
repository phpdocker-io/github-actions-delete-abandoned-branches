from src import github


def run_action() -> None:
    github.get_open_prs()
