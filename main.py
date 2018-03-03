import httplib2
from apiclient import discovery

import auth
import tree
import downloadMetadata
import createFileStructure
import config

"""
main method of the script
"""
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
    if config.DOWNLOAD_METADATA:
        downloadMetadata.downloadFileList(service)

    """
    create tree
    """
    nodeList = None
    if config.CREATE_TREE:
        nodeList = tree.createTree()

    """
    download files
    """
    if config.CREATE_STRUCTURE:
        createFileStructure.createStructure(nodeList, service)

    print ('')
    print ('script finished')
    
"""
run main-method
"""
if __name__ == '__main__':
    main()