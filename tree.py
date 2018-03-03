from anytree import NodeMixin, RenderTree, ContStyle, PreOrderIter
import json
import io, os
import createFileStructure
from createFileStructure import createStructure
import config

"""
gloabl node list
"""
nodeList = []

"""
list of files with more than a parent
"""
multipleParents = []


def loadJSON():
    
    # ToDo als Parameter uebergeben
    filename = os.path.join(config.DOWNLOAD_FOLDER, config.METADATA_FILE)
    
    """
    add root node to list
    """
    nodeList.append(NodeClass(name = 'root',
                              id = None, fileType = None,
                              parentsCreated = True,
                              parentCandidate = None,
                              parent = None))
    
    """
    open data file
    """
    with io.open(filename, mode = 'r',encoding='utf-8') as data_file:    
        data = json.load(data_file)
        
        """
        create a NodeClass-object for each file
        """
        for jsonFile in data:
            
            """
            request parent id and check if file already exists in array
            """
            parentID = handleParents(jsonFile) 
            parentNode = searchNode(parentID)
            
            
            if parentNode:
                """
                file has parent and node already exists
                """
                nodeList.append(NodeClass(name = jsonFile['name'], 
                                      id = jsonFile['id'],
                                      fileType = jsonFile['mimeType'],
                                      parentsCreated = True,
                                      parentCandidate = None,
                                      parent = parentNode))
                   
            elif parentID and not parentNode:
                """
                file has parents but their nodes do not exist know
                """ 
                nodeList.append(NodeClass(name = jsonFile['name'], 
                                      id = jsonFile['id'],
                                      fileType = jsonFile['mimeType'],
                                      parentsCreated = False,
                                      parentCandidate = parentID,
                                      parent = nodeList[0]))
                
            else:
                """
                file has no parents
                """
                nodeList.append(NodeClass(name = jsonFile['name'], 
                                      id = jsonFile['id'],
                                      fileType = jsonFile['mimeType'],
                                      parentsCreated = True,
                                      parentCandidate = None,
                                      parent = nodeList[0]))
                
    """
    DEBUG print array
    """
    #for node in nodeList:
    #    print("%s (%s)" % (node.name, node.id))

"""
"""
def createTree():
     
    
    """
    load data of file
    """
    loadJSON()
    
    """
    check all nodes with parentsCreated = False and set their parents
    """
    handleMissingParents()
    
    """
    save tree in a file
    """
    resultsFile = os.path.join(config.DOWNLOAD_FOLDER, config.TREE_FILE)
    
    # remove file before setting new content
    try:
        os.remove(resultsFile)
    except OSError: 
        print ('something went wrong')
    
    # open stream to file
    file = io.open(resultsFile, 'w', encoding='utf-8')
    
    # write result in file
    for pre, _, node in RenderTree(nodeList[0]): #root component 
        file.write("%s%s\n" % (pre, node.name))
    
    # close file strem
    file.close()
    
    """
    render tree
    """
    print ('')
    for pre, _, node in RenderTree(nodeList[0]): #root component
        print("%s%s" % (pre, node.name))
        
    """
    render nodeList -> only for debugging
    """
    # for node in nodeList:
    #     print("name: %s | type: %s | id: %s | parent: %s" % (node.name, node.fileType, node.id, node.parent))
        
    """
    return the tree
    """
    return nodeList
    
"""
search in current node list if the file with the given id already exists
returns the matching file or none
"""
def searchNode(searchId):
    for file in nodeList:
        if file.id == searchId:
            return file
    
    return None
    

"""
method handles the parents of a file
it returns only the first parent id, everything else gets safed in multipleParents-variable
"""
def handleParents(jsonFile):
    
    """
    catch key error if file has no parents
    """
    try:
        """
        return parent if file has only one
        """
        if len(jsonFile['parents']) == 1:
            return jsonFile['parents'][0]
        else:
            """
            return first parent and save file to multipleParents-variable if file has more than one parent
            """
            multipleParents.append(jsonFile)
            return jsonFile['parents'][0] 
        
    except KeyError:
        """
        return None if file has no parents
        """
        return None
    
"""
iterate through tree and check nodes if their parents already exist
as long as every node has its parents set
"""  
def handleMissingParents():
    
    """
    flag which determines if one more loop is necessary
    """
    oneMoreIteration = True
    
    """
    files with parentsCreated False
    """
    needyNodes = []
    
    """
    only get necessary files
    """
    for file in nodeList:
        
        if file.parentsCreated == False:
            needyNodes.append(file)
                
    """
    only iterate through necessary files
    """  
    while oneMoreIteration: 
        
        """
        set flag to False
        """
        oneMoreIteration = False
        
        """
        flag for comparing the last two loop results
        """
        nothingChangedInLastLoop = True
        
        for file in needyNodes:
            """
            request parent id and check if file already exists in array
            """
            parentNode = searchNode(file.parentCandidate)
            
            
            if parentNode:
                """
                file has parent and node already exists
                """
                file.parent = parentNode
                file.parentsCreated = True
                file.parentCandidate = None
                
                """
                remove file if its parents are set
                """
                needyNodes.remove(file)
                
                """
                set flag to false if something changed
                """
                nothingChangedInLastLoop = False
                
            else:
                """
                a parent node does not exist know
                """
                oneMoreIteration = True            
     
        """
        break while-loop if nothing changed in the last two loops
        """
        if nothingChangedInLastLoop:
            break
"""
class of the tree nodes 
"""
class NodeClass(NodeMixin):
    def __init__(self, name, id=None, fileType=None, parentsCreated = False, parentCandidate = None, parent=None):
        super(NodeClass, self).__init__()
        self.name = name
        self.id = id
        self.fileType = fileType
        self.parentsCreated = parentsCreated
        """
        parentCandidate is set when a parent node not exists
        """
        self.parentCandidate = parentCandidate
        self.parent = parent    