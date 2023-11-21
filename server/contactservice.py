from flask import Flask, jsonify
from flask import send_from_directory
from pymongo.mongo_client import MongoClient
from bson import json_util
from flask import request
import json
import os



# Connect to Mongo database
def connect_to_db():
    passcode = os.environ.get('Passcode')
    uri = "mongodb+srv://swingfsy:" + passcode + "@swingtestcluster0.n5iknl4.mongodb.net/"
    client = MongoClient(uri)

    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print("Failed to connect to MongoDB:",e)
        SystemExit(1)
    return client.contactList.contactData



# contact service
app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory('static', 'index.html')

# Read a contact
@app.route('/api/contacts/<phone>/', methods=['GET'])
def read_contact(phone):
    user = contactData.find_one({"Phone": phone})
    if user is not None:
        response_data = {
            "Phone": user["Phone"],
            "Sex": user["Sex"],
            "Name": user["Name"],
        }
        return jsonify(response_data),200
    else:
        return 404


# List all contact
@app.route('/api/contacts/', methods=['GET'])
def list_contacts():
    response_data = []

    for user in contactData.find():
        contact_json = {
            "Phone": user["Phone"],
            "Sex": user["Sex"],
            "Name": user["Name"],
        }
        response_data.append(contact_json)

    return jsonify(response_data),200

# Add a contact
@app.route("/api/contacts/", methods = ['POST'])
def add_contact():

    data = request.get_json()
    if contactData.find_one({"Phone": data['Phone']}) is not None:
        return 409 
    contactData.insert_one(data)
    count = contactData.count_documents({})
    response_data = {
        "count": count
        }  
    return jsonify(response_data),201


# Delete a contact
@app.route("/api/contacts/<phone>/", methods = ['DELETE'])
def delete_contact(phone):
    result = contactData.delete_one({"Phone": phone})
    if result.deleted_count != 0:
        count = contactData.count_documents({})
        response_data = {
            "count": count
            }  
        return jsonify(response_data),204
    else: 
        return 404


# Edit a contact
@app.route("/api/contacts/<phone>/", methods = ['PUT'])
def update_contact(phone):

    item = contactData.find_one({"Phone": phone})
    if item is not None:
        data = request.get_json()
        contactData.update_one(
            { "Phone": phone} ,
            {
                "$set": {
                    "Sex": data['Sex'],
                    "Name": data['Name']
                }
            }
        )
        return jsonify(data), 200
    else:
        return 404



if __name__ == '__main__':
    contactData = connect_to_db()
    app.run(host="127.0.0.1", port=8080)