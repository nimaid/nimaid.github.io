import csv
import json
import os
from datetime import datetime

print("r/TrippyVideos Database Updater by nimaid (made for trip.nimaid.com)")

import TRIPdump  # Clean main db and update CSV

old_json_size = TRIPdump.old_json_size
valid_vids = TRIPdump.valid_vids
clean_json = TRIPdump.clean_json
dump_name = TRIPdump.dump_name
database_name = TRIPdump.database_name

final_json_size = len(clean_json["videos"])
valid_vids_size = len(valid_vids)

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

print("")
vet_videos = ask_question("Would you like to vet dumped videos now? Y/N")
unvetted_vids = []
videos_left_to_vet = valid_vids_size
if(vet_videos == "Y"):
    print("Vetting videos now! Enter 'Q' to exit...\n")
    for i, vid in enumerate(valid_vids):
        print(videos_left_to_vet, "videos left! Current ID:", vid)
        vid_verdict = ask_question("Is this (G)ood, (B)ad, or should I (S)kip it? G/B/[S]/Q",
                                   options=["G", "B", "S", "Q"],
                                   default="S")
        if vid_verdict == "G":
            print("Adding to good videos..")
            clean_json["videos"].append(vid)
            print("Added", vid, "to good videos!\n")
        elif vid_verdict == "B":
            print("Adding to bad videos..")
            clean_json["bad_videos"].append(vid)
            print("Added", vid, "to bad videos!\n")
        elif vid_verdict == "Q":
            print("Stopping vetting process...\n")
            for v in valid_vids[i:]:
                unvetted_vids.append(v)
            break;
        else:
            print("Skipping ", vid, "...\n")
        videos_left_to_vet -= 1
    
    vetted_g_vids_size = len(clean_json["videos"])
    vetted_b_vids_size = len(clean_json["bad_videos"])

    print("Vetting done. Saving database to file...")
    clean_json["updated"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open(database_name, 'w') as f:
        json.dump(clean_json, f)
    print("Saved", vetted_g_vids_size, "videos to the database!\n")

    print("Saving unvetted videos...")
    with open(dump_name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows([[i] for i in unvetted_vids])
    unvetted_size = len(unvetted_vids)
    print("Saved", unvetted_size, "unvetted videos!\n")
    
    print("All done!", vetted_g_vids_size - old_json_size, "new videos added to database!", vetted_g_vids_size, "total,", unvetted_size, "unvetted.")  
else:
    print("Not vetting videos!", final_json_size, "videos in database,", valid_vids_size, "unvetted.")
