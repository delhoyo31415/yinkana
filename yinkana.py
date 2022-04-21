import challenges

USERNAME = ""

if __name__ == "__main__":
    identifier = USERNAME
    for challenge in challenges.all_challenges:
        identifier = challenge(identifier)
