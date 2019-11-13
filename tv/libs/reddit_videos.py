import praw

from . import yt

reddit_client_id = 'EwDc71J3wNcQqw'
reddit_client_secret = 'mB36bJ5cNX39zjcw0gLMPycTjzU'
reddit_user_agent = 'VideoGrabber'

def connect():
    return praw.Reddit(client_id=reddit_client_id,
                       client_secret=reddit_client_secret,
                       user_agent=reddit_user_agent)

def get_max_new(reddit, subreddit):
    videos = []
    for submission in reddit.subreddit(subreddit).new(limit=None):
        url = submission.url
        parsed_url = yt.parse_youtube_link(url)
        if (parsed_url != False) and ('v' in parsed_url):
            videos.append(parsed_url)

    return videos

def get_max_top(reddit, subreddit):
    videos = []
    for submission in reddit.subreddit(subreddit).top(limit=None):
        url = submission.url
        parsed_url = yt.parse_youtube_link(url)
        if (parsed_url != False) and ('v' in parsed_url):
            videos.append(parsed_url)

    return videos

def get_max_hot(reddit, subreddit):
    videos = []
    for submission in reddit.subreddit(subreddit).hot(limit=None):
        url = submission.url
        parsed_url = yt.parse_youtube_link(url)
        if (parsed_url != False) and ('v' in parsed_url):
            videos.append(parsed_url)

    return videos

def get_max_all(subreddit, prune=True):
    reddit = connect()
    all_vids = []
    
    print("Getting as many TOP videos as allowed...")
    for x in get_max_top(reddit, subreddit):
        all_vids.append(x['v'][0:11])
    top_size = len(all_vids)
    print("Got", top_size, "TOP video IDs!\n")

    print("Getting as many HOT videos as allowed...")
    for x in get_max_hot(reddit, subreddit):
        all_vids.append(x['v'[0:11]])
    hot_size = len(all_vids) - top_size
    print("Got", hot_size, "HOT video IDs!\n")

    print("Getting as many NEW videos as allowed...")
    for x in get_max_new(reddit, subreddit):
        all_vids.append(x['v'][0:11])
    new_size = len(all_vids) - hot_size - top_size
    print("Got", new_size, "NEW video IDs!\n")

    all_vids = list(set(all_vids))
    print("Only", len(all_vids), "IDs were unique.")

    if prune:
        print("Pruning bad video ID's...")
        valid_vids = yt.remove_bad_ids(all_vids)
        prune_size = len(valid_vids)
        print("Removed", new_size - prune_size, "bad IDs, only", prune_size, "remaining.")
        return valid_vids
    else:
        return all_vids
