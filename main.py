from src import actions, io

if __name__ == '__main__':
    ignore_branches, last_commit_age_days, dry_run, github_token, github_repo, github_base_url = io.parse_input()

    deleted_branches = actions.run_action(
        ignore_branches=ignore_branches,
        last_commit_age_days=last_commit_age_days,
        dry_run=dry_run,
        github_repo=github_repo,
        github_token=github_token,
        github_base_url=github_base_url
    )

    io.format_output({'deleted_branches': deleted_branches})
