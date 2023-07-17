from flask import Flask, request, jsonify, render_template, redirect
from models_class import register_user, contacts, login_user, add_user_contact, get_user_contacts, delete_user_contact

app = Flask(__name__)

@app.route('/api/users/register', methods=['POST'])
def api_register_user():
    data = request.get_json()
    name = data['name']
    email = data['email']
    password = data['password']

    # Call the register_user function and store the result
    user = register_user(name, email, password)

    if user is None:
        # Return an error response if user registration fails
        return jsonify({'message': 'Email is already registered.'}), 400

    # Return a success response with the newly created user data
    return jsonify({'message': 'User registered successfully.', 'user': user.__dict__}), 201


@app.route('/api/users/login', methods=['POST'])
def api_login_user():
    data = request.get_json()
    email = data['email']
    password = data['password']

    # Call the login_user function and store the result
    user = login_user(email, password)

    if user is None:
        # Return an error response if login fails
        return jsonify({'message': 'Invalid email or password.'}), 401

    # Return a success response with the user data
    return jsonify({'message': 'Login successful.', 'user': user.__dict__}), 200


@app.route('/api/users/<int:user_id>/contacts', methods=['POST'])
def api_add_user_contact(user_id):
    data = request.get_json()
    name = data['name']
    mobile = data['mobile']

    # Call the add_user_contact function and store the result
    contact = add_user_contact(user_id, name, mobile)

    # Return a success response with the newly created contact data
    return jsonify({'message': 'Contact added successfully.', 'contact': contact.__dict__}), 201


@app.route('/api/users/<int:user_id>/contacts', methods=['GET'])
def api_get_user_contacts(user_id):
    # Call the get_user_contacts function and store the result
    contacts = get_user_contacts(user_id)

    # Return a success response with the list of contacts
    return jsonify({'message': 'Contacts retrieved successfully.',
                    'contacts': [contact.__dict__ for contact in contacts]}) \
        , 200

@app.route('/api/users/<int:user_id>/contacts/<int:contact_id>', methods=['DELETE'])
def api_delete_user_contact(user_id, contact_id):
    # Call the delete_user_contact function and store the result
    success = delete_user_contact(user_id, contact_id)

    if not success:
        # Return an error response if deletion fails
        return jsonify({'message': 'Contact not found or not owned by user.'}), 404

    # Return a success response
    return jsonify({'message': 'Contact deleted successfully.'}), 200


#########################################
# old cold , api  below
#############################################

# Contacts API routes
@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    return jsonify(contacts)


@app.route('/api/contacts', methods=['POST'])
def add_contact():
    contact = request.get_json()
    contact['id'] = len(contacts)
    contacts.append(contact)
    return jsonify({'message': 'Contact added successfully.'})


@app.route('/api/contacts/<int:contact_id>', methods=['PUT'])
def edit_contact(contact_id):
    contact = request.get_json()
    contacts[contact_id] = contact
    return jsonify({'message': 'Contact updated successfully.'})


@app.route('/api/contacts/<int:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    global contacts
    contacts = [contact for contact in contacts if contact['id'] != contact_id]
    return jsonify({'message': 'Contact deleted successfully.'})


@app.route('/')
@app.route('/contacts')
def contacts_page():
    return render_template('contacts.html', contacts=contacts)


@app.route('/contacts/add', methods=['GET', 'POST'])
def add_contact_page():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        contact = {'name': name, 'mobile': mobile}
        contacts.append(contact)
        return redirect('/contacts')
    return render_template('add_contact.html')


@app.route('/contacts/edit/<int:contact_id>', methods=['GET', 'POST'])
def edit_contact_page(contact_id):
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        contact = {'name': name, 'mobile': mobile}
        contacts[contact_id] = contact
        return redirect('/contacts')
    return render_template('edit_contact.html', contact=contacts[contact_id])


if __name__ == '__main__':
    app.run(debug=True)
