from src import actions, io

if __name__ == '__main__':
    branches, last_commit_age_days, dry_run = io.parse_input()

    deleted_branches = actions.run_action(
        ignore_branches=branches,
        last_commit_age_days=last_commit_age_days,
        dry_run=dry_run
    )

    io.format_output(deleted_branches=deleted_branches)
