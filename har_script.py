import sys
import json
import os
import pandas as pd

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
    out_list = []

    print('********* NEW RUN **********')
    for k_ in drive_dict:
        print(k_)
        for k,v in har_dict[k_].items():
            path_ = "/volumes" + k.replace(k_, drive_dict[k_])
            if k_ == '2018':
                path_ = path_.replace('RECORDED/', '')
            # print(path_)
            size_match = False
            found = False
            
            try:

                local_size = os.stat(path_).st_size
                if local_size == v:
                    size_match = True
                print('local:')
                print(path_, local_size)
                print('remote:')
                print(k, v)
                found = True

            except FileNotFoundError:
                print('file not found: {}'.format(path_))
                local_size = ''

            listo = {
                'year': k_,
                'file_name': path_.split('/')[-1],
                'local_path': path_,
                'remote_path': k,
                'file_found': found,
                'local_size': local_size,
                'remote_size': v,
                'size_match': size_match
            }

            out_list.append(listo)

            print('--')

    print('outputting csv...')
    pd.DataFrame(out_list).to_csv('sophia_files.csv', index=False)

