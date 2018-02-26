from anytree import NodeMixin, RenderTree, ContStyle, PreOrderIter
import json
import io

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
    filename = 'data.txt'
    
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
    render tree
    """
    for pre, _, node in RenderTree(nodeList[0]): #root component
        print("%s%s" % (pre, node.name))
        
    print ('------------------------------------------------------------')
        
    """
    render nodeList
    """
    for node in nodeList:
        print("name: %s | type: %s | id: %s | parent: %s" % (node.name, node.fileType, node.id, node.parent))
    
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
                
            else:
                """
                a parent node does not exist know
                """
                oneMoreIteration = True            
     
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
        
if __name__ == '__main__':
    createTree()
    