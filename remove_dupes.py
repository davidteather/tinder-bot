import os
import json


all_profiles = []

dupe_count = 0
with open('data.json', 'r', encoding='utf-8') as i:
    data = json.loads(i.read())
    for p in data['profiles']:
        if p not in all_profiles:
            all_profiles.append(p)
        else:
            dupe_count += 1

with open('data_filtered.json', 'w+', encoding='utf-8') as f:
    json.dump({'profiles': all_profiles}, f, ensure_ascii=False, indent=4)

print(dupe_count)