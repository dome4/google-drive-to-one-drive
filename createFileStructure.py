import os
from anytree import PreOrderIter
import config

"""
create folder strucutre and download files
"""
def createStructure(nodeList, googleDriveService):

    print ('')
    print ('starting to create the file structure')
    print ('')
    
    """
    iterate through tree
    """
    for node in PreOrderIter(nodeList[0]):

        """
        go to next loop if node is root node
        """
        if node.name == 'root' and not node.parent:
            continue

        """
        create folder if it is a folder
        """
        if node.fileType == 'application/vnd.google-apps.folder':

            """
            get current folder path
            """ 
            path = getFilePath(node)

            """
            check if folder exists and create if not
            """
            createFolder(path)

        else:
            """
            else download file
            """
            path = getParentFolderPath(node)

            """
            check if folder exists and create if not
            """
            if path != '':
                createFolder(path)   

            """
            download file to target path
            """
            downloadFile(service = googleDriveService,
                        fileID = node.id,
                        fileName = node.name,
                        mimeType = node.fileType,
                        targetPath = path)
 
    print ('')
    print ('file structure finished')

"""
get the path of parent folder
"""
def getParentFolderPath(file):

    """
    folder path resulst
    """
    folderPath = ''
    
    """
    get file path
    """
    filePath = getFilePath(file)

    """
    remove file name at the end
    """

    # get length of file name
    fileNameLength = len(file.name)

    # cut off file name at then end
    folderPath = filePath[:-(fileNameLength)]

    """
    return folder path
    """
    return folderPath

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
            if not currentFile.name == 'root' and currentFile.parent:
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

def createFolder(directoryPath):

    """
    get root folder from the config file
    """
    rootPath = os.path.join(config.DOWNLOAD_FOLDER, 'data')

    """
    create folders in root-folder data
    """
    filePath = os.path.join(rootPath, directoryPath)

    try:
        """
        create folder if it does not exist yet
        """
        if not os.path.exists(filePath):
            os.makedirs(filePath)
    except OSError:
        print ('Error: Creating directory: ' +  filePath)

    return filePath
        

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
    check if necessary folder already exists
    """
    filePath = createFolder(targetPath)
    
    """
    save response in file
    """
    with open(os.path.join(filePath, fileName), "wb") as writeStream:
        writeStream.write(response)
