import random
from typing import NamedTuple

class Pair(NamedTuple):
    left: Token
    right: Token

type Token = Pair | str

# converts text to list of tokens
def construct_table(text: str) -> list[Token]:
    # initialise first 256 entries of table with ASCII characters
    table: list[Token] = []
    for i in range(256):
        table.append(chr(i))
    
    # convert text into list of leaves
    tokenised_text: list[Token] = []
    for char in text:
        tokenised_text.append(char)

    # count pairs initially
    pair_frequencies: dict[Token, int] = dict()
    for i in range(len(tokenised_text) - 1):
        pair: Token = Pair(tokenised_text[i], tokenised_text[i + 1])
        if pair in pair_frequencies:
            pair_frequencies[pair] += 1
        else:
            pair_frequencies[pair] = 1

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
        i: int = 0
        while i <= len(tokenised_text) - 2:
            pair = Pair(tokenised_text[i], tokenised_text[i + 1])
            if pair == max_pair:
                # decrement frequency of adjacent pairs
                # increment frequency of replacement pairs
                # e.g. if max_pair == "is" then "fish" -> "fXh"
                # frequency of "fi" and "sh" decrements
                # frequency of "fX" and "Xh" increments
                if (i - 1 >= 0):
                    pair_before: Pair = Pair(tokenised_text[i - 1], tokenised_text[i])
                    pair_frequencies[pair_before] -= 1
                    if pair_frequencies[pair_before] == 0:
                        del pair_frequencies[pair_before]
                    
                    replacement_pair_before: Pair = Pair(tokenised_text[i - 1], max_pair)
                    if replacement_pair_before in pair_frequencies:
                        pair_frequencies[replacement_pair_before] += 1
                    else:
                        pair_frequencies[replacement_pair_before] = 1
                if (i + 2 <= len(tokenised_text) - 1):
                    pair_after: Pair = Pair(tokenised_text[i + 1], tokenised_text[i + 2])
                    pair_frequencies[pair_after] -= 1
                    if pair_frequencies[pair_after] == 0:
                        del pair_frequencies[pair_after]
                    
                    replacement_pair_after: Pair = Pair(max_pair, tokenised_text[i + 2])
                    if replacement_pair_after in pair_frequencies:
                        pair_frequencies[replacement_pair_after] += 1
                    else:
                        pair_frequencies[replacement_pair_after] = 1
                # replace pair in tokenised_text
                tokenised_text[i:i+2] = [max_pair]
            i += 1
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
    random_tokens: list[Token] = []
    while True:
        next_pairs: list[Pair] = get_pairs_starting_with(token, table)

        if not next_pairs:
            break
        
        token = random.choice(next_pairs)
        random_tokens.append(token)
    return random_tokens

# helper function to convert token to human-readable string
def format_token(token: Token) -> str:
    if isinstance(token, str):
        return token
    return format_token(token.left) + format_token(token.right)

with open(r"datasets\frankenstein-letter-1-2.txt") as file:
    text: str = file.readline()

table: list[Token] = construct_table(text)
indices: dict[Token, int] = construct_indices(table)
print("TABLE MADE")

# extract a random token
first_token: Token = random.choice(table[256:])

random_tokens: list[Token] = build_random_tokens(first_token, table)

# make random_tokens human-readable
random_string: str = ''
for token in random_tokens:
    if isinstance(token, str):
        random_string += format_token(token) + '-'
    else:
        random_string += format_token(token.left) + '-'
if isinstance(random_tokens[-1], Pair):
    random_string += format_token(random_tokens[-1].right)

print('|' + random_string + '|')

# TESTING - WILL ERROR
last_token = random_tokens[-1]
print("last random token:", last_token)

if isinstance(last_token, str):
    print("tokens which end with the right token of last token:", get_pairs_starting_with(last_token, table)) # this should be empty
else:
    print("tokens which end with the right token of last token:", get_pairs_starting_with(last_token.right, table)) # this should be empty
    if isinstance(last_token.right, Pair):
        print("tokens which end with the right token of right token of last token:", get_pairs_starting_with(last_token.right.right, table))
        print(format_token(last_token), format_token(get_pairs_starting_with(last_token.right.right, table)[0]))