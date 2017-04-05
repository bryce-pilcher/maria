import jaydebeapi as jdb


def get_connection(database):
    conn = jdb.connect("org.h2.Driver", ["jdbc:h2:" + str(database), "", ""],jars="../resources/h2-1.4.194.jar")
    return conn


def write_to_database(table, values, columns, conn):
    curs = conn.cursor()
    sql_statement = 'insert into ' + table + ' (' + ','.join(columns) + ') values (' + ','.join(values) + ')'
    curs.execute(sql_statement)
    curs.fetchall()
    curs.close()


def create_table(tablename, conn):
    curs = conn.cursor()
    curs.execute('create table if not exists' + tablename)
    # curs.fetchall()
    curs.close()
