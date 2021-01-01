import statistics
import json

with open("data.json", 'r', encoding='utf-8') as i:
    data = json.loads(i.read())

print(f"# Of Profiles: {len(data['profiles'])}")

names = []
for p in data['profiles']:
    names.append(p['name'])
print(f"Most Common Name: {statistics.mode(names)}")


total_images = 0
for p in data['profiles']:
    for image in p['images']:
        total_images += 1

print(f"Total Images: {total_images}")