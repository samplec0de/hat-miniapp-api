from typing import List

from pymongo import MongoClient


class AppUser:
    __slots__ = ('mongo', 'vk_id')

    def __init__(self, vk_id: int, mongo: MongoClient):
        self.vk_id = vk_id  # user_id из vk api
        self.mongo = mongo

    def give_word(self, word: str) -> None:
        collection = self.mongo['data'][f'used_words']
        request = collection.find_one({'vk_id': self.vk_id})
        if request:
            words = request['words']
            if word not in words:
                words.append(word)
            collection.find_one_and_update({'vk_id': self.vk_id}, {'$set': {'words': words}})
        else:
            collection.insert_one({'vk_id': self.vk_id, 'words': [word]})

    def get_words(self) -> List[str]:
        """
        Get a list of user used words
        :return:
        """
        collection = self.mongo['data'][f'used_words']
        request = collection.find_one({'vk_id': self.vk_id})
        if request:
            return request['words']
        else:
            return []
