'''

Contributed by SagsMug. Thank you SagsMug.
https://github.com/oobabooga/text-generation-webui/pull/175

'''

import asyncio
import json
import random
import string

import csv

import websockets

# Gradio changes this index from time to time. To rediscover it, set VISIBLE = False in
# modules/api.py and use the dev tools to inspect the request made after clicking on the
# button called "Run" at the bottom of the UI
GRADIO_FN = 34


def random_hash():
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(9))


async def run(context, id):
    server = "127.0.0.1"
    params = {
    'max_new_tokens': 20,
        'do_sample': True,
        'temperature': 0.72,
        'top_p': 0.73,
        'typical_p': 1,
        'repetition_penalty': 1.1,
        'encoder_repetition_penalty': 1.0,
        'top_k': 0,
        'min_length': 0,
        'no_repeat_ngram_size': 0,
        'num_beams': 1,
        'penalty_alpha': 0,
        'length_penalty': 1,
        'early_stopping': False,
        'seed': -1,
        'add_bos_token': True,
        'truncation_length': 2048,
        'ban_eos_token': False,
        'skip_special_tokens': True,
    'stopping_strings': ["Statement", "\#", "\n"],
    }
    payload = json.dumps([context, params])
    session = random_hash()
    #print('the SESSION is', session, context)

    async with websockets.connect(f"ws://{server}:7860/queue/join") as websocket:
        while True:
            content = json.loads(await websocket.recv())

            msg = content["msg"]

            if msg == "send_hash":
                await websocket.send(json.dumps({
                    "session_hash": session,
                    "fn_index": GRADIO_FN
                }))
            elif msg == "estimation":
                pass
            elif msg == "send_data":
                await websocket.send(json.dumps({
                    "session_hash": session,
                    "fn_index": GRADIO_FN,
                    "data": [
                        payload
                    ]
                }))
            elif msg == "process_starts":
                pass
            elif msg == "process_completed":#  or msg == "process_generating" :
                #print(session, content)
                response = content["output"]["data"][0].split(prompt)[1]
                #answers[id]['r'] = get_last_word(response)
                answers[id]['v'].append(get_last_word(response))
                yield content["output"]["data"][0]
                # You can search for your desired end indicator and
                # stop generation by closing the websocket here
                if msg == "process_completed":
                    break

def filter_answer(answer):
    return answer.split(":")[1].strip().lower()

def get_last_word(sentence):
    # Remove all punctuation from the sentence
    translator = str.maketrans('', '', string.punctuation)
    sentence = sentence.translate(translator)

    # Convert the sentence to lowercase and split it into words
    words = sentence.lower().split()

    # Get the last word of the sentence
    last_word = words[-1]

    return last_word

#prompt = """###Statement: "I love dealing him he is such a joy."
###Question: What is the sentiment of the previous statement? Chose only from three options: ('Kind', 'Rude', or 'Neutral')?
###Answer? The answer is this statement is: 'Kind'.

###Statement: "This guy is an asshole and nobody likes him we all hate him"
###Question: What is the sentiment of the previous statement? Chose only from three options: ('Kind', 'Rude', or 'Neutral')?
###Answer? The answer is this statement"""

#prompt = """
### Info About Person A: "I love dealing him he is such a joy."
### Info About Person B: "This guy is an asshole and nobody likes him we all hate him"

###Question: What is the sentiment of the Info About Person A? Chose only from three options: ('Kind', 'Rude', or 'Neutral')?
###Answer? The answer is this Info About Person A is: 'Kind'.

###Question: What is the sentiment of the Info About Person B? Chose only from three options: ('Kind', 'Rude', or 'Neutral')?
###Answer? The answer is this Info About Person B"""
import pandas as pd
from collections import Counter

def accuracy(data):
    filtered_data = data[data['r'] == data['t']]

    # Step 2: Calculate the score (accuracy)
    accuracy = len(filtered_data) / len(data)

    print("Accuracy:", accuracy)

def most_popular(lst):
    return Counter(lst).most_common(1)[0][0]

async def get_result(prompt, index):
    async for response in run(prompt, index):
        # Print intermediate steps
        True
        #print('wtf', response, 'wt HECK')

    # Print final result
    #print(response)
    #after_text = response.split(prompt)[1]
    df = pd.DataFrame(answers)

    df['r'] = df['v'].apply(most_popular)

    print(df)
    accuracy(df)

answers = []

votes = 1

with open('data/hard.csv', 'r') as file:
    reader = csv.reader(file)
    #next(reader) # skip header row
    for index, row in enumerate(reader):
        answers.append({
            'q': row[0],
            'v': [], 
            'r': '',
            't': row[1].lower()
        })
        personality_description = row[0]
        kindness_rating = row[1]
        # Do something with personality_description and kindness_rating, such as:
        #print(personality_description)
        statement = personality_description

        prompt = f"""
### Info About Person A: "I love dealing him he is such a joy."
###Question: What is the sentiment of the Info About Person A? Well, since we can only choose from the 3 options: ('Kind', 'Rude', or 'Neutral') the answer is clear.
###Answer? The answer is this Info About Person A is: 'Kind'.

### Info About Person B: "{statement}"
###Question: What is the sentiment of the Info About Person B? Well, since we can only choose from the 3 options: ('Kind', 'Rude', or 'Neutral') the answer is clear.
###Answer? The answer is this Info About Person B"""


        #print(prompt)
        for _ in range(votes):
            asyncio.run(get_result(prompt, index))
        #exit()

