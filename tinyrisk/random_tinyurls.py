import random
import string
import urllib.request as urlreq
import csv
import json
import time
import itertools

filename = 'random_tinyurls'
SAVE_INT = 100

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
                    print('~' + address, end='')
                return (link, result[1])
            else:
                link_not_valid = True
                if(not quiet):
                    print(link + ' is not valid...')
                else:
                    print('.', end='')



count = SAVE_INT
while(True):
    # x and y appear to be the only valid prefixes
    link = random_tinyurl(quiet=True, prefixs=['x','y'])

    with open(filename + '.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(link)

    if count >= SAVE_INT - 1:
        with open(filename + '.csv', 'r') as f:
            reader = csv.reader(f)
            links = list(reader)
        links = [k for k,_ in itertools.groupby(links)]

        links_obj = {}
        links_obj['links'] = links

        print('~' + str(len(links)), end='')

        with open(filename + '.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(links)

        print('~' + 'csv', end='')
        
        with open(filename + '.json', 'w') as f:
            json.dump(links_obj, f)

        print('~' + 'json', end='')

    count += 1
    count %= SAVE_INT
