class _Node:
    def __init__(self, contact):
        self.contact = contact
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None
    
    def add(self, contact):
        if self.root is None:
            self.root = _Node(contact)
        else:
            self._add_recursive(self.root, contact)
    
    def _add_recursive(self, node, contact):
        if contact.key() < node.contact.key():
            if node.left is None:
                node.left = _Node(contact)
            else:
                self._add_recursive(node.left, contact)
        elif contact.key() > node.contact.key():
            if node.right is None:
                node.right = _Node(contact)
            else:
                self._add_recursive(node.right, contact)
        else:
            node.contact = contact
    
    def find(self, last, first):
        key = (last.strip().lower(), first.strip().lower())
        return self._find_recursive(self.root, key)
    
    def _find_recursive(self, node, key):
        if node is None:
            return None
        if key < node.contact.key():
            return self._find_recursive(node.left, key)
        elif key > node.contact.key():
            return self._find_recursive(node.right, key)
        else:
            return node.contact
    
    def delete(self, last, first):
        key = (last.strip().lower(), first.strip().lower())
        self.root, removed = self._delete_recursive(self.root, key)
        return removed
    
    def _delete_recursive(self, node, key):
        if node is None:
            return None, False
        
        if key < node.contact.key():
            node.left, removed = self._delete_recursive(node.left, key)
            return node, removed
        elif key > node.contact.key():
            node.right, removed = self._delete_recursive(node.right, key)
            return node, removed
        else:
            if node.left is None:
                return node.right, True
            elif node.right is None:
                return node.left, True
            else:
                successor = self._find_min(node.right)
                node.contact = successor.contact
                node.right, _ = self._delete_recursive(node.right, successor.contact.key())
                return node, True
    
    def _find_min(self, node):
        while node.left is not None:
            node = node.left
        return node
    
    def edit(self, last, first, new_contact):
        key = (last.strip().lower(), first.strip().lower())
        found = [False]
        
        def edit_recursive(node):
            if node is None:
                return None
            if key < node.contact.key():
                node.left = edit_recursive(node.left)
            elif key > node.contact.key():
                node.right = edit_recursive(node.right)
            else:
                node.contact = new_contact
                found[0] = True
            return node
        
        self.root = edit_recursive(self.root)
        return found[0]
    
    def traverse_in_order(self):
        result = []
        self._traverse_recursive(self.root, result)
        return result
    
    def _traverse_recursive(self, node, result):
        if node is None:
            return
        self._traverse_recursive(node.left, result)
        result.append(node.contact)
        self._traverse_recursive(node.right, result)
