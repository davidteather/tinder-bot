import statistics
import json
import datetime
import requests
import os

if not os.path.isdir('images'):
    os.mkdir('images')

if not os.path.isdir('images/unclassified'):
    os.mkdir('images/unclassified')

folder = 'images/unclassified'

with open("data_1.json", 'r', encoding='utf-8') as i:
    data = json.loads(i.read())

images = []
for p in data['profiles']:
    for image in p['images']:
        images.append(image)

index = -1
index += len([name for name in os.listdir(folder) if os.path.isfile(os.path.join(folder, name))]) * 100
for i in images[:5000]:
    index += 1
    req = requests.get(i, stream=True)
    if req.status_code == 200:
        url_split = i.split(".")
        with open(f"{folder}/{index}." + url_split[len(url_split)-1], "wb") as f:
            f.write(req.content)