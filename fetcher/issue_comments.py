from github import Github


def get_issue_comments(issue):
    issue_comments = issue.get_comments()
    # user, body