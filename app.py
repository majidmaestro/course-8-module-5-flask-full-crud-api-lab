from flask import Flask, jsonify, request
app = Flask(__name__)

class Event:
  def __init__(self, id, title):
    self.id = id
    self.title = title
  def to_dict(self):
    return {"id": self.id, "title": self.title}

events = [Event(1, "Tech Meetup"), Event(2, "Python Workshop")]
def find_event(event_id):
  for event in events:
    if event.id == event_id:
      return event
  return None

@app.route("/events", methods=["POST"])
def create_event():
  data = request.get_json()
  if not data or "title" not in data:
    return jsonify({"error": "Missing required field: title"}), 400
  new_id = max((event.id for event in events), default=0) + 1
  new_event = Event(new_id, data["title"])
  events.append(new_event)
  return jsonify(new_event.to_dict()), 201

@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
  event = find_event(event_id)
  if not event:
    return jsonify({"error": "Event not found"}), 404
  data = request.get_json()
  if not data or "title" not in data:
    return jsonify({"error": "Missing required field: title"}), 400
  event.title = data["title"]
  return jsonify(event.to_dict()), 200

@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
  event = find_event(event_id)
  if not event:
    return jsonify({"error": "Event not found"}), 404
  events.remove(event)
  return "", 204

if __name__ == "__main__":
  app.run(debug=True)