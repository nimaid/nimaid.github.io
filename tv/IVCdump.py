import praw
from urllib import parse
from random import shuffle
import requests
import sys

reddit_client_id = 'EwDc71J3wNcQqw'
reddit_client_secret = 'mB36bJ5cNX39zjcw0gLMPycTjzU'

subreddit = 'interdimensionalcable'

print("Interdimensional Video Catcher by nimaid (made for tv.nimaid.com)\n")

all_vids = []

print("Trying to read index.html...")
with open("index.html", "r", encoding="utf8") as f:
    index_html = f.read()
print("Read index.html!\n")

print("Trying to find variable location...")
start_index = index_html.find("var IVCdump")
if start_index == -1:
    print("Variable not found! Are you sure this is the right index.html? Exiting...")
    quit()
end_index = index_html.find(";", start_index) + 1
print("Found indexes to be " + str(start_index) + " to " + str(end_index) + "...\n")

print("Extracting existing videos...")
exist_str = index_html[start_index:end_index]
exist_start_index = exist_str.find("[")
exist_vids = exist_str[exist_start_index+2:-3].split('", "')
exist_size = len(exist_vids)
all_vids += exist_vids
print("Extracted " + str(exist_size) + " OLD video IDs!\n")

print("Connecting to Reddit...")
reddit = praw.Reddit(client_id=reddit_client_id,
                     client_secret=reddit_client_secret,
                     user_agent='InterdimensionalCableBox')
print("Fuck yes, we're in!\n")

api_base_url = 'https://www.youtube.com/oembed?format=json&url=https://www.youtube.com/watch?v='
def is_valid_id(id_code):
    result = requests.get(api_base_url + id_code)
    if result.status_code == 404:
        return False
    elif result.status_code == 200:
        return True
    else:
        return True

def parse_query(input_query):
    query_temp = input_query.split('&')
    query = {}
    for x in query_temp:
        split = x.split('=')
        if len(split) == 2:
            query.update({split[0]:split[1]})

    return query

def parse_youtube_link(link):
    link_parsed = parse.urlparse(link)
    if (link_parsed.netloc == 'www.youtube.com') or (link_parsed.netloc == 'youtube.com') or (link_parsed.netloc == 'm.youtube.com'):            
        if link_parsed.path == '/watch':
            #always a video (could have query codes)
            raw_query = link_parsed.query
            if raw_query[0] == '&':
                raw_query = raw_query[1:]
            if raw_query[-1] == '&':
                raw_query = raw_query[:-1]
            raw_query = raw_query.replace('repost', 'repost=1')
            raw_query = raw_query.replace('&t', '&t=0s')
            return parse_query(raw_query)
        elif link_parsed.path == '/attribution_link':
            #maybe a video? (could have query codes)
            attrib_parsed = parse.urlparse(parse.unquote(link_parsed.query))
            path_parsed = parse_query(attrib_parsed.path)
            
            if path_parsed['u'] == '/watch':
                #it IS as video!
                return parse_query(attrib_parsed.query)
    elif link_parsed.netloc == 'youtu.be':
        #always a video (no query codes allowed)
        return{'v':link_parsed.path[1:]}

    return False

def get_max_new():
    videos = []
    for submission in reddit.subreddit(subreddit).new(limit=None):
        url = submission.url
        parsed_url = parse_youtube_link(url)
        if (parsed_url != False) and ('v' in parsed_url):
            videos.append(parsed_url)

    return videos

def get_max_top():
    videos = []
    for submission in reddit.subreddit(subreddit).top(limit=None):
        url = submission.url
        parsed_url = parse_youtube_link(url)
        if (parsed_url != False) and ('v' in parsed_url):
            videos.append(parsed_url)

    return videos

def get_max_hot():
    videos = []
    for submission in reddit.subreddit(subreddit).hot(limit=None):
        url = submission.url
        parsed_url = parse_youtube_link(url)
        if (parsed_url != False) and ('v' in parsed_url):
            videos.append(parsed_url)

    return videos


print("Getting as many TOP videos as allowed...")
for x in get_max_top():
    all_vids.append(x['v'][0:11])
top_size = len(all_vids) - exist_size
print("Got " + str(top_size) + " TOP video IDs! We have sugar...\n")

print("Getting as many HOT videos as allowed...")
for x in get_max_hot():
    all_vids.append(x['v'[0:11]])
hot_size = len(all_vids) - top_size - exist_size
print("Got " + str(hot_size) + " HOT video IDs! We have spice...\n")

print("Getting as many NEW videos as allowed...")
for x in get_max_new():
    all_vids.append(x['v'][0:11])
new_size = len(all_vids) - hot_size - top_size - exist_size
print("Got " + str(new_size) + " NEW video IDs! We have everything nice...\n")

print("Throwing all the ingredients into a bowl...")
all_vids = list(set(all_vids))
min_size = len(all_vids)
print("Some of the same IDs merged. Now, there are only " + str(min_size) + " unique video IDs.\n")

print("Mixing the ingredients well...")
shuffle(all_vids)
print("Ingredients mixed pretty good, if I do say so myself.\n")

dot_interval = 100
cross_interval = 1000
print("Pruning bad video ID's... ('.' = " + str(dot_interval) + ", 'x' = " + str(cross_interval) + ")")
valid_vids = []
progress_count = 0
for vid_id in all_vids:
    if is_valid_id(vid_id):
        valid_vids.append(vid_id)
    progress_count += 1
    if progress_count % cross_interval == 0:
        sys.stdout.write("x")
        sys.stdout.flush()
    elif progress_count % dot_interval == 0:
        sys.stdout.write(".")
        sys.stdout.flush()
print("")
prune_size = len(valid_vids)
print("Removed " + str(min_size - prune_size) + " bad IDs, only " + str(prune_size) + " remaining.")

print("Adding Chemical X...")
IVCdump_output = "var IVCdump = [\"" + "\", \"".join(valid_vids) + "\"];"
print("Done! Variable string is compiled.\n")

print("Replacing variable with new ID database...")
index_html = index_html[:start_index] + IVCdump_output + index_html[end_index:]
print("Replaced variable with updated version!\n")

print("Overwritting original index.html...")
with open("index.html", "w", encoding="utf8") as f:
    f.write(index_html)
print("All done! Added " + str(min_size - exist_size) + " new videos! Have a good day!")


