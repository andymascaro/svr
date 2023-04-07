import json

#from gamedata import *

def json_to_english(json_data):
    descriptions = []
    for obj in json_data:
        #if 'img' in obj:
        #    description += f"Image: {obj['img']}\n"
        #if 'loc' in obj:
        #    x, y, z = obj['loc']
        #    description += f"Location: ({x}, {y}, {z})\n"
        description = ""

        name = obj.get('display') or obj.get('name')
        description += f"An item named {name} exists. "

        #if 'cash' in obj:
        #    description += f"Cash: {obj['cash']}\n"
        if 'description' in obj:
            description += f"{name} has this property: \"{obj['description']}\" "
        #if 'quests' in obj:
        #    description += f"Quests: {', '.join(obj['quests'])}\n"
        #if 'values' in obj:
        #    description += f"Values: {', '.join(map(str, obj['values']))}\n"
        #if 'wants' in obj:
        #    description += f"Wants: {', '.join(map(str, obj['wants']))}\n"
        #if 'resell' in obj:
        #    description += f"Resell Value: {obj['resell']}\n"
        
        descriptions.append(description)
    return "".join(descriptions)

with open('output.json', 'r') as f:
    # Load the JSON data into a Python dictionary
    json_data = json.load(f)
    json_data = json.loads(json_data)

    
print(json_to_english(json_data))

with open('items.txt', 'w') as f:
    # Write some text to the file
    f.write(json_to_english(json_data))