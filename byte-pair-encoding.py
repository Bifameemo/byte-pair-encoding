import random
from typing import NamedTuple

class Token(NamedTuple):
    left: int
    right: int | None

# converts text to list of all repeating substrings in text (tokens)
def construct_table(text: str) -> list[Token]:
    # initialise first 256 entries of table with ASCII characters
    table: list[Token] = []
    for i in range(256):
        table.append(Token(i, None))

    # convert text into list of token positions
    tokenised_text: list[int] = []
    for char in text:
        tokenised_text.append(ord(char))

    # count pairs initially
    pair_frequencies: dict[Token, int] = dict()
    for i in range(len(tokenised_text) - 1):
        pair: Token = Token(tokenised_text[i], tokenised_text[i + 1])
        if pair in pair_frequencies:
            pair_frequencies[pair] += 1
        else:
            pair_frequencies[pair] = 1

    # loop until break (when no repeated pairs exist)
    while True:
        # determine most frequent pair
        max_frequency: int = 0
        # initialise with invalid token
        max_pair: Token = Token(-1, -1)
        for pair, frequency in pair_frequencies.items():
            if frequency > max_frequency:
                max_frequency = frequency
                max_pair = pair
            
        # break if no repeated pairs exist
        if max_frequency <= 1:
            break
        
        # add most frequent pair to table
        table.append(max_pair)

        # replace max_pair in tokenised_text and update pair_frequencies
        i: int = 0
        while i <= len(tokenised_text) - 2:
            pair = Token(tokenised_text[i], tokenised_text[i + 1])
            if pair == max_pair:
                # decrement frequency of adjacent pairs
                # increment frequency of replacement pairs
                # e.g. if max_pair == "is" then "fish" -> "fXh"
                # frequency of "fi" and "sh" decrements
                # frequency of "fX" and "Xh" increments
                if (i - 1 >= 0):
                    pair_before: Token = Token(tokenised_text[i - 1], tokenised_text[i])
                    pair_frequencies[pair_before] -= 1
                    if pair_frequencies[pair_before] == 0:
                        del pair_frequencies[pair_before]
                    
                    replacement_pair_before: Token = Token(tokenised_text[i - 1], len(table) - 1)
                    if replacement_pair_before in pair_frequencies:
                        pair_frequencies[replacement_pair_before] += 1
                    else:
                        pair_frequencies[replacement_pair_before] = 1
                if (i + 2 <= len(tokenised_text) - 1):
                    pair_after: Token = Token(tokenised_text[i + 1], tokenised_text[i + 2])
                    pair_frequencies[pair_after] -= 1
                    if pair_frequencies[pair_after] == 0:
                        del pair_frequencies[pair_after]
                    
                    replacement_pair_after: Token = Token(len(table) - 1, tokenised_text[i + 2])
                    if replacement_pair_after in pair_frequencies:
                        pair_frequencies[replacement_pair_after] += 1
                    else:
                        pair_frequencies[replacement_pair_after] = 1
                # replace pair in tokenised_text
                tokenised_text[i:i+2] = [len(table) - 1]
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

# get all tokens which starts with a token index
def get_tokens_starting_with(index: int | None) -> list[Token]:
    valid_tokens: list[Token] = []
    for token in table:
        if token.left == index:
            valid_tokens.append(token)
    return valid_tokens

# helper function to convert token to human-readable string
def format_token(token: Token) -> str:
    if token.right == None:
        return chr(token.left)
    else:
        return format_token(table[token.left]) + format_token(table[token.right])

with open(r"datasets\frankenstein-letter-1-2.txt") as file:
    text: str = file.readline()

table: list[Token] = construct_table(text)
indices: dict[Token, int] = construct_indices(table)

random_tokens: list[Token] = []

# extract a random token
starting_token: Token = random.choice(table[256:])
random_tokens.append(starting_token)

next_tokens = get_tokens_starting_with(starting_token.right)
while len(next_tokens) >= 1:
    token: Token = random.choice(next_tokens)
    random_tokens.append(token)
    next_tokens = get_tokens_starting_with(token.right)

random_string: str = ''
for token in random_tokens:
    random_string += format_token(table[token.left])

last_token: Token = random_tokens[-1]
if last_token.right != None:
    random_string += format_token(table[last_token.right])

print('|' + random_string + '|')

last_token = random_tokens[-1]
print("last random token:", last_token)
print("tokens which end with the right token of last token:", get_tokens_starting_with(last_token.right)) # this should be empty
if last_token.right != None:
    print("tokens which end with the right token of right token of last token:", get_tokens_starting_with(table[last_token.right].right))
    print(format_token(last_token), format_token(get_tokens_starting_with(table[last_token.right].right)[0]))