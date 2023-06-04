from flask import Flask, request, jsonify
import pickle
from Model import Model
from flask_cors import CORS
from bson.json_util import dumps
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import logging
import openai
import re
app = Flask(__name__)
# enable CORS 
CORS(app)  

#database connection URL
databaseConnetion = ""
# Create a new client and connect to the server
client = MongoClient(databaseConnetion, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("You successfully connected ")
except Exception as e:
    print("Try again")

#Specify the database name abd the connection
database = client["remedydata"]
collection = database["remedy"]

# Load the exported model
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

#The remedy recomendation function 

@app.route('/recommend', methods=['POST'])
def recommend():
   
    remedy_type =  request.form['remedy-type']
    conditions =  request.form.getlist('condition-types')

    remedy_names, remedy_indexes = model.recommend_remedies(remedy_type, conditions)

    response = [name for name in remedy_indexes]
    return jsonify(response)

# The function to get the remedies by the ingredient 
@app.route('/search')
def search():
    keyword = request.args.get('keyword')
    remedies = []
    ingrdients = collection.find({"ingredients": {"$regex": keyword, "$options": "i"}})
    for remedy in ingrdients:
        remedies.append(remedy)
    try:
        return dumps(remedies)
    except Exception as e:
        logging.error(e)
        return jsonify({'remedy not found '}), 500

# the function to select and retrive the remedies by name  
@app.route('/search-remedies')
def search_remedies():
    name = request.args.get('name')
    print("Name: ", name)
    remedy = collection.find_one({"name": {"$regex": str(name), "$options": "i"}})
    print("Remedy: ", remedy)
    if remedy is not None:
        try:
            response = dumps(remedy)
            headers = {
                'Access-Control-Allow-Origin': '*'
            }
            return response, 200, headers
        except Exception as e:
            logging.error(e)
            return jsonify({'remedy not found '}), 500
    else:
        return jsonify({'Remedy not found'}), 404
    


openai.api_key = ""
import re

@app.route('/chat', methods=['POST'])
def chat():
    # Get input from user
    user_input = request.form.get('input')
    # Generate response using OpenAI GPT-3
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=user_input,
        max_tokens=300,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Get generated text from OpenAI response
    generated_text = response.choices[0].text.strip()
    # Split generated text into separate sentences or lines
    generated_text_list = re.split(r'[.?!]\s+', generated_text)

    # Return generated text as response to front-end
    response = jsonify({'generated_text_list': generated_text_list})
    response.headers.add('Content-Type', 'application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    app.run(debug=True)

