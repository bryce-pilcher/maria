from github import Github
from configobj import ConfigObj
from writer import h2_utils
from resources import string_utils
from datetime import datetime
import time


def get_issues(repository, owner, state='open'):
    config = ConfigObj("../settings.conf")
    # Set up variables to be used in this function
    user = config['username']
    password = config['password']
    conn = h2_utils.get_connection("../databases/" + repository)
    table_name = "issues"
    columns = ["title", "body", "labels", "closed_by", "assignee"]
    data_types = ["VARCHAR(256)", "VARCHAR(4096)","VARCHAR(256)", "VARCHAR(64)", "VARCHAR(64)"]

    # Make sure database is set up
    h2_utils.create_table(table_name, conn)
    h2_utils.add_columns(columns, data_types, table_name, conn)

    # Start the real work...
    git = Github(user, password)
    repo = git.get_repo(owner + '/' + repository)
    issues = repo.get_issues(state=state)

    # Iterate through issues
    for issue in issues:
        requests_left = git.rate_limiting[0]
        if requests_left < 20:
            git.get_rate_limit()
            reset_time = git.rate_limiting_resettime
            current_time = int(datetime.now().timestamp())
            time_remaining = min(reset_time - current_time, 0)
            print("sleeping for " + str(time_remaining) + " seconds...")
            time.sleep(time_remaining)

        # assignee, body, title, get_comments()
        if issue.pull_request is None:
            iss = string_utils.sanitize(issue.title)
            bod = string_utils.sanitize(issue.body)
            label_list = [l.name for l in issue.labels]
            labels = string_utils.sanitize(string_utils.list_to_string(label_list))
            if len(bod) > 4096:
                bod = bod[:4096]
            if len(iss) > 256:
                iss = iss[:256]
            if len(labels) > 256:
                labels = labels[:256]
            values = [iss, bod, labels]
            closer = issue.closed_by
            assignee = issue.assignee
            if closer is not None:
                values.append(closer.login)
            else:
                values.append("")
            if assignee is not None:
                values.append(assignee.login)
            else:
                values.append("")
            h2_utils.write_to_database("issues", values, columns, conn)


get_issues("tensorflow", "tensorflow", state='closed')



