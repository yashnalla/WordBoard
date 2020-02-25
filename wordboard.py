#subproblems
    # graph
        # graoh rep in python:
            # adjacency matrix 
            # adjacency list <- much better for mem
        #dfs to travel through adjacency list
        #   
    # validity
        #load english words into trie(choose because of context in string retreival); 
            # not all english words only possible words that can be started with unique board letters. and then next lvl will have also valid letters.... set intersection
            # prefix searching, aaa is not the start to any english word so toss the path, etc. 
            


from nltk.corpus import words

found_words = []

initial_board = [['r', 'a', 'e', 'l'],
                ['m', 'o', 'f', 's'],
                ['t', 'e', 'o', 'k'],
                ['n', 'a', 't', 'i']]
num_rows = len(initial_board)
num_cols = len(initial_board[0])

full_words = []

possible_characters = []
secondary_board = {}

#create a set of possible characters to refine trie making
for row in initial_board:
    for char in row:
        possible_characters.append(char)

possible_characters = set(possible_characters)

#create graph

def create_secondary_board():
    for row in range(len(initial_board)):
        for column in range(len(initial_board[0])):
            neighbors = get_neighbors(row, column)
            secondary_board[(row, column)] = neighbors

def get_neighbors(row, column):
    neighbors = []
    for i in range(row-1, row + 2):
        for j in range(column - 1, column + 2):
            if i > -1 and i < num_rows and j > -1 and j < num_cols and (i != row or j != column):
                neighbors.append((i, j))
    return neighbors

def dfs(visited, secondary_board, key, trie_node, current_word):
    key2 = initial_board[key[0]][key[1]]
    if key not in visited:
        visited.append(key)
        for neighbor in secondary_board[key]:
            neighbor2 = initial_board[neighbor[0]][neighbor[1]]
            if neighbor not in visited:
                new_node = valid_prefix(trie_node, neighbor2)
                if new_node:
                    current_word += new_node.char
                    if new_node.word_complete:
                        if current_word not in found_words:
                            found_words.append(current_word)
                        if len(new_node.children) > 0:
                            dfs(visited, secondary_board, neighbor, new_node, current_word)
                            current_word = current_word[:-1]
                            visited.remove(neighbor)
                        else:
                            return
                    else:
                        dfs(visited, secondary_board, neighbor, new_node, current_word)
                        current_word = current_word[:-1]
                        visited.remove(neighbor)


#create trie structure

class TrieNode(object):
    def __init__(self, char:str):
        self.char = char
        self.children = []
        self.word_complete = False
        self.counter = 0

def is_valid_word(word: str):
    word = set(word)
    if word & possible_characters == word:
        return True
    else:
        return False


def add(root, word:str):
    # check to see if word is even possible
    if is_valid_word(word):
        #tracker to find number of valid words
        full_words.append(word)
        root.counter += 1
        node = root
        for char in word:
            found_in_children = False
            #search for character from present node
            for child in node.children:
                if child.char == char:
                    #if found point the node to specific child and continue
                    node = child
                    found_in_children = True
                    break #exits for loop
            if not found_in_children:
                #if not found create new child
                new_node = TrieNode(char)
                node.children.append(new_node)
                node = new_node 
        node.word_complete = True


def valid_prefix(current_node, char:str):
    for child in current_node.children:
        if child.char == char:
            return child

    return False





def main():

    all_words = words.words()
    #all_words = ["cat", "dog", "byte", "tube", "can", "cant"] 
    root_node = TrieNode('*')

    for word in all_words:
        if len(word) >= 3 and len(word) <= 16:
            add(root_node, word)
    
    print(root_node.counter)
    create_secondary_board()
    #for elem in secondary_board:
        #print(elem)
        #print(secondary_board[elem])
    
    visited = []

    for key in secondary_board.keys():
        print(key)
        new_node = valid_prefix(root_node, initial_board[key[0]][key[1]])
        if new_node:
            dfs(visited, secondary_board, key, new_node, initial_board[key[0]][key[1]])
        visited = []
    found_words.sort()
    print(found_words)
    print(len(found_words))

if __name__ == '__main__':
    main()