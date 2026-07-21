import json
from pathlib import Path
from uuid import uuid4

ROOT = Path(__file__).parent

collection = {
    "info": {
        "_postman_id": str(uuid4()),
        "name": "Mogadpally Brothers API",
        "description": "Generated automatically.",
        "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
    },
    "item": [],
    "variable": []
}

for folder in sorted(ROOT.iterdir()):
    if not folder.is_dir():
        continue

    folder_item = {
        "name": folder.name,
        "item": []
    }

    for file in sorted(folder.glob("*.json")):
        with open(file, encoding="utf-8") as f:
            folder_item["item"].append(json.load(f))

    collection["item"].append(folder_item)

output = ROOT / "Mogadpally_Brothers.postman_collection.json"

with open(output, "w", encoding="utf-8") as f:
    json.dump(collection, f, indent=2)

print(f"Collection created successfully: {output}")