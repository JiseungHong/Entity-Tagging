import pickle
import trie
from trie import TrieNode

# TODO update tag dictionary.
tag_dictionary = {'PER': 50, 'Sun': 5, 'ORG': 20, 'PRO': 25}
with open("tagged_data.pickle", "rb") as f:
    tagged_data = pickle.load(f)
with open("prefix_root.pickle", "rb") as f:
    prefix_root = pickle.load(f)
with open("suffix_root.pickle", "rb") as f:
    suffix_root = pickle.load(f)

def spread(root, score: int, tag: list):
    """Inherit the current node's score & tag to its descendants.

    Args:
        root (TrieNode): Anscestor which GIVES the score & tag.
        score (int): Score.
        tag (list): Tag.
    """
    node = root
    if node.children is not None:
        for child in node.children:
            if child.word_finished:
                assert child.key is not None
                if score > tagged_data[child.key][0]:
                    tagged_data[child.key] = [score, tag]
            spread(child, score, tag)


def _match(root, prefix: str):
    node = root
    if not root.children:
        return None
    
    for char in prefix:
        char_not_found = True
        for child in node.children:
            if child.char == char:
                char_not_found = False
                node = child
                break
        if char_not_found:
            return None
    return node

def match(front_root, back_root, entity: str, tag: list):
    """Template Method Design Pattern

    Args:
        root (TrieNode): The root of the TrieNode in which comparison starts.
        entity (str): Named entity; String composed with portions splitted by whitespace.
        tag (list): Tag of the named entity.

    Returns:
        Boolean: We don't use the return value.
    """
    front_node = front_root
    back_node = back_root
    res = False
    representative = tag[0]
    if entity == '':
        return False
    portions = entity.split(' ')
    reverse_portions = entity[::-1].split(' ')
    
    for count, node in enumerate([front_node, back_node]):
        weight = -1
        if count == 0:
            weight = 1.0
        else:
            weight = 1.5
            portions = reverse_portions
            
        for portion in portions:
            node = _match(node, portion)
            if node:
                if node.word_finished:
                    assert node.key is not None
                    try:
                        new_score = tag_dictionary[representative] * node.length * weight
                        old_score = tagged_data[node.key][0]
                    except KeyError:
                        print("Key Error", node.key, tag)
                    
                    if new_score > old_score:
                        tagged_data[node.key] = [new_score, tag]
                    spread(node, score=new_score, tag=tag)
                else:
                    spread(node, tag_dictionary[representative] * node.length * weight, tag)
                res = True
            else:
                break
        if count==0:
            front_node = node
        else:
            back_node = node
    if front_node and back_node and front_node.word_finished and \
                back_node.word_finished and front_node.key == back_node.key:
        tagged_data[front_node.key][0] += 1000
    return res

if __name__ == "__main__":
    with open("entity.txt", "r", encoding='utf-8') as f:
            while True:
                entity = f.readline().strip().split('.')
                if len(entity) < 2:
                    break
                match(prefix_root, suffix_root, entity[0], [entity[1], entity[2], entity[3]])
    
    print(tagged_data)