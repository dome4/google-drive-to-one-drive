import httplib2
from apiclient import discovery

import auth
import tree
import downloadMetadata
import createFileStructure

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
    downloadMetadata.downloadFileList(service)

    """
    create tree
    """
    nodeList = tree.createTree()

    """
    download files
    """
    createFileStructure.createStructure(nodeList, service)

    print ('')
    print ('script finished')
    
"""
run main-method
"""
if __name__ == '__main__':
    main()