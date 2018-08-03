import praw
from urllib import parse

reddit_client_id = 'EwDc71J3wNcQqw'
reddit_client_secret = 'mB36bJ5cNX39zjcw0gLMPycTjzU'

subreddit = 'interdimensionalcable'

reddit = praw.Reddit(client_id=reddit_client_id,
                     client_secret=reddit_client_secret,
                     user_agent='InterdimensionalCableBox')

def parse_query(input_query):
    query_temp = input_query.split('&')
    query = {}
    for x in query_temp:
        split = x.split('=')
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
        if parsed_url != False:
            videos.append(parsed_url)

    return videos

def get_max_top():
    videos = []
    for submission in reddit.subreddit(subreddit).top(limit=None):
        url = submission.url
        parsed_url = parse_youtube_link(url)
        if parsed_url != False:
            videos.append(parsed_url)

    return videos

def get_max_hot():
    videos = []
    for submission in reddit.subreddit(subreddit).hot(limit=None):
        url = submission.url
        parsed_url = parse_youtube_link(url)
        if parsed_url != False:
            videos.append(parsed_url)

    return videos

def get_random():
    loop = True
    while loop:
        rand = reddit.subreddit(subreddit).random().url
        print(rand)
        parsed_rand = parse_youtube_link(rand)
        if parsed_rand != False:
            result = parsed_rand
            loop = False

    return result
