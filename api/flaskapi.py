from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory user storage (dictionary for simplicity)
users = {}

# GET all users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users), 200

# GET a specific user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify({user_id: user}), 200
    return jsonify({"error": "User not found"}), 404

# POST - Add new user
@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    if not data or "name" not in data:
        return jsonify({"error": "Invalid input"}), 400
    
    user_id = len(users) + 1
    users[user_id] = {"name": data["name"], "email": data.get("email", "")}
    return jsonify({"message": "User added", "user_id": user_id}), 201

# PUT - Update user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    
    users[user_id].update({
        "name": data.get("name", users[user_id]["name"]),
        "email": data.get("email", users[user_id]["email"])
    })
    return jsonify({"message": "User updated", "user": users[user_id]}), 200

# DELETE - Remove user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    del users[user_id]
    return jsonify({"message": f"User {user_id} deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
