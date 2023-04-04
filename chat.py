#https://www.mlq.ai/gpt-4-pinecone-website-ai-assistant/

import requests
import re
import urllib.request
from bs4 import BeautifulSoup
from collections import deque
from html.parser import HTMLParser
from urllib.parse import urlparse
import os
import pandas as pd
import tiktoken
import openai
import pinecone
import numpy as np
from openai.embeddings_utils import distances_from_embeddings, cosine_similarity

from creds import *

openai.api_key = OPENAI_KEY

def create_context(question, max_len, size):
    #return question

    # Define index name
    index_name = 'sea2'
    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_API_ENV)
    index = pinecone.Index(index_name)
    
    embed_model = "text-embedding-ada-002"
    user_input = question#"Who is on DEMI at Joe's?"
    
    embed_query = openai.Embedding.create(
        input=user_input,
        engine=embed_model
    )
    
    # retrieve from Pinecone
    query_embeds = embed_query['data'][0]['embedding']
    
    # get relevant contexts (including the questions)
    response = index.query(query_embeds, top_k=5, include_metadata=True)
    
    contexts = [item['metadata']['text'] for item in response['matches']]
    
    return "Databank files:"+"\n\n---\n\n".join(contexts)+"\n\n-----\n\n"+"The final question is: "+question


def answer_question(
    model="text-davinci-003",
    question="Am I allowed to publish model outputs to Twitter, without a human review?",
    max_len=1800,
    size="ada",
    debug=False,
    max_tokens=150,
    stop_sequence=None
):
    """
    Answer a question based on the most similar context from the dataframe texts
    """
    context = create_context(
        question,
        max_len=max_len,
        size=size,
    )
    augmented_query = context#"\n\n---\n\n".join(context)+"\n\n-----\n\n"+query

    # If debug, print the raw model response
    if debug:
        print("Context:\n" + context)
        print("\n\n")

    try:
        system_msg = f"""Everything in the Databank files before the final question is 100% true fact and today is the year 2071.
        
        I am Gavin, the space driver / space hauler.
        
        You are the Ai named "Record Index Gemma" who is onboard the spaceship DEMI. The Databank files contains references to "Record Index Gemma" and things she said - that is all information that YOU in fact said.  You are Gemma.  Answer as Gemma. 
        
        You will not respond with any reference to the fact that context is being listed because it is all information being pulled from your Ai databank. 
        
        Do not make up any assumptions for questions you do not know the answer to, and do not refer to 'the context' itself.
        
        If there is no information in the context or you do not know the answer say 'that information isn't available' and do not refer to 'the context' or 'the information provided'. If you must quote Record Index Gemma say 'as I can gather' - don't say 'according to record index gemma'.
        
        Whenever you need to list things do that in a bulleted list.

        Now, answer this final question:
"""
        # Create a completions using the questin and context
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": augmented_query}
            ]
        )
        if debug:
            print(response)
        return response["choices"][0]["message"]["content"].strip()
        
    except Exception as e:
        print(e)
        return ""

################################################################################
### Step 13
################################################################################

#print(answer_question(question="What day is it?", debug=True))

#print(answer_question(question="What is the climate in Seattle?"))

#print(answer_question(question="Who is on DEMI at Joe's?", debug=True))

#print(answer_question(question="Gather info on recent historical events in the past 50 years (so from 2021-2071)", debug=True))

#print(answer_question(question="What do we know about Constructs?", debug=True))

print(answer_question(question="I need to work with a hacker - do we know of any?", debug=True))