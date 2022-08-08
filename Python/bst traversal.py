class Node:
    def __init__(self, data, left = None, right = None):
        self.data = data
        self.left = left
        self.right = right
        
        
def insert(value, root):
    if value < root.data:
        if root.left != None:
            insert(value, root.left)
        else:
            root.left = Node(value)
            
    elif value > root.data:
        if root.right != None:
            insert(value, root.right)
        else:
            root.right = Node(value)     
 
def inorder(root):
    if root.left != None:
        inorder(root.left)
        
    print(f"{root.data} ", end="")
    
    if root.right != None:
        inorder(root.right)
    
    return
 
def preorder(root):
    print(f"{root.data} ", end="")
    
    if root.left != None:
        preorder(root.left)
        
    if root.right != None:
        preorder(root.right)
    return

def postorder(root):
    
    if root.left != None:
        postorder(root.left)
        
    if root.right != None:
        postorder(root.right)
        
    print(f"{root.data} ", end="")
    return  

        
def main():
    root = input("Enter Tree root: ")
    if not root.isnumeric():
        raise TypeError("Only numbers are allowed as root")
    tree = Node(root)
    del root
    
    print("Keep entering numbers to add to the BST. Enter a string to print Inorder, Preorder, Postorder of the tree.")
    while True:
        value = input()
        if value.isnumeric():
            insert(value, tree)
        else:
            break
    
    print("Inorder: ", end="")    
    inorder(tree)
    print("\nPreorder: ", end="")
    preorder(tree)
    print("\nPostorder: ", end="")
    postorder(tree)
    
if __name__ == '__main__':
    main()