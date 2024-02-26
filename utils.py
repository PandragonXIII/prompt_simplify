class TreeNode:
    def __init__(self, val):
        self.val = val #list like [NP] or [NN, cake]
        self.children = []

    def to_string(self):
        if len(self.val) == 2:
            return self.val[1]+' '
        else:
            result = ''
            for child in self.children:
                result += child.to_string()
            return result

def string_to_tree(s):
    root = TreeNode('')
    stack = [root]
    i = 0
    while i < len(s):
        if s[i] == '(':
            i += 1
            val = ''
            while i < len(s) and s[i] != '(' and s[i] != ')':
                val += s[i]
                i += 1
            node = TreeNode(val.strip().split())
            stack[-1].children.append(node)
            stack.append(node)
        elif s[i] == ')':
            stack.pop()
            i += 1
        else:
            while i < len(s) and s[i] != '(' and s[i] != ')':
                i += 1
    return root.children[0]