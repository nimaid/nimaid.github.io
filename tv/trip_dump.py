import csv
import json
import os
from datetime import datetime

import yt
import reddit_videos

subreddit = 'trippyvideos'

import trip_dbclean  # Prune the main DB
print("")

old_json_size = trip_dbclean.old_json_size

clean_json = trip_dbclean.json_file

folder_dir = trip_dbclean.folder_dir
database_name = trip_dbclean.database_name

dump_name = folder_dir + '/trip_database_dump.csv'

all_vids = []
print("Reading existing dump...")
with open(dump_name, 'r') as f:
    reader = csv.reader(f)
    all_vids = [i[0] for i in list(reader)]
exist_size = len(all_vids)
print("Read", exist_size, "valid OLD video IDs!\n")

print("Getting new videos...")
for x in reddit_videos.get_max_all(subreddit, prune=False):
    all_vids.append(x)
all_vids = list(set(all_vids))
new_size = len(all_vids)
print("Got", new_size - exist_size, "new ID's!\n")

print("Removing ID's in main database from dump...")
all_vids = [x for x in all_vids if x not in clean_json["videos"]]
all_vids = [x for x in all_vids if x not in clean_json["bad_videos"]]
removed_size = len(all_vids)
print("Removed", new_size - removed_size, "existing IDs, only", removed_size, "remaining.\n")

print("Pruning bad video ID's...")
valid_vids = yt.remove_bad_ids(all_vids)
prune_size = len(valid_vids)
print("Removed", removed_size - prune_size, "bad IDs, only", prune_size, "remaining.\n")

print("Saving CSV...")
with open(dump_name, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows([[i] for i in valid_vids])
print("Saved", prune_size - exist_size, "new videos to CSV!", prune_size, "total.")


