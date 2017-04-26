import jaydebeapi as jdb
from utils import string_utils as su


def get_connection(database):
    conn = jdb.connect("org.h2.Driver", ["jdbc:h2:" + str(database), "", ""],jars="../resources/h2-1.4.194.jar")
    return conn


def write_to_database(table, values, columns, conn):
    curs = conn.cursor()
    sql_statement = 'insert into ' + table + ' (' + ','.join(columns) + ') values (\'' + '\', \''.join(values) + '\')'
    print(sql_statement)
    curs.execute(sql_statement)
    curs.close()


def create_table(tablename, conn):
    curs = conn.cursor()
    curs.execute('create table if not exists ' + tablename)
    curs.close()


def add_columns(columns, data_types, table_name, conn):
    curs = conn.cursor()
    for c, dt in zip(columns, data_types):
        curs.execute('alter table ' + table_name + ' add if not exists ' + c + " " + dt)
    curs.close()


def get_number_of_issues(conn):
    curs = conn.cursor()
    curs.execute('select count(*) from issues')
    num_of_issues = curs.fetchall()
    curs.close()
    return num_of_issues[0][0]


def get_num_of_exceptions(conn):
    curs = conn.cursor()
    curs.execute('select count(*) from issues where body regexp \'[a-z|A-Z|\.]*Exception[\s\S]*at\'')
    num_of_exceptions = curs.fetchall()
    curs.close
    return num_of_exceptions[0][0]


def get_num_of_issues_with_filenames(conn):
    curs = conn.cursor()
    curs.execute('select count(*) from issues where body regexp \'' + su.file_name_regex + '\'')
    num_of_file_names = curs.fetchall()
    curs.close()
    return num_of_file_names[0][0]


def get_num_of_issues_with_excep_or_filename(conn):
    curs = conn.cursor()
    curs.execute('select count(*) from issues where body regexp \'' + su.file_name_regex + '\' '
                 'or body regexp \'[a-z|A-Z|\.]*Exception[\s\S]*at\'')
    num_of_both = curs.fetchall()
    curs.close()
    return num_of_both[0][0]


def get_exceptions_or_filename(conn):
    curs = conn.cursor()
    curs.execute('select * from issues where body regexp \'' + su.file_name_regex + '\' '
                 'or body regexp \'[a-z|A-Z|\.]*Exception[\s\S]*at\'')
    both = curs.fetchall()
    curs.close()
    return both


def get_all_issues(conn):
    curs = conn.cursor()
    curs.execute('select * from issues')
    all_issues = curs.fetchall()
    curs.close()
    return all_issues
