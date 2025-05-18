from flask import Flask, jsonify, request, render_template, redirect, url_for
from pymongo import MongoClient
import json
from datetime import datetime
import os

# ✅ Initialize Flask with correct template folder path
app = Flask(__name__, template_folder='../frontend/templates')

# ✅ MongoDB Atlas connection
MONGO_URI = "mongodb+srv://mohdazamuddin999:azam12@cluster0.ziejmqe.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["flask_db"]
collection = db["users"]

# ✅ Test MongoDB connection
try:
    client.admin.command('ping')
    print("✅ Connected to MongoDB successfully!")
except Exception as e:
    print("❌ MongoDB connection failed:", e)

# ✅ /api endpoint — return JSON data from file
@app.route('/api')
def api():
    try:
        file_path = os.path.join(os.path.dirname(__file__), 'data.json')
        with open(file_path, "r") as file:
            data = json.load(file)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Home route — form for inserting into MongoDB
@app.route('/', methods=['GET', 'POST'])
def form():
    error = None
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            if not name or not email:
                raise ValueError("Name and Email are required.")
            collection.insert_one({
                "name": name,
                "email": email,
                "timestamp": datetime.utcnow()
            })
            return redirect(url_for('success'))
        except Exception as e:
            error = str(e)
    return render_template('form.html', error=error)

# ✅ Success page route
@app.route('/success')
def success():
    return render_template('success.html')

# ✅ Run the Flask server
if __name__ == '__main__':
    app.run(debug=True)
