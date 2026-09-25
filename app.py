from flask import Flask, jsonify, request

app = Flask(__name__)


# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}


# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]


# Home route
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Event API"})


# Get all events
@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([event.to_dict() for event in events])


# Create a new event
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()

    # Validate the request
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    # Generate a new ID
    new_id = max([event.id for event in events], default=0) + 1

    # Create the event
    new_event = Event(new_id, data["title"])

    # Add it to the in-memory database
    events.append(new_event)

    # Return the newly created event
    return jsonify(new_event.to_dict()), 201


# Update an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    data = request.get_json()

    # Validate the request
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    # Find the event
    for event in events:
        if event.id == event_id:
            event.title = data["title"]

            return jsonify(event.to_dict()), 200

    # Event was not found
    return jsonify({"error": "Event not found"}), 404


# Delete an event
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):

    # Find the event
    for event in events:
        if event.id == event_id:
            events.remove(event)

            # 204 means successful deletion with no response body
            return "", 204

    # Event was not found
    return jsonify({"error": "Event not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)