import os
import json

files = ['data_1.json', "data_2.json"]

all_profiles = []

for f in files:
    with open(f, 'r', encoding='utf-8') as i:
        data = json.loads(i.read())
        for p in data['profiles']:
            all_profiles.append(p)

with open('data_combined.json', 'w+', encoding='utf-8') as f:
    json.dump({'profiles': all_profiles}, f, ensure_ascii=False, indent=4)

for f in files:
    os.remove(f)