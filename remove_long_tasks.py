import json

if __name__ == '__main__':
    json_data = json.loads(input("JSON:"))
    old_len = len(json_data["word"])
    json_data["word"] = [word for word in json_data["word"] if len(word) <= 13]
    print('Removed', old_len - len(json_data["word"]))
    print(json.dumps(json_data, ensure_ascii=False))

