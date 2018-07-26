class Tree(object):
    def __init__(self,root,children = None,parent = None):
        self.data = root
        self.parent = None
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)

    def add_child(self,child):
        self.children.append(child)

    def __delete__(self):
        del self

def print_tree(tree,level):
    if tree.data is not None:
        print("\t"*level + str(tree.data))
    if level != 1:
        for child in tree.children:
            if child is not None:
                print_tree(child,level-1)
