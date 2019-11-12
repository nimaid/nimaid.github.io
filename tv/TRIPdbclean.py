import json
import os
import sys
from datetime import datetime
import requests

folder_dir = os.path.dirname(os.path.realpath(__file__))

database_name = folder_dir + '/trip_database.json'


api_base_url = 'https://www.youtube.com/oembed?format=json&url=https://www.youtube.com/watch?v='
def is_valid_id(id_code):
    result = requests.get(api_base_url + id_code)
    if result.status_code == 404:
        return False
    elif result.status_code == 200:
        return True
    else:
        return True

def remove_bad_ids(vids_in, dot_interval=100, cross_interval=1000):
    print("Checking " + str(len(vids_in)) + " videos... ('.' = " + str(dot_interval) + ", 'x' = " + str(cross_interval) + ")")
    vids_out = []
    progress_count = 0
    for vid_id in vids_in:
        if is_valid_id(vid_id):
            vids_out.append(vid_id)
        progress_count += 1
        if progress_count % cross_interval == 0:
            sys.stdout.write("x")
            sys.stdout.flush()
        elif progress_count % dot_interval == 0:
            sys.stdout.write(".")
            sys.stdout.flush()
    print("done")
    return vids_out

print("\nReading existing videos...")
json_file = dict()
with open(database_name, 'r') as f:
    json_file = json.load(f)
print("Read " + str(len(json_file["videos"])) + " OLD video IDs!\n")

print("Pruning bad video ID's from main database...")
old_json_size = len(json_file["videos"])
json_file["videos"] = remove_bad_ids(json_file["videos"])
json_file["updated"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
with open(database_name, 'w') as f:
    json.dump(json_file, f)
new_json_size = len(json_file["videos"])
print("Removed " + str(old_json_size - new_json_size) + " bad IDs from main database, only " + str(new_json_size) + " remaining.")
