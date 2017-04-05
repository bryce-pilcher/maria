class Neo4jNode:
    id = 0
    type = ""
    unique_attr = ""
    unique_attr_value = ""
    attributes = {}

    def __init__(self, neo_type, neo_unique_attr, neo_unique_attr_value, neo_attributes, neo_id=0):
        """
        
        
        :param neo_type: 
        :param neo_unique_attr: 
        :param neo_unique_attr_value: 
        :param neo_attributes: 
        :param neo_id: 
        """
        self.id = neo_id
        self.type = neo_type
        self.unique_attr = neo_unique_attr
        self.unique_attr_value = neo_unique_attr_value
        self.attributes = neo_attributes

    def __str__(self):
        return "<Node id=" + str(self.id) + " label=" + self.type + \
               " properties={" + ", ".join(("\"" + k + "\":\"" + v + "\"") for k, v in self.attributes.items()) + "}>"
