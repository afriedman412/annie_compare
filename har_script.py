import sys
import json
import os

def createHarDict(verbose=False):
    har_dict = {}
    root = './har_files/'
    for har in os.listdir(root):
        dir_ = har.split('_')[1]
        if dir_ not in har_dict:
            har_dict[dir_] = {}
            
        h = json.load(open(root + har, 'rb'))
        for n, l in enumerate(h['log']['entries']):
            if 'https://rmwhosannie.mediashuttle.com/REST/v4.0/portal/' in l['request']['url']:
                if verbose:
                    print(n)
                try:
                    for file in json.loads(l['response']['content']['text'])['teamspaceFiles']:
                        if verbose:
                            print(file['fullPath'], file['size'])
                        if not file['isDirectory']:
                            har_dict[dir_][file['fullPath']] = file['size']
                except KeyError:
                    continue

    return har_dict



if __name__ == "__main__":

    drive_dict = {
    '2018': "WHO'S ANNIE PILOT_BACKUP/WHO'S ANNIE-PILOT/SHOOT 2",
    '2019': 'WHOS ANNIE_PILOT_08-2019/SHOOT 3',
    '2020': 'WA0920 main/WHOS ANNIE PILOT/2020'
}

    har_dict = createHarDict()

    print('********* NEW RUN **********')
    for k_ in drive_dict:
        print(k_)
        for k,v in har_dict[k_].items():
            path_ = "/volumes" + k.replace(k_, drive_dict[k_])
            # print(path_)
            try:
                local_size = os.stat(path_).st_size
                # if local_size != v:
                print('local:')
                print(path_, local_size)
                print('remote:')
                print(k, v)

            except FileNotFoundError:
                print('file not found: {}'.format(path_))
            print('--')

