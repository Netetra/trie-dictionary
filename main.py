import json
import os
import urllib.parse

root_node_dir = f"{os.getcwd()}/nodes"
root_node_file = "root"


def read_node(file):
    with open(f"{root_node_dir}/{file}.json", "r") as f:
        return json.load(f)


def write_node(file, data):
    with open(f"{root_node_dir}/{file}.json", "w") as f:
        json.dump(data, f, indent=4)

def insert_node(word, description, edit_node_file):
    node = read_node(edit_node_file)
    if f"{edit_node_file}.json" == f"node_{word}.json":
        node["word"] = word
        node["description"] = description
        node["isEnd"] = True
        write_node(edit_node_file, node)
        return

    def gen_relay_node_data(index):
        relay_node_data = {
            "word": None,
            "description": None,
            "index": index,
            "child": {
                word[index+1]: f"node_{word[:index+2]}"
            },
            "isEnd": False
        }
        return relay_node_data
    
    node["child"][word[0]] = f"node_{word[0]}"
    write_node(edit_node_file, node)

    for index in range(node["index"]+1, len(word)-1):
        relay_node_file = f"node_{word[:index+1]}"
        relay_node = gen_relay_node_data(index)
        write_node(relay_node_file, relay_node)

    end_node_file = f"node_{word}"
    end_node = {
        "word": word,
        "description": description,
        "index": len(word)-1,
        "child": {},
        "isEnd": True
    }
    write_node(end_node_file, end_node)


def search_node(word, node_file, index=0, before_node_file=None):
    node = read_node(node_file)
    if len(word) == index:
        if node["isEnd"]:
            return None
        else:
            return node_file
    try:
        file_name = node["child"][word[index]]
    except KeyError:
        return node_file
    return search_node(word, file_name, index+1, node_file)


def main():
    word = input("word > ")
    edit_node_file = search_node(word, root_node_file)
    if edit_node_file == None:
        print("登録済みの単語です")
        return
    word_description = input("description > ")
    insert_node(word, word_description, edit_node_file)


main()
