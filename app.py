from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# Helper: find an event by id, or return None if it doesn't exist
def find_event(event_id):
    for event in events:
        if event.id == event_id:
            return event
    return None

# GET / - welcome message
@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Event Manager API!"})

# GET /events - return all events as a JSON array
@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([event.to_dict() for event in events])

# POST /events - create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json(silent=True)
    # Validate: body must exist and contain a non-empty title
    if not data or not data.get("title"):
        return jsonify({"error": "Title is required"}), 400

    # Use max id + 1 so ids stay unique even after deletions
    new_id = max((e.id for e in events), default=0) + 1
    new_event = Event(new_id, data["title"])
    events.append(new_event)
    return jsonify(new_event.to_dict()), 201

# PATCH /events/<id> - update the title of an event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    event = find_event(event_id)
    if event is None:
        return jsonify({"error": "Event not found"}), 404

    data = request.get_json(silent=True)
    if not data or not data.get("title"):
        return jsonify({"error": "Title is required"}), 400

    event.title = data["title"]
    return jsonify(event.to_dict()), 200

# DELETE /events/<id> - remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = find_event(event_id)
    if event is None:
        return jsonify({"error": "Event not found"}), 404

    events.remove(event)
    return "", 204

if __name__ == "__main__":
    app.run(debug=True)