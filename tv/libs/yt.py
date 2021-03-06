import requests
import sys
from urllib import parse

SUCCESS_CODES = [200]
FAIL_CODES = [401, 404]
API_BASE_URL = 'https://www.youtube.com/oembed?format=json&url=https://www.youtube.com/watch?v='

def get_id_info(id_code):
    result = requests.get(API_BASE_URL + id_code)
    if result.status_code in FAIL_CODES:
        return False
    elif result.status_code in SUCCESS_CODES:
        return result.json()
    else:
        return result.json()

def get_id_channel(id_code):
    id_info = get_id_info(id_code)
    if id_info == False:
        return False
    else:
        return id_info["author_url"].split("/")[-1]
    
def is_valid_id(id_code):
    result = requests.get(API_BASE_URL + id_code)
    if result.status_code in FAIL_CODES:
        return False
    elif result.status_code in SUCCESS_CODES:
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

def remove_bad_ids(vids_in, dot_interval=100, cross_interval=1000):
    print("Checking", len(vids_in), "videos... ('.' = " + str(dot_interval) + ", 'x' = " + str(cross_interval) + ")")
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

def remove_bad_ids_and_channels(vids_in, bad_channels, dot_interval=100, cross_interval=1000):
    print("Checking", len(vids_in), "videos... ('.' = " + str(dot_interval) + ", 'x' = " + str(cross_interval) + ")")
    vids_out = []
    progress_count = 0
    for vid_id in vids_in:
        vid_channel = get_id_channel(vid_id)
        if vid_channel != False:
            if vid_channel not in bad_channels:
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
