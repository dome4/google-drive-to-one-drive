from anytree import NodeMixin, RenderTree, ContStyle
import json
import io


def loadJSON():
    
    # ToDo als Parameter uebergeben
    filename = 'data.txt'
    
    with io.open(filename, mode = 'r',encoding='utf-8') as data_file:    
        data = json.load(data_file)
        
    
        for file in data:
            print file['mimeType']
            
        
            """
            ToDo fuer jedes File ein neues NodeClass-Object erstellen und in Feld speichern
            """
    


"""
"""
def createTree():
    
    # for debugging
    loadJSON()


    """
    Die Reihenfolge spielt eine wichtige Rolle !!!
    Files koennen mehr als einen Parent haben in Google!
    Beispiel-Baum
    """
    root = NodeClass('root')
    
    node1 = NodeClass(name = 'API Test', id = '1cGR1jyzi6irzPRsl85Daz_MY4GTr9Xs_', fileType = 'application/vnd.google-apps.folder', parent = root)
    node2 = NodeClass(name = 'Folder 1', id = '1lWx0ibKWx7ZEfBlquFvgM28DCcOLDIzJ', fileType = 'application/vnd.google-apps.folder', parent = node1)
    node3 = NodeClass(name = 'Folder 2', id = '1kJtVfm26RzHi7cNKuIhlh5tvtV-Ezjf8', fileType = 'application/vnd.google-apps.folder', parent = node1)    
    node4 = NodeClass(name = 'Folder 1_1', id = '1yycs6WSYGIAB0yZqIJ1vSTzqoBSYNJw-', fileType = 'application/vnd.google-apps.folder', parent = node2)    
    node5 = NodeClass(name = 'Folder 1_2', id = '1pR_TJYMHi15dGSJbzFPNMoDkUcNX3pZ6', fileType = 'application/vnd.google-apps.folder', parent = node2)    
    node6 = NodeClass(name = 'Test', id = '1lWYBhzUWX5wj-OjRKWfW5YCWr6LJWV_IN0tPTgirluc', fileType = 'application/vnd.google-apps.document', parent = node4)
    node7 = NodeClass(name = 'Test 2', id = '11seIce8iS3NvP7Nr8qAa79xmTkDMD9hjmp3yakYG3NY', fileType = 'application/vnd.google-apps.spreadsheet', parent = node5)

    
    """
    render tree
    """
    for pre, _, node in RenderTree(root): #root component
        print("%s%s" % (pre, node.name))
    

"""
class of the tree nodes 
"""
class NodeClass(NodeMixin):
    def __init__(self, name, id=None, fileType=None, parent=None):
        super(NodeClass, self).__init__()
        self.name = name
        self.id = id
        self.fileType = fileType
        self.parent = parent
        
if __name__ == '__main__':
    createTree()