import random
import string
import urllib.request as urlreq
import csv
import json
import time
import itertools

filename = 'random_tinyurls'

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



try:
    while(True):
        # x and y appear to be the only valid prefixes
        link = random_tinyurl(quiet=True, prefixs=['x','y'])

        with open(filename + '.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(link)

        time.sleep(0.1)
except KeyboardInterrupt:
    print('\nConverting to JSON...')

    with open(filename + '.csv', 'r') as f:
        reader = csv.reader(f)
        links = list(reader)

    links_obj = {}
    links_obj['links'] = [k for k,_ in itertools.groupby(links)]
    
    with open(filename + '.json', 'w') as f:
        json.dump(links_obj, f)

    print('Exported ' + str(len(links)) + ' links to ' + filename + '.json')
