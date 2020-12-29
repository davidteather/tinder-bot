from tinder import Tinder
import time
import json
import os

t = Tinder()
t.login_google(os.environ['google_username'], os.environ['google_password'])

time.sleep(1)


profiles = []

t.slide_current()
time.sleep(2)
while True:
    try:
        profile = t.extract_current()
        print(profile)
        profiles.append(profile)
        t.dislike()
        with open('data.json', 'w+', encoding='utf-8') as f:
            json.dump({'profiles': profiles}, f, ensure_ascii=False, indent=4)
    except KeyboardInterrupt:
        break
    except:
        continue
