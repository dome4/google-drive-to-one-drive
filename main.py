from __future__ import print_function
import httplib2
import os
import auth
import io, json
import tree
import downloadMetadata

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

def main():

    print ('script started')

    """
    google api code
    """
    credentials = auth.get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    
    """
    download file list
    """
    downloadMetadata.downloadFileList(service)

    """
    create tree
    """
    tree.createTree(service)

    print ('')
    print ('script finished')
    
"""
run main-method
"""
if __name__ == '__main__':
    main()