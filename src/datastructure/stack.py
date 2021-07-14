class Node:
    def __init__(self, data, next_node):
        self.data = data
        self.next_node = next_node
    

class Stack:
    def __init__(self):
        self.top = None
    

    def peek(self):
        return self.top
    

    def push(self, data):
        self.next_node = self.top
        new_node = Node(data, self.next_node)
        self.top = new_node

    
    def pop(self):
        if self.top is None:
            return None
        removed = self.top
        self.top = self.top.next_node
        return removed
