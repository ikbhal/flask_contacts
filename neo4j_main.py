from flask import Flask, request, jsonify, render_template, redirect
# from models_class import register_user, contacts, login_user, add_user_contact, get_user_contacts, delete_user_contact
from neo4j_model_class import User, graph, Contact

app = Flask(__name__)

@app.route('/api/users/register', methods=['POST'])
def api_register_user():
    data = request.get_json()
    name = data['name']
    email = data['email']
    password = data['password']

    # Check if email is already registered
    existing_user = User.find_by_email(email)
    if existing_user:
        return jsonify({'message': 'Email is already registered.'}), 400

    # Create a new user
    user = User.create(name, email, password)

    # Return the newly created user data
    return jsonify({'message': 'User registered successfully.', 'user': user.node}), 201

@app.route('/api/users/login', methods=['POST'])
def api_login_user():
    data = request.get_json()
    email = data['email']
    password = data['password']

    # Find the user by email
    user = User.find_by_email(email)

    # Check if the user exists and the password is correct
    if user is None or not user.check_password(password):
        # Return an error response if login fails
        return jsonify({'message': 'Invalid email or password.'}), 401

    # Return a success response with the user data
    return jsonify({'message': 'Login successful.', 'user': user.node}), 200

# not working below failing user_id 
@app.route('/api/users/<int:user_id>/contacts', methods=['POST'])
def api_add_user_contact(user_id):
    data = request.get_json()
    name = data['name']
    mobile = data['mobile']

    # Find the user node
    user_node = graph.nodes[user_id]

    # Create a new contact
    contact = Contact.create(user_node, name, mobile)

    # Return a success response with the newly created contact data
    return jsonify({'message': 'Contact added successfully.', 'contact': contact.node}), 201

if __name__ == '__main__':
    app.run(debug=True, port=8000)
