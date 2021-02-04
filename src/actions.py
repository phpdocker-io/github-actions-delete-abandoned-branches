import json

from src.github import Github


def run_action(
        github_repo: str,
        ignore_branches: list,
        last_commit_age_days: int,
        github_token: str,
        github_event_path: str,
        dry_run: bool = True
) -> list:
    print({
        'github_repo': github_repo,
        'ignore_branches': ignore_branches,
        'last_commit_age_days': last_commit_age_days,
        'dry_run': dry_run,
    })

    github = Github(github_repo=github_repo, github_token=github_token)

    github_event = get_github_event(github_event_path)

    print(github_event)
    # branches = github.get_deletable_branches(last_commit_age_days=last_commit_age_days, ignore_branches=ignore_branches)
    #
    # print(f"Branches queued for deletion: {branches}")
    # if dry_run is False:
    #     print('This is NOT a dry run, deleting branches')
    #     github.delete_branches(branches=branches)
    # else:
    #     print('This is a dry run, skipping deletion of branches')

    return []


def get_github_event(event_path: str) -> dict:
    """
    Github writes a file on the path given by event_path during a github action in our runtime. It has
    certain info about what we're building.
    """
    with open(event_path) as json_file:
        return json.load(json_file)
