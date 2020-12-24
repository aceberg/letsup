import json
import requests
import sys
import os
import time

keys = {
    'key1' : 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    'key2' : 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
}

apiurl = 'https://letsupload.io/api/v2/'
authfile = '/tmp/letsupload.auth'
idfile = '/tmp/letsupload.id'
upload_file = ''
parent_folder = ''
upload_folder = ''
auth_data = {
    'account_id': '',
    'access_token': '',
    'folder_id': '',
    'parent_folder_id': ''
}

def auth():
    response = requests.post(apiurl+'authorize',data=keys)
    print(response.json()['data'])
    f = open(authfile, 'w')
    f.write(response.json()['data']['access_token'])
    f.close()
    f = open(idfile, 'w')
    f.write(response.json()['data']['account_id'])
    f.close()


def get_token():
    if os.path.isfile(authfile):
        last_mod = time.time() - os.path.getmtime(authfile)
        print('Last modified (seconds): %s' % last_mod)
        if last_mod > 3000: auth() # if 50 minutes passed
    else: auth()
    f = open(authfile, 'r')
    auth_data['access_token'] = f.read()
    f.close()
    f = open(idfile, 'r')
    auth_data['account_id'] = f.read()
    f.close()


def folder_list(parent_folder):
    get_token()
    auth_data['parent_folder_id'] = parent_folder
    response = requests.post(apiurl+'folder/listing',data=auth_data)
    folders = response.json()['data']['folders']
    files = response.json()['data']['files']
    print('Folders:')
    for i in range(len(folders)):
        print(folders[i]['folderName']+': '+folders[i]['id'])
    print('')
    print('Files:')
    for i in range(len(files)):
        print(files[i]['filename']+': '+files[i]['id'])


def file_upload(upload_file,upload_folder):
    get_token()
    auth_data['folder_id'] = upload_folder
    files = {'upload_file': open(upload_file,'rb')}
    response = requests.post(apiurl+'file/upload', files=files, data=auth_data)
    print(response.json()['_status'])


def usage():
    print('Usage: letsup.py auth | list [FOLDER_ID] | upload FILE [FOLDER_ID]')


def main():
    if len(sys.argv) == 2:
        if sys.argv[1] == 'auth': auth()
        elif sys.argv[1] == 'list': folder_list(parent_folder)
        else: usage()
    elif len(sys.argv) == 3:
        if sys.argv[1] == 'list': folder_list(sys.argv[2])
        elif sys.argv[1] == 'upload': file_upload(sys.argv[2],upload_folder)
        else: usage()
    elif len(sys.argv) == 4:
        if sys.argv[1] == 'upload': file_upload(sys.argv[2],sys.argv[3])
        else: usage()
    else: usage()


if __name__ == "__main__":
    main()
