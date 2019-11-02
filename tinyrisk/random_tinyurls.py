import random
import string
import urllib.request as urlreq
import csv
import json
import itertools
import sys
import signal
import os

filename = 'random_tinyurls'
SAVE_INT = 100

folder_dir = os.path.dirname(os.path.realpath(__file__))
filename = folder_dir + '/' + filename

def print_raw(message):
    sys.stdout.write(message)
    sys.stdout.flush()

def random_string(stringLength=10):
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(stringLength))

def resolve_tinyurl(url):
    try:
        result = urlreq.urlopen(url)
        return (True, result.url)
    except:
        return (False, '')

def random_tinyurl(quiet=False, prefixs = ['']):
        link_not_valid = True
        link_base = 'https://tinyurl.com/'
        while(link_not_valid):
            prefix = random.choice(prefixs)
            address = prefix + random_string(8 - len(prefix))
            link = link_base + address
            result = resolve_tinyurl(link)
            if(result[0]):
                link_not_valid = False
                if(not quiet):
                    print(link + ' = ' + result[1])
                else:
                    print_raw('~' + address)
                return (link, result[1])
            else:
                link_not_valid = True
                if(not quiet):
                    print(link + ' is not valid...')
                else:
                    print_raw('.')


def save_all():
    with open(filename + '.csv', 'r') as f:
        reader = csv.reader(f)
        links = list(reader)

    # Remove duplicates
    links = [k for k,_ in itertools.groupby(links)]

    # Remove tinyurl.com/nospam links
    spamindex = [i for i, s in enumerate(links) if 'tinyurl.com/nospam' in s[1]]
    for i in spamindex[::-1]:
        temp = links.pop(i)
    
    links_obj = {}
    links_obj['links'] = links

    print_raw('~' + str(len(links)))

    with open(filename + '.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(links)

    print_raw('~' + 'csv')
    
    with open(filename + '.json', 'w') as f:
        json.dump(links_obj, f)

    print_raw('~' + 'json')


kill_loop = False
def signal_handler(signal, frame):
    global kill_loop
    print_raw('~Exiting')
    kill_loop = True

signal.signal(signal.SIGINT, signal_handler)


count = 0
while(not kill_loop):
    # x and y appear to be the only valid prefixes
    link = random_tinyurl(quiet=True, prefixs=['x', 'y'])

    with open(filename + '.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(link)

    if (count >= SAVE_INT - 1) or (kill_loop):
        save_all()

    count += 1
    count %= SAVE_INT

print('\nThank you for being risky today. ;)')
