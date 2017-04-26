from utils import h2_utils as h2, neo4j_utils as neo, string_utils as su, time_utils as tu
from collections import defaultdict
import plotly.plotly as py
from plotly.graph_objs import *


def new_repo(repo, owner, language):
    d = Repo(repo, owner, language)
    return d


def plot_multiple_lists(list_of_lists, legend, limit=0):
    data = []
    for r, l in zip(legend, list_of_lists):
        lim = limit if limit != 0 else len(l)+1
        count = defaultdict(int)
        for c in l:
            count[c] += 1
        sorted_l = sorted(count, key=count.get, reverse=True)
        data.append(Scatter(x=[i for i in range(1, lim)],
                y=[count[c] for c in sorted_l], name=r))
    return py.iplot(data, filename="multi_plot")


def get_top_of_list(l):
    count = defaultdict(int)
    for c in l: count[c] += 1
    sorted_l = sorted(count, key=count.get, reverse=True)
    return sorted_l


class Repo:

    repository = ""
    owner = ""
    language = ""
    path_to_repo_db = ""
    num_of_issues = 0
    issues = []
    num_of_exceptions = 0
    num_of_commits = 0
    commits = []
    authors_of_commits = []
    num_of_contrib = 0
    num_of_files = 0
    num_of_issues_with_filenames = 0
    num_of_issues_with_excep_or_filename = 0
    excep_or_filename = []
    repo_neo_port = ""
    results = []
    CLOSED_BY = 4
    accuracy = -1
    predicted_correctly = []
    issues_without_name_or_email = []

    def __init__(self, repo, owner, language):
        self.repository = repo
        self.owner = owner
        self.language = language
        self.path_to_repo_db = "./databases/" + repo
        self.repo_neo_port = "7688" if repo == "keras" else "7687" if repo == "tensorflow" else "7689"

    def __str__(self):
        return "Repo: {0:15} Owner: {1:15} Primary Language: {2:15}".format(self.repository, self.owner, self.language)

    def get_number_of_issues(self):
        if self.num_of_issues == 0:
            conn = h2.get_connection(self.path_to_repo_db)
            self.num_of_issues = h2.get_number_of_issues(conn)
        return str(self.num_of_issues)

    def get_number_of_exceptions(self):
        if self.num_of_exceptions == 0:
            conn = h2.get_connection(self.path_to_repo_db)
            self.num_of_exceptions = h2.get_num_of_exceptions(conn)
        return str(self.num_of_exceptions)

    def get_number_issues_with_filenames(self):
        if self.num_of_issues_with_filenames == 0:
            conn = h2.get_connection(self.path_to_repo_db)
            self.num_of_issues_with_filenames = h2.get_num_of_issues_with_filenames(conn)
        return str(self.num_of_issues_with_filenames)

    def get_number_of_contributors(self):
        if self.num_of_contrib == 0:
            driver = neo.get_driver(neo.ip, self.repo_neo_port)
            self.num_of_contrib = neo.get_num_of_type(driver, "Author")
        return str(self.num_of_contrib)

    def get_number_of_commits(self):
        if self.num_of_commits == 0:
            driver = neo.get_driver(neo.ip, self.repo_neo_port)
            self.num_of_commits = neo.get_num_of_type(driver, "Commit")
        return str(self.num_of_commits)

    def get_number_of_files(self):
        if self.num_of_files == 0:
            driver = neo.get_driver(neo.ip, self.repo_neo_port)
            self.num_of_files = neo.get_num_of_type(driver, "File")
        return str(self.num_of_files)

    def get_number_of_issues_with_excep_or_filename(self):
        if self.num_of_issues_with_excep_or_filename == 0:
            conn = h2.get_connection(self.path_to_repo_db)
            self.num_of_issues_with_excep_or_filename = h2.get_num_of_issues_with_excep_or_filename(conn)
        return str(self.num_of_issues_with_excep_or_filename)

    """Section that contains functions for getting all of items.  """
    def get_excep_or_filename(self):
        if len(self.excep_or_filename) == 0:
            conn = h2.get_connection(self.path_to_repo_db)
            self.excep_or_filename = h2.get_exceptions_or_filename(conn)
        return self.excep_or_filename

    def get_all_issues(self):
        if len(self.issues) == 0:
            conn = h2.get_connection(self.path_to_repo_db)
            self.issues = h2.get_all_issues(conn)
        return self.issues

    def get_all_commits(self):
        if len(self.commits) == 0:
            driver = neo.get_driver(neo.ip, self.repo_neo_port)
            self.commits = neo.get_all_of_type(driver, "Commit")
        return self.commits

    def get_authors_of_commits(self):
        if len(self.authors_of_commits) == 0:
            driver = neo.get_driver(neo.ip, self.repo_neo_port)
            self.authors_of_commits = neo.get_all_authors_of_commits(driver)
        return self.authors_of_commits

    """Misc Functions"""
    def get_issue_percentage(self, numerator):
        """ Get's percentages over issues
        
        :param numerator: item to be compared to issues
        :return: string representing percentage
        """

        if self.num_of_issues == 0:
            self.get_number_of_issues()
        return '{0:3.2f}'.format((numerator/self.num_of_issues)*100) + "%"

    def plot_closer_count(self, issues_list):
        """
        Function that plots a count of items in a dict with a closed by column. 
        :param issues_list: list to be plotted
        :return: plot
        """
        closers = self.get_closer_data(issues_list)
        closer_count = defaultdict(int)
        for c in closers: closer_count[c] += 1
        closer_count_sorted = sorted(closer_count, key=closer_count.get, reverse=True)
        data = [Scatter(x=closer_count_sorted,
                    y=[closer_count[c] for c in closer_count_sorted])]

        return py.iplot(data, filename= self.repository + '_closer_count')

    def get_closer_data(self, count_dict):
        closers = [i[self.CLOSED_BY] for i in count_dict]
        return closers

    def plot_list(self, list_to_plot):
        list_count = defaultdict(int)
        for c in list_to_plot: list_count[c] += 1
        list_count_sorted = sorted(list_count, key=list_count.get, reverse=True)
        data = [Scatter(x=list_count_sorted,
                        y=[list_count[c] for c in list_count_sorted])]

        return py.iplot(data, filename=self.repository + '_list_count')

    def get_accuracy(self):
        if self.accuracy == -1:
            right = []
            less = []
            for a, p in self.results:
                if a[2] == "":
                    if a[1] != "":
                        if a[1] == p[1]:
                            right.append(p)
                        else:
                            less.append(a)
                else:
                    if a[2] == p[2]:
                        right.append(p)

            self.accuracy = len(right)/(len(list(self.results))-len(less))
            self.predicted_correctly = right
            self.issues_without_name_or_email = less
        return self.accuracy

    def store_results(self, res):
        self.results = res

    """Run the algorithm"""

    def run_last_touch(self):
        if len(list(self.results)) == 0:
            issues = self.get_excep_or_filename()
            driver = neo.get_driver(neo.ip, self.repo_neo_port)
            prediction = []
            actual = []
            for issue in issues:
                BODY = 1
                for match in su.regex_match(su.file_name_regex, issue[BODY]):
                    file_matches = neo.search_for_file(driver, match)
                    if len(file_matches) > 0:
                        actual.append((issue[0], issue[3], issue[4].replace("\n", "")))
                        author_date = []
                        for fm in file_matches:
                            author_date.append((fm[0], fm[1], tu.date_from_string(fm[2].replace('\n', ''))))

                        sorted_author_date = sorted(author_date, key=lambda a: a[2], reverse=True)
                        prediction.append((issue[0], sorted_author_date[0][0], sorted_author_date[0][1].replace('\n', '')))
                        break

            self.results = [x for x in zip(actual, prediction)]
            self.get_accuracy()
        return self.results

    def print_results(self):
        print('{0:15} {1:10} {2:21} {3:15} {4:15} {5:20} {6:10}'
              .format(self.repository, self.get_number_of_issues(),
                      self.get_number_of_issues_with_excep_or_filename(),
                      str(len(self.results)),
                      str(len(self.issues_without_name_or_email)),
                      str(len(self.predicted_correctly)),
                      su.dec_to_percent(self.accuracy)))
