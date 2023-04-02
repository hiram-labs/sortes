import pickle


def dump(path, data):
    with open(path, "wb") as file:
        pickle.dump(data, file)


def load(path):
    with open(path, "rb") as file:
        return pickle.load(file)
