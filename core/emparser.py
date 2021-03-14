import json

event_map = {}
with open("event-map.json", "r") as read_file:
    data = json.load(read_file)

event_map_json = data["event_map"]

for e in event_map_json:
    print(e)
    event_map[e["event_name"]] = e["workflow_names"]

print(event_map)