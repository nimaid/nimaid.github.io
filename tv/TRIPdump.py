import csv
import json
import os
from datetime import datetime

import yt
import reddit_videos

subreddit = 'trippyvideos'

import TRIPdbclean  # Prune the main DB
print("")

old_json_size = TRIPdbclean.old_json_size

clean_json = TRIPdbclean.json_file

folder_dir = TRIPdbclean.folder_dir
database_name = TRIPdbclean.database_name

dump_name = folder_dir + '/trip_database_dump.csv'

all_vids = []
print("Reading existing dump...")
with open(dump_name, 'r') as f:
    reader = csv.reader(f)
    all_vids = [i[0] for i in list(reader)]
exist_size = len(all_vids)
print("Read " + str(exist_size) + " valid OLD video IDs!\n")

print("Getting new videos...")
for x in reddit_videos.get_max_all(subreddit, prune=False):
    all_vids.append(x)
all_vids = list(set(all_vids))
new_size = len(all_vids)
print("Got " + str(new_size - exist_size) + " new ID's!\n")

print("Pruning bad video ID's...")
valid_vids = yt.remove_bad_ids(all_vids)
prune_size = len(valid_vids)
print("Removed " + str(new_size - prune_size) + " bad IDs, only " + str(prune_size) + " remaining.\n")

print("Removing ID's in main database from dump...")
valid_vids = [x for x in valid_vids if x not in clean_json["videos"]]
valid_vids = [x for x in valid_vids if x not in clean_json["bad_videos"]]
final_size = len(valid_vids)
print("Removed " + str(prune_size - final_size) + " existing IDs, only " + str(final_size) + " remaining.\n")

print("Saving CSV...")
with open(dump_name, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows([[i] for i in valid_vids])
print("Saved " + str(final_size - exist_size) + " new videos to CSV!")


