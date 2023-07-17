from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# In-memory data structures
contacts = []
pages = []


# Contacts API routes

@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    return jsonify(contacts)


@app.route('/api/contacts', methods=['POST'])
def add_contact():
    contact = request.get_json()
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


# Pages API routes

@app.route('/api/pages', methods=['GET'])
def get_pages():
    return jsonify(pages)


@app.route('/api/pages', methods=['POST'])
def add_page():
    page = request.get_json()
    pages.append(page)
    return jsonify({'message': 'Page added successfully.'})


@app.route('/api/pages/<int:page_id>', methods=['PUT'])
def edit_page(page_id):
    page = request.get_json()
    pages[page_id] = page
    return jsonify({'message': 'Page updated successfully.'})


@app.route('/api/pages/<int:page_id>', methods=['DELETE'])
def delete_page(page_id):
    del pages[page_id]
    return jsonify({'message': 'Page deleted successfully.'})


# HTML page routes

@app.route('/contacts')
def contacts_page():
    return render_template('contacts.html', contacts=contacts)


@app.route('/pages')
def pages_page():
    return render_template('pages.html', pages=pages)


if __name__ == '__main__':
    app.run(debug=True)
