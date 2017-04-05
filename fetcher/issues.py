from github import Github


def get_issues(repository, owner, state='open'):
    git = Github()
    repo = git.get_repo(owner + '/' + repository)
    issues = repo.get_issues(state=state)
    for issue in issues:
        # assignee, body, title, get_comments()
        if issue.pull_request is not None:
            print(issue.title)



