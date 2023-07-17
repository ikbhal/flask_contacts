from py2neo import Graph, Node

# Connect to Neo4j
graph = Graph("bolt://localhost:7687", auth=("neo4j", "password"))

class Contact:
    def __init__(self, name, mobile):
        self.name = name
        self.mobile = mobile

    def save(self):
        contact_node = Node("Contact", name=self.name, mobile=self.mobile)
        graph.create(contact_node)

    @staticmethod
    def retrieve_contacts():
        query = "MATCH (c:Contact) RETURN c"
        result = graph.run(query).data()
        contacts = [Contact(node["c"]["name"], node["c"]["mobile"]) for node in result]
        return contacts

# Example usage
if __name__ == "__main__":
    # Save contacts
    contact1 = Contact("John Doe", "1234567890")
    contact2 = Contact("Jane Smith", "9876543210")
    contact1.save()
    contact2.save()

    # Retrieve contacts
    contacts = Contact.retrieve_contacts()
    for contact in contacts:
        print("Name:", contact.name)
        print("Mobile:", contact.mobile)
        print()
