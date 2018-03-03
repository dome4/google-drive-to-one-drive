from __future__ import print_function
import httplib2
import os
import auth
import io, json
import tree

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

"""
download file list from google drive and save in file
"""
def downloadFileList(service):

    """
    save response in file
    """
    filename = 'data.txt'

    # remove file before setting new content
    try:
        os.remove(filename)
    except OSError: 
        print ('something went wrong')
    
    # open stream to file
    file = io.open(filename, 'w', encoding='utf-8')
            
    """
    loop through result pages and save them in the file
    """
    iteration = 0
    nextPageToken = None
    allFiles = []
    while nextPageToken != None or (iteration == 0 and nextPageToken == None):
        print ('iteration: ' + str(iteration))
        
        # send request
        result = request(service, nextPageToken)
        
        # set nextPageToken
        nextPageToken = result.get('nextPageToken')
        
        # set result content
        content = result.get('files', [])
        
        # write content in file
        if not content:
            print('No files found.')
        else:
            allFiles = allFiles + content
            # allFiles = allFiles + content + [{"separator":"page finished"}] 
        
        
        # increment iteration flag
        iteration = iteration + 1
  
    """
    write result in file
    """   
    file.write(json.dumps(allFiles, ensure_ascii=False))
    
    """
    close file strem
    """
    file.close()
  
"""
request files
"""          
def request(service, nextPageToken):

    results = service.files().list(
        pageSize=300, 
        pageToken = nextPageToken,
        fields="nextPageToken, files(id, name, parents, owners, mimeType)").execute()
    
    return results