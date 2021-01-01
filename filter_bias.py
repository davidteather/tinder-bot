import glob
import os
import random

os.chdir("images/classified")
neg = len(glob.glob("negative/*"))
pos = len(glob.glob("positive/*"))

print(neg) 
print(pos)

if neg > pos:
    # more negatives than positives
    diff = neg - pos

    negatives = glob.glob('negative/*')
    random.shuffle(negatives)

    for f in range(diff):
        # delete some negative photos
        os.remove(negatives[f])
elif pos > neg:
    # more negatives than positives
    diff = pos - neg

    positives = glob.glob('positive/*')
    random.shuffle(positives)

    for f in range(diff):
        # delete some negative photos
        os.remove(positives[f])
c