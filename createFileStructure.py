import os
from anytree import PreOrderIter

"""
create folder strucutre and download files
"""
def createStructure(nodeList):
    
    print ('starting to create the file structure')
    
    """
    iterate through tree
    """
    for node in PreOrderIter(nodeList[0]):
        node.name
        """
        create folder if it is a folder
        """
        if node.fileType == 'application/vnd.google-apps.folder':
            path = getFilePath(node)

            print ('-------------')
            print (path)
            print ('-------------')

            
        
 
    
    print ('file structure finished')

"""
get the whole path of the current file
"""
def getFilePath(file):
    path = file.name
    currentFile = None

    if file.parent:
        """
        check if current file has a parent file
        """
        currentFile = file.parent

        while True:
            """
            concatinate path
            """
            path = currentFile.name + '/' + path     

            """
            break loop if root node is reached
            """
            if not currentFile.parent and currentFile.name == 'root':

                """
                return path if root-node is reached
                """
                return path

            else:
                """
                get next parent if it exists
                """
                currentFile = currentFile.parent
    else:
        """
        only the root file has no parents
        """
        return path

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)
        

# Example
# createFolder('./data/')
# Creates a folder in the current directory called data

def downloadFile(service, fileID, fileName, mimeType, targetPath):
    
    """
    Download Google Files
    """
    if 'application/vnd.google-apps' in mimeType:
            if 'form' in mimeType:
                print('Google Form - cannot be downloaded. Skiping...' + str(fileID))
                
            elif 'document' in mimeType:
                request = service.files().export_media(fileId=fileID, mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                fileName = fileName + '.docx'
                
            elif 'spreadsheet' in mimeType:
                request = service.files().export_media(fileId=fileID, mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                fileName = fileName + '.xlsx' 
                   
            elif 'presentation' in mimeType:
                request = service.files().export_media(fileId=fileID, mimeType='application/vnd.openxmlformats-officedocument.presentationml.presentation')
                fileName = fileName + '.pptx'
            else:
                print ('unhandeld google format: ' + str(mimeType))
                  
    else: 
        """
        build download requests for other files
        """ 
        request = service.files().get_media(fileId=fileID)
      
    """
    download files
    """                  
    print("Downloading -- {}".format(fileName))
    response = request.execute()
    
    """
    file path
    """
    filePath = os.path.join('./pg-data/', targetPath)
    
    """
    check if necessary folder already exists
    """
    createFolder(filePath)
    
    """
    save response in file
    """
    with open(os.path.join(filePath, fileName), "wb") as writeStream:
        writeStream.write(response)
