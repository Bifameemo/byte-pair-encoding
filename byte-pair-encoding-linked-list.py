import random
from typing import NamedTuple

class Pair(NamedTuple):
    left: Token
    right: Token

type Token = Pair | str

class Node:
    def __init__(self, token: Token, next: Node | None) -> None:
        self.token: Token = token
        self.next: Node | None = next

    def __str__(self) -> str:
        if self.next == None:
            return format_token(self.token)
        return format_token(self.token) + self.next.__str__()

# converts text to list of tokens
def construct_table(text: str) -> list[Token]:
    # initialise first 256 entries of table with ASCII characters
    table: list[Token] = []
    for i in range(256):
        table.append(chr(i))
    
    # convert text into linked list of tokens
    text_root: Node = Node(text[0], None)
    current_node: Node = text_root
    for char in text[1:]:
        current_node.next = Node(char, None)
        current_node = current_node.next
    
    # count pairs initially
    pair_frequencies: dict[Token, int] = dict()
    current_node = text_root
    while current_node.next:
        pair: Token = Pair(current_node.token, current_node.next.token)
        if pair in pair_frequencies:
            pair_frequencies[pair] += 1
        else:
            pair_frequencies[pair] = 1
        current_node = current_node.next

    # loop until break (when no repeated pairs exist)
    while True:
        # determine most frequent pair
        max_frequency: int = 0
        max_pair: Token = next(iter(pair_frequencies.keys()))
        for pair, frequency in pair_frequencies.items():
            if frequency > max_frequency:
                max_frequency = frequency
                max_pair = pair
        
        # break if no repeated pairs exist
        if max_frequency <= 1:
            break
        
        # add most frequent pair to table
        table.append(max_pair)

        # replace all instances of max_pair in tokenised_text and update pair_frequencies
        # current_node -> current_node.next  -> current_node.next.next -> current_node.next.next.next
        # before       -> first char of pair -> second char of pair    -> after
        current_node = text_root
        while current_node.next and current_node.next.next and current_node.next.next.next:
            pair = Pair(current_node.next.token, current_node.next.next.token)
            if pair == max_pair:
                # decrement frequency of adjacent pairs
                # increment frequency of replacement pairs
                # e.g. if max_pair == "is" then "fish" -> "fXh"
                # frequency of "fi" and "sh" decrements
                # frequency of "fX" and "Xh" increments

                # pair_before
                pair_before: Pair = Pair(current_node.token, current_node.next.token)
                pair_frequencies[pair_before] -= 1
                if pair_frequencies[pair_before] == 0:
                    del pair_frequencies[pair_before]
                
                replacement_pair_before: Pair = Pair(current_node.token, max_pair)
                if replacement_pair_before in pair_frequencies:
                    pair_frequencies[replacement_pair_before] += 1
                else:
                    pair_frequencies[replacement_pair_before] = 1

                # pair_after
                pair_after: Pair = Pair(current_node.next.next.token, current_node.next.next.next.token)
                pair_frequencies[pair_after] -= 1
                if pair_frequencies[pair_after] == 0:
                    del pair_frequencies[pair_after]
                
                replacement_pair_after: Pair = Pair(max_pair, current_node.next.next.next.token)
                if replacement_pair_after in pair_frequencies:
                    pair_frequencies[replacement_pair_after] += 1
                else:
                    pair_frequencies[replacement_pair_after] = 1
                
                # replace pair in tokenised_text
                replacement_node: Node = Node(max_pair, current_node.next.next.next)
                current_node.next = replacement_node
            current_node = current_node.next
        # remove max_pair from pair_frequencies since it has been replaced
        del pair_frequencies[max_pair]
    return table

# converts table to mapping from Token -> index in table
def construct_indices(table: list[Token]) -> dict[Token, int]:
    indices: dict[Token, int] = dict()
    for i, token in enumerate(table):
        indices[token] = i
    return indices

# get all pairs which start with a given token
def get_pairs_starting_with(starting_token: Token, table: list[Token]) -> list[Pair]:
    valid_tokens: list[Pair] = []
    for token in table:
        if isinstance(token, Pair) and token.left == starting_token:
            valid_tokens.append(token)
    return valid_tokens

# builds a list of tokens where the left of each token matches the previous token
def build_random_tokens(token: Token, table: list[Token]) -> list[Token]:
    random_tokens: list[Token] = [token]
    while True:
        next_pairs: list[Pair] = get_pairs_starting_with(token, table)

        if not next_pairs:
            if isinstance(token, str):
                break
            token = token.right
            continue
        
        token = random.choice(next_pairs)
        random_tokens.append(token)
    return random_tokens

# helper function to convert token to human-readable string
def format_token(token: Token) -> str:
    if isinstance(token, str):
        return token
    return format_token(token.left) + format_token(token.right)

with open(r"datasets\frankenstein-letters.txt") as file:
    text: str = file.readline()

table: list[Token] = construct_table(text)
indices: dict[Token, int] = construct_indices(table)
print("TABLE CONSTRUCTED")

# extract a random token
first_token: Token = random.choice(table[256:])
assert(isinstance(first_token, Pair))

random_tokens: list[Token] = build_random_tokens(first_token, table)

# make random_tokens human-readable
random_string: str = format_token(first_token.left)
for token in random_tokens:
    if isinstance(token, str):
        random_string += format_token(token)
    else:
        random_string += format_token(token.right)

print(random_string)