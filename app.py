from flask import Flask, jsonify, request, render_template, redirect, url_for
from pymongo import MongoClient
import json
from datetime import datetime

app = Flask(__name__)

# ✅ MongoDB Atlas URI
MONGO_URI = "mongodb+srv://mohdazamuddin999:azam12@cluster0.ziejmqe.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# ✅ Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["flask_db"]
collection = db["users"]

# ✅ Test connection
try:
    client.admin.command('ping')
    print("✅ Connected to MongoDB successfully!")
except Exception as e:
    print("❌ MongoDB connection failed:", e)

# ✅ /api endpoint that reads from file and returns JSON
@app.route('/api')
def api():
    with open("data.json", "r") as file:
        data = json.load(file)
    return jsonify(data)

# ✅ Form route to insert data into MongoDB
@app.route('/', methods=['GET', 'POST'])
def form():
    error = None
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            if not name or not email:
                raise ValueError("Name and Email are required")
            collection.insert_one({"name": name, "email": email, "timestamp": datetime.utcnow()})
            return redirect(url_for('success'))
        except Exception as e:
            error = str(e)
    return render_template('form.html', error=error)

# ✅ Success page
@app.route('/success')
def success():
    return render_template('success.html')

# ✅ Run the app
if __name__ == '__main__':
    app.run(debug=True)
