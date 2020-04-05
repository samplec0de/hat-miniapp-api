from json import loads
from pathlib import Path


def get_words():
    dataset = Path('/app/dataset.json')
    return loads(dataset.read_text())['word']
