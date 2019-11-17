import json
import os
import sys
from datetime import datetime
import requests
from random import shuffle

from libs import yt

folder_dir = os.path.dirname(os.path.realpath(__file__))

database_name = folder_dir + '/trip_database.json'

print("\nReading existing videos...")
json_file = dict()
with open(database_name, 'r') as f:
    json_file = json.load(f)
old_json_size = len(json_file["videos"])
old_json_bad_size = len(json_file["bad_videos"])
print("Read", old_json_size, "OLD video IDs!\n")

print("Pruning invalid/unwanted video ID's from main database...")
json_file["videos"] = yt.remove_bad_ids_and_channels(json_file["videos"], json_file["bad_channels"])
new_json_size = len(json_file["videos"])
print("Removed", old_json_size - new_json_size,"invalid/unwanted IDs from main database, only", new_json_size, "remaining.\n")

print("Pruning invalid/unwanted bad video ID's from main database...")
json_file["bad_videos"] = yt.remove_bad_ids_and_channels(json_file["bad_videos"], json_file["bad_channels"])
new_json_bad_size = len(json_file["bad_videos"])
print("Removed", old_json_bad_size - new_json_bad_size,"invalid/unwanted bad IDs from main database, only", new_json_bad_size, "remaining.\n")

print("Shuffling ID's...")
shuffle(json_file["videos"])
print("ID's shuffled!\n")

print("Saving main database...")
json_file["updated"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
with open(database_name, 'w') as f:
    json.dump(json_file, f)
print("Saved cleaned main database!")
