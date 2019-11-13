from random import shuffle
import json
import os
from datetime import datetime

from libs import reddit_videos
yt = reddit_videos.yt

folder_dir = os.path.dirname(os.path.realpath(__file__))

subreddit = 'interdimensionalcable'

database_name = folder_dir + '/interdimensional_database.json'

print("Interdimensional Cable Box Database Updater by nimaid (made for tv.nimaid.com)\n")

intro_vid = ""
all_vids = []

json_file = dict()

print("Reading existing videos...")
with open(database_name, 'r') as f:
    json_file = json.load(f)
all_vids = json_file['videos']
exist_size = len(all_vids)
print("Read " + str(exist_size) + " OLD video IDs!\n")

print("Getting new videos...")
for x in reddit_videos.get_max_all(subreddit, prune=False):
    all_vids.append(x)
all_vids = list(set(all_vids))
new_size = len(all_vids)
print("Got " + str(new_size - exist_size) + " new ID's! Now there are " + str(new_size) + " IDs.\n")

print("Pruning bad video ID's...")
valid_vids = yt.remove_bad_ids(all_vids)
prune_size = len(valid_vids)
print("Removed " + str(new_size - prune_size) + " bad IDs, only " + str(prune_size) + " remaining.\n")

print("Shuffling ID's...")
shuffle(valid_vids)
print("ID's shuffled!\n")

print("Updating database.json...")
json_file['videos'] = valid_vids
json_file['updated'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
with open(database_name, 'w') as f:
    json.dump(json_file, f)
print("All done! Added " + str(prune_size - exist_size) + " new videos! Have a good day!")


