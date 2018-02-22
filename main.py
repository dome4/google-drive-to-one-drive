from __future__ import print_function
import httplib2
import os
import auth

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

def main():
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """
    credentials = auth.get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    request(service)
    
            
def request(service):
    """
    request 10 files
    """
    results = service.files().list(
        pageSize=100, fields="nextPageToken, files(id, name, parents, owners)").execute()
    items = results.get('files', [])
    
    
    """
    print results
    """
    if not items:
        print('No files found.')
    else:
        
        print('Files:')
        for item in items:
            print('{0} ({1}) ({2})'.format(item['name'], item['id'], item['parents']))

if __name__ == '__main__':
    main()
