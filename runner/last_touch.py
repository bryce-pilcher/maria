from utils import neo4j_utils as neo, string_utils as su, time_utils as tu


def run(repo):
    if len(list(repo.results)) == 0:
        issues = repo.get_excep_or_filename()
        driver = neo.get_driver(neo.ip, repo.repo_neo_port)
        prediction = []
        actual = []
        for issue in issues:
            BODY = 1
            for match in su.regex_match(su.file_name_regex, issue[BODY]):
                file_matches = neo.search_for_file(driver, match)
                if len(file_matches) > 0:
                    actual.append((issue[0], issue[3]))
                    author_date = []
                    for fm in file_matches:
                        author_date.append((fm[0], tu.date_from_string(fm[1].replace('\n',''))))

                    sorted_author_date = sorted(author_date, key=lambda a: a[1], reverse=True)
                    prediction.append((issue[0], sorted_author_date[0][0]))
                    break

        repo.results = zip(actual, prediction)
    return repo.results
