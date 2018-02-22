from anytree import NodeMixin, RenderTree, ContStyle


"""
"""
def createTree():


    """
    Die Reihenfolge spielt eine wichtige Rolle !!!
    """
    node7 = NodeClass('Ordner1', 12345)
    node6 = NodeClass('Ordner2', 12345, parent = node7)
    node5 = NodeClass('Ordner3', 12345, parent = node7)
    
    node0 = NodeClass('Dok1', 12345, parent = node7)
    node1 = NodeClass('Dok2', 12345, parent = node6)
    node2 = NodeClass('Dok3', 12345, parent = node5)
    node3 = NodeClass('Dok4', 12345, parent = node5)
    node4 = NodeClass('Dok5', 12345)
    
    
    """
    Beispiel-Baum aufbauen
    """
    
    """
    render tree
    """
    for pre, _, node in RenderTree(node7): #root component
        print("%s%s" % (pre, node.name))
    

"""
class of the tree nodes 
"""
class NodeClass(NodeMixin):
    def __init__(self, name, id, fileType, parent=None):
        super(NodeClass, self).__init__()
        self.name = name
        self.id = id
        self.fileType = fileType
        self.parent = parent
        
if __name__ == '__main__':
    createTree()