from flask import Flask, request, jsonify, render_template 
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, template_folder='templates')

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/crud'  # Ganti dengan informasi koneksi MySQL Anda
db = SQLAlchemy(app)

class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    phone_no = db.Column(db.String(20), nullable=False)

def set_response(status="success", message="", data={}):
    return {
        "status": status,
        "message": message,
        "data": data,
    }


@app.route('/', methods=['GET'])
def index():
    return render_template ('index.html')

@app.route('/contact/list', methods=['GET'])
def get_contacts():
    contacts = Contact.query.all()
    contact_list = []
    for contact in contacts:
        print (contact.id)
        contact_list.append({
            'id': contact.id,
            'name': contact.name,
            'phone_no': contact.phone_no
        })

    return jsonify(set_response("success", "", { "contacts": contact_list }))

@app.route('/contact/add', methods=['POST'])
def create_contact():
    data = request.get_json()
    new_contact = Contact(name=data['name'], phone_no=data['phone_no'])
    db.session.add(new_contact)
    db.session.commit()
    return jsonify(set_response("success", "Contact created successfully"))

@app.route('/contact/update', methods=['PUT'])
def update_contact():
    data = request.get_json()
    id = int(data["id"])
    contact = Contact.query.get(id)
    if not contact:
        return jsonify({'error': 'Contact not found'})
    contact.name = data['name']
    contact.phone_no = data['phone_no']
    db.session.commit()
    return jsonify(set_response("success", "Contact updated successfully"))

@app.route('/contact/delete/<int:id>', methods=['DELETE'])
def delete_contact(id):
    contact = Contact.query.get(id)
    if not contact:
        return jsonify({'error': 'Contact not found'})
    db.session.delete(contact)
    db.session.commit()
    return jsonify(set_response("success", "Contact deleted successfully"))

with app.app_context():
    db.create_all()
    app.run(debug=True, port=8080)