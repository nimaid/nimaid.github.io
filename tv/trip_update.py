#!/usr/bin/env python3

import csv
import json
import os
from datetime import datetime

try:
    import webbrowser
    can_use_webbrowser = True
except ImportError:
    can_use_webbrowser = False
    print("WARNING: 'webbrowser' module not found!")
    print("The program will still work, but it will not be able to automatically open videos.")
    print("Run 'pip install webbrowser' to enable this feature!")

print("r/TrippyVideos Database Updater by nimaid (made for trip.nimaid.com)")

import trip_dump  # Clean main db and update CSV

old_json_size = trip_dump.old_json_size
valid_vids = trip_dump.valid_vids
clean_json = trip_dump.clean_json
dump_name = trip_dump.dump_name
database_name = trip_dump.database_name

final_json_size = len(clean_json["videos"])
valid_vids_size = len(valid_vids)

if can_use_webbrowser:
    wb = webbrowser.get()
    open_in_browser = False

youtube_link_base = "https://youtu.be/"

def ask_question(question="Y/N", options=["Y", "N"], default=None):
    options = [x.upper() for x in options]
    answer = None
    error_string = "Please enter one of the following:"
    while answer not in options:
        answer = input(question + ": ").upper()
        if answer in options:
            return answer
        else:
            if answer.strip() == "":
                if (default == None) or (default not in options):
                    print(error_string, options)
                else:
                    return default
            else:
                print(error_string, options)

def save_progress(json_database, csv_dump):
    json_database["updated"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open(database_name, 'w') as f:
        json.dump(json_database, f)
    
    with open(dump_name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows([[i] for i in csv_dump])

print("")
vet_videos = ask_question("Would you like to vet dumped videos now? Y/N")
unvetted_vids = []
if(vet_videos == "Y"):
    if can_use_webbrowser:
        open_in_browser_resp = ask_question("Would you also like to automatically open them in your default browser? Y/[N]", default="N")
        if open_in_browser_resp == "Y":
            open_in_browser = True
            print("Will open videos in default browser!\n")
        else:
            open_in_browser = False
            print("Will not open videos!\n")
    
    print("Vetting videos now! Enter 'Q' to exit...\n")
    for i, vid in enumerate(valid_vids):
        current_video_link = youtube_link_base + vid
        print(valid_vids_size - i, "videos left! Current video:", current_video_link)
        if can_use_webbrowser:
            if open_in_browser:
                print("Opening in browser...")
                wb.open_new_tab(current_video_link)
        
        vid_verdict = ask_question("Is this (G)ood, (B)ad, or should I (S)kip it? G/B/[S]/Q",
                                   options=["G", "B", "S", "Q"],
                                   default="S")
        if vid_verdict == "G":
            print("Adding to good videos..")
            clean_json["videos"].append(vid)
            print("Added", vid, "to good videos!")
        elif vid_verdict == "B":
            print("Adding to bad videos..")
            clean_json["bad_videos"].append(vid)
            print("Added", vid, "to bad videos!")
        elif vid_verdict == "Q":
            print("Stopping vetting process...\n")
            unvetted_vids += valid_vids[i:]
            break;
        else:
            print("Skipping", vid, "...")
            unvetted_vids.append(vid)
        
        save_progress(clean_json, unvetted_vids + valid_vids[i+1:])
        print("Saved progress.\n")
    
    vetted_g_vids_size = len(clean_json["videos"])
    vetted_b_vids_size = len(clean_json["bad_videos"])
    unvetted_size = len(unvetted_vids)

    print("Vetting done. Saving files...")
    save_progress(clean_json, unvetted_vids)
    print("Saved", vetted_g_vids_size, "videos to the JSON database!")
    print("Saved", unvetted_size, "unvetted videos to the CSV dump!\n")
    
    print("All done!", vetted_g_vids_size - old_json_size, "new good videos added to database!", vetted_g_vids_size, "total,", unvetted_size, "unvetted.")  
else:
    print("Not vetting videos!", final_json_size, "videos in database,", valid_vids_size, "unvetted.")
