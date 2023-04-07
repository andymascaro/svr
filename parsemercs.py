import json

from gamedata import *


with open('itemsgood.json', 'r') as f:
    # Load the JSON data into a Python dictionary
    items = json.load(f)
    items = json.loads(items)

with open('inventories.json', 'r') as f:
    # Load the JSON data into a Python dictionary
    cargos = json.load(f)
    cargos = json.loads(cargos)

# Join cargos and inv on the key 'name'
def join_cargos_and_inv(cargos, inv_list):
    result = {}
    for person, items in cargos.items():
        result[person] = []
        for cargo in items:
            for inv in inv_list:
                if cargo[0] == inv['name']:
                    result[person].append(inv)
    return result

cargolist = join_cargos_and_inv(cargos, items)

def json_to_english(json_data):
    descriptions = []
    for obj in json_data:
        #if 'img' in obj:
        #    description += f"Image: {obj['img']}\n"
        #if 'loc' in obj:
        #    x, y, z = obj['loc']
        #    description += f"Location: ({x}, {y}, {z})\n"
        description = ""
        if 'loc' in obj:
            x, y, z = obj['loc']
            system = systems[x]
            planet = planets[system][y]
            city = cities[system][planet][z]['display']
            description += f"At the location: {planet}, {city}, "

        name = obj.get('display') or obj.get('name')
        description += f"a merchant named {name} exists. "

        #if 'cash' in obj:
        #    description += f"Cash: {obj['cash']}\n"
        if 'quote' in obj:
            description += f"{name} says: \"{obj['quote']}\" "

        if obj.get('name') in cargolist:
            for thing in cargolist[obj.get('name')]:
                description += f"{name} has this item for sale: \"{thing['display']}\""
                if 'description' in thing:
                    description += f" which is known for: \"{thing['description']}\". "
                else:
                    description += f". "

        #if 'quests' in obj:
        #    description += f"Quests: {', '.join(obj['quests'])}\n"
        #if 'values' in obj:
        #    description += f"Values: {', '.join(map(str, obj['values']))}\n"
        #if 'wants' in obj:
        #    description += f"Wants: {', '.join(map(str, obj['wants']))}\n"
        #if 'resell' in obj:
        #    description += f"Resell Value: {obj['resell']}\n"
        if 'index' in obj:
            #description += "\nIndex:\n"
            for index_obj in obj['index']:
                topic = index_obj.get('topic', '')
                result = index_obj.get('result', '')
                description += f"When asking {name} \"{topic}\", {name} says: \"{result}\". "

        description += "\n"
        description += "\n"
        descriptions.append(description)
    return "".join(descriptions)

with open('mercs.json', 'r') as f:
    # Load the JSON data into a Python dictionary
    json_data = json.load(f)

    
print(json_to_english(json_data))

with open('output.txt', 'w') as f:
    # Write some text to the file
    f.write(json_to_english(json_data))