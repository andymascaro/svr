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

# Define index name
index_name = 'sea2'
pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_API_ENV)
index = pinecone.Index(index_name)

embed_model = "text-embedding-ada-002"
user_input = "Who is on DEMI at Joe's?"

embed_query = openai.Embedding.create(
    input=user_input,
    engine=embed_model
)

# retrieve from Pinecone
query_embeds = embed_query['data'][0]['embedding']

# get relevant contexts (including the questions)
response = index.query(query_embeds, top_k=5, include_metadata=True)

print(response)