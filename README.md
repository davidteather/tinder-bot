# tinder-bot

This is a repository to use AI to automate tinder stuff. AI part heavily based on [Auto-Tinder](https://github.com/joelbarmettlerUZH/auto-tinder), but it doesn't use the tinder API directly so it's more visual for the accompanying [YouTube Video](https://youtu.be/OnWH1GnzyNE).

# Demo/YouTube Video

[![](assets/tinder_bot.png?raw=true)](https://youtu.be/OnWH1GnzyNE)

## Important Notes

I do recommend just following [Auto-Tinder](https://github.com/joelbarmettlerUZH/auto-tinder) if you don't want the visual aspect of swiping on a selenium instance because it complicates things a lot more. However, you can follow this messy guide to use this semi-messy code.

## Part 1 - Data Aggregation

We need photos to train the AI on, so first off, you'll need a Tinder account linked to a google account, you'll need to set `google_password` and `google_username` as environment variables that correspond to your google credentials. Then you can run `python extract_profiles.py` , it will log you into google and prompt you `please log into google` hit enter after you finish 2 factor authentication.


The script will save profiles to data.json. Once you're satisfied with the amount of profiles you've extracted run `python remove_dupes.py` to make sure that you don't have duplicate profiles. You can also run `python stats.py` if you want to see some basic statistics on your dataset, however this isn't required.

## Part 2 - Downloading Images

Run `python image_downloader.py` this will download all the images in data.json

## Part 3 - Labeling Data

You'll now need to classify a like or dislike or not a person for all the photos you downloaded. Run `python image_classifier.py` , left click is a like, right click is a dislike, and middle mouse is if the photo isn't a person. (If you have non-people in your training data it might mess up the AI)

## Part 4 - Pre-Processing

Run `python prepare_data.py` this will crop and convert images to gray-scale

## Part 5 - Training

Now you have to train the AI, **MAKE SURE ALL THE DIRECTORIES EXIST THAT ARE REFERENCED IN THIS COMMAND** (I made this mistake after 4 hours of training :( ), you can mess around with some of the arguments as to get a good model your training data is different from mine.

```
python retrain.py --bottleneck_dir=tf/training_data/bottlenecks --saved_model_dir=tf/training_data/inception --summaries_dir=tf/training_data/summaries/basic --output_graph=tf/training_output/retrained_graph.pb --output_labels=tf/training_output/retrained_labels.txt --image_dir=./images/classified --how_many_training_steps=25000 --testing_percentage=20 --learning_rate=0.0005
```

## Part 6 - Using The AI

Follow the steps for environment variables in part 1, but run `python use_model.py` and hopefully it'll work for you!


There are some directories that don't auto generate and I forget what directories they are as they were defined in [Auto-Tinder](https://github.com/joelbarmettlerUZH/auto-tinder). I also probably forgot to include something here that's critical to getting this working.