from tinder import Tinder

import logging
import time
import json
import os

t = Tinder()
t.login_google(os.environ['google_username'], os.environ['google_password'])

time.sleep(1)


profiles = []

t.slide_current()
time.sleep(2)

index_error = 0
while True:
    try:
        profile = t.extract_current()
        print(profile)
        profiles.append(profile)
        t.dislike()
        with open('data.json', 'w+', encoding='utf-8') as f:
            json.dump({'profiles': profiles}, f, ensure_ascii=False, indent=4)
        index_error = 0
    except KeyboardInterrupt:
        break
    except IndexError:
        #t.dislike()
        index_error += 1

        if index_error < 3:
            time.sleep(5)
        else:
            t.dislike()
            time.sleep(5)
    except Exception as e:
        logging.critical(e)
        continue
