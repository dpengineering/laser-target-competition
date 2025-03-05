import json

# Python dictionary
data = {
    "rank": 1,
    "name": "HLS",
    "score": 12800
}

# Convert Python dictionary to JSON string
json_string = json.dumps(data, indent=4)
print("JSON string:", json_string)

# Convert JSON string to Python dictionary
new_data = json.loads(json_string)
print("Python dictionary:", new_data)

# Writing JSON data to a file
with open("data.json", "w") as f:
    json.dump(data, f, indent=4)

# Reading JSON data from a file
with open("data.json", "r") as f:
    loaded_data = json.load(f)
print("Loaded data from file:", loaded_data)