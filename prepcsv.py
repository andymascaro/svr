#https://www.mlq.ai/gpt-4-pinecone-website-ai-assistant/

import openai
import tiktoken
import pinecone
import os
import pandas as pd
import numpy as np
import re
import requests
import urllib.request
from bs4 import BeautifulSoup
from collections import deque
from html.parser import HTMLParser
from urllib.parse import urlparse
from IPython.display import Markdown

from creds import *

openai.api_key = OPENAI_KEY

max_tokens = 500

texts=[]

def remove_newlines(serie):
    serie = serie.str.replace('\n', ' ')
    serie = serie.str.replace('\\n', ' ')
    serie = serie.str.replace('  ', ' ')
    serie = serie.str.replace('  ', ' ')
    return serie

# Open the file and read the text
with open('output.txt', 'r') as f:
    text = f.read()

    texts.append(('output.txt', text))

# Create a dataframe from the list of texts
df = pd.DataFrame(texts, columns = ['fname', 'text'])

# Set the text column to be the raw text with the newlines removed
df['text'] = remove_newlines(df.text)
df.to_csv('processed/scraped.csv')
df.head()