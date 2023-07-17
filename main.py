from flask import Flask, request, jsonify, render_template, redirect

app = Flask(__name__)

# In-memory data structures
contacts = []
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
    del contacts[contact_id]
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
