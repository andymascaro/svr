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


df=pd.read_csv('processed/embeddings.csv', index_col=0)
df['embeddings'] = df['embeddings'].apply(eval).apply(np.array)

df.head()

# Add an 'id' column to the DataFrame
from uuid import uuid4
df['id'] = [str(uuid4()) for _ in range(len(df))]

print(df)
#exit()
# Define index name
index_name = 'sea3'

# Initialize connection to Pinecone
pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_API_ENV)

# Check if index already exists, create it if it doesn't
if index_name not in pinecone.list_indexes():
    pinecone.create_index(index_name, dimension=1536, metric='dotproduct')

# Connect to the index and view index stats
index = pinecone.Index(index_name)
index.describe_index_stats()

from tqdm.auto import tqdm

batch_size = 100  # how many embeddings we create and insert at once

# Convert the DataFrame to a list of dictionaries
chunks = df.to_dict(orient='records')

# Upsert embeddings into Pinecone in batches of 100
for i in tqdm(range(0, len(chunks), batch_size)):
    i_end = min(len(chunks), i+batch_size)
    meta_batch = chunks[i:i_end]
    ids_batch = [x['id'] for x in meta_batch]
    embeds = [x['embeddings'].tolist() for x in meta_batch]
    meta_batch = [{
        'text': x['text']
    } for x in meta_batch]
    to_upsert = list(zip(ids_batch, embeds, meta_batch))
    index.upsert(vectors=to_upsert)