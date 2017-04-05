from neo4j.v1 import GraphDatabase, basic_auth
from writer.neo4j_objects.neo4j_node import Neo4jNode

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

    query += ")"
    session.run(query, a_node.attributes)


def add_relationship(a_node, b_node, rel_type, rel_property, rel_property_value, driver):
    session = driver.session()

    query = "Match (a:" + a_node.type + "),(b:" + b_node.type + ") "
    query += "Where a." + a_node.unique_attr + " = \'" + a_node.unique_attr_value + "\'"
    query += " AND "
    query += "b." + b_node.unique_attr + " = \'" + b_node.unique_attr_value + "\' "
    query += "CREATE (a)-[r:" + rel_type + " {" + rel_property + ": " + rel_property_value + "}]->(b)"

    session.run(query)


def get_node(a_node, driver):
    session = driver.session()

    query = "Match (n:" + a_node.type + " { " + a_node.unique_attr + ": \'" + a_node.unique_attr_value + "\'}) return n"
    test = session.run(query)
    nodes = []
    for record in test:
        nodes.append(process_node(record[0]))
    if len(nodes) < 1:
        return None

    return nodes

label_switch = {
    "Author" : "name",
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

# create_node(Neo4jNode("Database","name","Neo4j",{"name":"SQL"}), get_driver("192.168.1.2", "7687"))
