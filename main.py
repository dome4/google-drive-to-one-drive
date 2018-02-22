from __future__ import print_function
import httplib2
import os
import auth
import io, json

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

    iteration = 0
    nextPageToken = None
    while nextPageToken != None or (iteration == 0 and nextPageToken == None):
        print ('iteration: ' + str(iteration))
        nextPageToken = request(service, nextPageToken)
        iteration = iteration + 1
        
        """
        ToDo remove break mark
        """
        if iteration == 10:
            break
        """
        """
    
            
def request(service, nextPageToken):
    """
    request 10 files
    """
    results = service.files().list(
        pageSize=10, 
        pageToken = nextPageToken,
        fields="nextPageToken, files(id, name, parents, owners)").execute()
    items = results.get('files', [])
    
    
    """
    print results
    """
    if not items:
        print('No files found.')
    else:
        
        print('Files:')
        #for item in items:
         #   print('{0} ({1}) ({2})'.format(item['name'], item['id'], item['parents']))
        
        """
        save response in file
        """
        filename = 'data.txt'
        # remove file before setting new content
        """
        try:
            os.remove(filename)
        except OSError: 
            print ('something went wrong')
        """
        
        with io.open(filename, 'w', encoding='utf-8') as f:
            f.write(json.dumps(items, ensure_ascii=False))
            # f.write(unicode('{"separator":"-------------------------------------------------"}'))
            f.close()
            
        return results['nextPageToken']

if __name__ == '__main__':
    main()
