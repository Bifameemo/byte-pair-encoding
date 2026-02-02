# TODO
- investigate why linked lists reduce performance (intended to reduce time complexity of replacing max_pair in text)
- recursively retry building next_tokens using last_token.right (only done in linked-list copy)
- construct a dictionary which maps tokens to tokens which start with that token
- construct a dictionary which measures frequency of each token within original text
- choose next word weighted by frequency in original text
- only count non-overlapping pairs
- add support for files passed as arguments through CLI
