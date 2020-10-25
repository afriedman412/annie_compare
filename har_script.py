import sys
import json
import os

har_dict = {}
root = './har_files/'
for har in os.listdir(root):
    dir_ = har.split('_')[1]
    if dir_ not in har_dict:
        har_dict[dir_] = {}
        
    h = json.load(open(root + har, 'rb'))
    for n, l in enumerate(h['log']['entries']):
#         with open('annie_files.txt', 'a+') as f:
        if 'https://rmwhosannie.mediashuttle.com/REST/v4.0/portal/' in l['request']['url']:
            print(n)
            try:
                for file in json.loads(l['response']['content']['text'])['teamspaceFiles']:
                    print(file['fullPath'], file['size'])
                    if not file['isDirectory']:
                        har_dict[dir_][file['fullPath']] = file['size']
#                         f.write(file['fullPath'] + ' || ' + str(file['size']) +'\n')
            except KeyError:
                continue