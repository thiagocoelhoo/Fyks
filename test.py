import json

with open("themes.json", "r") as f:
    data = json.load(f)

print(data)