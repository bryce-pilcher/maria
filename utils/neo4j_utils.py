from neo4j.v1 import GraphDatabase, basic_auth
from utils.neo4j_objects.neo4j_node import Neo4jNode

ip = "192.168.1.2"
port = "7687"


def get_driver(ip_address, port):
    driver = GraphDatabase.driver("bolt://" + ip_address + ":" + port, auth = basic_auth("neo4j", "github"))
    return driver


def create_node(a_node, driver):
    session = driver.session()

    query = "Create (a:" + a_node.type + " {"
    length_of_attr = len(a_node.attributes.keys()) - 1
    for i, k in enumerate(a_node.attributes):
        query += k + ": {" + k + "}"
        if i != length_of_attr:
            query += ", "
        else:
            query += "}"
            break

    query += ") return a"
    result = session.run(query, a_node.attributes)
    session.sync()
    session.close()


def add_relationship(a_node, b_node, rel_type, rel_property_map, driver):
    session = driver.session()

    query = "Match (a:" + a_node.type + "),(b:" + b_node.type + ") "
    query += "Where a." + a_node.unique_attr + " = \'" + a_node.unique_attr_value + "\'"
    query += " AND "
    query += "b." + b_node.unique_attr + " = \'" + b_node.unique_attr_value + "\' "
    query += "CREATE (a)-[r:" + rel_type
    query += " {" + ", ".join(k + ": " + "\'" + v + "\'" for k, v in rel_property_map.items()) + "}]->(b) "
    query += "return r"

    result = session.run(query)
    session.sync()
    session.close()


def get_node(a_node, driver):
    session = driver.session()

    query = "Match (n:" + a_node.type + " { " + a_node.unique_attr + ": \"" + a_node.unique_attr_value + "\"}) return n"
    records = session.run(query)
    session.sync()
    nodes = []
    for record in records:
        nodes.append(process_node(record[0]))
    session.close()
    if len(nodes) < 1:
        return None

    return nodes

label_switch = {
    "Author" : "email",
    "Commit" : "hash",
    "File" : "file_path"
}


def process_node(record):
    label = record.labels.pop()
    attr = {}
    for key in record.keys():
        attr[key] = record[key]
    node = Neo4jNode(label, label_switch[label], record[label_switch[label]], attr, record.id)
    return node


def get_num_of_type(driver, node_type):
    session = driver.session()
    query = "match(n:" + node_type + ") return count(n)"
    records = session.run(query)
    num_contrib = records.single()["count(n)"]
    return num_contrib


def get_all_of_type(driver, node_type):
    session = driver.session()
    query = "match(n:" + node_type + ") return n"
    records = session.run(query)
    all_of_type = [r for r in records.records()]
    return all_of_type


def get_all_authors_of_commits(driver):
    session = driver.session()
    query = "match(n: Commit)-[]-(a: Author) return a.email as email"
    records = session.run(query)
    authors_of_commits = [r['email'] for r in records.records()]
    return authors_of_commits


def search_for_file(driver, file_name):
    session = driver.session()
    query = "match(:File{file_name: \'" + file_name + \
            "\'})-[]-()-[r]-(a: Author) return a.email as email, a.name as name, r.date as date"
    records = session.run(query)
    file_matches = [(r['name'], r['email'], r['date']) for r in records.records()]
    return file_matches
