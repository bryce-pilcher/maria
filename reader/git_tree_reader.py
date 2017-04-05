from writer import neo4j_utils as neo
from writer.neo4j_objects.neo4j_node import Neo4jNode

driver = neo.get_driver(neo.ip, neo.port)


def read_git_log(file_to_read):
        with open(file_to_read) as git_log:
            commit_node = {}
            for line in git_log:
                words = line.split(" ")
                if line.startswith("commit"):
                    hash = words[1]
                    commit_node = Neo4jNode("Commit", "hash", hash, {"hash": hash})
                    nodes = neo.get_node(commit_node, driver)
                    if nodes is None:
                        neo.create_node(commit_node, driver)
                if "Author:" in line:
                    name = ""
                    for x in range(1,len(words)):
                        if "<" not in words[x]:
                            name += words[x] + " "
                    name = name.strip(" ")
                    author_node = Neo4jNode("Author", "name", name, {"name": name})
                    nodes = neo.get_node(author_node, driver)
                    if nodes is None:
                        neo.create_node(author_node, driver)
                    neo.add_relationship(author_node, commit_node, "committed",
                                         "author", "\'" + author_node.attributes['name'] + "\'", driver)
                if "|" in line:
                    file_path = words[1]
                    file_parts = file_path.split("/")
                    file_name = file_parts[len(file_parts) - 1]
                    file_node = Neo4jNode("File", "file_path", file_path,
                                          {"file_name": file_name,
                                           "file_path": file_path})
                    nodes = neo.get_node(file_node, driver)
                    if nodes is None:
                        neo.create_node(file_node, driver)
                    neo.add_relationship(commit_node, file_node, "changed",
                                         "lines_edited", "\'" + words[3] + "\'", driver)

