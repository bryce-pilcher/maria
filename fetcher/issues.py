import time
from datetime import datetime

from configobj import ConfigObj
from github import Github

from utils import h2_utils, string_utils


def get_issues(repository, owner, state='open'):
    config = ConfigObj("../settings.conf")
    # Set up variables to be used in this function
    user = config['username']
    password = config['password']
    conn = h2_utils.get_connection("../databases/" + repository)
    table_name = "issues"
    columns = ["title", "body", "labels", "closed_by_name", "closed_by_email", "assignee"]
    data_types = ["VARCHAR(256)", "VARCHAR(4096)","VARCHAR(256)", "VARCHAR(64)", "VARCHAR(64)", "VARCHAR(64)"]

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
            r = git.get_rate_limit()
            reset_time = r.rate.reset.timestamp()
            current_time = int(datetime.utcnow().timestamp())
            time_remaining = max(reset_time - current_time, 0) + 10
            print("sleeping for " + str(time_remaining) + " seconds... ")
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
            if closer is not None and closer.name is not None:
                values.append(string_utils.sanitize(closer.name))
            else:
                values.append("")
            if closer is not None and closer.email is not None:
                values.append(string_utils.sanitize(closer.email))
            else:
                values.append("")
            if assignee is not None and assignee.name is not None:
                values.append(string_utils.sanitize(assignee.name))
            else:
                values.append("")
            h2_utils.write_to_database("issues", values, columns, conn)


get_issues("spring-boot","spring-projects", state="closed")
