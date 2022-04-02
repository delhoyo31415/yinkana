import functools

import challenges

USERNAME = ""

if __name__ == "__main__":
    functools.reduce(lambda id_, challenge: challenge(id_), challenges.all_challenges, USERNAME)
