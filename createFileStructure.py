import os

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
                print ('unhandeld format: ' + str(mimeType))
                  
    else: 
        """
        Download other files
        """ 
        request = service.files().drive_service.files().get_media(fileId=fileID)
      
    
                           
    print("Downloading -- {}".format(fileName))
    
    response = request.execute()
    
    with open(os.path.join(targetPath, fileName), "wb") as writeStream:
        writeStream.write(response)
