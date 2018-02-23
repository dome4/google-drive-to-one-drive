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
    nodeList.append(NodeClass(name = 'root', id = None, fileType = None, parentsCreated = True, parent = None))
    
    """
    open data file
    """
    with io.open(filename, mode = 'r',encoding='utf-8') as data_file:    
        data = json.load(data_file)
        
        """
        create a NodeClass-object for each file
        """
        for file in data:
            
            """
            request parent id and check if file already exists in array
            """
            parentID = handleParents(file) 
            parentNode = searchNode(parentID)
            
            
            if parentNode:
                """
                file has parent and node already exists
                """
                nodeList.append(NodeClass(name = file['name'], 
                                      id = file['id'],
                                      fileType = ['mimeType'],
                                      parentsCreated = True,
                                      parent = parentNode))
                   
            elif parentID and not parentNode:
                """
                file has parents but their nodes do not exist know
                """ 
                nodeList.append(NodeClass(name = file['name'], 
                                      id = file['id'],
                                      fileType = ['mimeType'],
                                      parentsCreated = False,
                                      parent = None))
                
            else:
                """
                file has no parents
                """
                nodeList.append(NodeClass(name = file['name'], 
                                      id = file['id'],
                                      fileType = ['mimeType'],
                                      parentsCreated = True,
                                      parent = None))
                
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
def handleParents(file):
    
    """
    catch key error if file has no parents
    """
    try:
        
        # debug
        print(len(file['parents']))
        
        """
        return parent if file has only one
        """
        if len(file['parents']) == 1:
            return file['parents'][0]
        else:
            """
            return first parent and save file to multipleParents-variable if file has more than one parent
            """
            multipleParents.append(file)
            return file['parents'][0] 
        
    except KeyError:
        """
        return None if file has no parents
        """
        return None
    
"""
iterate through tree and check nodes if their partens already exist
as long as every node has its partens set
"""  
def handleMissingParents():
    
    oneMoreIteration = False
    
    for file in nodeList:
        if file.parentsCreated == False:
            """
            request parent id and check if file already exists in array
            """
            parentID = handleParents(file) 
            parentNode = searchNode(parentID)
            
            
            if parentNode:
                """
                file has parent and node already exists
                """
                file.parent = parentNode
                file.parentsCreated = True
                
            else:
                """
                a parent node does not exist know
                """
                oneMoreIteration = True
            
         
    """
    if a parent node is missing iterate once more over the tree
    """   
    if oneMoreIteration:
        handleMissingParents()

     
"""
class of the tree nodes 
"""
class NodeClass(NodeMixin):
    def __init__(self, name, id=None, fileType=None, parentsCreated = False, parent=None):
        super(NodeClass, self).__init__()
        self.name = name
        self.id = id
        self.fileType = fileType
        self.parentsCreated = parentsCreated
        self.parent = parent
        
if __name__ == '__main__':
    createTree()