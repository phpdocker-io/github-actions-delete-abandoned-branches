from src.github import Github
import github as pygithub


def run_action(
        github_repo: str,
        ignore_branches: list,
        last_commit_age_days: int,
        github_token: str,
        dry_run: bool = True,
        issue_repos: list = None
) -> list:
    input_data = {
        'github_repo': github_repo,
        'ignore_branches': ignore_branches,
        'last_commit_age_days': last_commit_age_days,
        'dry_run': dry_run,
        'issue_repos': issue_repos
    }

    print(f"Starting github action to cleanup old branches. Input: {input_data}")

    github = Github(github_repo=github_repo, github_token=github_token)
    branches = github.get_deletable_branches(last_commit_age_days=last_commit_age_days, ignore_branches=ignore_branches)

    # scanning for references in other repos in an open issue
    if issue_repos is None:
        issue_repos = []

    gh = pygithub.Github(github_token)
    issue_repos = [gh.get_repo(r) for r in issue_repos]

    def keep_branch(name):
        for issue_repo in issue_repos:
            for issue in issue_repo.get_issues(state="open"):
                for comment in issue.get_comments():
                    if name in comment.body:
                        print(f"`{name}` was mentioned in {comment.html_url}")
                        return False
        return True

    branches = [keep_branch(branch) for branch in branches]

    print(f"Branches queued for deletion: {branches}")
    if dry_run is False:
        print('This is NOT a dry run, deleting branches')
        github.delete_branches(branches=branches)
    else:
        print('This is a dry run, skipping deletion of branches')

    return branches
