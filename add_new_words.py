import json
import random
import pymorphy2
from pathlib import Path


def get_words():
    return json.loads((Path(__file__).parent / 'flask_app' / 'dataset.json').read_text())['word']


def get_dict():
    return [word.strip() for word in (Path(__file__).parent / 'big_dict.txt').read_text('cp1251').split('\n')]


dataset_words = get_words()
dict_words = get_dict()
random.shuffle(dict_words)
morph = pymorphy2.MorphAnalyzer()
for word in dict_words:
    if len(word) > 13:
        continue
    m_res = morph.parse(word)[0]
    if 'NOUN' not in m_res.tag:
        continue
    word = m_res.normal_form
    print(word)
    res = input()
    if len(res) == 0:
        continue
    if res[0] == 'e':
        break
    dataset_words.append(word)
    print(f'Добавлено, {len(dataset_words)} в базе!')
print(json.dumps({"word": dataset_words}, ensure_ascii=False), file=open('fresh_dataset.json', 'w'))
