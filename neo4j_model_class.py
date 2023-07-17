from py2neo import Graph, Node, Relationship

graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))

class User:
    def __init__(self, node):
        self.node = node

    @classmethod
    def create(cls, name, email, password, is_verified=False):
        node = Node("User", name=name, email=email, password=password, is_verified=is_verified)
        graph.create(node)
        return cls(node)

    @classmethod
    def find_by_email(cls, email):
        query = "MATCH (u:User {email: $email}) RETURN u"
        result = graph.run(query, email=email).evaluate()
        if result:
            return cls(result)
        return None

    def check_password(self, password):
        stored_password = self.node["password"]
        return stored_password == password

class Contact:
    def __init__(self, node):
        self.node = node

    @classmethod
    def create(cls, user, name, mobile):
        node = Node("Contact", name=name, mobile=mobile)
        graph.create(node)
        relationship = Relationship(user.node, "HAS_CONTACT", node)
        graph.create(relationship)
        return cls(node)

    @classmethod
    def find_by_user(cls, user):
        query = "MATCH (u:User)-[:HAS_CONTACT]->(c:Contact) WHERE ID(u) = $user_id RETURN c"
        result = graph.run(query, user_id=user.node.id).evaluate()
        return [cls(record) for record in result]

    def delete(self):
        graph.delete(self.node)
