import json

from gamedata import *


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
        descriptions.append(description)
    return "".join(descriptions)

# Example usage
json_data = [
    {
        'display': 'Nexus Red Glint Portal',
        'name': 'torchoutput',
        'img': 'hm11',
        'trader': True,
        'hidden': True,
        'loc': [0, 4, 2],
        'cash': 999.0,
        'quote': 'You own this Nexus Red Warp Torch.  Come back to retrieve new Glint output daily.',
        'quests': [],
        'values': ['*', 0],
        'wants': ['*', 0],
        'resell': 0.75
    },
    {
        'display': 'Scorched One',
        'name': 'z1',
        'loc': [0, 5, 0],
        'cash': 999.0,
        'quote': 'We are far from home.',
        'values': [],
        'wants': [],
        'resell': 0.75
    }
]


with open('mercs.json', 'r') as f:
    # Load the JSON data into a Python dictionary
    json_data = json.load(f)

    
print(json_to_english(json_data))
