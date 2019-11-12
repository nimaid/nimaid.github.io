import json
import os
import sys
from datetime import datetime
import requests
from random import shuffle

import yt

folder_dir = os.path.dirname(os.path.realpath(__file__))

database_name = folder_dir + '/trip_database.json'

print("\nReading existing videos...")
json_file = dict()
with open(database_name, 'r') as f:
    json_file = json.load(f)
old_json_size = len(json_file["videos"])
print("Read", old_json_size, "OLD video IDs!\n")

print("Pruning bad video ID's from main database...")
json_file["videos"] = yt.remove_bad_ids(json_file["videos"])
new_json_size = len(json_file["videos"])
print("Removed", old_json_size - new_json_size,"bad IDs from main database, only", new_json_size, "remaining.\n")

print("Shuffling ID's...")
shuffle(json_file["videos"])
print("ID's shuffled!\n")

print("Saving main database...")
json_file["updated"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
with open(database_name, 'w') as f:
    json.dump(json_file, f)
print("All done!")
