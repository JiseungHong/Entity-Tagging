from typing import Tuple
import pickle

tag_dictionary = {'PER': 50, 'Sun': 5, 'ORG': 20, 'PRO': 25}
tagged_data = dict({})

class TrieNode(object):
    """Trie Object for Noun Phrase Tagging with Named Entity Dictionary.

    Args:
        object (-): -
    """
    
    def __init__(self, char: str, length: int):
        """Initialization of TRIENODE.

        Args:
            char (str): The charactor which each node will be received.
            length (int): The length of the word(from root to current node).
        """
        
        self.char = char
        self.children = []
        self.word_finished = False
        self.length = length
        self.key = None
    
    def accept(self, visitor):
        self._accept(visitor, '')
    
    def _accept(self, visitor, prefix: str):
        if self.children is not None:
            for child in self.children:
                if child.word_finished:
                    print(prefix + child.char + ": ", tagged_data[child.key])
            for child in self.children:
                child._accept(visitor, prefix + child.char)
    
class Visitor(object):
    """Visitor Design Pattern
    Just for debugging.

    Args:
        object ([type]): [description]
    """
    
    def __init__(self):
        self.errors = 0
    
    def visit(self, node: TrieNode):
        return node.accept(self)
    
    def error(self, str):
        """Output a fatal compilation error."""
        
        print("error: %s" % str)
        self.errors += 1
            
def add_front(root, word: str):
    """
    Adding a word in the trie structure
    """
    node = root
    phrase = word
    for count, char in enumerate(phrase):
        found_in_child = False
        for child in node.children:
            if child.char == char:
                node = child
                found_in_child = True
                break
        if not found_in_child:
            new_node = TrieNode(char, count+1)
            node.children.append(new_node)
            node = new_node
    node.word_finished = True
    node.key = word
    tagged_data[word] = [0, ['No tag matched.', '-', '-']]
    
def add_back(root, word: str):
    """
    Adding a word in the trie structure
    """
    node = root
    phrase = word
    for count, char in reversed(list(enumerate(phrase))):
        found_in_child = False
        for child in node.children:
            if child.char == char:
                node = child
                found_in_child = True
                break
        if not found_in_child:
            new_node = TrieNode(char, count+1)
            node.children.append(new_node)
            node = new_node
    node.word_finished = True
    node.key = word

def prefix_length(root, prefix: str):
    node = root
    if not root.children:
        return 0
    for char in prefix:
        char_not_found = True
        for child in node.children:
            if child.char == char:
                char_not_found = False
                node = child
                break
        if char_not_found:
            return 0
    return node.length

if __name__ == "__main__":
    prefix_root = TrieNode('*', 0)
    suffix_root = TrieNode('*', 0)
    visitor = Visitor()
    
    with open("phrase.txt", "r", encoding='utf-8') as f:
        while True:
            phrase = f.readline().strip()
            if phrase=='':
                break
            add_front(prefix_root, phrase)
            add_back(suffix_root, phrase)
        
        # visitor.visit(prefix_root)
        # visitor.visit(suffix_root)
        
    with open("tagged_data.pickle", "wb") as f:
        pickle.dump(tagged_data, f)
    
    with open("prefix_root.pickle", "wb") as f:
        pickle.dump(prefix_root, f)
    
    with open("suffix_root.pickle", "wb") as f:
        pickle.dump(suffix_root, f)