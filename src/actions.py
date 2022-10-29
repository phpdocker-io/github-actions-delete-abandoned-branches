from src.github import Github


def run_action(
        github_repo: str,
        ignore_branches: list,
        last_commit_age_days: int,
        github_token: str,
        github_base_url: str,
        dry_run: bool = True
) -> list:
    input_data = {
        'github_repo': github_repo,
        'ignore_branches': ignore_branches,
        'last_commit_age_days': last_commit_age_days,
        'dry_run': dry_run,
        'github_base_url': github_base_url
    }

    print(f"Starting github action to cleanup old branches. Input: {input_data}")

    github = Github(github_repo=github_repo, github_token=github_token, github_base_url=github_base_url)

    branches = github.get_deletable_branches(last_commit_age_days=last_commit_age_days, ignore_branches=ignore_branches)

    print(f"Branches queued for deletion: {branches}")
    if dry_run is False:
        print('This is NOT a dry run, deleting branches')
        github.delete_branches(branches=branches)
    else:
        print('This is a dry run, skipping deletion of branches')

    return branches
